from app.agents.state import DecisionState
from app.inference.factory import get_inference_client
from app.core.logging import get_logger

logger = get_logger()


class PlannerAgent:
    """
    Planner Agent:
    - Looks at retrieved evidence
    - Identifies which policies / clauses are relevant
    - Does NOT make a decision
    """

    def __init__(self) -> None:
        self.inference = get_inference_client()

    async def run(self, state: DecisionState) -> DecisionState:
        if not state.evidence:
            logger.warning(
                "planner_no_evidence",
                query=state.query,
            )
            return state

        prompt = (
            "You are a financial policy planner.\n"
            "Your task is to identify which of the following policy statements "
            "are relevant to the user's question.\n\n"
            "USER QUESTION:\n"
            f"{state.query}\n\n"
            "POLICY STATEMENTS:\n"
            + "\n---\n".join(state.evidence)
            + "\n\n"
            "Return ONLY the relevant policy statements verbatim."
        )

        response = await self.inference.generate(prompt=prompt)

        raw_text = response.get("response", "")
        applicable = [
            line.strip()
            for line in raw_text.splitlines()
            if line.strip()
        ]

        state.applicable_policies = applicable

        logger.info(
            "planner_completed",
            applicable_policy_count=len(applicable),
        )

        return state
