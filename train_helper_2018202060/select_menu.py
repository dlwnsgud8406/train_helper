import sys
import os.path
import webbrowser
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QPixmap, QIcon


class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.pixmap = QPixmap('assets/menu.png')
        self.label=QLabel(self)
        self.label.setPixmap(self.pixmap)
        self.label.move(80, 0)
        self.label.resize(self.pixmap.width(), self.pixmap.height())

        f = open("assets/train_select.txt")
        kind = f.readline() # ktx인지 srt인지 확인

        button1 = QPushButton('예매하러 가기', self)
        # button1.setCheckable(True)
        button1.move(100, 130)
        reservation_state = button1.clicked.connect(lambda  : self.GoToReservation(kind))


        go_event = kind + " 이벤트 보러가기"
        button2 = QPushButton(go_event, self)
        # button2.setCheckable(True)
        button2.move(80, 180)
        button2.clicked.connect(lambda  : self.GoToEvent(kind))

        go_announcement = kind + " 공지사항 보러가기"
        button3 = QPushButton(go_announcement, self)
        # button2.setCheckable(True)
        button3.move(75, 230)
        button3.clicked.connect(lambda  : self.GoToAnouncement(kind))

        button4 = QPushButton("종료", self)
        button4.move(120, 280)
        button4.clicked.connect(QCoreApplication.instance().quit)


        vbox = QVBoxLayout()
        vbox.addWidget(button1)
        vbox.addWidget(button2)
        vbox.addWidget(button3)
        vbox.addWidget(button4)
        # SRT_select.toggle()

        self.setWindowTitle('Menu')
        self.setGeometry(300, 350, 300, 350)
        self.show()

    def GoToReservation(self, kind):
        exit()

    def GoToEvent(self, kind):
        if kind == 'SRT':
            webbrowser.open('https://etk.srail.kr/cms/article/list.do?pageId=TK0502000000')
        elif kind == 'KTX':
            webbrowser.open('https://www.letskorail.com/ebizcom/event/tourist/EbizcomEvtTourWcus06701.do')

    def GoToAnouncement(self, kind):
        if kind == "SRT":
            webbrowser.open("https://etk.srail.kr/cms/article/list.do?pageId=TK0502000000")
        elif kind =="KTX":
            webbrowser.open("https://www.letskorail.com/ebizcom/event/total/EbizcomEventTotallw_cus06101.do")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
