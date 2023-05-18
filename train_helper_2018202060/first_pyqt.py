import sys
import os.path
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QPixmap, QIcon


class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        label1 = QLabel('KTX와 SRT중 탑승할 기차를 선택하시오.', self)
        label1.move(45, 40) # 설명

        self.pixmap = QPixmap('assets/select_train.png') #사진 보여주기

        self.label=QLabel(self)
        self.label.setPixmap(self.pixmap)
        self.label.setContentsMargins(10, 20, 10, 20)
        self.label.resize(self.pixmap.width(), self.pixmap.height())


        #KTX와 SRT중 고르는 체크박스
        KTX_select = QCheckBox('KTX', self)
        KTX_select.move(20, 200)
        # KTX_select.toggle()
        KTX_select.clicked.connect(self.changeTitle1)

        SRT_select = QCheckBox('SRT', self)
        SRT_select.move(220, 200)
        SRT_select.clicked.connect(self.changeTitle2)

        #버튼과 버튼을 누르면 이벤트 발생
        button1 = QPushButton('OK', self)
        # button1.setCheckable(True)
        button1.move(60, 250)
        button1.clicked.connect(self.button1_clicked)

        button2 = QPushButton('Cancel', self)
        # button2.setCheckable(True)
        button2.move(150, 250)
        button2.clicked.connect(QCoreApplication.instance().quit)


        vbox = QVBoxLayout()
        vbox.addWidget(button1)
        vbox.addWidget(button2)
        # SRT_select.toggle()


        self.setWindowTitle('Train Reservation - selecting')
        self.setGeometry(300, 300, 300, 300)
        self.show()

    def button1_clicked(self): # OK를 눌렀을때 생기는 이벤트
        check_file = "assets/train_select.txt"
        if os.path.isfile(check_file) :
            QCoreApplication.instance().quit()


    def changeTitle1(self): # ktx를 체크박스로 입력했을때
        f = open("assets/train_select.txt", 'w')
        f.write('KTX')

        f.close()

    def changeTitle2(self): #SRT를 체크박스로 입력했을때
        f = open("assets/train_select.txt", 'w')
        f.write('SRT')
        f.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
