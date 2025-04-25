import json
import re
from fastapi import HTTPException
import requests
import os
from datetime import datetime
from bson import ObjectId
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


def process_compliance_request(standard: str, excerpt: str, entry_id: str = None):
    """
    Sends request to Open WebUI and stores extracted requirements in MongoDB,
    unless an entry with the given ID already exists.
    """

    # Check if an ID is provided and if the entry already exists in MongoDB
    if entry_id:
        try:
            object_id = ObjectId(entry_id)
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid ID format.")

        collection = get_collection("compliance_entries")
        existing_entry = collection.find_one({"_id": object_id})
        if existing_entry:
            return {
                "id": str(existing_entry["_id"]),
                "standard": existing_entry["standard"],
                "timestamp": existing_entry["timestamp"],
                "excerpt": existing_entry["excerpt"],
                "extracted_requirements": existing_entry["extracted_requirements"]
            }

    # Load the prompt and inject the excerpt
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

        # Extract JSON array of requirements from the LLM response
        extracted_requirements_list = []
        if "choices" in response_data and len(response_data["choices"]) > 0:
            message_content = response_data["choices"][0]["message"]["content"]
            match = re.search(r"\[\s*\{.*?\}\s*\]", message_content, re.DOTALL)

            if match:
                json_array_str = match.group(0)
                try:
                    extracted_requirements = json.loads(json_array_str)
                    if not isinstance(extracted_requirements, list):
                        raise ValueError("Extracted data is not a valid list.")

                    for req in extracted_requirements:
                        if not isinstance(req, dict) or "requirement" not in req:
                            raise ValueError("Each requirement must be a dictionary with a 'requirement' key.")

                    extracted_requirements_list = [req["requirement"] for req in extracted_requirements]

                except (json.JSONDecodeError, ValueError) as e:
                    raise HTTPException(status_code=500, detail=f"Invalid extracted requirements format: {str(e)}")
            else:
                raise HTTPException(status_code=500, detail="No valid extracted requirements found in the response.")

        if not extracted_requirements_list:
            raise HTTPException(status_code=500, detail="No valid requirements were extracted from the LLM response.")

        # Prepare the model for MongoDB
        compliance_entry = ComplianceModel(
            standard=standard,
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            excerpt=excerpt,
            extracted_requirements=extracted_requirements_list
        )

        collection = get_collection("compliance_entries")
        result = collection.insert_one(compliance_entry.dict())

        return {
            "message": "Requirements extracted successfully.",
            "inserted_id": str(result.inserted_id),
            "extracted_requirements": extracted_requirements_list
        }

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Request error: {str(e)}")


def get_requirement_by_id(entry_id):
    """
    Retrieves a specific requirement by its ID from MongoDB.
    """
    collection = get_collection("compliance_entries")
    compliance_entry = collection.find_one({"_id": ObjectId(entry_id)})

    if not compliance_entry:
        raise HTTPException(status_code=404, detail="Requirement not found.")
    return {
        "id": str(compliance_entry["_id"]),
        "standard": compliance_entry["standard"],
        "timestamp": compliance_entry["timestamp"],
        "excerpt": compliance_entry["excerpt"],
        "extracted_requirements": compliance_entry["extracted_requirements"]
    }


def get_requirement_by_standard(standard):
    """
    Retrieves all requirements for a specific standard from MongoDB.
    """
    collection = get_collection("compliance_entries")
    compliance_entries = list(collection.find({"standard": standard}))

    if not compliance_entries:
        raise HTTPException(status_code=404, detail="No requirements found for this standard.")

    return [
        {
            "id": str(entry["_id"]),
            "standard": entry["standard"],
            "timestamp": entry["timestamp"],
            "excerpt": entry["excerpt"],
            "extracted_requirements": entry["extracted_requirements"]
        }
        for entry in compliance_entries
    ]
