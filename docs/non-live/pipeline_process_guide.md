# Visual Process Guide: End-to-End Behavioral Pipeline & ML Survival Engine

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       INGESTION SUBSYSTEM (CLI: --mode ingest)               │
├─────────────────────────────────────────────────────────────────────────────┤
│  Cohort Generator ──► Concurrency Engine ──► Clinical State Machine        │
│                              │                      │                       │
│                              ▼                      ▼                       │
│                   Fact Chunks Generator    Markov Shift Observer           │
│                              │                      │                       │
│                              └──────────┬───────────┘                       │
│                                         ▼                                   │
│            SQLite Bulk Repository Sink (Versioning & Job Control)          │
└─────────────────────────────────────────┬───────────────────────────────────┘
                                          │  [Decoupled File Boundary]
                                          ▼  output/clinical_star_schema.db
┌─────────────────────────────────────────────────────────────────────────────┐
│                          ML SUBSYSTEM (CLI: --mode ml)                      │
├─────────────────────────────────────────────────────────────────────────────┤
│  ClinicalMLBridge ──► Feature Matrix (X, y) ──► Random Forest Classifier    │
│                              │                        │                     │
│                              ▼                        ▼                     │
│                   TTE Survival Dataset     Gini Feature Importances (W)     │
│                              │                        │                     │
│                              └──────────┬─────────────┘                     │
│                                         ▼                                   │
│                     Feature-Weighted Cox Proportional Hazards               │
│                                         │                                   │
│                                         ▼                                   │
│                 Visualization Suite & ElasticSearch NDJSON Export           │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Step 1: Ingestion & Markov State Evaluation
Each day, the state engine computes latent balance:
$$ \text{latent\_balance} = 100.0 - |\text{focus\_score} - \text{radical\_acceptance\_score}| $$

## Step 2: Predictive Machine Learning & Survival Analysis
1. **Random Forest Classifier**: Fits feature matrix $X$ to predict binary burnout flags and extracts Gini importance weights $W$.
2. **Weighted Cox PH Regression**: Scales features by $W$ to fit time-to-event survival models ($S(t)$).
