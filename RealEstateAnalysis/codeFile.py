import os
import pandas as pd
from RealEstateAnalysis.api import get_data, get_items
#from RealEstateAnalysis.data.apitest1 import get_items

code_file = './data/법정동코드 전체자료.txt'
code = pd.read_csv(code_file, sep='\t')

# 컬럼명 영문으로 변경
code.columns = ['code', 'name', 'is_exist']
# 폐지된 법정코드 삭제
code = code[code['is_exist'] == '존재']

# 법정동 코드 int 형변환 - string
#print(type(code['code'][0]))
code['code'] = code['code'].apply(str)
#print(type(code['code'][0]))

year = [str("%02d" %(y)) for y in range(2019, 2025)]
month = [str("%02d" %(m)) for m in range(1, 13)]
date_list = ["%s%s" %(y, m) for y in year for m in month]

# ✅ 각 구별 코드 (변경할 값)
print('원하는 법정동 구 입력 ex)강남구')
gu = input()
gu_code = code[(code['name'].str.contains(gu))]
gu_code = gu_code['code'].reset_index(drop=True)
gu_code = str(gu_code[0])[0:5]
print(gu_code)

# 실거래 데이터얻기
items_list = []
for date in date_list:
    res = get_data(gu_code, date)
    items_list += get_items(res)
print(len(items_list))

items = pd.DataFrame(items_list)
items = items[['aptDong', 'aptNm', 'buildYear', 'dealAmount', 'dealDay', 'dealMonth', 'dealYear', 'excluUseAr', 'floor', 'umdNm']]
items['전용면적_평수'] = items['excluUseAr'].astype(float)/3.3
#print(items['전용면적_평수'])
items = items.rename(columns={
    'aptDong': '동',
    'aptNm': '아파트명',
    'buildYear': '건축년도',
    'dealAmount': '거래 금액',
    'dealDay': '거래 일',
    'dealMonth': '거래 월',
    'dealYear': '거래 연도',
    'excluUseAr': '전용 면적(㎡)',
    '전용면적_평수': '전용면적_평수',
    'floor': '층수',
    'umdNm': '읍면동'

})
#print(items.head())
items = items.sort_values(ascending=[True,True], by=["전용면적_평수","거래 금액"])
#print(items.head())
#print(items[['아파트명', '전용면적_평수','거래 금액', '층수', '읍면동', '거래 월', '거래 일', '거래 연도', '건축년도']].head())
#print(items[['아파트명', '전용면적_평수','거래 금액', '층수', '읍면동', '거래 월', '거래 일', '거래 연도', '건축년도']].head(-1))
items.to_csv(os.path.join("./data/%s_%s~%s.csv" %(gu, year[0], year[-1])), index=False,encoding="euc-kr")