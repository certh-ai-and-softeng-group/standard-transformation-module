from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel
from services.compliance_service import process_compliance_request
from services.compliance_service import get_requirement_by_id
from services.compliance_service import get_requirement_by_standard
app = FastAPI()

# Define the request model
class ComplianceRequest(BaseModel):
    standard: str
    excerpt: str
    id: Optional[str] = None  # New optional field
@app.get("/")
async def root():
    return {"message": "Standard Transformation Module is running!"}

@app.post("/extract-requirements/")
async def extract_requirements(request: ComplianceRequest):
    """
    Endpoint to extract security requirements and store them in MongoDB.
    If an ID is provided and exists, the existing entry is returned.
    """
    return process_compliance_request(request.standard, request.excerpt, request.id)


@app.get("/requirement/id/{requirement_id}")
async def get_requirement(requirement_id: str):
    """
    Endpoint to retrieve a specific requirement by its ID.
    """
    return get_requirement_by_id(requirement_id)

@app.get("/requirement/standard/{standard}")
async def get_requirements_by_standard(standard: str):
    """
    Endpoint to retrieve all requirements for a specific standard.
    """
    return get_requirement_by_standard(standard)