import os

import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import matplotlib.font_manager as fm

# 📌 데이터 불러오기
df_keywords = pd.read_csv("csv/yearly_keywords.csv", encoding="utf-8-sig")

# 📌 한글 폰트 설정 (사용자 환경에 맞게 변경 가능)
font_path = "C:/Windows/Fonts/malgun.ttf"
font_prop = fm.FontProperties(fname=font_path)

# 📌 저장 폴더 설정 (없으면 생성)
output_dir = "wordcloud_images"
os.makedirs(output_dir, exist_ok=True)

# 📌 연도별 WordCloud 생성
years = df_keywords["년도"].unique()

for year in years:
    # 해당 연도의 키워드 및 빈도수 가져오기
    year_data = df_keywords[df_keywords["년도"] == year]
    # 상위 5개 키워드 가져오기
    top_keywords = year_data.nlargest(5, "빈도수")
    print(f"\n📌 {year}년 주요 키워드 Top 5")
    print(top_keywords[["키워드", "빈도수"]].to_string(index=False))

    # WordCloud 데이터 생성
    word_freq = {row["키워드"]: row["빈도수"] for _, row in year_data.iterrows()}
    wordcloud = WordCloud(font_path=font_path, background_color="white", width=800, height=600)
    wordcloud.generate_from_frequencies(word_freq)

    # 이미지 저장
    img_path = os.path.join(output_dir, f"wordcloud_{year}.png")
    wordcloud.to_file(img_path)
    print(f"✅ {year}년 WordCloud 저장 완료 → {img_path}")

print("\n🎉 연도별 WordCloud 생성 및 주요 키워드 출력 완료!")
