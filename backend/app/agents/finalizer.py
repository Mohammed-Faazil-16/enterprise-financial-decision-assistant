from app.agents.state import DecisionState
from app.core.logging import get_logger

logger = get_logger()


class FinalizerAgent:
    """
    Finalizer Agent:
    - Produces the final decision
    - Respects verifier outcome
    - Assigns confidence
    - Formats explanation
    """

    async def run(self, state: DecisionState) -> DecisionState:
        # If verification failed, we must stop safely
        if not state.verified:
            state.decision = "unable_to_confirm"
            state.confidence = 0.2

            logger.warning(
                "finalizer_blocked_by_verifier",
                verification_notes=state.verification_notes,
            )

            return state

        # If verified, we can produce a decision
        state.decision = "approved_with_conditions"
        state.confidence = 0.75

        logger.info(
            "finalizer_completed",
            decision=state.decision,
            confidence=state.confidence,
        )

        return state
