import numpy as np
import pandas as pd
from urllib.request import urlopen
from urllib import parse
from urllib.request import Request
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import json

#naver map api key
client_id = '47w6fakof4';    # 본인이 할당받은 ID 입력
client_pw = 'WAsqeff6Q5NQiICxlP8gweDU92gW9qoAX0cCrhvJ';    # 본인이 할당받은 Secret 입력

api_url = 'https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode?query='

# 주소 목록 파일 (.csv)
# data = pd.read_csv('파일명.csv')
# 주소 목록 파일 (.xlsx)
data = pd.read_excel("C:/Users/82106/Desktop/프로그래밍/바로 가기/Python3.9/충북대 이동약자 지도/충북대건물좌표.xlsx", sheet_name=1)
print(data)
# 네이버 지도 API 이용해서 위경도 찾기
geo_coordi = []     
for add in data['도로명주소']:
    add_urlenc = parse.quote(add)  
    url = api_url + add_urlenc
    request = Request(url)
    request.add_header('X-NCP-APIGW-API-KEY-ID', client_id)
    request.add_header('X-NCP-APIGW-API-KEY', client_pw)
    try:
        response = urlopen(request)
    except HTTPError as e:
        print('HTTP Error!')
        latitude = None
        longitude = None
    else:
        rescode = response.getcode()
        if rescode == 200:
            response_body = response.read().decode('utf-8')
            response_body = json.loads(response_body)   # json
            if response_body['addresses'] == [] :
                print("'result' not exist!")
                latitude = None
                longitude = None
            else:
                latitude = response_body['addresses'][0]['y']
                longitude = response_body['addresses'][0]['x']
                print("Success!")
        else:
            print('Response error code : %d' % rescode)
            latitude = None
            longitude = None

    geo_coordi.append([latitude, longitude])


np_geo_coordi = np.array(geo_coordi)
pd_geo_coordi = pd.DataFrame({"도로명": data['도로명주소'].values,
                              "위도": np_geo_coordi[:, 0],
                              "경도": np_geo_coordi[:, 1]})

pd_geo_coordi.to_excel('네이버 맵 api로 위도경도 조사.xlsx')