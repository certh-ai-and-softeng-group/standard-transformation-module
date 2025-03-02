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

# Load environment variables
load_dotenv()

# Load Authorization Token from ENV
OPENWEBUI_AUTH = os.getenv("OPENWEBUI_AUTH")
if not OPENWEBUI_AUTH:
    raise RuntimeError("OPENWEBUI_AUTH environment variable is missing. Set it before running the app.")

BASE_URL = os.getenv("BASE_URL")
if not BASE_URL:
    raise RuntimeError("BASE_URL environment variable is missing. Set it before running the app.")


def process_compliance_request(standard: str, excerpt: str):
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
                try:
                    extracted_requirements = json.loads(json_array_str)  # Convert to Python list
                    if not isinstance(extracted_requirements, list):
                        raise ValueError("Extracted data is not a valid list.")

                    # Ensure each item in the list is a dictionary and has a "requirement" key
                    for req in extracted_requirements:
                        if not isinstance(req, dict) or "requirement" not in req:
                            raise ValueError("Each requirement must be a dictionary with a 'requirement' key.")

                    extracted_requirements_list = [req["requirement"] for req in extracted_requirements]

                except (json.JSONDecodeError, ValueError) as e:
                    raise HTTPException(status_code=500, detail=f"Invalid extracted requirements format: {str(e)}")
            else:
                raise HTTPException(status_code=500, detail="No valid extracted requirements found in the response.")

        # Ensure we have extracted requirements before inserting into MongoDB
        if not extracted_requirements_list:
            raise HTTPException(status_code=500, detail="No valid requirements were extracted from the LLM response.")

        # Create ComplianceModel instance
        compliance_entry = ComplianceModel(
            standard=standard,
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            excerpt=excerpt,
            extracted_requirements=extracted_requirements_list
        )

        # Insert into MongoDB (Synchronous)
        collection = get_collection("compliance_entries")
        result = collection.insert_one(compliance_entry.dict())  # ✅ No await here!

        return {
            "message": "Requirements extracted successfully.",
            "inserted_id": str(result.inserted_id),
            "extracted_requirements": extracted_requirements_list
        }

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Request error: {str(e)}")
