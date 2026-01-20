import logging

logger = logging.getLogger("planner")

async def run(state: dict) -> dict:
    query = state.get("query")
    evidence = state.get("evidence", [])

    if not evidence:
        logger.warning("planner_no_evidence", extra={"query": query})
        state["plan"] = "insufficient_evidence"
        return state

    logger.info("planner_evidence_received", extra={"count": len(evidence)})
    state["plan"] = "analyze_with_evidence"
    return state
