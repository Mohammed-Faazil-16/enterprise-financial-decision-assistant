from app.agents.state import DecisionState
from app.inference.factory import get_inference_client
from app.core.logging import get_logger

logger = get_logger()


class AnalyzerAgent:
    """
    Analyzer Agent:
    - Evaluates user eligibility
    - Uses ONLY applicable policy clauses
    - Produces structured reasoning
    - Does NOT finalize decision
    """

    def __init__(self) -> None:
        self.inference = get_inference_client()

    async def run(self, state: DecisionState) -> DecisionState:
        if not state.applicable_policies:
            logger.warning(
                "analyzer_no_applicable_policies",
                query=state.query,
            )
            state.analysis = "No applicable policy clauses found."
            return state

        prompt = (
            "You are a financial eligibility analyst.\n"
            "Analyze the user's eligibility strictly based on the provided policy clauses.\n\n"
            "USER QUESTION:\n"
            f"{state.query}\n\n"
            "APPLICABLE POLICY CLAUSES:\n"
            + "\n---\n".join(state.applicable_policies)
            + "\n\n"
            "Provide a concise eligibility analysis. Do NOT make a final decision."
        )

        response = await self.inference.generate(prompt=prompt)

        analysis_text = response.get("response", "").strip()
        state.analysis = analysis_text

        logger.info(
            "analyzer_completed",
            analysis_length=len(analysis_text),
        )

        return state
