import sys
from PyQt5.QtWidgets import *


class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUI()

    # ui 설정
    def setupUI(self):
        self.setGeometry(800, 200, 300, 300)
        self.setWindowTitle("Open Excel-도서목록")

        # 파일 오픈 버튼
        self.pushButton = QPushButton("File Open")
        # 버튼 이벤트 pushButtonClicked 함수 호출
        self.pushButton.clicked.connect(self.pushButtonClicked)
        # 라벨 호출
        self.label = QLabel()

        # 레이아웃 박스 호출
        layout = QVBoxLayout()
        # 레이아웃에 버튼과 라벨 합치기
        layout.addWidget(self.pushButton)
        layout.addWidget(self.label)

        self.setLayout(layout)

    # 오픈 할 파일을 선택했을 때, 파일의 경로를 라벨에 나타냄
    def pushButtonClicked(self):
        fname = QFileDialog.getOpenFileName(self)
        self.label.setText(fname[0])


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    app.exec_()
