from app.core.logging import get_logger

logger = get_logger("verifier")

async def run(state: dict) -> dict:
    plan = state.get("plan")
    eligible = state.get("eligible")
    analysis = state.get("analysis")

    # No evidence → cannot verify
    if plan == "insufficient_evidence":
        logger.warning("verification_failed_insufficient_evidence")
        state["verified"] = False
        return state

    # Analyzer must explicitly say yes/no
    if eligible not in {"yes", "no"}:
        logger.warning("verification_failed_uncertain_eligibility")
        state["verified"] = False
        return state

    # Valid analysis + eligibility
    if analysis:
        logger.info("verification_passed")
        state["verified"] = True
        return state

    state["verified"] = False
    return state
