import json
import logging
from app.inference.ollama_client import OllamaClient

logger = logging.getLogger("analyzer")

ollama = OllamaClient()

SYSTEM_PROMPT = """
You are a conservative financial risk analyst.

Rules:
- Use ONLY the provided evidence.
- If evidence is insufficient, say so clearly.
- Do NOT assume user income, credit score, or documents.
- Be cautious and explicit.
- Output MUST be valid JSON.
"""

def build_prompt(query: str, evidence: list[str]) -> str:
    evidence_block = "\n".join(f"- {e}" for e in evidence) if evidence else "NO EVIDENCE PROVIDED"

    return f"""
{SYSTEM_PROMPT}

User Query:
{query}

Evidence:
{evidence_block}

Respond strictly in JSON with this schema:
{{
  "analysis": string,
  "risk_flags": list[string],
  "eligible": "yes" | "no" | "unknown"
}}
"""

async def run(state: dict) -> dict:
    query = state.get("query", "")
    evidence = state.get("evidence", [])

    if not evidence:
        logger.warning("analysis_skipped_no_evidence")
        state["analysis"] = ""
        state["eligible"] = "unknown"
        return state

    prompt = build_prompt(query, evidence)

    try:
        response = await ollama.generate(prompt)
        parsed = json.loads(response)

        state["analysis"] = parsed.get("analysis", "")
        state["risk_flags"] = parsed.get("risk_flags", [])
        state["eligible"] = parsed.get("eligible", "unknown")

        logger.info("analysis_completed_llm")

    except Exception as e:
        logger.exception("analysis_failed_llm")
        state["analysis"] = ""
        state["eligible"] = "unknown"

    return state
