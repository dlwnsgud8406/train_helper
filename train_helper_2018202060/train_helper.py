import os
import time
# import send_from_Gmail_to_AnotherMail as sendmail
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from dotenv import load_dotenv
from first_pyqt import MyApp
from PyQt5.QtWidgets import *

received_value = os.system("python3 first_pyqt.py") # python 파일 실행
information_value = os.system("python3 information.py") # python 파일 실행
select_window = os.system("python3 select_menu.py") # python 파일 실행
f = open("assets/train_select.txt") # srt인지 ktx인지 확인
kind = f.readline()
if kind == "SRT":
    go_SRT = os.system("python3 reservation_SRT.py") # python 파일 실행
elif kind == "KTX":
    go_KTX = os.system("python3 reservation_KTX.py") # python 파일 실행

