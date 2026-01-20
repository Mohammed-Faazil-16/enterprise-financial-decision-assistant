from app.core.logging import get_logger

logger = get_logger("analyzer")

async def run(state: dict) -> dict:
    evidence = state.get("evidence", [])

    analysis = " ".join(evidence)
    logger.info("analysis_completed")

    state["analysis"] = analysis
    return state
