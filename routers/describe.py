from fastapi import APIRouter, HTTPException
from utils.etf_loader import load_etf_data

router = APIRouter()
etf_data = load_etf_data()

@router.get("/etf/describe/{etf_name}")
def describe_etf(etf_name: str):
    for etf in etf_data:
        if etf["ETF"].lower() == etf_name.lower():
            top = etf["Top10"][:5]
            desc = ", ".join(f"{s['종목명']}({s['구성비']}%)" for s in top)
            return {
                "etf": etf_name,
                "description": f"투자자님께서 가진 ETF는 {etf_name}입니다. 주요 구성 종목은 {desc} 등으로 구성되어 있습니다."
            }
    raise HTTPException(status_code=404, detail="ETF not found")
