from datetime import datetime
from enum import Enum
from sqlmodel import Session
from src.models.schemas import (
    TransitionMatrix3x3,
    CohortStateFact,
    CohortStateTransitionPayload,
)


class CohortStateMachine:
    """Determines cohort transitions from 3x3 transition metrics and logs facts."""

    STATES = ["LOW_RISK", "MODERATE_RISK", "HIGH_RISK_DETERIORATION"]
    

    # TODO - See how this impact the calculation of the transition counts
    # ENUM_STATES = Enum("LOW_RISK"= 1,
        "MODERATE_RISK" = 2,
        "HIGH_RISK_DETERIORATION" = 3)

    def evaluate_transition(
        self, matrix: TransitionMatrix3x3, current_state: str = "LOW_RISK"
    ) -> CohortStateTransitionPayload:
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
            metadata={"trigger_rule": "3x3_off_diagonal_threshold"},
        )

    def persist_transition(
        self, session: Session, payload: CohortStateTransitionPayload
    ) -> CohortStateFact:
        fact = CohortStateFact(
            patient_id=payload.patient_id,
            encounter_id=payload.encounter_id,
            previous_state=payload.from_state,
            current_state=payload.to_state,
            transition_trigger=payload.metadata.get("trigger_rule", "unknown"),
            matrix_score=payload.transition_score,
            recorded_at=payload.timestamp,
        )
        session.add(fact)
        session.commit()
        session.refresh(fact)
        return fact
