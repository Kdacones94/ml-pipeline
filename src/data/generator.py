import random
from datetime import datetime, timedelta
from typing import List
from src.models.schemas import ObservationRecordDTO

class SyntheticClinicalGenerator:
    """Generates synthetic longitudinal clinical vitals and lab observations."""

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
