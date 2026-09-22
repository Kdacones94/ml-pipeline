import numpy as np
from typing import List
from src.models.schemas import TransitionMatrix3x3

class ClinicalFeatureSelector:
    """Extracts flattened feature vectors and summary statistics from transition matrices."""

    def flatten_matrix(self, transition_matrix: TransitionMatrix3x3) -> List[float]:
        return [cell for row in transition_matrix.matrix for cell in row]

    def compute_stability_index(self, transition_matrix: TransitionMatrix3x3) -> float:
        """Diagonal trace represents state stability probability."""
        arr = np.array(transition_matrix.matrix)
        return float(np.trace(arr) / 3.0)
