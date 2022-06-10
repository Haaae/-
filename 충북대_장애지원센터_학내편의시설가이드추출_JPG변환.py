import os
from pdf2image import convert_from_path

#각 pdf파일을 jpg로 변환(folium의 popup에 띄우기위해)
file_list = os.listdir("C:/Users/장정환/OneDrive/바탕 화면/map_pdf/")

for name in file_list:
    pages=convert_from_path("C:/Users/장정환/OneDrive/바탕 화면/map_pdf/"+name, size = (650,650))
    for i, page in enumerate(pages):
        page.save("C:/Users/장정환/OneDrive/바탕 화면/map_img/"+name.strip(".pdf")+".jpg","JPEG")