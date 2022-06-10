'''충북대 장애지원센터에 있는 학내편의시설 가이드pdf 파일에서
 해당 건물의 pdf페이지만 추출 새로운 개별 pdf파일로 저장
'''
#pip install python-dateutil
from PyPDF2 import PdfFileReader, PdfFileWriter

#장애학생을 위한 학내편의시설가이드 pdf
origin = PdfFileReader(open("C:/Users/장정환/Downloads/201.pdf", 'rb'))


#pdf파일(장애학생을 위한)에 있는 N구역 건물번호
N_building_num=["2","4","5","7","9","10_1","10_2","11","12_1","12_2","13","14","15","16_1","16_2","16_3","18","19","20_1"]
n_list=[]
#각 건물번호에 대해 pdfFileWriter객체 생성 후 리스트에 추가
for name in N_building_num:
    name = PdfFileWriter()
    n_list.append(name)
    
# 원본 pdf파일에서 원하는 페이지를 추출해서 각 pdfFileWriter객체에 추가
for i, j in zip(range(0,len(N_building_num)),range(9,28)):
    n_list[i].addPage(origin.getPage(j))

# 각 건물에 대한 새 pdf파일로 저장
for name , j in zip(N_building_num,range(0,len(N_building_num))):
    n_list[j].write(open("C:/Users/장정환/OneDrive/바탕 화면/map_pdf/N"+name+".pdf",'wb'))