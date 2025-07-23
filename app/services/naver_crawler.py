from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from typing import List, Dict

def crawl_reports(etf_holdings: List[str], max_pages: int = 3) -> List[Dict]:
    """
    ETF 구성 종목명 리스트를 기반으로 네이버 리서치 페이지에서 관련 기업 리포트를 크롤링합니다.

    Args:
        etf_holdings (List[str]): 종목명 리스트 (예: ["삼성전자", "NAVER"])
        max_pages (int): 크롤링할 최대 페이지 수

    Returns:
        List[Dict]: 각 기업별 제목, 요약 포함된 리포트 리스트
    """

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(options=chrome_options)

    url = "https://finance.naver.com/research/company_list.naver"
    driver.get(url)
    time.sleep(2)

    matched_reports = []

    for page in range(1, max_pages + 1):
        print(f"🔍 Page {page}")
        for row in range(3, 48):  # 표의 유효 범위
            try:
                company_xpath = f'//*[@id="contentarea_left"]/div[2]/table[1]/tbody/tr[{row}]/td[1]/a'
                report_xpath = f'//*[@id="contentarea_left"]/div[2]/table[1]/tbody/tr[{row}]/td[2]/a'
                company_name = driver.find_element(By.XPATH, company_xpath).text.strip()

                if company_name in etf_holdings:
                    print(f"✅ 매칭: {company_name}")
                    report_link = driver.find_element(By.XPATH, report_xpath)
                    report_link.click()
                    time.sleep(1)

                    try:
                        title_xpath = '//*[@id="contentarea_left"]/div[2]/table/tbody/tr[4]/td/div[1]/p[1]/strong'
                        title = driver.find_element(By.XPATH, title_xpath).text.strip()

                        # 요약문 유연하게 추출
                        summary = ""
                        for idx in [2, 3]:
                            try:
                                summary_xpath = f'//*[@id="contentarea_left"]/div[2]/table/tbody/tr[4]/td/div[1]/p[{idx}]'
                                summary = driver.find_element(By.XPATH, summary_xpath).text.strip()
                                if summary:
                                    break
                            except:
                                continue

                        if not summary:
                            summary = "(요약문을 찾을 수 없습니다)"

                        matched_reports.append({
                            "company": company_name,
                            "title": title,
                            "summary": summary
                        })

                    except Exception as e:
                        print(f"❗ 리포트 상세페이지 파싱 실패: {e}")

                    driver.back()
                    time.sleep(1)

            except Exception:
                continue

        # 페이지 넘기기
        try:
            next_page_xpath = f'//*[@id="contentarea_left"]/div[2]/table[2]/tbody/tr/td[{page + 1}]/a'
            driver.find_element(By.XPATH, next_page_xpath).click()
            time.sleep(2)
        except Exception:
            print("⛔ 더 이상 페이지 없음")
            break

    driver.quit()
    return matched_reports
