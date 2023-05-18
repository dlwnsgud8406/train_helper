import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import send_from_Gmail_to_AnotherMail as sendmail
from dotenv import load_dotenv
import sys
import pyautogui
from pathlib import Path
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QPixmap, QIcon


class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.user_datetime=0
        self.input_date = 0
        self.input_time = 0
        self.received_email=0
        self.initUI()

    def initUI(self):
        self.pixmap = QPixmap('assets/map_KTX.png')
        self.label=QLabel(self)
        self.label.setPixmap(self.pixmap)
        self.label.move(0, 0)
        self.label.resize(self.pixmap.width(), self.pixmap.height())

        self.lbl1 = QLabel(self)
        self.lbl1.move(1024, 1024) # lbl1 텍스트 안보이게
        self.lbl2 = QLabel(self)
        self.lbl2.move(1024, 1024) # lbl2 텍스트 안보이게

        do_resevation_button = QPushButton('예약', self)
        do_resevation_button.move(520, 644)

        datetimeedit = QDateTimeEdit(self)
        datetimeedit.setDateTime(QDateTime.currentDateTime())
        datetimeedit.setDateTimeRange(QDateTime(1900, 1, 1, 00, 00, 00), QDateTime(2100, 1, 1, 00, 00, 00))
        datetimeedit.setDisplayFormat('yyyy.MM.dd hh:mm:ss')

        datetimeedit.move(370, 649)

        txt_label = QLabel('나는 \t \t \t   에서     \t    \t    \t     로',self)
        txt_label.move(10, 650) # 출발역 도착역 출발날짜및 시간 입력받기

        box_department_station = QComboBox(self)
        box_department_station.addItem('선택')
        box_department_station.addItem('서울')
        box_department_station.addItem('연산')
        box_department_station.addItem('영등포')
        box_department_station.addItem('수원')
        box_department_station.addItem('대전')
        box_department_station.addItem('천안아산')
        box_department_station.addItem('서대전')
        box_department_station.addItem('오송')
        box_department_station.addItem('김천구미')
        box_department_station.addItem('동대구')
        box_department_station.addItem('포항')
        box_department_station.addItem('밀양')
        box_department_station.addItem('구포')
        box_department_station.addItem('부산')
        box_department_station.addItem('신경주')
        box_department_station.addItem('마산')
        box_department_station.addItem('울산(통도사)')
        box_department_station.addItem('창원중앙')
        box_department_station.addItem('경산')
        box_department_station.addItem('논산')
        box_department_station.addItem('익산')
        box_department_station.addItem('정읍')
        box_department_station.addItem('광주송정')
        box_department_station.addItem('목포')
        box_department_station.addItem('전주')
        box_department_station.addItem('순천')
        box_department_station.addItem('여수EXPO(구,여수역)')
        box_department_station.addItem('청량리')
        box_department_station.addItem('강릉')
        box_department_station.addItem('행신')
        box_department_station.addItem('정동진')
        box_department_station.move(30, 645)

        box_department_station.activated[str].connect(self.write_department_station)

        box_arrivement_station = QComboBox(self)
        box_arrivement_station.addItem('선택')
        box_arrivement_station.addItem('서울')
        box_arrivement_station.addItem('연산')
        box_arrivement_station.addItem('영등포')
        box_arrivement_station.addItem('수원')
        box_arrivement_station.addItem('대전')
        box_arrivement_station.addItem('천안아산')
        box_arrivement_station.addItem('서대전')
        box_arrivement_station.addItem('오송')
        box_arrivement_station.addItem('김천구미')
        box_arrivement_station.addItem('동대구')
        box_arrivement_station.addItem('포항')
        box_arrivement_station.addItem('밀양')
        box_arrivement_station.addItem('구포')
        box_arrivement_station.addItem('부산')
        box_arrivement_station.addItem('신경주')
        box_arrivement_station.addItem('마산')
        box_arrivement_station.addItem('울산(통도사)')
        box_arrivement_station.addItem('창원중앙')
        box_arrivement_station.addItem('경산')
        box_arrivement_station.addItem('논산')
        box_arrivement_station.addItem('익산')
        box_arrivement_station.addItem('정읍')
        box_arrivement_station.addItem('광주송정')
        box_arrivement_station.addItem('목포')
        box_arrivement_station.addItem('전주')
        box_arrivement_station.addItem('순천')
        box_arrivement_station.addItem('여수EXPO(구,여수역)')
        box_arrivement_station.addItem('청량리')
        box_arrivement_station.addItem('강릉')
        box_arrivement_station.addItem('행신')
        box_arrivement_station.addItem('정동진')
        box_arrivement_station.move(200, 645)

        box_arrivement_station.activated[str].connect(self.write_arrivement_station)
        user_datetime = datetimeedit.dateTime()
        datetimeedit.dateTimeChanged.connect(lambda : self.set_and_preprocessing_depart_datetime(datetimeedit.dateTime()))
        do_resevation_button.clicked.connect(self.GoToReservation) # 예약버튼을 누르면 이벤트 발생
        # print(user_datetime)
        # do_resevation_button.clicked.connect(self.do_reservation_clicked)

        self.setWindowTitle('Menu')
        self.setGeometry(600, 700, 600, 700)
        self.show()

    def write_department_station(self, text): # 출발역 입력
        self.lbl1.setText(text)
        f = open("assets/.env", 'a')
        department_station = "depart_station=" + "\"" + text + "\""
        f.write(department_station)
        f.write("\n")
        f.close()

    def write_arrivement_station(self, text): #도착역 입력
        self.lbl2.setText(text)
        f = open("assets/.env", 'a')
        arrivement_station = "arrival_station=" + "\"" + text + "\""
        f.write(arrivement_station)
        f.write("\n")
        f.close()

    def set_and_preprocessing_depart_datetime(self, datetime): #출발시각및 날짜 입력
        self.user_datetime = datetime
        string_user_datetime = str(self.user_datetime)
        r1 = string_user_datetime.split('.', 3)
        r2 = r1[2]
        idx = r2.find(')')
        name = r2[1:idx]
        input_datetime = name[9:idx]
        before_split_user_datetime = input_datetime.split(', ',7)

        if int(before_split_user_datetime[1]) < 10:
            before_split_user_datetime[1]='0'+before_split_user_datetime[1]
        if int(before_split_user_datetime[2]) < 10:
            before_split_user_datetime[2] = '0' + before_split_user_datetime[2]

        after_split_user_depart_date = before_split_user_datetime[0]+before_split_user_datetime[1]+before_split_user_datetime[2]
        after_split_user_depart_time = before_split_user_datetime[3]

        self.input_date = "depart_date=" + "\"" + after_split_user_depart_date + "\""
        self.input_time = "depart_time=" + "\"" + after_split_user_depart_time + "\""

    def GoToReservation(self): # 예약 버튼 눌러졌을때
        f = open("assets/.env", 'a')
        f.write(self.input_date)
        f.write("\n")
        f.write(self.input_time)
        f.write("\n")
        f.close()

        dotenv_path = Path('assets/.env')
        load_dotenv(dotenv_path=dotenv_path)
        get_member_num = os.environ.get("member_num")
        get_pw = os.environ.get("pwd")
        get_depart_station = os.environ.get("depart_station")
        get_arrival_station = os.environ.get("arrival_station")
        get_depart_date = os.environ.get("depart_date")
        get_depart_time = os.environ.get("depart_time")
        get_received_email = os.environ.get("email") # dotenv를 통해 .env에 저장해둔 정보들 불러오기


        #날짜 및 시간 전처리
        year = get_depart_date[0:4]
        print(year)
        month = get_depart_date[5:6]
        if int(month)<10:
            month = '0' + month
        print(month)
        day = get_depart_date[6:8]
        print(day)
        if int(get_depart_time)<12:
            if int(get_depart_time)<10:
                get_depart_time = get_depart_time+" (오전0"+get_depart_time + ")"
            else:
                get_depart_time = get_depart_time+" (오전 "+get_depart_time + ")"
        elif int(get_depart_time)<24:
            if int(get_depart_time)<22:
                get_depart_time = get_depart_time+" (오후0"+str(int(get_depart_time)-12) + ")"
            else:
                get_depart_time = get_depart_time+" (오후 "+str(int(get_depart_time)-12) + ")"

        driver = webdriver.Chrome("chromedriver")
        #Chrome driver 실행
        driver = webdriver.Chrome("chromedriver")
        driver.get('https://www.letskorail.com/korail/com/login.do')
        driver.implicitly_wait(15)
        #요소를 찾아서 입력
        driver.find_element(By.ID, 'txtMember').send_keys(get_member_num)
        driver.find_element(By.ID, 'txtPwd').send_keys(get_pw)
        driver.find_element(By.XPATH, '//*[@id="loginDisplay1"]/ul/li[3]').click()
        driver.implicitly_wait(5)

        driver.get('https://www.letskorail.com/ebizprd/EbizPrdTicketpr21100W_pr21110.do')
        driver.implicitly_wait(5)

        dep_stn = driver.find_element(By.ID, 'start')
        dep_stn.clear()
        dep_stn.send_keys(get_depart_station)

        arr_stn = driver.find_element(By.ID, 'get')
        arr_stn.clear()
        arr_stn.send_keys(get_arrival_station)

        elm_year = driver.find_element(By.ID, "s_year")
        driver.execute_script("arguments[0].setAttribute('style','display: True;')", elm_year)
        Select(driver.find_element(By.ID, "s_year")).select_by_value(year)

        elm_month = driver.find_element(By.ID, "s_month")
        driver.execute_script("arguments[0].setAttribute('style','display: True;')", elm_month)
        Select(driver.find_element(By.ID, "s_month")).select_by_value(month)

        elm_day = driver.find_element(By.ID, "s_day")
        driver.execute_script("arguments[0].setAttribute('style','display: True;')", elm_day)
        Select(driver.find_element(By.ID, "s_day")).select_by_value(day)

        elm_time = driver.find_element(By.ID, "s_hour")
        driver.execute_script("arguments[0].setAttribute('style','display: True;')", elm_time)
        Select(driver.find_element(By.ID, "s_hour")).select_by_visible_text(get_depart_time)

        driver.find_element(By.XPATH, '//*[@id="center"]/form/div/p/a/img').click()
        # result-form > fieldset > div.tbl_wrap.th_thead > table > tbody > tr:nth-child(1) > td:nth-child(7) > div > a
        # result-form > fieldset > div.tbl_wrap.th_thead > table > tbody > tr:nth-child(1) > td:nth-child(7) > a > span
        is_booked = False
        # want_reserve = False
        is_not_booked_count = 0
        while True:
            for i in range(1, 5): #1~5번째 예약이 떠있는 경우 예약하기
                standard_seat = driver.find_element(By.CSS_SELECTOR,
                                                    f"#tableResult > tbody > tr:nth-child({2*i-1}) > td:nth-child(6)").text
                # result-form > fieldset > div.tbl_wrap.th_thead > table > tbody > tr:nth-child(1) > td:nth-child(7) > a > span
                # tableResult > tbody > tr:nth-child(1) > td:nth-child(6) > a:nth-child(1) > img
                # tableResult > tbody > tr:nth-child(5) > td:nth-child(6) > a:nth-child(1) > img
                # reservation = driver.find_element(By.CSS_SELECTOR,
                #                                   f"#result-form > fieldset > div.tbl_wrap.th_thead > table > tbody > tr:nth-child({i}) > td:nth-child(8)").text
                if "예매" in standard_seat:
                    print("예약 가능")
                    driver.find_element(By.CSS_SELECTOR,
                                        f"##tableResult > tbody > tr:nth-child({2*i-1}) > td:nth-child(6) > a:nth-child(1) > img").click()
                    driver.implicitly_wait(2)
                    pyautogui.press('enter', presses = 7, interval = 1)
                    pyautogui.press('enter', presses = 7, interval = 1)
                    pyautogui.press('enter', presses = 7, interval = 1)
                    pyautogui.press('enter', presses = 7, interval = 1)
                    pyautogui.press('enter', presses = 7, interval = 1)
                    pyautogui.press('enter', presses = 7, interval = 1)
                    pyautogui.press('enter', presses = 7, interval = 1)


                    is_booked = True
                    print("예약 성공")
                    if driver.find_elements(By.ID, 'isFalseGotoMain'):
                        break

                    else:
                        print("잔여석 없음. 다시 검색")
                        driver.back()
                        driver.implicitly_wait(2)

            if not is_booked:
                time.sleep(2)

                submit = driver.find_element(By.XPATH, '//*[@id="tableResult"]/tbody/tr[1]/td[6]/a[1]/img').click()
                # driver.execute_script("arguments[0].click();", submit)
                is_not_booked_count += 1

                print("새로고침 ", is_not_booked_count, "회")
                sendmail.main(get_received_email) # 예약 완료 후 이메일 보내기
                driver.implicitly_wait(2)
                time.sleep(0.5)

            else:
                break


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
