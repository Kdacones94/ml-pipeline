# Longitudinal Clinical Star Schema & Behavioral State Engine

## Technical Design Specification & Architecture Reference

### 1. Architectural Overview & Migration Rationale

The refactored dataset architecture transitions from a static, pseudo-normalized hub-and-spoke model (1:1 forced relationship across 10 tables) to a **Longitudinal Clinical Star Schema** (1:N temporal depth tracking 1,000 patients over 90 daily encounters).

#### Key Design Shifts:

1. **Decoupled Layers**: Abstract contracts (ABCs) enforce serialization contracts, keeping static Data Transfer Objects (DTOs) completely separate from dynamic state orchestration and SQL storage adapters.

   - **Ingestion Component (`data_ingestion/`)**: Concurrent cohort generator, state machine evaluator, SQLite persistence sink (`output/clinical_star_schema.db`), schema versioning (`sys_schema_version`), and batch job tracking (`sys_orchestration_job_runs`).

   - **ML Engine Component (`ml_engine/`)**: Query connector, Random Forest classifier, Weighted Cox PH survival model, and plot generator.

2. **Secularization of Metrics**: Subjective/religious variables are remapped to clinical behavioral standards:
   - `faith_score` → `radical_acceptance_score`
   - `prayer_time` → `focused_reflection_time`
   - `spiritual_practice` → `mindfulness_routine`
   - `surrender_consistency` → `cognitive_flexibility_index`

3. **Behavioral State Machine Orchestration**: Markov clinical state flows (`Stable`, `At-Risk`, `Critical`) are managed by a state engine tracking state inertia (`days_in_previous_state`) without generating pseudo-transitions.

4. **Streaming Concurrency & Slotted Immutability**: Using `@dataclass(frozen=True, slots=True)` reduces memory footprint by ~60%, while Python generator functions streaming to a parameterized SQLite bulk sink maintain $O(1)$ RAM usage at $100,000+$ records.

---

### 2. Multi-Tier Layer Architecture

``` mmd
┌─────────────────────────────────────────────────────────────┐
│ 1. CONTRACT LAYER: BaseEntityContract, StateObserver       │
└──────────────────────────────┬──────────────────────────────┘
                               │ Implements
┌──────────────────────────────▼──────────────────────────────┐
│ 2. LOGICAL LAYER: Slotted Immutable DTO Dataclasses         │
└──────────────────────────────┬──────────────────────────────┘
                               │ Processed by
┌──────────────────────────────▼──────────────────────────────┐
│ 3. ORCHESTRATION LAYER: ClinicalStateMachine (Markov Rules)  │
└──────────────────────────────┬──────────────────────────────┘
                               │ Streamed via
┌──────────────────────────────▼──────────────────────────────┐
│ 4. RUNTIME LAYER: ThreadPoolExecutor + Generator Stream      │
└──────────────────────────────┬──────────────────────────────┘
                               │ Persisted via
┌──────────────────────────────▼──────────────────────────────┐
│ 5. PERSISTENCE LAYER: ClinicalDatabaseRepository (Bulk SQL) │
└─────────────────────────────────────────────────────────────┘
```

---

### 3. Schema & Entity Definitions

#### A. Dimensions

- **`dim_concept_dictionary`**: LOINC/SNOMED-style lookup table defining scale bounds and clinical definitions.
- **`dim_behavioral_archetypes`**: Standardized cohort profiles (e.g., *High-Drive / Low-Flexibility*, *Balanced Resilient*).
- **`dim_users`**: Master patient index capturing age, gender, profession, mindfulness routine, baseline discipline, and baseline flexibility.

#### B. Facts & Flow Tables

- **`fact_encounters_daily`**: Actionable daily encounter logs (work hours, screen time) per patient per date.
- **`fact_observations_mental`**: Daily clinical observations (`stress_level`, `focus_score`, `radical_acceptance_score`, `focused_reflection_time`) bound 1:1 to daily encounter timestamps.
- **`fact_state_transitions`**: Sparse Markov flow table recording clinical state shifts (`previous_state`, `new_state`, `days_in_previous_state`).
- **`fact_clinical_events`**: Emergent stochastic event logs for burnout shocks, modeled via binomial distribution hazards in the `Critical` state.

---

### 4. Verification & Audit Metrics

The pipeline automatically runs an integrity verification suite upon execution:

- **Primary & Foreign Key Integrity**: 100% uniqueness across 1,000 patients and 90,000 encounters.
- **Zero Orphaned Records**: $0$ observations missing parent encounter IDs.
- **Zero Pseudo-Transitions**: $0$ state transition rows where `previous_state == new_state`.
