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

# for i in list:
    # url = 'http://www.yes24.co.kr/'
    # data = {'제목' : '뻘짓은 나만 하는줄 알았어', '저자' : '피터 홀린스'}
    # response = requests.post(url, data=data)
    # print(response)
    #
    # html = response.text
    # soup = bs(html, 'html.parser')
    # results = soup.select('td[class=goods_infogrp]')
    # print(results)



url = 'http://www.yes24.co.kr/'
data = {'query' : '뻘짓은 나만 하는줄 알았어 피터홀린스'}
# data = unquote(data).decode('utf8')
response = requests.post(url, data=data)
print(response)


aa = '%C3%D6%B0%AD%C0%C7%C0%CE%BB%FD'
aa = urllib.parse.unquote_plus(aa)
print(aa)

# %C3%D6%B0%AD%C0%C7%C0%CE%BB%FD

# url = 'http://www.yes24.com/searchcorner/Search?keywordAd=&keyword=&domain=ALL&qdomain=%C0%FC%C3%BC&query=%BB%B9%C1%FE%C0%BA%B3%AA%B8%B8%C7%CF%B4%C2%C1%D9%BE%CB%BE%D2%BE%EE'
# response = requests.get(url)
# html = response.text
# soup = bs(html, 'html.parser')
# res = soup.select('td[class=goods_infogrp] > p[class=goods_price] > strong')
# print(res)
#
# for i in res:
#     print(i.text)

    # td class='goods_infogrp' > p class='goods_price' > strong - 가격 /
    # 만약 text가 절판이라면 '절판'text를 디비에 저장
    # 절판이 아니라면 null 값으로 저장