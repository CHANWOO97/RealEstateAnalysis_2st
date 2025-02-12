# api 사용하여 아파트 매매 실거래가 데이터 가져오기
import requests
import datetime

# API URL
url = 'http://apis.data.go.kr/1613000/RTMSDataSvcAptTrade/getRTMSDataSvcAptTrade?'

service_key = 'iX7cWRfHPxT7QQh9jUylodoYKug1nxysQgUp%2BsQIffV%2B1IkgnrcgM2tdIFN51daq%2BDbQV1Aqp0l6Hx6mnLqc9g%3D%3D'
deal_ymd = '202407'
lawd_cd = '41271' ## 법정동코드 전체자료에서, 안산시 상록구(41271) 확인 / 단원구(41273)
pageNo = '1'
numOfRows = '10'
# 요청 파라미터
payload = "serviceKey=" + service_key + "&" + \
          "LAWD_CD=" + lawd_cd + "&" + \
          "DEAL_YMD=" + deal_ymd + "&" + \
          "pageNo="+ pageNo +"&" + "numOfRows="+numOfRows

#res = requests.get(url + payload, verify=False)
res = requests.get(url + payload)
print(res)

import xml.etree.ElementTree as ET
import pandas as pd

def get_items(response):
    root = ET.fromstring(response.content)
    item_list = []
    for child in root.find('body').find('items'):
        elements = child.findall('*')
        data = {}
        for element in elements:
            tag = element.tag.strip()
            text = element.text.strip()
            # print tag, text
            data[tag] = text
        item_list.append(data)
    return item_list


items_list = get_items(res)
items = pd.DataFrame(items_list)
print(items.head())

