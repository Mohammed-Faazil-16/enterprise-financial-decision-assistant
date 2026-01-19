from app.core.logging import get_logger

logger = get_logger()

class FinalizerAgent:
    async def run(self, state: dict) -> dict:
        if not state.get("verified"):
            state["decision"] = "unable_to_confirm"
            state["confidence"] = 0.2
            return state

        state["decision"] = "approved_with_conditions"
        state["confidence"] = 0.75
        return state
