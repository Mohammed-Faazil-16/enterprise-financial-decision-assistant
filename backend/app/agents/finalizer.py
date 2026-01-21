from app.core.logging import get_logger

logger = get_logger("finalizer")

async def run(state: dict) -> dict:
    plan = state.get("plan")
    verified = state.get("verified")
    eligible = state.get("eligible")

    if plan == "insufficient_evidence":
        state["decision"] = "cannot_decide"
        state["confidence"] = 0.2
        return state

    if not verified:
        state["decision"] = "cannot_decide"
        state["confidence"] = 0.3
        return state

    if eligible == "yes":
        state["decision"] = "approved_with_conditions"
        state["confidence"] = 0.75
        return state

    if eligible == "no":
        state["decision"] = "rejected"
        state["confidence"] = 0.8
        return state

    state["decision"] = "cannot_decide"
    state["confidence"] = 0.2
    return state
