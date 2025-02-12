import requests
import xml.etree.ElementTree as ET
def get_data(gu_code, base_date):
    url = 'http://apis.data.go.kr/1613000/RTMSDataSvcAptTrade/getRTMSDataSvcAptTrade?'
    service_key = 'iX7cWRfHPxT7QQh9jUylodoYKug1nxysQgUp%2BsQIffV%2B1IkgnrcgM2tdIFN51daq%2BDbQV1Aqp0l6Hx6mnLqc9g%3D%3D'
    payload = "LAWD_CD=" + gu_code + "&" + \
              "DEAL_YMD=" + base_date + "&" + \
              "serviceKey=" + service_key + "&"

    res = requests.get(url + payload)
    return res
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