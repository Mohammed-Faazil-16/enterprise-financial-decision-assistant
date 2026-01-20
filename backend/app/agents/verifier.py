from app.core.logging import get_logger

logger = get_logger("verifier")

async def run(state: dict) -> dict:
    analysis = state.get("analysis")

    if not analysis:
        logger.warning("verification_failed_no_analysis")
        state["verified"] = False
        return state

    logger.info("verification_passed")
    state["verified"] = True
    return state
