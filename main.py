import os
import requests
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")
AIRTABLE_BASE_ID = os.getenv("AIRTABLE_BASE_ID")
AIRTABLE_TABLE_NAME = "Personas"  # hardcoded, because that's the one we know works

@app.get("/personas")
def get_personas():
    url = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{AIRTABLE_TABLE_NAME}"
    headers = {
        "Authorization": f"Bearer {AIRTABLE_API_KEY}"
    }

    print("📦 Fetching from Airtable URL:", url)
    print("🪪 Using token:", AIRTABLE_API_KEY[:10] + "..." + AIRTABLE_API_KEY[-5:])  # hide middle
    print("📄 Headers:", headers)

    try:
        response = requests.get(url, headers=headers)
        print("📥 Response status:", response.status_code)
        print("🧾 Response text:", response.text)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as err:
        return JSONResponse(
            status_code=500,
            content={
                "error": "Failed to fetch data",
                "details": response.text
            }
        )