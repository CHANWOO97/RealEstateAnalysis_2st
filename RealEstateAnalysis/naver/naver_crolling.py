import requests
from bs4 import BeautifulSoup
import pandas as pd
import time


def get_news_data(query, year, max_pages=3):
    """해당 연도의 아파트 매매 관련 뉴스 데이터를 수집"""
    news_data = []
    base_url = "https://search.naver.com/search.naver"

    for page in range(1, max_pages + 1):
        params = {
            "where": "news",
            "query": f"{query} {year} 아파트 매매",
            "sm": "tab_pge",
            "start": (page - 1) * 10 + 1
        }

        response = requests.get(base_url, params=params, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(response.text, "html.parser")
        articles = soup.select("ul.list_news li")

        for article in articles:
            title_tag = article.select_one("a.news_tit")
            if title_tag:
                title = title_tag.text  # 뉴스 제목
                link = title_tag["href"]  # 뉴스 링크

                # 본문 크롤링
                content = get_news_content(link)
                news_data.append([year, title, content, link])
        time.sleep(1)  # 요청 간격 조절

    return news_data


def get_news_content(url):
    """뉴스 기사 본문을 가져오는 함수 (일부 사이트는 크롤링 제한)"""
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(response.text, "html.parser")
        content = soup.get_text(separator=" ", strip=True)
        return content[:500]  # 본문 내용 일부 (500자)
    except:
        return "본문 없음"


# 📌 특정 연도 뉴스 데이터 수집
years = range(2019, 2025)
all_news = []

for year in years:
    print(f"{year}년 뉴스 크롤링 중...")
    all_news.extend(get_news_data("아파트 매매", year))

# 📌 데이터 저장
df_news = pd.DataFrame(all_news, columns=["년도", "제목", "본문", "링크"])
df_news.to_csv("news_data.csv", index=False, encoding="utf-8-sig")

print("뉴스 데이터 수집 완료!")
