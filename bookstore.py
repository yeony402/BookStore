import sys
import xlrd
import requests
from urllib.request import quote
import urllib.parse
from bs4 import BeautifulSoup as bs
import mysql.connector
import pandas as pd


##########################################################
# query = sys.argv[1]

# 알리딘 api로 가져올 데이터
data = urllib.parse.urlencode({
	'ttbkey' : 'ttbyeony4022121001',
    'SearchTarget':'Book',
    'Query':'코딩인터뷰 완전분석 게일라크만',
    'QueryType':'Keyword',
    'Sort':'Title',
})
# 검색api url
url = 'http://www.aladdin.co.kr/ttb/api/ItemSearch.aspx'
con = urllib.request.urlopen(url +'?' + data)
html = con.read()
con.close()

# 요청한 값 lxml로 읽어오기
soup = bs(html, "lxml")
soupString = str(soup)

list=[]
stock_list=[]
if soupString.find('<error xml') > -1:
	for s in soup('errormessage'):
		print ('## Error!! ##')
		print ("Error Message: ")
else:
    # 도서별로 리스트에 담기
    for title in soup('title')[1] :
        stock_list.append(title)
        for author in soup('author')[1]:
            stock_list.append(author)
            for publisher in soup('publisher')[1]:
                stock_list.append(publisher)
                for pricesales in soup('pricesales')[1]:
                    stock_list.append(pricesales)
                    for stockstatus in soup('stockstatus')[1]:
                        stock_list.append(stockstatus)
    list.append(stock_list)
    print(list)
