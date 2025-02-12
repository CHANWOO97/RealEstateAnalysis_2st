import os
import pandas as pd
from RealEstateAnalysis.api import get_data
from RealEstateAnalysis.data.apitest1 import get_items

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
def gucode(gu):
    gu_code = code[(code['name'].str.contains(gu))]
    gu_code = gu_code['code'].reset_index(drop=True)
    gu_code = str(gu_code[0])[0:5]
    return gu_code
print(gucode('단원구'))
print(gucode('강남구'))

# 실거래 데이터얻기
items_list = []
for date in date_list:
    res = get_data(gucode('단원구'), date)
    items_list += get_items(res)
print(len(items_list))

items_list = []
for date in date_list:
    res = get_data(gucode('강남구'), date)
    items_list += get_items(res)
print(len(items_list))