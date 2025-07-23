from fastapi import APIRouter
from services.etf_data import load_etf_data

router = APIRouter(prefix="/etf", tags=["ETF"])

@router.get("/{etf_name}")
def get_etf_info(etf_name: str):
    data = load_etf_data()
    result = next((etf for etf in data if etf["ETF"] == etf_name), None)
    return result or {"error": "ETF not found"}
