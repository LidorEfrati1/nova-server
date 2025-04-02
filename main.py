from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import os
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
json_creds = os.getenv("GOOGLE_APPLICATION_CREDENTIALS_JSON")
if not json_creds:
    raise Exception("Missing GOOGLE_APPLICATION_CREDENTIALS_JSON environment variable")

info = json.loads(json_creds)
credentials = Credentials.from_service_account_info(info, scopes=SCOPES)
service = build("sheets", "v4", credentials=credentials)

class SpreadsheetRequest(BaseModel):
    spreadsheet_id: str
    range: str

@app.post("/get-values")
async def get_values(req: SpreadsheetRequest):
    try:
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=req.spreadsheet_id, range=req.range).execute()
        return result.get("values", [])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
