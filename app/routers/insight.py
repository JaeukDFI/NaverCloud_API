from fastapi import APIRouter
from services.etf_data import load_etf_data
from services.naver_crawler import crawl_reports
from services.summarizer import summarize_reports

router = APIRouter(prefix="/insight", tags=["Insight"])

@router.get("/{etf_name}")
def get_etf_insight(etf_name: str):
    etfs = load_etf_data()
    target = next((e for e in etfs if e["ETF"] == etf_name), None)
    if not target:
        return {"error": "ETF not found"}

    holdings = [x["종목명"] for x in target["Top10"]][:5]
    reports = crawl_reports(holdings, max_pages=2)
    summary = summarize_reports(reports)
    return {"summary": summary, "raw": reports}
