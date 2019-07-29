import xlrd
import requests
from urllib.request import quote
import urllib.parse
from bs4 import BeautifulSoup as bs
import pymysql
import pandas as pd

# 엑셀파일 읽어오기
wb = xlrd.open_workbook('C:/Users/yeony/Desktop/test_excel.xlsx')
# 모든 시트 가져오기
sheets = wb.sheets()
# 모든 시트 디비로 저장
## 첫번째 시트만 가져오기
# sheet = wb.sheet_by_index(0)
book_list = []

for sheet in sheets:
    for i in range(1, sheet.nrows):
        a1 = sheet.cell_value(i, 0)
        a2 = sheet.cell_value(i, 1)
        book_list.append(str(a1)+' '+str(a2))
# print(book_list)


##########################################################
# query = sys.argv[1]
conn = pymysql.connect(user='root',
                              password='root',
                              host='127.0.0.1',
                              database='bookstore')
cursor = conn.cursor()
list = []
for query in book_list:
    # 알리딘 api로 가져올 데이터
    data = urllib.parse.urlencode({
        'ttbkey': 'ttbyeony4022121001',
        'SearchTarget': 'Book',
        'Query': query,
        'QueryType': 'Keyword',
        'Sort': 'Title',
    })
    # 검색api url
    url = 'http://www.aladdin.co.kr/ttb/api/ItemSearch.aspx'
    con = urllib.request.urlopen(url + '?' + data)
    html = con.read()
    con.close()

    # 요청한 값 lxml로 읽어오기
    soup = bs(html, "lxml")
    soupString = str(soup)
    # print(soupString)

    sub_list = []
    if soupString.find('<error xml') > -1:
        for s in soup('errormessage'):
            print('## Error!! ##')
            print("Error Message: ")
    else:
        # 도서별로 리스트에 담기
        for title in soup('title')[1]:
            sub_list.append(title)
        for author in soup('author')[0]:
            sub_list.append(author)
        for publisher in soup('publisher')[0]:
            sub_list.append(publisher)
        for pricesales in soup('pricesales')[0]:
            sub_list.append(pricesales)
        for stockstatus in soup('stockstatus')[0]:
            sub_list.append(stockstatus)
    list.append(sub_list)
print(list)

for sub_list in list:
    if len(sub_list) == 4:
        sub_list.append(' ')
    add_data = tuple(sub_list)
    print(add_data)
    add_info = ("INSERT INTO bookinfo (title, author, publisher, price, stock) VALUES (%s, %s, %s, %s, %s)")
    cursor.execute(add_info, add_data)
    conn.commit()
cursor.close()
conn.close()
