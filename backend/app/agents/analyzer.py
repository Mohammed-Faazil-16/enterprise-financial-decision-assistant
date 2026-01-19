from app.inference.factory import get_inference_client
from app.core.logging import get_logger

logger = get_logger()

class AnalyzerAgent:
    def __init__(self) -> None:
        self.inference = get_inference_client()

    async def run(self, state: dict) -> dict:
        applicable = state.get("applicable_policies", [])
        query = state.get("query", "")

        if not applicable:
            state["analysis"] = "No applicable policy clauses found."
            return state

        prompt = (
            "You are a financial eligibility analyst.\n"
            "Analyze strictly using the provided policy clauses.\n\n"
            "USER QUERY:\n"
            f"{query}\n\n"
            "APPLICABLE POLICIES:\n"
            + "\n---\n".join(applicable) +
            "\n\nProvide a concise analysis."
        )

        response = await self.inference.generate(prompt)
        state["analysis"] = response.get("response", "").strip()
        return state
