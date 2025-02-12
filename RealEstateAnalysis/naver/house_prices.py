import pandas as pd

# 📌 데이터 불러오기
df = pd.read_csv("../강남구_2019~2024.csv", encoding="cp949")

# 📌 '거래 금액' 숫자로 변환 (콤마 제거 후 정수 변환)
df["거래 금액"] = df["거래 금액"].str.replace(",", "").astype(int)

# 📌 연도별 평균 매매가 계산
df_avg_price = df.groupby("거래 연도")["거래 금액"].mean().reset_index()
df_avg_price.columns = ["년도", "평균 매매가"]

# 📌 연도별 변동률(%) 계산
df_avg_price["변동률(%)"] = df_avg_price["평균 매매가"].pct_change() * 100

# 📌 결과 출력
print(df_avg_price)

# 📌 CSV 저장
df_avg_price.to_csv("apart_prices.csv", encoding="utf-8-sig", index=False)
print("✅ 연도별 매매가 변동률 CSV 저장 완료!")