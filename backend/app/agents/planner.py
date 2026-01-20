from app.core.logging import get_logger

logger = get_logger("planner")

async def run(state: dict) -> dict:
    query = state.get("query")
    evidence = state.get("evidence", [])

    if not evidence:
        logger.warning(f"planner_no_evidence query={query}")
        state["plan"] = "insufficient_evidence"
        return state

    logger.info("planner_created_plan")
    state["plan"] = "analyze_evidence"
    return state
