import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 📌 한글 폰트 설정 (Windows)
plt.rc('font', family='Malgun Gothic')
# 📌 마이너스(-) 기호 깨짐 방지
plt.rcParams['axes.unicode_minus'] = False

# csv 파일 불러오기
df1 = pd.read_csv("단원구_2019~2024.csv", encoding='cp949')
df2 = pd.read_csv('강남구_2019~2024.csv', encoding='cp949')

# 두 데이터프레임에 '지역' 컬럼 추가
df1['지역'] = '안산 단원구'
df2['지역'] = '서울 강남구'

# 두 데이터를 하나의 데이터프레임으로 병합
df = pd.concat([df1, df2])

# 거래금액 컬럼 숫자 변환 (숫자형으로 변환하기 위해 콤마 제거 후 정수 변환)
df['거래 금액'] = df['거래 금액'].str.replace(',','').astype(int)

# 중복 제거
df = df.drop_duplicates()

# 1️⃣ 연도별 평균 매매가 비교 (선 그래프) - 정규화 x
plt.figure(figsize=(12, 5))
sns.lineplot(data=df, x="거래 연도", y="거래 금액", hue="지역", marker="o")
plt.title("연도별 평균 매매가 비교")
plt.xlabel("연도")
plt.ylabel("평균 매매가 (만원)")
plt.grid(True)
plt.legend(title="지역")
#plt.show()

# 1️⃣ 연도별 평균 매매가 비교 (선 그래프)
plt.figure(figsize=(12, 5))

# 강남구 데이터
gangnam_mean = df[df['지역'] == '서울 강남구'].groupby('거래 연도')['거래 금액'].mean()
gangnam_norm = (gangnam_mean - gangnam_mean.min()) / (gangnam_mean.max() - gangnam_mean.min())

# 단원구 데이터
danwon_mean = df[df['지역'] == '안산 단원구'].groupby('거래 연도')['거래 금액'].mean()
danwon_norm = (danwon_mean - danwon_mean.min()) / (danwon_mean.max() - danwon_mean.min())

plt.plot(gangnam_norm, marker="o", label="강남구 (표준화)")
plt.plot(danwon_norm, marker="s", label="단원구 (표준화)")
plt.title('연도별 평균 매매가 비교 (표준화)')
plt.xlabel('연도')
plt.ylabel('표준화된 매매가')
plt.grid(True)
plt.legend()
#plt.show()

# 2️⃣ 연도별 거래량 비교 (막대 그래프)
plt.figure(figsize=(12, 5))
df_count = df.groupby(['거래 연도', '지역']).size().reset_index(name='거래량')
sns.barplot(data=df_count, x='거래 연도', y='거래량', hue='지역')
plt.title('연도별 거래량 비교')
plt.xlabel('연도')
plt.ylabel('거래 건수')
plt.legend(title='지역')
plt.grid(True)
#plt.show()

# ✅ 3️⃣ 전용면적(평수)별 매매가 비교 (Y축 로그 스케일 적용 및 이상치 제거)
plt.figure(figsize=(12, 6))
# 이상치 제거 (5% ~ 95% 백분위수 범위 유지)
q_low = df["거래 금액"].quantile(0.05)
q_high = df["거래 금액"].quantile(0.95)
df_filtered = df[(df["거래 금액"] >= q_low) & (df["거래 금액"] <= q_high)]

# 전용면적 그룹화 (5평 단위)
df_filtered = df_filtered.copy()  # 원본과의 연결을 끊음
df_filtered["전용면적_그룹"] = (df_filtered["전용면적_평수"] // 5) * 5
# sns.boxplot(data=df_filtered, x="전용면적_그룹", y="거래 금액", hue="지역")
sns.boxplot(x="전용면적_그룹", y="거래 금액", hue="지역", data=df_filtered, palette="Set2", showfliers=False)
sns.stripplot(x="전용면적_그룹", y="거래 금액", hue="지역", data=df_filtered, palette="dark:.3", dodge=True, size=2, alpha=0.5)
plt.title("전용면적별 매매가 분포 비교 (이상치 제거, 로그 스케일)")
plt.xlabel("전용면적 (평) 단위")
plt.ylabel("거래금액 (만원)")
plt.xticks(rotation=45)  # x축 라벨 회전
plt.yscale("log")  # Y축 로그 스케일 적용
plt.grid(True)
plt.legend(title="지역", loc="upper left")
plt.show()