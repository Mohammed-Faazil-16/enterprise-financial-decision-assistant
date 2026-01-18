from app.agents.state import DecisionState
from app.inference.factory import get_inference_client
from app.core.logging import get_logger

logger = get_logger()


class VerifierAgent:
    """
    Verifier Agent:
    - Checks if analysis is grounded in provided policies
    - Detects hallucinations or unsupported claims
    - Flags compliance issues
    """

    def __init__(self) -> None:
        self.inference = get_inference_client()

    async def run(self, state: DecisionState) -> DecisionState:
        if not state.analysis or not state.applicable_policies:
            logger.warning(
                "verifier_insufficient_input",
                query=state.query,
            )
            state.verified = False
            state.verification_notes = "Insufficient analysis or policy context."
            return state

        prompt = (
            "You are a financial compliance verifier.\n"
            "Your task is to verify whether the following analysis is fully supported "
            "by the given policy clauses.\n\n"
            "POLICY CLAUSES:\n"
            + "\n---\n".join(state.applicable_policies)
            + "\n\n"
            "ANALYSIS:\n"
            f"{state.analysis}\n\n"
            "Answer with ONLY one of the following formats:\n"
            "- VERIFIED: <short reason>\n"
            "- NOT VERIFIED: <short reason>\n"
        )

        response = await self.inference.generate(prompt=prompt)
        text = response.get("response", "").strip()

        if text.upper().startswith("VERIFIED"):
            state.verified = True
            state.verification_notes = text
        else:
            state.verified = False
            state.verification_notes = text

        logger.info(
            "verifier_completed",
            verified=state.verified,
        )

        return state
