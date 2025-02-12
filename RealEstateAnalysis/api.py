import requests
import datetime
def get_data(gu_code, base_date):
    url = 'http://apis.data.go.kr/1613000/RTMSDataSvcAptTrade/getRTMSDataSvcAptTrade?'
    service_key = 'iX7cWRfHPxT7QQh9jUylodoYKug1nxysQgUp%2BsQIffV%2B1IkgnrcgM2tdIFN51daq%2BDbQV1Aqp0l6Hx6mnLqc9g%3D%3D'
    payload = "LAWD_CD=" + gu_code + "&" + \
              "DEAL_YMD=" + base_date + "&" + \
              "serviceKey=" + service_key + "&"

    res = requests.get(url + payload)
    return res