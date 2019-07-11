import xlrd, xlwt
import requests
from urllib.request import quote
import urllib.parse
from bs4 import BeautifulSoup as bs
import pandas as pd

# 엑셀파일 읽어오기
wb = xlrd.open_workbook('C:/Users/yeony/Desktop/test_excel.xlsx')
# 모든 시트 가져오기
sheets = wb.sheets()
# 모든 시트 디비로 저장
## 첫번째 시트만 가져오기
# sheet = wb.sheet_by_index(0)
list = []

for sheet in sheets:
    for i in range(1, sheet.nrows):
        a1 = sheet.cell_value(i, 0)
        a2 = sheet.cell_value(i, 1)
        list.append(str(a1)+str(a2))
    print(list)



url = 'http://www.yes24.co.kr/'
data = {'query' : '뻘짓은 나만 하는줄 알았어 피터홀린스'}
# data = unquote(data).decode('utf8')
response = requests.post(url, data=data)
print(response)


aa = '%C3%D6%B0%AD%C0%C7%C0%CE%BB%FD'
aa = urllib.parse.unquote_plus(aa)
print(aa)

bb = '최강의 강의'
bb = urllib.parse.quote_plus(bb)
print(bb)

# yes24에 '최강의 강의'를 검색했을 때 url에 나타나는 암호를
# aa와 같이 디코딩했을 때 결과 - �ְ����λ�
# '최강의 강의'를 인코딩했을 때 결과 - %EC%B5%9C%EA%B0%95%EC%9D%98+%EA%B0%95%EC%9D%98