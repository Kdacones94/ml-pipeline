# Clinical Enterprise Data Warehouse (EDW) Schema Design

## Overview
The clinical database uses a **Dimensional Star Schema** optimized for longitudinal vitals, laboratory observation feeds, and state machine tracking.

### Tables & Entity Descriptions

1. **`dim_patient` (Patient Dimension)**
   - Core demographic record for uniquely identified patients.
   - Key attributes: `patient_id` (PK), `mrn`, `gender`, `birth_date`, `race`, `ethnicity`.

2. **`dim_encounter` (Encounter Dimension)**
   - Clinical contact episodes (e.g., Inpatient, ICU, Emergency Department).
   - Key attributes: `encounter_id` (PK), `patient_id` (FK), `encounter_type`, `admission_timestamp`, `discharge_timestamp`.

3. **`fact_observation` (Clinical Observation Fact Table)**
   - High-volume narrow fact table storing longitudinal time-series vitals, labs, and monitor streams.
   - Key attributes: `observation_id` (PK), `patient_id` (FK), `encounter_id` (FK), `code` (LOINC/SNOMED), `value_numeric`, `recorded_at`.

4. **`fact_cohort_state` (Cohort State Fact Table)**
   - Operational state audit tracking patient progressions across risk states over time.
   - Key attributes: `state_fact_id` (PK), `patient_id` (FK), `encounter_id` (FK), `previous_state`, `current_state`, `matrix_score`, `recorded_at`.

---

## Data Mapping File Specification (Legacy CSV to EDW Star Schema)

| Legacy Source Column | Target Table | Target Column | Data Transformation Rule |
| :--- | :--- | :--- | :--- |
| `PAT_ID`, `MRN_NO` | `dim_patient` | `mrn` | Strip whitespace, prefix clean `MRN-` |
| `GENDER_CD` | `dim_patient` | `gender` | Standardize `M`/`F`/`U` |
| `DOB`, `BIRTH_DT` | `dim_patient` | `birth_date` | Parse ISO-8601 or ISO string |
| `VISIT_ID`, `ENC_ID` | `dim_encounter` | `encounter_id` | Integer coercion |
| `ENC_TYPE` | `dim_encounter` | `encounter_type` | Map `1`->`Inpatient`, `2`->`ICU`, `3`->`ED` |
| `VITAL_CODE`, `LAB_ID` | `fact_observation` | `code` | Map local codes to LOINC (e.g., `HR` -> `8867-4`) |
| `MEAS_VALUE`, `RESULT` | `fact_observation` | `value_numeric` | Cast string to float, drop non-numeric outliers |
| `MEAS_TIME` | `fact_observation` | `recorded_at` | Convert UTC timestamps |
