from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# נתיב לקובץ ה-Secret שהגדרת ב-Render
SERVICE_ACCOUNT_FILE_PATH = "/etc/secrets/google_credentials.json"
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# קריאת הקובץ וטעינת האישורים
with open(SERVICE_ACCOUNT_FILE_PATH) as f:
    info = json.load(f)

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
