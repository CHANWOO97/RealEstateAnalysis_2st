# 🏡 RealEstateAnalysis (부동산 데이터 분석)

## 📌 프로젝트 개요
이 프로젝트는 **아파트 매매가 변동률**과 **뉴스 키워드 빈도수** 간의 상관관계를 분석하는 것을 목표로 합니다.  
국토교통부 및 한국부동산원의 실거래가 데이터와 네이버 뉴스에서 추출한 키워드를 활용하여 **부동산 시장 흐름을 파악**합니다.

---

## 📂 프로젝트 구조

```plaintext
RealEstateAnalysis_2st/
│── README.md           # 프로젝트 설명 파일
RealEstateAnalysis/
  │── data/             # 데이터셋 (CSV 파일)
  │── naver/            # 네이버 뉴스 크롤링 ("아파트 매매" 검색하여 키워드 추출)
  |── api.py            # API 활용 데이터 get 함수, xml 파싱 함수
  |── codeFile.py       # 실거래가 데이터 수집후 csv 파일 생성
  │── graph.py          # 분석 결과 (그래프, 이미지)
  │── plt_sns.py        # 연도별 평균 아파트 매매가 변동 (2019 ~ 2024) 그래프 확인
