from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import os
import requests
from collections import Counter

app = FastAPI()

# Health check
@app.get("/")
def read_root():
    return {
        "greeting": "Hello, Phil!",
        "message": "You're running your own FastAPI app now 🚀"
    }

# Dummy POST endpoint
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

def fetch_airtable_data():
    url = f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_NAME}"
    headers = {"Authorization": f"Bearer {AIRTABLE_API_KEY}"}
    all_records = []
    offset = None

    while True:
        params = {}
        if offset:
            params["offset"] = offset
        response = requests.get(url, headers=headers, params=params)

        if response.status_code != 200:
            raise Exception(f"Failed to fetch data: {response.text}")

        data = response.json()
        all_records.extend(data.get("records", []))

        offset = data.get("offset")
        if not offset:
            break

    return all_records

@app.get("/insight/female-top-locations")
def female_top_locations():
    try:
        records = fetch_airtable_data()
        location_counts = Counter()

        for record in records:
            fields = record.get("fields", {})
            if fields.get("gender") == "Female":
                location = fields.get("location")
                if location:
                    location_counts[location] += 1

        top_3 = location_counts.most_common(3)
        result = [{"location": loc, "count": count} for loc, count in top_3]

        return {"top_3_locations": result}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})