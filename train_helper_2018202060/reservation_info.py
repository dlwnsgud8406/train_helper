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

        self.pixmap = QPixmap('assets/map_SRT.png')
        self.label=QLabel(self)
        self.label.setPixmap(self.pixmap)
        self.label.move(110, 70)
        self.label.resize(self.pixmap.width(), self.pixmap.height())

        self.setWindowTitle('Menu')
        self.setGeometry(600, 700, 600, 700)
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
