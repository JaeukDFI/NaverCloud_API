from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from typing import List
import os
import json

app = FastAPI()

# ETF 데이터 로드
ETF_JSON_PATH = "data/etf_data.json"
PDF_DIR = "data/pdfs"

with open(ETF_JSON_PATH, encoding='utf-8') as f:
    etf_data = json.load(f)

@app.get("/")
def read_root():
    return {"message": "ETF & PDF API 작동 중"}

# ✅ ETF 정보 API
@app.get("/etf/{etf_name}")
def get_etf_info(etf_name: str):
    for etf in etf_data:
        if etf["ETF"].lower() == etf_name.lower():
            return etf
    raise HTTPException(status_code=404, detail="ETF not found")

# ✅ 모든 ETF 목록
@app.get("/etf")
def list_etfs():
    return [etf["ETF"] for etf in etf_data]

# ✅ PDF 파일 목록
@app.get("/pdfs")
def list_pdfs() -> List[str]:
    return [f for f in os.listdir(PDF_DIR) if f.endswith(".pdf")]

# ✅ PDF 다운로드 API
@app.get("/pdfs/{filename}")
def get_pdf(filename: str):
    file_path = os.path.join(PDF_DIR, filename)
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type='application/pdf', filename=filename)
    raise HTTPException(status_code=404, detail="PDF file not found")
