# Mind Bender Machine Learning: Clinical EDW & Transition Engine

A modular clinical machine learning platform built on a SQLModel/SQLAlchemy clinical data warehouse star schema. The platform ingests longitudinal patient vitals and lab observations, builds 3x3 state transition feature matrices, updates cohort state transition logs, and trains downstream predictive models.

## Repository Layout

```text
mind_bender_machine_learning/
├── src/
│   ├── core/           # Abstract base classes and custom pipeline exceptions
│   ├── data/           # Synthetic generator and database EDW connectors/loaders
│   ├── features/       # 3x3 transition matrix builder and feature selection
│   ├── models/         # SQLModel database star schema and training loop
│   ├── state/          # Cohort state transition machine
│   └── pipeline.py     # Main orchestrator pipeline
├── docs/               # Architecture diagrams, math formulas, schema specs, legacy audits
├── data_legacy/        # Sample raw dirty legacy CSV files for ETL benchmarking
├── pyproject.toml      # Build metadata
├── setup.py            # Package installation setup
└── bootstrap.py        # Repository setup generator script
```

## Quick Start

1. Install package in editable mode:
   ```bash
   pip install -e .
   ```

2. Run the full end-to-end pipeline:
   ```bash
   python -m src.pipeline --db-url "sqlite:///clinical_star_schema.db" --generate-synthetic
   ```

3. Explore documentation in `docs/`:
   - `docs/schema_design.md`: EDW Star Schema & Data Mapping specifications.
   - `docs/architecture_and_diagrams.md`: Mermaid ERDs and sequence flows.
   - `docs/mathematical_formulation.md`: LaTeX math formulas for $3 \times 3$ matrices and scoring.
   - `docs/features_and_models.md`: Feature matrix construction and model training docs.
   - `docs/methodology.md`: Clinical cohort transition strategy.
   - `docs/legacy_data_audit.md`: Analysis of legacy unstructured/dirty CSV inputs.


## Background

I was going through through medium and saw an article talking about mental health, addiction, & religion. The article basically said that you cannot recover from substance use without having god. As someone who struggled with addiction and mental health I felt extremely upset with that comment. 

I also stayed at a sober living house in Chicago where I was repeatedly told that I could not get sober without having some "higher power". Every single day I was told this by AA, NA, and my sober living house. I refused to accept that. Sadly, this overly religious institution kicked me out for singing a song called "rich baby daddy" by Drake. They without notice threw me out onto the street not for using drugs, not for putting anyones sobriety at risk, but because they fundamentally could not accept my stance. They are shit. Their science is shit. Im gonna prove it. 

This sample dataset is roughly equivalent to the type of data that the application process that Bonaventure (The sober living house) collected about us. I downloaded this when I found it and since the article and data have been taken down. 
I am taking the opportunity to take the same dataset and critique it for its flaws and make into something productive. 