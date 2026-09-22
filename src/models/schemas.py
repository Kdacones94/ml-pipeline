from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, ConfigDict, Field as PydanticField
from sqlmodel import SQLModel, Field, Relationship

# =============================================================================
# 1. DATABASE TABLE MODELS (SQLModel Entities - Star Schema)
# =============================================================================


class PatientDimension(SQLModel, table=True):
    """Dimension table storing patient demographic information."""

    __tablename__: str = "dim_patient"  # type: ignore

    patient_id: Optional[int] = Field(default=None, primary_key=True)
    mrn: str = Field(index=True, unique=True, description="Medical Record Number")
    gender: str = Field(description="Patient biological sex")
    birth_date: datetime = Field(description="Patient date of birth")
    race: Optional[str] = Field(default=None)
    ethnicity: Optional[str] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    encounters: List["EncounterDimension"] = Relationship(back_populates="patient")
    observations: List["ClinicalObservationFact"] = Relationship(
        back_populates="patient"
    )
    state_history: List["CohortStateFact"] = Relationship(back_populates="patient")


class EncounterDimension(SQLModel, table=True):
    """Dimension table capturing clinical encounter details."""

    __tablename__: str = "dim_encounter"  # type: ignore

    encounter_id: Optional[int] = Field(default=None, primary_key=True)
    patient_id: int = Field(foreign_key="dim_patient.patient_id", index=True)
    encounter_type: str = Field(description="Inpatient, Outpatient, ED, ICU")
    admission_timestamp: datetime
    discharge_timestamp: Optional[datetime] = Field(default=None)
    admission_source: Optional[str] = Field(default=None)
    primary_diagnosis_code: Optional[str] = Field(default=None)

    # Relationships
    patient: Optional[PatientDimension] = Relationship(back_populates="encounters")
    observations: List["ClinicalObservationFact"] = Relationship(
        back_populates="encounter"
    )
    state_history: List["CohortStateFact"] = Relationship(back_populates="encounter")


class ClinicalObservationFact(SQLModel, table=True):
    """Fact table storing longitudinal clinical measurements (vitals, labs, signals)."""

    __tablename__: str = "fact_observation"  # type: ignore

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
    encounter: Optional[EncounterDimension] = Relationship(
        back_populates="observations"
    )


class CohortStateFact(SQLModel, table=True):
    """Fact table tracking state machine transitions and audit events for a patient."""

    __tablename__: str = "fact_cohort_state"  # type: ignore

    state_fact_id: Optional[int] = Field(default=None, primary_key=True)
    patient_id: int = Field(foreign_key="dim_patient.patient_id", index=True)
    encounter_id: int = Field(foreign_key="dim_encounter.encounter_id", index=True)

    previous_state: str = Field(description="Previous cohort state name")
    current_state: str = Field(description="New cohort state name")
    transition_trigger: str = Field(description="Event or threshold trigger name")
    matrix_score: Optional[float] = Field(
        default=None, description="Calculated 3x3 feature composite score"
    )
    recorded_at: datetime = Field(default_factory=datetime.utcnow, index=True)

    # Relationships
    patient: Optional[PatientDimension] = Relationship(back_populates="state_history")
    encounter: Optional[EncounterDimension] = Relationship(back_populates="patient")


# =============================================================================
# 2. DOMAIN DATA MODELS & PIPELINE DTOs (In-Memory Processing)
# =============================================================================


class ObservationRecordDTO(BaseModel):
    """Data transfer object for raw ingested or synthetic observation records."""

    patient_id: int
    encounter_id: int
    code: str
    value: float
    unit: str
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)


class TransitionMatrix3x3(BaseModel):
    """Domain model representing a normalized 3x3 transition matrix feature representation."""

    patient_id: int
    encounter_id: int
    window_start: datetime
    window_end: datetime
    # 3x3 nested floating-point matrix representing state transitions or feature interactions
    matrix: List[List[float]] = PydanticField(
        ...,
        description="3x3 feature/transition matrix [[m00, m01, m02], [m10, m11, m12], [m20, m21, m22]]",
    )

    def validate_shape(self) -> bool:
        """Check if matrix strictly conforms to 3x3 array layout."""
        if len(self.matrix) != 3:
            return False
        return all(len(row) == 3 for row in self.matrix)


class CohortStateTransitionPayload(BaseModel):
    """Payload emitted by the state machine upon cohort stage changes."""

    patient_id: int
    encounter_id: int
    from_state: str
    to_state: str
    transition_score: float
    timestamp: datetime = PydanticField(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = PydanticField(default_factory=dict)


class ModelTrainingInput(BaseModel):
    """DTO combining patient features, 3x3 transition matrix, and target classification labels."""

    patient_id: int
    encounter_id: int
    feature_matrix: List[List[float]]
    demographic_vector: List[float]
    target_label: int
    timestamp: datetime


class ModelInferenceResult(BaseModel):
    """Structured output from model inference execution."""

    patient_id: int
    encounter_id: int
    predicted_class: int
    class_probabilities: Dict[str, float]
    model_version: str
    execution_timestamp: datetime = PydanticField(default_factory=datetime.utcnow)
