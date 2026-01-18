from typing import Dict, Any

from app.retrieval.vector_store import VectorStore
from app.inference.factory import get_inference_client
from app.core.logging import get_logger

logger = get_logger()


class DecisionEngine:
    """
    Core decision engine that performs:
    - evidence retrieval
    - grounded inference
    - explainable output
    """

    def __init__(self) -> None:
        self.vector_store = VectorStore()
        self.inference_client = get_inference_client()

    async def evaluate(self, query: str) -> Dict[str, Any]:
        # 1. Retrieve evidence
        evidence = self.vector_store.similarity_search(query, k=5)

        if not evidence:
            logger.warning(
                "decision_no_evidence",
                query=query,
            )
            return {
                "decision": "insufficient_evidence",
                "explanation": "No relevant policy or guideline found.",
                "evidence": [],
                "confidence": 0.0,
            }

        # 2. Construct grounded prompt
        prompt = (
            "You are a financial decision assistant.\n"
            "Answer ONLY using the provided evidence.\n\n"
            "EVIDENCE:\n"
            + "\n---\n".join(evidence)
            + "\n\nQUESTION:\n"
            + query
        )

        # 3. Call inference
        response = await self.inference_client.generate(prompt=prompt)

        # 4. Assemble explainable output
        result = {
            "decision": "generated",
            "answer": response.get("response"),
            "evidence": evidence,
            "confidence": 0.7,  # placeholder (later evaluated)
        }

        logger.info(
            "decision_generated",
            query=query,
            evidence_count=len(evidence),
        )

        return result
