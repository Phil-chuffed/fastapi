from fastapi import FastAPI
from pydantic import BaseModel
import os
import requests

app = FastAPI()

@app.get("/")
def read_root():
    return {
        "greeting": "Hello, Phil!",
        "message": "You're running your own FastAPI app now 🚀"
    }

class PersonaRequest(BaseModel):
    age: int
    location: str
    income: str

@app.post("/generate")
def generate_persona(data: PersonaRequest):
    return {
        "summary": f"A {data.age}-year-old from {data.location} earning {data.income}."
    }

# Airtable config
AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")
BASE_ID = os.getenv("AIRTABLE_BASE_ID")
TABLE_ID = "tbLh7YLxhVDcsZTuA"  # Use table ID instead of table name

@app.get("/personas")
def get_personas():
    url = f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_ID}"
    headers = {
        "Authorization": f"Bearer {AIRTABLE_API_KEY}"
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return {"error": "Failed to fetch data", "details": response.text}

    return response.json()