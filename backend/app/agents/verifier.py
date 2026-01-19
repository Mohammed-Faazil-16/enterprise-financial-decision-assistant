from app.inference.factory import get_inference_client
from app.core.logging import get_logger

logger = get_logger()

class VerifierAgent:
    def __init__(self) -> None:
        self.inference = get_inference_client()

    async def run(self, state: dict) -> dict:
        applicable = state.get("applicable_policies", [])
        analysis = state.get("analysis", "")

        if not analysis or not applicable:
            state["verified"] = False
            state["verification_notes"] = "Insufficient data"
            return state

        prompt = (
            "Verify that analysis is supported by the given policies.\n\n"
            "POLICIES:\n"
            + "\n---\n".join(applicable) +
            "\n\nANALYSIS:\n"
            f"{analysis}\n\n"
            "Answer with either:\n"
            "- VERIFIED: <reason>\n"
            "- NOT VERIFIED: <reason>"
        )

        response = await self.inference.generate(prompt)
        txt = response.get("response", "").strip()

        if txt.upper().startswith("VERIFIED"):
            state["verified"] = True
        else:
            state["verified"] = False
        state["verification_notes"] = txt
        return state
