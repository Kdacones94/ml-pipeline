import numpy as np
from typing import List
from sklearn.linear_model import LogisticRegression
from src.models.schemas import ModelTrainingInput, ModelInferenceResult


class ModelTrainer:
    """Supervised model trainer accepting 3x3 matrix inputs and demographic vectors."""

    def __init__(self):
        self.model = LogisticRegression(solver="lbfgs")
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

        X = np.array(X, dtype=object)
        y = np.array(y, dtype=object)
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
                model_version="0.1.0-untrained",
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
            model_version="0.1.0-logistic",
        )
