from app.core.logging import get_logger

logger = get_logger("finalizer")

async def run(state: dict) -> dict:
    verified = state.get("verified", False)

    if not verified:
        decision = "cannot_decide"
        confidence = 0.2
    else:
        decision = "approved_with_conditions"
        confidence = 0.75

    logger.info(f"decision_finalized decision={decision} confidence={confidence}")

    state["decision"] = decision
    state["confidence"] = confidence
    return state
