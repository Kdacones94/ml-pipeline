from typing import List, Generator
from sqlmodel import SQLModel, create_engine, Session, select
from src.models.schemas import PatientDimension, EncounterDimension, ClinicalObservationFact, ObservationRecordDTO
from src.core.base import BaseDataLoader

class EDWDatabaseConnector(BaseDataLoader):
    """Database Connector managing engine pooling, schema creation, and session queries."""

    def __init__(self, db_url: str = "sqlite:///clinical_star_schema.db", echo: bool = False):
        self.db_url = db_url
        self.engine = create_engine(self.db_url, echo=echo)

    def initialize_schema(self) -> None:
        """Execute DDL to build Star Schema tables."""
        SQLModel.metadata.create_all(self.engine)

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
            return session.exec(stmt).all()
