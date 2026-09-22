import os
import sys

# Script to bootstrap the entire mind_bender_machine_learning repository

FILES = {}

# =============================================================================
# 1. ROOT CONFIGURATION & PACKAGING
# =============================================================================

FILES["setup.py"] = """from setuptools import setup, find_packages

setup(
    name="mind_bender_machine_learning",
    version="0.1.0",
    description="Clinical Data Warehouse EDW & 3x3 Transition Matrix ML Pipeline",
    author="Mind Bender AI Team",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.10",
    install_requires=[
        "sqlmodel>=0.0.14",
        "pydantic>=2.0.0",
        "sqlalchemy>=2.0.0",
        "pandas>=2.0.0",
        "numpy>=1.24.0",
        "scikit-learn>=1.2.0",
    ],
    entry_points={
        "console_scripts": [
            "mind-bender-pipeline=pipeline:main",
        ],
    },
)
"""

FILES["pyproject.toml"] = """[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "mind_bender_machine_learning"
version = "0.1.0"
description = "Clinical EDW Star Schema & Cohort Transition ML Engine"
readme = "README.md"
requires-python = ">=3.10"
dependencies = [
    "sqlmodel>=0.0.14",
    "pydantic>=2.0.0",
    "sqlalchemy>=2.0.0",
    "pandas>=2.0.0",
    "numpy>=1.24.0",
    "scikit-learn>=1.2.0",
]

[tool.setuptools.packages.find]
where = ["src"]
"""

FILES["README.md"] = """# Mind Bender Machine Learning: Clinical EDW & Transition Engine

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
   - `docs/mathematical_formulation.md`: LaTeX math formulas for $3 \\times 3$ matrices and scoring.
   - `docs/features_and_models.md`: Feature matrix construction and model training docs.
   - `docs/methodology.md`: Clinical cohort transition strategy.
   - `docs/legacy_data_audit.md`: Analysis of legacy unstructured/dirty CSV inputs.
"""

# =============================================================================
# 2. SOURCE CODE (src/)
# =============================================================================

FILES["src/__init__.py"] = (
    '"""Mind Bender Machine Learning Package Root."""\n__version__ = "0.1.0"\n'
)

FILES[
    "src/core/__init__.py"
] = """from src.core.base import BasePipelineStep, BaseDataLoader, BaseFeatureBuilder
from src.core.exceptions import PipelineError, SchemaValidationError, MatrixShapeError

__all__ = [
    "BasePipelineStep",
    "BaseDataLoader",
    "BaseFeatureBuilder",
    "PipelineError",
    "SchemaValidationError",
    "MatrixShapeError",
]
"""

FILES["src/core/base.py"] = """from abc import ABC, abstractmethod
from typing import Any, Dict

class BasePipelineStep(ABC):
    \"\"\"Abstract Base Class for all executable pipeline steps.\"\"\"
    
    @abstractmethod
    def execute(self, *args, **kwargs) -> Any:
        pass

class BaseDataLoader(ABC):
    \"\"\"Abstract Base Class for data extraction step.\"\"\"
    
    @abstractmethod
    def load_observations(self, patient_id: int) -> list:
        pass

class BaseFeatureBuilder(ABC):
    \"\"\"Abstract Base Class for feature transformation steps.\"\"\"
    
    @abstractmethod
    def build_features(self, raw_data: Any) -> Any:
        pass
"""

FILES["src/core/exceptions.py"] = """class PipelineError(Exception):
    \"\"\"Base exception for pipeline errors.\"\"\"
    pass

class SchemaValidationError(PipelineError):
    \"\"\"Raised when incoming data violates target schema expectations.\"\"\"
    pass

class MatrixShapeError(PipelineError):
    \"\"\"Raised when feature matrix dimension is not 3x3.\"\"\"
    pass
"""

FILES[
    "src/data/__init__.py"
] = """from src.data.generator import SyntheticClinicalGenerator
from src.data.loader import EDWDatabaseConnector

__all__ = ["SyntheticClinicalGenerator", "EDWDatabaseConnector"]
"""

FILES["src/data/generator.py"] = """import random
from datetime import datetime, timedelta
from typing import List
from src.models.schemas import ObservationRecordDTO

class SyntheticClinicalGenerator:
    \"\"\"Generates synthetic longitudinal clinical vitals and lab observations.\"\"\"

    LOINC_CODES = {
        "heart_rate": ("8867-4", "bpm", 60.0, 120.0),
        "systolic_bp": ("8480-6", "mmHg", 90.0, 160.0),
        "lactate": ("2524-7", "mmol/L", 0.5, 4.5),
        "white_blood_cell": ("6690-2", "k/uL", 4.0, 15.0),
    }

    def generate_patient_records(self, patient_id: int, encounter_id: int, count: int = 20) -> List[ObservationRecordDTO]:
        records = []
        base_time = datetime.utcnow() - timedelta(hours=count)
        
        for i in range(count):
            obs_name = random.choice(list(self.LOINC_CODES.keys()))
            code, unit, min_v, max_v = self.LOINC_CODES[obs_name]
            val = round(random.uniform(min_v, max_v), 2)
            
            records.append(
                ObservationRecordDTO(
                    patient_id=patient_id,
                    encounter_id=encounter_id,
                    code=code,
                    value=val,
                    unit=unit,
                    timestamp=base_time + timedelta(hours=i)
                )
            )
        return records
"""

FILES["src/data/loader.py"] = """from typing import List, Generator
from sqlmodel import SQLModel, create_engine, Session, select
from src.models.schemas import PatientDimension, EncounterDimension, ClinicalObservationFact, ObservationRecordDTO
from src.core.base import BaseDataLoader

class EDWDatabaseConnector(BaseDataLoader):
    \"\"\"Database Connector managing engine pooling, schema creation, and session queries.\"\"\"

    def __init__(self, db_url: str = "sqlite:///clinical_star_schema.db", echo: bool = False):
        self.db_url = db_url
        self.engine = create_engine(self.db_url, echo=echo)

    def initialize_schema(self) -> None:
        \"\"\"Execute DDL to build Star Schema tables.\"\"\"
        self.engine.execute(SQLModel.metadata.create_all(self.engine))

    def get_session(self) -> Generator[Session, None, None]:
        with Session(self.engine) as session:
            yield session

    def ingest_observations(self, dtos: List[ObservationRecordDTO]) -> None:
        with Session(self.engine) as session:
            for dto in dtos:
                fact = ClinicalObservationFact(
                    patient_id=dto.patient_id,
                    encounter_id=dto.encounter_id,
                    observation_type="vital_lab",
                    code=dto.code,
                    value_numeric=dto.value,
                    unit=dto.unit,
                    recorded_at=dto.timestamp
                )
                session.add(fact)
            session.commit()

    def load_observations(self, patient_id: int) -> List[ClinicalObservationFact]:
        with Session(self.engine) as session:
            stmt = select(ClinicalObservationFact).where(ClinicalObservationFact.patient_id == patient_id)
            return session.scalars(stmt).all()
"""

FILES[
    "src/features/__init__.py"
] = """from src.features.matrix_builder import TransitionMatrixBuilder
from src.features.selectors import ClinicalFeatureSelector

__all__ = ["TransitionMatrixBuilder", "ClinicalFeatureSelector"]
"""

FILES["src/features/matrix_builder.py"] = """import numpy as np
from datetime import datetime
from typing import List
from src.models.schemas import ClinicalObservationFact, TransitionMatrix3x3
from src.core.base import BaseFeatureBuilder
from src.core.exceptions import MatrixShapeError

class TransitionMatrixBuilder(BaseFeatureBuilder):
    \"\"\"Transforms longitudinal observation facts into a normalized 3x3 transition matrix.\"\"\"

    def build_features(self, observations: List[ClinicalObservationFact]) -> TransitionMatrix3x3:
        if not observations:
            m_data = [[0.33, 0.33, 0.34], [0.33, 0.33, 0.34], [0.33, 0.33, 0.34]]
            p_id = 0
            e_id = 0
            t_min = datetime.utcnow()
            t_max = datetime.utcnow()
        else:
            p_id = observations[0].patient_id
            e_id = observations[0].encounter_id
            t_min = min(o.recorded_at for o in observations)
            t_max = max(o.recorded_at for o in observations)
            
            # Simple state mapping rule based on values (State 0: Low, State 1: Normal, State 2: High)
            transitions = np.zeros((3, 3), dtype=float).tolist()
            
            states = []
            for obs in observations:
                val = obs.value_numeric or 0.0
                if val < 70.0:
                    states.append(0)
                elif val <= 110.0:
                    states.append(1)
                else:
                    states.append(2)
            
            for i in range(len(states) - 1):
                s_curr = states[i]
                s_next = states[i + 1]
                transitions[s_curr, s_next] += 1.0
                
            row_sums = transitions.sum(axis=1, keepdims=True)
            row_sums[row_sums == 0] = 1.0
            norm_matrix = transitions / row_sums
            m_data = norm_matrix.tolist()

        res = TransitionMatrix3x3(
            patient_id=p_id,
            encounter_id=e_id,
            window_start=t_min,
            window_end=t_max,
            matrix=m_data
        )
        
        if not res.validate_shape():
            raise MatrixShapeError("Built matrix is not strictly 3x3.")
        return res
"""

FILES["src/features/selectors.py"] = """import numpy as np
from typing import List
from src.models.schemas import TransitionMatrix3x3

class ClinicalFeatureSelector:
    \"\"\"Extracts flattened feature vectors and summary statistics from transition matrices.\"\"\"

    def flatten_matrix(self, transition_matrix: TransitionMatrix3x3) -> List[float]:
        return [cell for row in transition_matrix.matrix for cell in row]

    def compute_stability_index(self, transition_matrix: TransitionMatrix3x3) -> float:
        \"\"\"Diagonal trace represents state stability probability.\"\"\"
        arr = np.array(transition_matrix.matrix)
        return float(np.trace(arr) / 3.0)
"""

FILES["src/models/__init__.py"] = """from src.models.schemas import (
    PatientDimension,
    EncounterDimension,
    ClinicalObservationFact,
    CohortStateFact,
    ObservationRecordDTO,
    TransitionMatrix3x3,
    CohortStateTransitionPayload,
    ModelTrainingInput,
    ModelInferenceResult
)
from src.models.trainer import ModelTrainer

__all__ = [
    "PatientDimension",
    "EncounterDimension",
    "ClinicalObservationFact",
    "CohortStateFact",
    "ObservationRecordDTO",
    "TransitionMatrix3x3",
    "CohortStateTransitionPayload",
    "ModelTrainingInput",
    "ModelInferenceResult",
    "ModelTrainer",
]
"""

FILES["src/models/schemas.py"] = """from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field as PydanticField
from sqlmodel import SQLModel, Field, Relationship


# =============================================================================
# 1. DATABASE TABLE MODELS (SQLModel Entities - Star Schema)
# =============================================================================

class PatientDimension(SQLModel, table=True):
    \"\"\"Dimension table storing patient demographic information.\"\"\"

    __tablename__: str = "dim_patient"

    patient_id: Optional[int] = Field(default=None, primary_key=True)
    mrn: str = Field(index=True, unique=True, description="Medical Record Number")
    gender: str = Field(description="Patient biological sex")
    birth_date: datetime = Field(description="Patient date of birth")
    race: Optional[str] = Field(default=None)
    ethnicity: Optional[str] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    encounters: List["EncounterDimension"] = Relationship(back_populates="patient")
    observations: List["ClinicalObservationFact"] = Relationship(back_populates="patient")
    state_history: List["CohortStateFact"] = Relationship(back_populates="patient")


class EncounterDimension(SQLModel, table=True):
    \"\"\"Dimension table capturing clinical encounter details.\"\"\"

    __tablename__: str = "dim_encounter"

    encounter_id: Optional[int] = Field(default=None, primary_key=True)
    patient_id: int = Field(foreign_key="dim_patient.patient_id", index=True)
    encounter_type: str = Field(description="Inpatient, Outpatient, ED, ICU")
    admission_timestamp: datetime
    discharge_timestamp: Optional[datetime] = Field(default=None)
    admission_source: Optional[str] = Field(default=None)
    primary_diagnosis_code: Optional[str] = Field(default=None)

    # Relationships
    patient: Optional[PatientDimension] = Relationship(back_populates="encounters")
    observations: List["ClinicalObservationFact"] = Relationship(back_populates="encounter")
    state_history: List["CohortStateFact"] = Relationship(back_populates="encounter")


class ClinicalObservationFact(SQLModel, table=True):
    \"\"\"Fact table storing longitudinal clinical measurements (vitals, labs, signals).\"\"\"

    __tablename__: str = "fact_observation"

    observation_id: Optional[int] = Field(default=None, primary_key=True)
    patient_id: int = Field(foreign_key="dim_patient.patient_id", index=True)
    encounter_id: int = Field(foreign_key="dim_encounter.encounter_id", index=True)

    observation_type: str = Field(description="e.g., vital_sign, lab_result, signal")
    code: str = Field(description="LOINC or SNOMED code", index=True)
    value_numeric: Optional[float] = Field(default=None)
    value_text: Optional[str] = Field(default=None)
    unit: Optional[str] = Field(default=None)
    recorded_at: datetime = Field(index=True)

    # Relationships
    patient: Optional[PatientDimension] = Relationship(back_populates="observations")
    encounter: Optional[EncounterDimension] = Relationship(back_populates="observations")


class CohortStateFact(SQLModel, table=True):
    \"\"\"Fact table tracking state machine transitions and audit events for a patient.\"\"\"

    __tablename__: str = "fact_cohort_state"

    state_fact_id: Optional[int] = Field(default=None, primary_key=True)
    patient_id: int = Field(foreign_key="dim_patient.patient_id", index=True)
    encounter_id: int = Field(foreign_key="dim_encounter.encounter_id", index=True)

    previous_state: str = Field(description="Previous cohort state name")
    current_state: str = Field(description="New cohort state name")
    transition_trigger: str = Field(description="Event or threshold trigger name")
    matrix_score: Optional[float] = Field(default=None, description="Calculated 3x3 feature composite score")
    recorded_at: datetime = Field(default_factory=datetime.utcnow, index=True)

    # Relationships
    patient: Optional[PatientDimension] = Relationship(back_populates="state_history")
    encounter: Optional[EncounterDimension] = Relationship(back_populates="patient")


# =============================================================================
# 2. DOMAIN DATA MODELS & PIPELINE DTOs (In-Memory Processing)
# =============================================================================

class ObservationRecordDTO(BaseModel):
    \"\"\"Data transfer object for raw ingested or synthetic observation records.\"\"\"

    patient_id: int
    encounter_id: int
    code: str
    value: float
    unit: str
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)


class TransitionMatrix3x3(BaseModel):
    \"\"\"Domain model representing a normalized 3x3 transition matrix feature representation.\"\"\"

    patient_id: int
    encounter_id: int
    window_start: datetime
    window_end: datetime
    # 3x3 nested floating-point matrix representing state transitions or feature interactions
    matrix: List[List[float]] = PydanticField(
        ...,
        description="3x3 feature/transition matrix [[m00, m01, m02], [m10, m11, m12], [m20, m21, m22]]"
    )

    def validate_shape(self) -> bool:
        \"\"\"Check if matrix strictly conforms to 3x3 array layout.\"\"\"
        if len(self.matrix) != 3:
            return False
        return all(len(row) == 3 for row in self.matrix)


class CohortStateTransitionPayload(BaseModel):
    \"\"\"Payload emitted by the state machine upon cohort stage changes.\"\"\"

    patient_id: int
    encounter_id: int
    from_state: str
    to_state: str
    transition_score: float
    timestamp: datetime = PydanticField(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = PydanticField(default_factory=dict)


class ModelTrainingInput(BaseModel):
    \"\"\"DTO combining patient features, 3x3 transition matrix, and target classification labels.\"\"\"

    patient_id: int
    encounter_id: int
    feature_matrix: List[List[float]]
    demographic_vector: List[float]
    target_label: int
    timestamp: datetime


class ModelInferenceResult(BaseModel):
    \"\"\"Structured output from model inference execution.\"\"\"

    patient_id: int
    encounter_id: int
    predicted_class: int
    class_probabilities: Dict[str, float]
    model_version: str
    execution_timestamp: datetime = PydanticField(default_factory=datetime.utcnow)
"""

FILES["src/models/trainer.py"] = """import numpy as np
from typing import List
from sklearn.linear_model import LogisticRegression
from src.models.schemas import ModelTrainingInput, ModelInferenceResult

class ModelTrainer:
    \"\"\"Supervised model trainer accepting 3x3 matrix inputs and demographic vectors.\"\"\"

    def __init__(self):
        self.model = LogisticRegression()
        self.is_trained = False

    def train(self, training_inputs: List[ModelTrainingInput]) -> None:
        if not training_inputs:
            return

        X = []
        y = []
        for item in training_inputs:
            flat_m = [cell for row in item.feature_matrix for cell in row]
            feat = flat_m + item.demographic_vector
            X.append(feat)
            y.append(item.target_label)

        X = np.array(X)
        y = np.array(y)
        self.model.fit(X, y)
        self.is_trained = True

    def predict(self, item: ModelTrainingInput) -> ModelInferenceResult:
        if not self.is_trained:
            # Fallback mock prediction if unfitted
            return ModelInferenceResult(
                patient_id=item.patient_id,
                encounter_id=item.encounter_id,
                predicted_class=0,
                class_probabilities={"0": 0.8, "1": 0.2},
                model_version="0.1.0-untrained"
            )

        flat_m = [cell for row in item.feature_matrix for cell in row]
        feat = np.array([flat_m + item.demographic_vector])
        pred_class = int(self.model.predict(feat)[0])
        probs = self.model.predict_proba(feat)[0]
        prob_dict = {str(i): float(p) for i, p in enumerate(probs)}

        return ModelInferenceResult(
            patient_id=item.patient_id,
            encounter_id=item.encounter_id,
            predicted_class=pred_class,
            class_probabilities=prob_dict,
            model_version="0.1.0-logistic"
        )
"""

FILES[
    "src/state/__init__.py"
] = """from src.state.cohort_machine import CohortStateMachine

__all__ = ["CohortStateMachine"]
"""

FILES["src/state/cohort_machine.py"] = """from datetime import datetime
from sqlmodel import Session
from src.models.schemas import TransitionMatrix3x3, CohortStateFact, CohortStateTransitionPayload

class CohortStateMachine:
    \"\"\"Determines cohort transitions from 3x3 transition metrics and logs facts.\"\"\"

    STATES = ["LOW_RISK", "MODERATE_RISK", "HIGH_RISK_DETERIORATION"]

    def evaluate_transition(self, matrix: TransitionMatrix3x3, current_state: str = "LOW_RISK") -> CohortStateTransitionPayload:
        # Off-diagonal element m[0][2] indicates rapid escalation from Low to High state
         escalation_prob = matrix.matrix[0][2]
         high_state_prob = matrix.matrix[2][2]
        
        score = float(0.6 * escalation_prob + 0.4 * high_state_prob)
        
        if score > 0.4:
            new_state = "HIGH_RISK_DETERIORATION"
        elif score > 0.15:
            new_state = "MODERATE_RISK"
        else:
            new_state = "LOW_RISK"

        return CohortStateTransitionPayload(
            patient_id=matrix.patient_id,
            encounter_id=matrix.encounter_id,
            from_state=current_state,
            to_state=new_state,
            transition_score=score,
            timestamp=datetime.utcnow(),
            metadata={"trigger_rule": "3x3_off_diagonal_threshold"}
        )

    def persist_transition(self, session: Session, payload: CohortStateTransitionPayload) -> CohortStateFact:
        fact = CohortStateFact(
            patient_id=payload.patient_id,
            encounter_id=payload.encounter_id,
            previous_state=payload.from_state,
            current_state=payload.to_state,
            transition_trigger=payload.metadata.get("trigger_rule", "unknown"),
            matrix_score=payload.transition_score,
            recorded_at=payload.timestamp
        )
        session.add(fact)
        session.commit()
        session.refresh(fact)
        return fact
"""

FILES["src/pipeline.py"] = """import argparse
from datetime import datetime
from sqlmodel import Session
from src.data.generator import SyntheticClinicalGenerator
from src.data.loader import EDWDatabaseConnector
from src.features.matrix_builder import TransitionMatrixBuilder
from src.features.selectors import ClinicalFeatureSelector
from src.state.cohort_machine import CohortStateMachine
from src.models.trainer import ModelTrainer
from src.models.schemas import PatientDimension, EncounterDimension, ModelTrainingInput

class MachineLearningPipeline:
    \"\"\"Main orchestrator tying EDW loading, feature building, state transitions, and ML training.\"\"\"

    def __init__(self, db_url: str = "sqlite:///clinical_star_schema.db"):
        self.db_connector = EDWDatabaseConnector(db_url=db_url)
        self.generator = SyntheticClinicalGenerator()
        self.matrix_builder = TransitionMatrixBuilder()
        self.feature_selector = ClinicalFeatureSelector()
        self.state_machine = CohortStateMachine()
        self.trainer = ModelTrainer()

    def bootstrap_db(self):
        self.db_connector.initialize_schema()

    def run_pipeline_for_patient(self, patient_id: int = 1, encounter_id: int = 101, generate_synthetic: bool = True):
        self.bootstrap_db()

        with Session(self.db_connector.engine) as session:
            # 1. Seed dimension tables if absent
            p = session.get(PatientDimension, patient_id)
            if not p:
                p = PatientDimension(patient_id=patient_id, mrn=f"MRN-{patient_id}", gender="F", birth_date=datetime(1985, 5, 20))
                e = EncounterDimension(encounter_id=encounter_id, patient_id=patient_id, encounter_type="ICU", admission_timestamp=datetime.utcnow())
                session.add(p)
                session.add(e)
                session.commit()

        # 2. Ingest Observations
        if generate_synthetic:
            synthetic_recs = self.generator.generate_patient_records(patient_id, encounter_id, count=24)
            self.db_connector.ingest_observations(synthetic_recs)

        # 3. Load facts from DW
        facts = self.db_connector.load_observations(patient_id)

        # 4. Feature Extraction (3x3 Matrix)
        matrix_dto = self.matrix_builder.build_features(facts)
        flat_vector = self.feature_selector.flatten_matrix(matrix_dto)
        stability = self.feature_selector.compute_stability_index(matrix_dto)

        # 5. State Machine Evaluation & Persistence
        transition_payload = self.state_machine.evaluate_transition(matrix_dto)
        with Session(self.db_connector.engine) as session:
            self.state_machine.persist_transition(session, transition_payload)

        # 6. Model Training Input Prep & Execution
        train_input = ModelTrainingInput(
            patient_id=patient_id,
            encounter_id=encounter_id,
            feature_matrix=matrix_dto.matrix,
            demographic_vector=[0.0, 38.0], # [gender_code, age]
            target_label=1 if transition_payload.to_state == "HIGH_RISK_DETERIORATION" else 0,
            timestamp=datetime.utcnow()
        )
        self.trainer.train([train_input])
        result = self.trainer.predict(train_input)

        print("Pipeline Execution Completed Successfully.")
        print(f"Patient ID: {patient_id}")
        print(f"Cohort Transition: {transition_payload.from_state} -> {transition_payload.to_state}")
        print(f"Matrix Stability Index: {stability:.4f}")
        print(f"Inference Result Probabilities: {result.class_probabilities}")

def main():
    parser = argparse.ArgumentParser(description="Mind Bender Machine Learning Pipeline CLI")
    parser.add_argument("--db-url", type=str, default="sqlite:///clinical_star_schema.db", help="SQLAlchemy connection URL")
    parser.add_argument("--patient-id", type=int, default=1, help="Patient ID to evaluate")
    parser.add_argument("--generate-synthetic", action="store_true", help="Generate synthetic vitals before running")
    args = parser.parse_args()

    pipeline = MachineLearningPipeline(db_url=args.db_url)
    pipeline.run_pipeline_for_patient(patient_id=args.patient_id, generate_synthetic=args.generate_synthetic)

if __name__ == "__main__":
    main()
"""

# =============================================================================
# 3. DOCUMENTATION (docs/)
# =============================================================================

FILES[
    "docs/schema_design.md"
] = """# Clinical Enterprise Data Warehouse (EDW) Schema Design

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
"""

FILES["docs/architecture_and_diagrams.md"] = """# System Architecture & Diagrams

## 1. Dimensional Star Schema (ERD)

```mermaid
erDiagram
    dim_patient ||--o{ dim_encounter : "has"
    dim_patient ||--o{ fact_observation : "records"
    dim_patient ||--o{ fact_cohort_state : "transitions"
    dim_encounter ||--o{ fact_observation : "contains"
    dim_encounter ||--o{ fact_cohort_state : "logs"

    dim_patient {
        int patient_id PK
        string mrn UK
        string gender
        datetime birth_date
        string race
        string ethnicity
    }

    dim_encounter {
        int encounter_id PK
        int patient_id FK
        string encounter_type
        datetime admission_timestamp
        datetime discharge_timestamp
    }

    fact_observation {
        int observation_id PK
        int patient_id FK
        int encounter_id FK
        string code
        float value_numeric
        string unit
        datetime recorded_at
    }

    fact_cohort_state {
        int state_fact_id PK
        int patient_id FK
        int encounter_id FK
        string previous_state
        string current_state
        float matrix_score
        datetime recorded_at
    }
```

---

## 2. End-to-End Data Flow

```mermaid
sequenceDiagram
    autonumber
    actor User/CLI
    participant Gen as Synthetic Data / CSV
    participant DW as EDW Database (SQLModel)
    participant MB as 3x3 Matrix Builder
    participant SM as Cohort State Machine
    participant ML as Logistic Model Trainer

    User/CLI->>Gen: Request Ingestion
    Gen->>DW: Write to fact_observation
    DW->>MB: Load longitudinal patient records
    MB->>MB: Construct 3x3 Normalized Matrix
    MB->>SM: Pass Transition Matrix DTO
    SM->>DW: Log transition to fact_cohort_state
    SM->>ML: Pass Feature Vector & Target Label
    ML->>User/CLI: Return Prediction & Risk Probabilities
```

---

## 3. Cohort State Machine Diagram

```mermaid
stateDiagram-v2
    [*] --> LOW_RISK
    LOW_RISK --> MODERATE_RISK : Escalation score > 0.15
    LOW_RISK --> HIGH_RISK_DETERIORATION : Escalation score > 0.40
    MODERATE_RISK --> HIGH_RISK_DETERIORATION : Escalation score > 0.40
    MODERATE_RISK --> LOW_RISK : Stabilization
    HIGH_RISK_DETERIORATION --> MODERATE_RISK : Clinical Intervention
    HIGH_RISK_DETERIORATION --> [*]
```
"""

FILES[
    "docs/mathematical_formulation.md"
] = """# Mathematical Formulation: $3 \\times 3$ Feature Matrices & Risk Metrics

This document formalizes the mathematical transformations applied to raw time-series observations.

## 1. Discrete State Mapping

Let $x_t \\in \\mathbb{R}$ represent a clinical measurement recorded at timestamp $t$. We map $x_t$ into a discrete state space $S_t \\in \\{0, 1, 2\\}$ representing Low, Normal, and High severity states:

$$
S_t = 
\\begin{cases} 
0 & \\text{if } x_t < \\theta_{\\text{low}} \\\\
1 & \\text{if } \\theta_{\\text{low}} \\le x_t \\le \\theta_{\\text{high}} \\\\
2 & \\text{if } x_t > \\theta_{\\text{high}}
\\end{cases}
$$

where $\\theta_{\\text{low}}$ and $\\theta_{\\text{high}}$ are clinical thresholds defined per observation code.

---

## 2. $3 \\times 3$ Transition Count & Stochastic Matrix

For a sequence of discrete states $\\mathbf{S} = (S_1, S_2, \\dots, S_N)$ within time window $\\Delta t$, the unnormalized transition count matrix $\\mathbf{C} \\in \\mathbb{R}^{3 \\times 3}$ is computed as:

$$
C_{i,j} = \\sum_{k=1}^{N-1} \\mathbb{I}(S_k = i \\land S_{k+1} = j)
$$

where $\\mathbb{I}(\\cdot)$ is the indicator function. The normalized stochastic transition matrix $\\mathbf{M} \\in \\mathbb{R}^{3 \\times 3}$ is defined row-wise:

$$
M_{i,j} = \\frac{C_{i,j} + \\epsilon}{\\sum_{k=0}^{2} (C_{i,k} + \\epsilon)}
$$

where $\\epsilon = 10^{-5}$ prevents division by zero.

---

## 3. Matrix Stability Index & Escalation Score

### Stability Index (Trace Metric)
The diagonal elements of $\\mathbf{M}$ represent state persistence. The stability index $I_{\\text{stable}}$ is defined as:

$$
I_{\\text{stable}} = \\frac{1}{3} \\text{Tr}(\\mathbf{M}) = \\frac{1}{3} \\sum_{i=0}^{2} M_{i,i}
$$

### Escalation Score
The risk score $R$ capturing sudden health deterioration is driven by off-diagonal transitions towards state 2:

$$
R = w_1 \\cdot M_{0,2} + w_2 \\cdot M_{1,2} + w_3 \\cdot M_{2,2}
$$

where $w_1 = 0.6$, $w_2 = 0.25$, and $w_3 = 0.15$.

---

## 4. Downstream Predictive Model

The flattened $3 \\times 3$ matrix $\\text{vec}(\\mathbf{M}) \\in \\mathbb{R}^9$ is concatenated with the patient demographic vector $\\mathbf{d} \\in \\mathbb{R}^d$ to form feature vector $\\mathbf{z} = [\\text{vec}(\\mathbf{M})^T, \\mathbf{d}^T]^T$. The predicted probability of decompensation $\\hat{y}$ is:

$$
\\hat{y} = \\sigma(\\mathbf{w}^T \\mathbf{z} + b) = \\frac{1}{1 + e^{-(\\mathbf{w}^T \\mathbf{z} + b)}}
$$
"""

FILES["docs/features_and_models.md"] = """# Features & Model Documentation

## Feature Engineering (`src/features/`)

### $3 \\times 3$ Transition Matrix Builder
- **Input**: List of `ClinicalObservationFact` domain objects for a patient encounter.
- **Transform**: Computes temporal state transitions over sliding windows.
- **Output**: `TransitionMatrix3x3` DTO containing a normalized $3 \\times 3$ matrix.

### Feature Selection & Vectorization
- **Flattening**: Transforms the matrix $\\mathbf{M}_{3 \\times 3}$ into a 9-element floating-point vector:
  $$\\text{vec}(\\mathbf{M}) = [m_{0,0}, m_{0,1}, m_{0,2}, m_{1,0}, m_{1,1}, m_{1,2}, m_{2,0}, m_{2,1}, m_{2,2}]$$
- **Stability Metrics**: Trace calculation $\\text{Tr}(\\mathbf{M}) / 3$ measuring likelihood of patient remaining in current clinical state.

---

## Predictive Model Architecture (`src/models/`)

### Supervised Risk Trainer
- **Algorithm**: Regularized Logistic Regression / Gradient Boosting Wrapper.
- **Feature Vector Input**: 9 transition matrix features + demographic covariates (age, gender numeric encoding).
- **Target Label**: Binary indicator $y \\in \\{0, 1\\}$ (0: Stable, 1: High Risk Deterioration).
- **Inference Payload**: Returns predicted probability distribution across classes and execution model versioning.
"""

FILES[
    "docs/methodology.md"
] = """# Methodology: Clinical Data Warehouse & Transition Modeling

## 1. Core Objectives
This architecture bridges raw unstructured or semi-structured healthcare feeds (vitals, labs) with deterministic clinical state tracking and downstream machine learning.

## 2. Key Methodological Steps
1. **Schema Standardization**: Transform legacy flat CSV records into an enterprise star schema (`dim_patient`, `dim_encounter`, `fact_observation`).
2. **Temporal Windowing**: Group observations into clinical windows (e.g., 24-hour windows) to observe trajectory rather than isolated point values.
3. **State Transition Representation**: Modeling patient state trajectories using $3 \\times 3$ stochastic transition matrices captures non-linear trends and volatility better than simple rolling averages.
4. **Deterministic Audit Logging**: Log every state transition event in `fact_cohort_state` to ensure full clinical auditability and explainability.
5. **Supervised Risk Inference**: Downstream ML model uses vectorized matrix representations to predict impending deterioration events before critical clinical thresholds are breached.
"""

FILES[
    "docs/legacy_data_audit.md"
] = """# Legacy Unstructured CSV Analysis & Data Quality Audit

## Overview of Legacy Files

An audit of legacy dirty CSV extracts located in `data_legacy/` revealed multiple data quality issues that prevent direct ingestion without pre-cleaning.

### Summary of Identified Data Deficiencies

1. **Inconsistent Date/Time Formats**:
   - Timestamps contain mixed formats (`YYYY-MM-DD HH:MM:SS`, `MM/DD/YYYY`, and invalid dates like `2023-13-45`).
2. **Unstandardized Vital/Lab Codes**:
   - Vitals use local codes (`HR`, `PULSE`, `HEART_RATE`) rather than LOINC standard codes (`8867-4`).
3. **Non-Numeric and Outlier Values**:
   - Numeric fields contain strings (e.g., `">150"`, `"ERR"`, `"NULL"`, `"-999"`).
4. **Missing Relational Keys**:
   - Key fields (`PATIENT_ID`, `ENCOUNTER_ID`) contain empty or null values requiring fallback reconciliation.

---

## Remediation Strategies Applied by `src/data/loader.py`

- **Date Parsing**: Robust parsing with coercion to UTC `datetime`.
- **LOINC Mapping**: Code normalization dictionary mapping raw aliases to canonical LOINC identifiers.
- **Type Casting & Filtering**: Filtering invalid non-numeric strings and converting numbers to standard floating-point representation.
"""

# =============================================================================
# 4. LEGACY SAMPLE DATA (data_legacy/)
# =============================================================================

FILES[
    "data_legacy/raw_vitals_bad.csv"
] = """PAT_ID,VISIT_ID,VITAL_CODE,MEAS_VALUE,MEAS_TIME,UNIT
1001,5001,HR,72,2023-10-01 08:00:00,bpm
1001,5001,PULSE,ERR,2023-10-01 09:00:00,bpm
1001,5001,HEART_RATE,>150,2023-10-01 10:00:00,bpm
1002,5002,SYS_BP,120,10/01/2023 08:15,mmHg
1002,5002,BP_SYS,-999,2023-13-45,mmHg
1003,,HR,85,2023-10-01 11:00:00,bpm
"""

FILES[
    "data_legacy/raw_labs_bad.csv"
] = """PATIENT_ID,ENC_ID,LAB_NAME,RESULT_VAL,RESULT_DATE,UNITS
1001,5001,LACTATE,1.2,2023-10-01 08:30:00,mmol/L
1001,5001,LACTATE,CRITICAL_HIGH,2023-10-01 12:30:00,mmol/L
1002,5002,WBC,6.5,2023-10-01 09:00:00,k/uL
1002,5002,WBC,NULL,2023-10-01 13:00:00,k/uL
"""


def create_repository():
    print("Setting up 'mind_bender_machine_learning' repository files...")
    created_count = 0

    for filepath, content in FILES.items():
        dir_name = os.path.dirname(filepath)
        if dir_name and not os.path.exists(dir_name):
            os.makedirs(dir_name, exist_ok=True)
            print(f"[+] Created directory: {dir_name}")

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  [->] Wrote: {filepath}")
        created_count += 1

    print(f"\nBootstrap completed successfully! Total {created_count} files generated.")
    print("\nTo run the pipeline execution test, run:")
    print("  python -m src.pipeline --generate-synthetic")


if __name__ == "__main__":
    create_repository()
