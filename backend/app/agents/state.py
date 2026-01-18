from typing import List, Optional
from pydantic import BaseModel


class DecisionState(BaseModel):
    # User input
    query: str

    # Retrieved evidence
    evidence: List[str] = []

    # Planner output
    applicable_policies: List[str] = []

    # Analyzer output
    analysis: Optional[str] = None

    # Verifier output
    verified: bool = False
    verification_notes: Optional[str] = None

    # Final output
    decision: Optional[str] = None
    confidence: float = 0.0
