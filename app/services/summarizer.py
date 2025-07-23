import os
import openai
from typing import List, Dict

openai.api_key = os.getenv("OPENAI_API_KEY")

def summarize_reports(reports: List[Dict[str, str]]) -> str:
    if not reports:
        return "관련 리포트가 없습니다."

    summaries = []

    for report in reports:
        prompt = f"""
당신은 금융 애널리스트입니다. 다음은 {report['company']}에 대한 최근 리서치 요약입니다:

[제목]: {report['title']}
[요약 내용]: {report['summary']}

위 내용을 바탕으로 투자 관점에서 핵심 내용을 요약하고, 긍정적인지 부정적인지 간단히 평가해 주세요.
"""
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "당신은 엄밀한 금융 애널리스트입니다."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=300
            )
            ai_reply = response.choices[0].message["content"].strip()
            summaries.append(f"📌 {report['company']}\n{ai_reply}\n")
        except Exception as e:
            summaries.append(f"📌 {report['company']} - 요약 실패: {e}")

    final_summary = "\n\n".join(summaries)
    return final_summary
