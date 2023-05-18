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
        layout = QGridLayout()
        self.setLayout(layout)

        label1 = QLabel('회원정보를 입력하시s오.', self) # 설명
        label1.move(45, 40)

        self.pixmap = QPixmap('assets/input_information.jpeg')

        self.label=QLabel(self)
        self.label.setPixmap(self.pixmap)
        self.label.setContentsMargins(10, 10, 10, 10)
        self.label.resize(self.pixmap.width(), self.pixmap.height())

        self.lbl = QLabel(self)
        self.lbl.move(60, 40)

        #  QLineEdit 인스턴스인 qle를 생성

        qle1 = QLineEdit(self) # 회원번호 입력하기
        qle1.move(500, 200)
        #  입력모드를 Normal로 설정: 입력된 문자를 표시합니다. (기본값)
        qle1.setEchoMode(QLineEdit.Normal)


        label2 = QLabel('회원번호', self)
        label2.move(450, 200)


        qle2 = QLineEdit(self) # 비밀번호 입력하기
        qle2.move(500, 250)
        #  입력모드를 Password로 설정: 입력된 문자 대신 비밀번호 가림용 문자를 표시합니다.
        qle2.setEchoMode(QLineEdit.PasswordEchoOnEdit)

        label3 = QLabel('비밀번호', self)
        label3.move(450, 250)

        label4 = QLabel('결제알림 이메일 : ',self)
        label4.move(450, 300)

        qle3 = QLineEdit(self) # 이메일 입력하기
        qle3.move(550, 300)
        #  입력모드를 Normal로 설정: 입력된 문자를 표시합니다. (기본값)
        qle3.setEchoMode(QLineEdit.Normal)

        button1 = QPushButton('OK', self)
        # button1.setCheckable(True)
        button1.move(425, 500)
        button1.clicked.connect(lambda : self.button1_clicked(qle1.text(), qle2.text(), qle3.text())) # ok를 눌렀을때 이벤트 발생

        button2 = QPushButton('Cancel', self)
        # button2.setCheckable(True)
        button2.move(530, 500)
        button2.clicked.connect(QCoreApplication.instance().quit) # cancel을 누르면 종료

        self.setWindowTitle('information - input')
        self.setGeometry(1300, 1300, 1300, 1300)
        self.show()

    def button1_clicked(self, mem_number, mem_passwd, mem_email): # ok를 눌렀을때의 이벤트
        f = open("assets/.env", 'w')
        mem_number_string = "member_num=" + "\"" + mem_number + "\""
        mem_passwd_string = "pwd=" + "\"" + mem_passwd + "\""
        mem_email_string = "email=" + "\"" + mem_email + "\""
        f.write(mem_number_string)
        f.write("\n")
        f.write(mem_passwd_string)
        f.write("\n")
        f.write(mem_email_string)
        f.write("\n")
        f.close()
        exit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
