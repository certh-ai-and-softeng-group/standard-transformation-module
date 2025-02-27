import json
import re

from fastapi import HTTPException
import requests
import os
from datetime import datetime
from models.database import get_collection
from models.ComplianceModel import ComplianceModel
from utils.utils import load_prompt_wrapper
from dotenv import load_dotenv

# Open WebUI API Endpoint
BASE_URL = "http://160.40.52.27:3000/api/chat/completions"

load_dotenv()
# Load Authorization Token from ENV
OPENWEBUI_AUTH = os.getenv("OPENWEBUI_AUTH")
if not OPENWEBUI_AUTH:
    raise RuntimeError("OPENWEBUI_AUTH environment variable is missing. Set it before running the app.")

async def process_compliance_request(standard: str, excerpt: str):
    """
    Sends request to Open WebUI and stores extracted requirements in MongoDB.
    """

    prompt_template = load_prompt_wrapper()
    formatted_prompt = prompt_template.replace("{excerpt --> user input}", excerpt)

    headers = {
        "Authorization": f"Bearer {OPENWEBUI_AUTH}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "deepseek-r1:70b",
        "messages": [{"role": "user", "content": formatted_prompt}]
    }

    try:
        response = requests.post(BASE_URL, json=payload, headers=headers)
        response.raise_for_status()
        response_data = response.json()

        # Extract requirements from the response
        extracted_requirements_list = []
        if "choices" in response_data and len(response_data["choices"]) > 0:
            message_content = response_data["choices"][0]["message"]["content"]
            match = re.search(r"\[\s*\{.*\}\s*\]", message_content, re.DOTALL)

            if match:
                json_array_str = match.group(0)  # Extracted JSON array as a string
                extracted_requirements = json.loads(json_array_str)  # Convert to Python list
                extracted_requirements_list = [req["requirement"] for req in extracted_requirements]
            else:
                raise HTTPException(status_code=500, detail="No extracted requirements found in the response.")

        # Create ComplianceModel instance
        compliance_entry = ComplianceModel(
            standard=standard,
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            excerpt=excerpt,
            extracted_requirements=extracted_requirements_list
        )

        # Insert into MongoDB
        collection = await get_collection("compliance_entries")
        result = await collection.insert_one(compliance_entry.dict())

        return {"id": str(result.inserted_id), "status": "Stored successfully"}

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Request error: {str(e)}")
