import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import pearsonr

# 📌 한글 폰트 설정 (Windows)
plt.rc('font', family='Malgun Gothic')
# 📌 마이너스(-) 기호 깨짐 방지
plt.rcParams['axes.unicode_minus'] = False

# 📌 데이터 불러오기
df_keywords = pd.read_csv("csv/yearly_keywords.csv", encoding="utf-8-sig")  # 키워드 빈도수 데이터
df_prices = pd.read_csv("csv/apart_prices.csv", encoding="utf-8-sig")  # 연도별 아파트 매매가 변동률 데이터

# 📌 연도별 주요 키워드 자동 선택 (상위 5개)
top_keywords = (
    df_keywords.groupby("년도")
    .apply(lambda x: x.nlargest(5, "빈도수"))
    .reset_index(drop=True)
)["키워드"].unique()

print(f"🔍 자동 선정된 주요 키워드: {list(top_keywords)}")

# 📌 상관계수 결과 저장
correlation_results = {}

for keyword in top_keywords:
    # 특정 키워드의 연도별 빈도수 추출
    keyword_data = df_keywords[df_keywords["키워드"] == keyword].set_index("년도")["빈도수"]

    # 연도 기준으로 데이터 병합
    merged_data = df_prices.set_index("년도").join(keyword_data, how="left").fillna(0)

    # 데이터 타입 변환
    merged_data["변동률(%)"] = merged_data["변동률(%)"].astype(float)
    merged_data["빈도수"] = merged_data["빈도수"].astype(float)

    # 빈도수가 모두 0이면 Pearson 계산이 불가능하므로 예외 처리
    if merged_data["빈도수"].sum() == 0:
        correlation_results[keyword] = None  # 데이터 부족
    else:
        corr, _ = pearsonr(merged_data["변동률(%)"], merged_data["빈도수"])
        correlation_results[keyword] = corr

# 📌 상관관계 결과 출력
print("\n📊 키워드와 매매가 변동률 상관계수")
for keyword, corr in correlation_results.items():
    if corr is None:
        print(f"{keyword}: 데이터 부족 (계산 불가)")
    else:
        print(f"{keyword}: {corr:.2f}")

# 📌 상관계수 시각화
plt.figure(figsize=(8, 6))
sns.barplot(
    x=list(correlation_results.keys()),
    y=[corr if corr is not None else 0 for corr in correlation_results.values()],  # None 값은 0으로 처리
    palette="coolwarm"
)
plt.axhline(0, color="black", linestyle="--", linewidth=1)
plt.xlabel("키워드", fontsize=12)
plt.ylabel("상관계수", fontsize=12)
plt.title("키워드 빈도와 매매가 변동률 상관관계", fontsize=14)
plt.xticks(rotation=45)
plt.show()

print("키워드와 매매가 변동률 상관분석 완료!")

