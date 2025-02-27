from pydantic import BaseModel
from typing import List

class ComplianceModel(BaseModel):
    standard: str
    timestamp: str  # Format: dd/mm/yyyy
    excerpt: str
    extracted_requirements: List[str]

    class Config:
        arbitrary_types_allowed = True

# Helper to convert MongoDB document to dictionary
def compliance_helper(compliance) -> dict:
    return {
        "id": str(compliance["_id"]),
        "standard": compliance["standard"],
        "timestamp": compliance["timestamp"],
        "excerpt": compliance["excerpt"],
        "extracted_requirements": compliance["extracted_requirements"],
    }
