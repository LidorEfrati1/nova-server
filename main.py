from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SERVICE_ACCOUNT_FILE = "nova-agent-455520-94f93f3c538a.json"

credentials = Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)
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
