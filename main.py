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

@app.post("/extract-requirements/")
async def extract_requirements(request: ComplianceRequest):
    """
    Endpoint to extract security requirements and store them in MongoDB.
    """
    return process_compliance_request(request.standard, request.excerpt)

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