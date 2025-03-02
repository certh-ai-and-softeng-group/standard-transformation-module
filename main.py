from fastapi import FastAPI
from pydantic import BaseModel
from services.compliance_service import process_compliance_request

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
