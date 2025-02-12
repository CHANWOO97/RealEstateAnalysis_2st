import pandas as pd
from konlpy.tag import Okt
from collections import Counter
import re

# 📌 데이터 불러오기
df_news = pd.read_csv("csv/news_data.csv", encoding="utf-8-sig")

# 📌 자연어 처리 객체 생성
okt = Okt()

# 📌 불용어 리스트 (추가 가능)
stopwords = ["아파트", "매매", "가격", "부동산", "시장", "거래", "관련", "올해", "등", "및", "제", "것", "위해", "더", "기사", "뉴스", '바로가기', '일반', '칼럼', '검색', '전체']


def extract_keywords(text):
    """본문에서 명사만 추출하여 불용어 제거"""
    text = re.sub(r"[^가-힣\s]", "", str(text))  # 한글 이외 제거
    nouns = okt.nouns(text)  # 명사 추출
    nouns = [word for word in nouns if word not in stopwords and len(word) > 1]  # 불용어 및 한 글자 제거
    return nouns


# 📌 연도별 키워드 분석
year_keywords = {}

for year in df_news["년도"].unique():
    year_data = df_news[df_news["년도"] == year]

    # 모든 기사에서 명사 추출
    all_words = []
    for text in year_data["본문"]:
        all_words.extend(extract_keywords(text))

    # 빈도 분석
    word_counts = Counter(all_words).most_common(20)  # 상위 20개 키워드
    year_keywords[year] = word_counts

#  결과 출력
for year, keywords in year_keywords.items():
    print(f"\n {year}년 주요 키워드:")
    print(keywords)

# 키워드 데이터를 DataFrame으로 변환하여 저장
df_keywords = pd.DataFrame([(year, word, count) for year, words in year_keywords.items() for word, count in words],
                           columns=["년도", "키워드", "빈도수"])
df_keywords.to_csv("./csv/yearly_keywords.csv", index=False, encoding="utf-8-sig")

print("연도별 키워드 분석 완료!")
