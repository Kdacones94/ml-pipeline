-- Longitudinal Clinical Star Schema DDL with Triggers & Job Control
CREATE TABLE IF NOT EXISTS dim_concept_dictionary (
    concept_id INTEGER PRIMARY KEY,
    concept_name TEXT NOT NULL,
    scale_min REAL NOT NULL,
    scale_max REAL NOT NULL,
    clinical_definition TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS dim_behavioral_archetypes (
    archetype_id INTEGER PRIMARY KEY,
    archetype_name TEXT NOT NULL,
    description TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS dim_users (
    user_id INTEGER PRIMARY KEY,
    age INTEGER NOT NULL,
    gender TEXT NOT NULL,
    profession_category TEXT NOT NULL,
    mindfulness_routine INTEGER CHECK(mindfulness_routine IN (0,1)),
    baseline_discipline REAL NOT NULL,
    baseline_flexibility REAL NOT NULL,
    archetype_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (archetype_id) REFERENCES dim_behavioral_archetypes(archetype_id)
);

CREATE TABLE IF NOT EXISTS fact_encounters_daily (
    encounter_id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    date_str TEXT NOT NULL,
    work_hours REAL NOT NULL,
    screen_time REAL NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES dim_users(user_id)
);

CREATE TABLE IF NOT EXISTS fact_observations_mental (
    observation_id INTEGER PRIMARY KEY,
    encounter_id INTEGER UNIQUE NOT NULL,
    stress_level REAL NOT NULL,
    focus_score REAL NOT NULL,
    radical_acceptance_score REAL NOT NULL,
    focused_reflection_time REAL NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (encounter_id) REFERENCES fact_encounters_daily(encounter_id)
);

CREATE TABLE IF NOT EXISTS fact_state_transitions (
    transition_id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    previous_state TEXT NOT NULL,
    new_state TEXT NOT NULL,
    transition_date TEXT NOT NULL,
    days_in_previous_state INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES dim_users(user_id)
);

CREATE TABLE IF NOT EXISTS fact_clinical_events (
    event_id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    event_type TEXT NOT NULL,
    event_date TEXT NOT NULL,
    severity_score REAL NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES dim_users(user_id)
);

CREATE TABLE IF NOT EXISTS sys_schema_version (
    version_id INTEGER PRIMARY KEY AUTOINCREMENT,
    version_number TEXT NOT NULL,
    migration_name TEXT NOT NULL,
    description TEXT,
    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS sys_orchestration_job_runs (
    job_run_id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_name TEXT NOT NULL,
    execution_mode TEXT NOT NULL,
    status TEXT NOT NULL CHECK(status IN ('PENDING', 'RUNNING', 'COMPLETED', 'FAILED')),
    batch_number TEXT NOT NULL UNIQUE,
    num_users INTEGER NOT NULL,
    num_days INTEGER NOT NULL,
    db_path TEXT NOT NULL,
    start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    end_time TIMESTAMP,
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS sys_orchestration_events (
    event_id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_run_id INTEGER,
    event_type TEXT NOT NULL,
    component TEXT NOT NULL,
    message TEXT NOT NULL,
    metadata_json TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (job_run_id) REFERENCES sys_orchestration_job_runs(job_run_id)
);

CREATE INDEX idx_encounters_user_date ON fact_encounters_daily(user_id, date_str);
CREATE INDEX idx_transitions_user ON fact_state_transitions(user_id);
CREATE INDEX idx_events_user ON fact_clinical_events(user_id);
CREATE INDEX idx_job_runs_batch ON sys_orchestration_job_runs(batch_number);

CREATE TRIGGER trg_update_dim_concept_dictionary_modtime AFTER UPDATE ON dim_concept_dictionary
FOR EACH ROW WHEN (NEW.updated_at IS OLD.updated_at)
BEGIN UPDATE dim_concept_dictionary SET updated_at = CURRENT_TIMESTAMP WHERE ROWID = NEW.ROWID; END;

CREATE TRIGGER trg_update_dim_behavioral_archetypes_modtime AFTER UPDATE ON dim_behavioral_archetypes
FOR EACH ROW WHEN (NEW.updated_at IS OLD.updated_at)
BEGIN UPDATE dim_behavioral_archetypes SET updated_at = CURRENT_TIMESTAMP WHERE ROWID = NEW.ROWID; END;

CREATE TRIGGER trg_update_dim_users_modtime AFTER UPDATE ON dim_users
FOR EACH ROW WHEN (NEW.updated_at IS OLD.updated_at)
BEGIN UPDATE dim_users SET updated_at = CURRENT_TIMESTAMP WHERE ROWID = NEW.ROWID; END;

CREATE TRIGGER trg_update_fact_encounters_daily_modtime AFTER UPDATE ON fact_encounters_daily
FOR EACH ROW WHEN (NEW.updated_at IS OLD.updated_at)
BEGIN UPDATE fact_encounters_daily SET updated_at = CURRENT_TIMESTAMP WHERE ROWID = NEW.ROWID; END;

CREATE TRIGGER trg_update_fact_observations_mental_modtime AFTER UPDATE ON fact_observations_mental
FOR EACH ROW WHEN (NEW.updated_at IS OLD.updated_at)
BEGIN UPDATE fact_observations_mental SET updated_at = CURRENT_TIMESTAMP WHERE ROWID = NEW.ROWID; END;

CREATE TRIGGER trg_update_fact_state_transitions_modtime AFTER UPDATE ON fact_state_transitions
FOR EACH ROW WHEN (NEW.updated_at IS OLD.updated_at)
BEGIN UPDATE fact_state_transitions SET updated_at = CURRENT_TIMESTAMP WHERE ROWID = NEW.ROWID; END;

CREATE TRIGGER trg_update_fact_clinical_events_modtime AFTER UPDATE ON fact_clinical_events
FOR EACH ROW WHEN (NEW.updated_at IS OLD.updated_at)
BEGIN UPDATE fact_clinical_events SET updated_at = CURRENT_TIMESTAMP WHERE ROWID = NEW.ROWID; END;

CREATE TRIGGER trg_update_sys_schema_version_modtime AFTER UPDATE ON sys_schema_version
FOR EACH ROW WHEN (NEW.updated_at IS OLD.updated_at)
BEGIN UPDATE sys_schema_version SET updated_at = CURRENT_TIMESTAMP WHERE ROWID = NEW.ROWID; END;

CREATE TRIGGER trg_update_sys_orchestration_job_runs_modtime AFTER UPDATE ON sys_orchestration_job_runs
FOR EACH ROW WHEN (NEW.updated_at IS OLD.updated_at)
BEGIN UPDATE sys_orchestration_job_runs SET updated_at = CURRENT_TIMESTAMP WHERE ROWID = NEW.ROWID; END;

CREATE TRIGGER trg_update_sys_orchestration_events_modtime AFTER UPDATE ON sys_orchestration_events
FOR EACH ROW WHEN (NEW.updated_at IS OLD.updated_at)
BEGIN UPDATE sys_orchestration_events SET updated_at = CURRENT_TIMESTAMP WHERE ROWID = NEW.ROWID; END;
