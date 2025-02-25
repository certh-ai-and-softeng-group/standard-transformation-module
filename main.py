from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
import requests

app = FastAPI()

# Open WebUI API Endpoint
BASE_URL = "http://160.40.52.27:3000/api/chat/completions"

# Request Schema
class ChatRequest(BaseModel):
    model: str
    prompt: str

@app.post("/generate")
def generate_text(request: ChatRequest, authorization: str = Header(None)):
    """
    Forward the prompt request to Open WebUI using the JWT token provided in the request headers.
    """

    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization token")

    headers = {
        "Authorization": authorization,  # Pass the token received from the FastAPI request
        "Content-Type": "application/json"
    }

    payload = {
        "model": request.model,
        "messages": [{"role": "user", "content": request.prompt}]
    }

    try:
        response = requests.post(BASE_URL, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Request error: {str(e)}")
