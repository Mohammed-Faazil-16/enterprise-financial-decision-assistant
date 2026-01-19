from app.inference.factory import get_inference_client
from app.core.logging import get_logger

logger = get_logger()

class PlannerAgent:
    def __init__(self) -> None:
        self.inference = get_inference_client()

    async def run(self, state: dict) -> dict:
        # Get evidence from dict
        evidence = state.get("evidence", [])
        query = state.get("query", "")

        if not evidence:
            logger.warning("planner_no_evidence", query=query)
            return state

        prompt = (
            "You are a financial policy planner.\n"
            "Identify relevant policy statements to the user's question.\n\n"
            "USER QUESTION:\n"
            f"{query}\n\n"
            "POLICIES:\n"
            + "\n---\n".join(evidence) +
            "\n\nReturn only relevant statements verbatim."
        )

        response = await self.inference.generate(prompt)
        raw_text = response.get("response", "")

        # Update state using dict access
        state["applicable_policies"] = [
            line.strip() for line in raw_text.splitlines() if line.strip()
        ]
        return state
