import argparse
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
    """Main orchestrator tying EDW loading, feature building, state transitions, and ML training."""

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
