import sys
from PyQt5.QtWidgets import *
import xlrd
from urllib.request import quote
import urllib.parse
from bs4 import BeautifulSoup as bs
import pymysql



class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        self.setGeometry(800, 200, 300, 300)
        self.setWindowTitle("PyStock v0.1")

        self.pushButton = QPushButton("File Open")
        self.pushButton.clicked.connect(self.pushButtonClicked)
        self.label = QLabel()

        layout = QVBoxLayout()
        layout.addWidget(self.pushButton)
        layout.addWidget(self.label)

        self.setLayout(layout)

    def pushButtonClicked(self):
        # filter = "csv(*.csv)"
        fname = QFileDialog.getOpenFileName(self) # 엑셀파일만 읽어오는 것으로 수정해야함 !!!!!!!!!!!
        # 엑셀파일 읽어오기
        wb = xlrd.open_workbook(fname[0])
        # 모든 시트 가져오기
        sheets = wb.sheets()
        ## 첫번째 시트만 가져오기
        # sheet = wb.sheet_by_index(0)
        book_list = []

        for sheet in sheets:
            for i in range(1, sheet.nrows):
                a1 = sheet.cell_value(i, 0)
                a2 = sheet.cell_value(i, 1)
                book_list.append(str(a1)+' '+str(a2))
        print(book_list)

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
                # if문을 포함하지 않으면 TypeError: not enough arguments for format string 발생
                if len(sub_list)==4:
                    sub_list.append(' ')
            list.append(tuple(sub_list))
        print(list)

        conn = pymysql.connect(user='root',
                               password='root',
                               host='127.0.0.1',
                               database='bookstore')
        cursor = conn.cursor()
        # 기존에 for문을 이용하면 데이터가 들어올 때마다 mysql에 접속하게 만드는 문제점이 있기 때문에 수정
        cursor.executemany("INSERT INTO bookinfo (title, author, publisher, price, stock) VALUES (%s, %s, %s, %s, %s)", list)
        conn.commit()
        cursor.close()
        conn.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    app.exec_()
