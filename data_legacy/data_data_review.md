# Surrender vs Effort → Success Dataset

A synthetic relational dataset of **100,000 individuals** across **52 countries**, designed to study the interplay between **effort** (hard work, productivity, drive) and **surrender** (faith, acceptance, detachment, mindfulness) and how their balance predicts **success, burnout, and life satisfaction**.

This dataset is unique because most real-world datasets only track *effort*. Here we also track *inner state*, *behavior patterns*, and *environment* — making it suitable for advanced ML, causal analysis, and behavioral research.

---

## 📊 Dataset Overview

| Property | Value |
|---|---|
| Total people (rows in `users.csv`) | 100,000 |
| Tables | 10 |
| Total rows across all tables | 1,000,000 |
| Countries represented | 52 |
| Genders | Male (49.5%), Female (49.5%), Non-binary (1%) |
| Age range | 19 – 85 |
| Format | CSV (UTF-8) |
| Foreign-key integrity | 100% (zero orphans) |

---

## 🗂️ Files in this archive

```
csv/
├── users.csv                    # Master table (100k rows)
├── effort_profile.csv           # Work, drive, productivity (100k)
├── surrender_profile.csv        # Faith, acceptance, mindfulness (100k)
├── mental_state.csv             # Stress, focus, emotions (100k)
├── daily_activity_logs.csv      # One-day snapshot per user (100k)
├── goal_tracking.csv            # Goals + achievement (100k)
├── life_events.csv              # Major life events (100k)
├── performance_outcome.csv      # Success / burnout labels (100k)
├── behavior_patterns.csv        # Habits, coping, learning style (100k)
└── environment_factors.csv      # Work, family, social context (100k)
README.md                        # This file
```

---

## 🔗 Relational Schema

All tables connect through `user_id` (foreign key → `users.user_id`).

```
                       ┌──────────────┐
                       │    users     │  ← PK: user_id
                       └──────┬───────┘
                              │ 1:1 (one row per user in each child table)
        ┌─────────────┬───────┼───────┬─────────────┬──────────────┐
        ▼             ▼       ▼       ▼             ▼              ▼
  effort_profile  surrender  mental  daily_logs  goal_tracking  life_events
                  _profile   _state
        ┌─────────────────┬──────────────────┬──────────────────┐
        ▼                 ▼                  ▼                  ▼
  performance_outcome  behavior_patterns  environment_factors
```

Each child table has its own primary key (`effort_id`, `surrender_id`, etc.) and references `user_id`.

---

## 📋 Table Schemas

### 1. `users` (master)
Demographics + latent personality traits.
**Key columns:** `user_id`, `name`, `age`, `gender`, `country`, `profession`, `education_level`, `marital_status`, `income_level`, `health_score`, `sleep_hours`, `diet_quality`, `physical_activity`, `spiritual_practice`, `personality_type` (16 MBTI types), `introversion_score`, `discipline_score`, `risk_tolerance`, `life_satisfaction`, `created_at`.

### 2. `effort_profile`
How hard the person works.
**Key columns:** `daily_work_hours`, `weekly_work_hours`, `intensity_level`, `multitasking_score`, `goal_pressure`, `deadline_frequency`, `overtime_hours`, `productivity_score`, `learning_hours`, `skill_improvement`, `repetition_rate`, `fatigue_level`, `burnout_index`, `external_pressure`, `competition_level`, `time_management_score`, `task_completion_rate`, `effort_consistency`.

### 3. `surrender_profile`
Inner state of letting go and faith.
**Key columns:** `faith_score`, `trust_level`, `detachment_level`, `acceptance_level`, `gratitude_score`, `mindfulness_score`, `prayer_time`, `meditation_time`, `emotional_release`, `control_need`, `ego_level`, `patience_score`, `resilience`, `surrender_consistency`, `inner_peace`, `purpose_alignment`, `fear_level`.

### 4. `mental_state`
Cognitive and emotional snapshot.
**Key columns:** `stress_level`, `anxiety_level`, `depression_score`, `focus_score`, `distraction_level`, `emotional_stability`, `mood_score`, `clarity_score`, `decision_fatigue`, `overthinking_score`, `self_doubt`, `confidence_level`, `calmness`, `anger_level`, `happiness_index`, `mental_energy`.

### 5. `daily_activity_logs`
One-day behavioral snapshot.
**Key columns:** `date`, `wake_time`, `sleep_time`, `work_hours`, `deep_work_hours`, `break_time`, `exercise_time`, `screen_time`, `social_media_time`, `reading_time`, `prayer_time`, `meditation_time`, `journaling`, `caffeine_intake`, `water_intake`, `meals_count`, `step_count`, `productivity_score`.

### 6. `goal_tracking`
A goal the person is currently pursuing.
**Key columns:** `goal_type` (Career, Health, Financial, Educational, Personal, Spiritual, Relationship, Skill, Creative, Fitness), `start_date`, `end_date`, `target_value`, `achieved_value`, `progress_percentage`, `consistency_score`, `motivation_level`, `obstacle_score`, `adjustment_count`, `clarity_level`, `alignment_score`, `deadline_pressure`, `external_support`, `internal_drive`, `success_flag` (1 if progress ≥ 70%).

### 7. `life_events`
A significant life event.
**Key columns:** `event_type` (Marriage, Divorce, Job Change, Promotion, Layoff, Childbirth, Bereavement, Relocation, Illness, Recovery, Financial Loss, Investment Win, Education Milestone, Retirement, Travel, Accident, Spiritual Awakening, Reconciliation), `event_date`, `impact_score`, `emotional_impact`, `financial_impact`, `stress_impact`, `recovery_time`, `support_received`, `lesson_learned`, `adaptation_score`, `resilience_score`, `mindset_shift`, `behavioral_change`, `risk_taken`, `outcome_effect`, `long_term_effect`.

### 8. `performance_outcome` ⭐ (target table for ML)
Final outcome label.
**Key columns:** `period`, `effort_score`, `surrender_score`, **`balance_index`** (100 − |effort − surrender|), `success_score`, `failure_score`, `productivity`, `creativity`, `leadership`, `financial_growth`, `career_growth`, `relationship_score`, `health_improvement`, `happiness_score`, **`burnout_flag`** (1/0), **`success_label`** (1 if success_score ≥ 65).

### 9. `behavior_patterns`
Stable behavioral tendencies.
**Key columns:** `habit_strength`, `habit_consistency`, `procrastination_score`, `discipline_score`, `addiction_score`, `distraction_pattern`, `focus_pattern`, `stress_pattern`, `coping_style`, `decision_style`, `thinking_style`, `learning_style`, `risk_behavior`, `emotional_pattern`, `social_pattern`, `growth_pattern`, `stability_index`.

### 10. `environment_factors`
External context.
**Key columns:** `work_environment`, `noise_level`, `family_support`, `peer_influence`, `financial_pressure`, `job_security`, `work_life_balance`, `social_pressure`, `cultural_factor`, `digital_exposure`, `internet_usage`, `community_support`, `mentor_presence`, `competition_level`, `opportunity_index`, `stress_triggers`, `growth_opportunities`.

---

## 🌍 Demographic Distribution

**Countries (top 15 of 52):** China, India, USA, Indonesia, Pakistan, Nigeria, Brazil, Bangladesh, Russia, Mexico, Japan, Philippines, Ethiopia, Egypt, Vietnam — distribution roughly tracks real-world population shares, with broader long-tail coverage of European, Latin American, African, and Southeast Asian countries.

**Age:** broadly distributed 19–85, with a working-age skew (median ~47).

**Gender:** ~49.5% Male, ~49.5% Female, ~1% Non-binary.

**Education:** spans No-formal → PhD with realistic proportions (largest group: Bachelor, ~30%).

---

## 🧪 Built-in correlations (so ML actually finds patterns)

Unlike pure random data, this dataset has **realistic latent structure**:

- `discipline` drives → habits, focus, productivity, time management, low procrastination
- `spiritual` drives → faith, acceptance, mindfulness, low fear, inner peace
- `work_drive` drives → work hours, intensity, goal pressure, motivation
- **`balance_index` = 100 − |effort − surrender|** → strongly predicts `success_score`
- High effort + low surrender → high `burnout_flag`
- Stress and burnout correlate negatively with sleep, mindfulness, life satisfaction
- Income correlates with education and age

This means a well-tuned model can hit **~80%+ AUC** predicting `success_label` or `burnout_flag` — but only if it captures the *interaction* between effort and surrender, not either one alone.

---

## 🚀 Quick start

```python
import pandas as pd

users    = pd.read_csv('csv/users.csv')
effort   = pd.read_csv('csv/effort_profile.csv')
surr     = pd.read_csv('csv/surrender_profile.csv')
outcome  = pd.read_csv('csv/performance_outcome.csv')

# Build a master ML frame
df = (users
      .merge(effort,  on='user_id')
      .merge(surr,    on='user_id')
      .merge(outcome, on='user_id'))

print(df.shape)            # (100000, ~80 columns)
print(df['success_label'].mean())   # ~0.34 — class is imbalanced but learnable
```

### SQL load (PostgreSQL example)
```sql
CREATE TABLE users (user_id INT PRIMARY KEY, ...);
\COPY users FROM 'csv/users.csv' CSV HEADER;
-- Repeat for each child table, then:
ALTER TABLE effort_profile ADD CONSTRAINT fk_effort_user
  FOREIGN KEY (user_id) REFERENCES users(user_id);
```

---

## 🎯 Suggested ML tasks

1. **Binary classification** — predict `success_label` (performance_outcome) from demographics + effort + surrender + behavior + environment.
2. **Burnout prediction** — predict `burnout_flag`; investigate whether high `surrender_score` is protective.
3. **Regression** — predict `life_satisfaction` or `happiness_index`.
4. **Clustering** — discover behavioral archetypes (e.g., "Effort-heavy burnouts" vs "Surrender-balanced high performers").
5. **Causal analysis** — does increasing meditation_time → reduce stress_level → improve success_score?
6. **Fairness audits** — does the model behave consistently across `gender` and `country`?

---

## ⚠️ Notes & caveats

- This is **synthetic data** for research, ML practice, and prototyping. Patterns are designed by the generator and do not reflect any real population.
- Gender includes a small Non-binary group (~1%); models should handle this category gracefully.
- Country distribution approximates real population shares but is not exact.
- Names are placeholders (`User_000001` … `User_100000`) — no PII.
- All dates are within 2022–2025.
- Score columns are scaled 0–100 unless otherwise noted; some impact/growth columns can be negative.

---

## 📜 License

Released under **CC0 / public domain**. Use freely for research, teaching, and commercial ML projects. No attribution required (but appreciated).

---

*Generated with a deterministic seed — re-running the generator produces the same dataset.*
