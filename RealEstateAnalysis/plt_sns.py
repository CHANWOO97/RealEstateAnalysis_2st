import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.lines import lineStyles
import matplotlib.font_manager as fm

# csv 파일 불러오기
df = pd.read_csv("강남구_2019~2024.csv", encoding='cp949')

# 데이터 타입 확인 (거래 금액을 숫자로 변환)
# 천 단위 콤마 제거 후 정수 변환
df['거래 금액'] = df['거래 금액'].str.replace(',','').astype(int)
# print(df['거래 금액'][0])

# 연도별 평균 매매가 계산
df_grouped = df.groupby('거래 연도')['거래 금액'].mean().reset_index()
# print(df_grouped)

# 그래프 스타일 설정
sns.set_style("whitegrid")
plt.figure(figsize=(10, 5))

# 📌 한글 폰트 설정 (Windows)
plt.rc('font', family='Malgun Gothic')
# 📌 마이너스(-) 기호 깨짐 방지
plt.rcParams['axes.unicode_minus'] = False

# 그래프 그리기
plt.plot(df_grouped['거래 연도'], df_grouped['거래 금액'],
         marker='o', linestyle='-', color='b', label='평균 매매가')

# 그래프 제목 및 축 레이블 설정
plt.title("강남구 연도별 평균 아파트 매매가 변동 (2019~2024)", fontsize=14)
plt.xlabel("연도", fontsize=12)
plt.ylabel("평균 매매가 (만원)", fontsize=12)
plt.xticks(df_grouped['거래 연도']) # x축 눈금 연도 표시
plt.legend()

# 그래프 표시
plt.show()