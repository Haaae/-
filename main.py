from turtle import position
import folium
import os
import pandas as pd
import folium.plugins as plug
import base64
import requests
from bs4 import BeautifulSoup






df=pd.read_excel('C:/Users/장정환/map_project/충북대 전체건물좌표.xlsx')


m=folium.Map(location=[36.6286813647,127.4559668598],
zoom_start=16,
max_bounds = True,  #지도 범위 제한

min_zoom = 16,
min_lat = 36.621 ,
max_lat = 36.634,
min_lon= 127.449,
max_lon = 127.464)

# map에 S동, N동, E동 구분할 MarkerCluster 객체생성 후 m에 추가 #
mcg=plug.MarkerCluster(control=False)
m.add_child(mcg)

# MarkerCluster에 구역 추가 #
Area_S_cluster=plug.FeatureGroupSubGroup(mcg,'S구역').add_to(m)
Area_N_cluster=plug.FeatureGroupSubGroup(mcg,'N구역').add_to(m)
Area_E_cluster=plug.FeatureGroupSubGroup(mcg,'E구역').add_to(m)
Area_Dormitory_cluster=plug.FeatureGroupSubGroup(mcg,'학생생활관').add_to(m)

# 검색 기능 구현 시 layer로 지정할 geojson 객체 생성 시 필요한 건물 좌표를 저장할 빈 리스트 생성 #
point_list = []

for name, lat, lng, area, image in zip(df.건물이름, df.위도, df.경도, df.건물구역, df.사진):
    if(area=='S'):
        pic = base64.b64encode(open(image,'rb').read()).decode()
        image_tag = '<img src="data:image/jpg;base64,{}">'.format(pic)
        iframe = folium.IFrame(image_tag, width=650, height=650)
        popup = folium.Popup(iframe, max_width=300)
        
        folium.Marker([lat,lng],
                      popup=popup,
                      tooltip=name,
                     icon=folium.Icon(color='red',icon='asterisk',)).add_to(Area_S_cluster)
    if(area=='N'):
        pic = base64.b64encode(open(image,'rb').read()).decode()
        image_tag = '<img src="data:image/jpg;base64,{}">'.format(pic)
        iframe = folium.IFrame(image_tag, width=650, height=650)
        popup = folium.Popup(iframe, max_width=300)
        
        folium.Marker([lat,lng],
                      popup=popup,
                      tooltip=name,
                     icon=folium.Icon(color='blue',icon='asterisk')).add_to(Area_N_cluster)
    if(area=='E'):
        pic = base64.b64encode(open(image,'rb').read()).decode()
        image_tag = '<img src="data:image/jpg;base64,{}">'.format(pic)
        iframe = folium.IFrame(image_tag, width=650, height=650)
        popup = folium.Popup(iframe, max_width=300)
        
        folium.Marker([lat,lng],
                      popup=popup,
                      tooltip=name,
                     icon=folium.Icon(color='green',icon='asterisk')).add_to(Area_E_cluster)
    if(area=='학생생활관'):
        pic = base64.b64encode(open(image,'rb').read()).decode()
        image_tag = '<img src="data:image/jpg;base64,{}">'.format(pic)
        iframe = folium.IFrame(image_tag, width=650, height=650)
        popup = folium.Popup(iframe, max_width=300)
        
        folium.Marker([lat,lng],
                      popup=popup,
                      tooltip=name,
                     icon=folium.Icon(color='orange',icon='asterisk')).add_to(Area_Dormitory_cluster)
    
    # json 생성 형식에 맞춰 point_list에 좌표 및 정보 저장 #
    # 참고: http://www.gisdeveloper.co.kr/?p=8002
    point_list.append({
      "type": "Feature",
      "geometry": {
        "type": "Point",
        "coordinates": [lng, lat]
      },
      "properties": {
        "name": name
      }
    })

# point_list 활용하여 Geojson 객체를 위한 양식 완성 #
points = {
    "type": "FeatureClooection",
    "features": point_list
}   

# points 활용하여 검색을 위한 GeoJson 객체 생성 #
building_geojson_obj = folium.GeoJson(points, overlay=False).add_to(m)

# 만들어둔 geojson 객체 building_geojson_obj를 layer롤 설정하여 검색 기능 버튼 삽입 #
map_search = plug.Search(layer=building_geojson_obj,
            search_label="name",
            search_zoom=18,
            geom_type='Point',
            position='topleft'
           ).add_to(m)
    
## 내 위치 확인 버튼 삽입 ##
plug.LocateControl(auto_start=True).add_to(m)

## 전체화면 버튼 삽입 ##
plug.Fullscreen(
    position='topright',
    title='Expand me',
    title_cancel='Exit me',
    force_separate_button=True  
).add_to(m)
folium.LayerControl().add_to(m)

## 경로 표시 ##
# 평지 혹은 완만한 경사의 경로 표시#
location_data_df1 = pd.read_excel("C:/Users/장정환/map_project/휠체어진입가능여부표시경로_평지또는매우완만한경사.xlsx", sheet_name=None)


for sheet in list(location_data_df1.keys()) :
    location_data_posibile = []
    for lat, lng in zip(location_data_df1[sheet].위도, location_data_df1[sheet].경도) :
        location_data_posibile.append([lat, lng])
    folium.PolyLine(locations=location_data_posibile, tooltip="평지 혹은 완만한 경사").add_to(m)

# 자주식 휠체어 이동 가능 경로 표시#
location_data_df2 = pd.read_excel("C:/Users/장정환/map_project/휠체어진입가능여부표시경로_자주식휠체어등반가능한경사.xlsx", sheet_name=None)


for sheet in list(location_data_df2.keys()) :
    location_data_posibile = []
    for lat, lng in zip(location_data_df2[sheet].위도, location_data_df2[sheet].경도) :
        location_data_posibile.append([lat, lng])
    folium.PolyLine(locations=location_data_posibile, color="yellow", tooltip="자주식 휠체어 등반 가능한 경로").add_to(m)  

# 자주식 휠체어 이동 불가능 경로 표시#
location_data_df3 = pd.read_excel("C:/Users/장정환/map_project/휠체어진입가능여부표시경로_자주식휠체어등반곤란한경사.xlsx", sheet_name=None)


for sheet in list(location_data_df3.keys()) :
    location_data_posibile = []
    for lat, lng in zip(location_data_df3[sheet].위도, location_data_df3[sheet].경도) :
        location_data_posibile.append([lat, lng])
    folium.PolyLine(locations=location_data_posibile, color="red", tooltip="자주식 휠체어 등반 곤란한 경로").add_to(m)
    

m.save("전체구역좌표_및_검색기능구현.html")