import json
import logging
from app.inference.ollama_client import OllamaClient

logger = logging.getLogger("analyzer")

ollama = OllamaClient()

SYSTEM_PROMPT = """
You are a conservative financial risk analyst.

Rules:
- Use ONLY the provided evidence.
- If evidence is insufficient, clearly state what is missing.
- Do NOT assume income, credit score, or documents.
- Do NOT approve or reject without facts.
- Output MUST be valid JSON in this schema:

{
  "analysis": "...",
  "eligible": "yes | no | unknown",
  "decision": "approved | rejected | cannot_decide",
  "confidence": 0.0
}
"""

def build_prompt(query: str, evidence: list[str]) -> str:
    evidence_block = "\n".join(f"- {e}" for e in evidence) if evidence else "NO EVIDENCE PROVIDED"

    return f"""
{SYSTEM_PROMPT}

Query:
{query}

Evidence:
{evidence_block}

Respond ONLY with valid JSON.
"""

async def run(state: dict) -> dict:
    query = state["query"]
    evidence = state.get("evidence", [])

    logger.warning("analyzer_llm_called_no_evidence" if not evidence else "analyzer_llm_called")

    prompt = build_prompt(query, evidence)

    raw = await ollama.generate(prompt)

    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        logger.error("analyzer_invalid_json_from_llm")
        return {
            **state,
            "analysis": "",
            "eligible": "unknown",
            "decision": "cannot_decide",
            "confidence": 0.1,
        }

    return {
        **state,
        "analysis": parsed.get("analysis", ""),
        "eligible": parsed.get("eligible", "unknown"),
        "decision": parsed.get("decision", "cannot_decide"),
        "confidence": float(parsed.get("confidence", 0.2)),
    }
