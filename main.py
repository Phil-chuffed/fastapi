from fastapi import FastAPI
from pydantic import BaseModel
import os
import requests

app = FastAPI()

# Confirm app is live
@app.get("/")
def read_root():
    return {
        "greeting": "Hello, Phil!",
        "message": "You're running your own FastAPI app now 🚀"
    }

# Dummy POST endpoint for testing
class PersonaRequest(BaseModel):
    age: int
    location: str
    income: str

@app.post("/generate")
def generate_persona(data: PersonaRequest):
    return {
        "summary": f"A {data.age}-year-old from {data.location} earning {data.income}."
    }

# Airtable connection
AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")
BASE_ID = os.getenv("AIRTABLE_BASE_ID")
TABLE_NAME = "Personas"

@app.get("/personas")
def get_personas():
    url = f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_NAME}"
    headers = {
        "Authorization": f"Bearer {AIRTABLE_API_KEY}"
    }

    print("URL:", url)
    print("Headers:", headers)

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return {"error": "Failed to fetch data", "details": response.text}

    return response.json()