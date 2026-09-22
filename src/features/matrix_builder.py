import numpy as np
from datetime import datetime
from typing import List
from src.models.schemas import ClinicalObservationFact, TransitionMatrix3x3
from src.core.base import BaseFeatureBuilder
from src.core.exceptions import MatrixShapeError

class TransitionMatrixBuilder(BaseFeatureBuilder):
    """Transforms longitudinal observation facts into a normalized 3x3 transition matrix."""

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
            transitions = np.zeros((3, 3), dtype=float)
            
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
