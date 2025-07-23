import streamlit as st
import requests

API_BASE = "https://<your-render-url>/"

st.title("📊 TIGER ETF 챗봇")

etf_name = st.text_input("ETF 이름 입력 (예: TIGER_200)")

if st.button("ETF 정보 가져오기"):
    resp = requests.get(f"{API_BASE}/etf/{etf_name}").json()
    if "Top10" in resp:
        st.subheader("✅ 구성 종목")
        for stock in resp["Top10"]:
            st.write(f"- {stock['종목명']} ({stock['구성비']}%)")
    else:
        st.warning("ETF 정보를 찾을 수 없습니다.")

if st.button("ETF 전망 분석"):
    st.subheader("🔍 AI 분석 요약")
    result = requests.get(f"{API_BASE}/insight/{etf_name}").json()
    st.write(result.get("summary", "분석 실패"))
