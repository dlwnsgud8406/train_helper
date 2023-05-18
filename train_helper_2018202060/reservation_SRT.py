import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import send_from_Gmail_to_AnotherMail as sendmail
from dotenv import load_dotenv
import sys
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
        self.pixmap = QPixmap('assets/map_SRT.png') #SRT 지도 보여주기
        self.label=QLabel(self)
        self.label.setPixmap(self.pixmap)
        self.label.move(0, 0)
        self.label.resize(self.pixmap.width(), self.pixmap.height())

        self.lbl1 = QLabel(self)
        self.lbl1.move(1024, 1024) # lbl1 텍스트 안보이게
        self.lbl2 = QLabel(self)
        self.lbl2.move(1024, 1024) # lbl2 텍스트 안보이게

        do_resevation_button = QPushButton('예약', self)
        do_resevation_button.move(420, 644)

        datetimeedit = QDateTimeEdit(self)
        datetimeedit.setDateTime(QDateTime.currentDateTime())
        datetimeedit.setDateTimeRange(QDateTime(1900, 1, 1, 00, 00, 00), QDateTime(2100, 1, 1, 00, 00, 00)) # 출발시각 및 날짜 입력받기
        datetimeedit.setDisplayFormat('yyyy.MM.dd hh:mm:ss')

        datetimeedit.move(273, 649)

        txt_label = QLabel('나는                            에서                            로',self)
        txt_label.move(10, 650)

        box_department_station = QComboBox(self)
        box_department_station.addItem('선택')
        box_department_station.addItem('수서')
        box_department_station.addItem('동탄')
        box_department_station.addItem('평택지제')
        box_department_station.addItem('천안아산')
        box_department_station.addItem('오송')
        box_department_station.addItem('공주')
        box_department_station.addItem('익산')
        box_department_station.addItem('정읍')
        box_department_station.addItem('광주송정')
        box_department_station.addItem('나주')
        box_department_station.addItem('목포')
        box_department_station.addItem('대전')
        box_department_station.addItem('김천(구미)')
        box_department_station.addItem('서대구')
        box_department_station.addItem('동대구')
        box_department_station.addItem('신경주')
        box_department_station.addItem('울산(통도사)')
        box_department_station.addItem('부산')
        box_department_station.move(30, 645)

        box_department_station.activated[str].connect(self.write_department_station)

        box_arrivement_station = QComboBox(self)
        box_arrivement_station.addItem('선택')
        box_arrivement_station.addItem('수서')
        box_arrivement_station.addItem('동탄')
        box_arrivement_station.addItem('평택지제')
        box_arrivement_station.addItem('천안아산')
        box_arrivement_station.addItem('오송')
        box_arrivement_station.addItem('공주')
        box_arrivement_station.addItem('익산')
        box_arrivement_station.addItem('정읍')
        box_arrivement_station.addItem('광주송정')
        box_arrivement_station.addItem('나주')
        box_arrivement_station.addItem('목포')
        box_arrivement_station.addItem('대전')
        box_arrivement_station.addItem('김천(구미)')
        box_arrivement_station.addItem('서대구')
        box_arrivement_station.addItem('동대구')
        box_arrivement_station.addItem('신경주')
        box_arrivement_station.addItem('울산(통도사)')
        box_arrivement_station.addItem('부산')
        box_arrivement_station.move(150, 645)
        box_arrivement_station.activated[str].connect(self.write_arrivement_station)
        #출발역 및 도착역 입력받기
        user_datetime = datetimeedit.dateTime()
        datetimeedit.dateTimeChanged.connect(lambda : self.set_and_preprocessing_depart_datetime(datetimeedit.dateTime())) #시각 입력받았을때의 이벤트
        do_resevation_button.clicked.connect(self.GoToReservation) # 예약 입력받았을때 이벤트
        # print(user_datetime)
        # do_resevation_button.clicked.connect(self.do_reservation_clicked)

        self.setWindowTitle('Menu')
        self.setGeometry(500, 700, 500, 700)
        self.show()

    def write_department_station(self, text): #출발역 입력
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

    def set_and_preprocessing_depart_datetime(self, datetime): # 출발시각 및 날짜 입력 및 전처리
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

    def GoToReservation(self): #예약 버튼 입력받았을때의 이벤트
        f = open("assets/.env", 'a')
        f.write(self.input_date)
        f.write("\n")
        f.write(self.input_time)
        f.write("\n")
        f.close()
        #dotenv를 통해 env에 있는 파일 변수 load
        dotenv_path = Path('assets/.env')
        load_dotenv(dotenv_path=dotenv_path)
        get_member_num = os.environ.get("member_num")
        get_pw = os.environ.get("pwd")
        get_depart_station = os.environ.get("depart_station")
        get_arrival_station = os.environ.get("arrival_station")
        get_depart_date = os.environ.get("depart_date")
        get_depart_time = os.environ.get("depart_time")
        get_recevied_email = os.environ.get("email")

        #chrome driver 실행
        driver = webdriver.Chrome("chromedriver")
        driver.get('https://etk.srail.co.kr/cmc/01/selectLoginForm.do')
        driver.implicitly_wait(15)
        # SRT 크롤링 시작 및 입력변수에 변수 입력
        driver.find_element(By.ID, 'srchDvNm01').send_keys(get_member_num)
        driver.find_element(By.ID, 'hmpgPwdCphd01').send_keys(get_pw)
        driver.find_element(By.XPATH, '//*[@id="login-form"]/fieldset/div[1]/div[1]/div[2]/div/div[2]/input').click()
        driver.implicitly_wait(5)

        driver.get('https://etk.srail.kr/hpg/hra/01/selectScheduleList.do')
        driver.implicitly_wait(5)

        dep_stn=driver.find_element(By.ID, 'dptRsStnCdNm')
        dep_stn.clear()
        dep_stn.send_keys(get_depart_station)

        arr_stn=driver.find_element(By.ID, 'arvRsStnCdNm')
        arr_stn.clear()
        arr_stn.send_keys(get_arrival_station)

        elm_dptDt=driver.find_element(By.ID, "dptDt")
        driver.execute_script("arguments[0].setAttribute('style','display: True;')", elm_dptDt)

        Select(driver.find_element(By.ID,"dptDt")).select_by_value(get_depart_date)

        elm_dptTm=driver.find_element(By.ID, "dptDt")
        driver.execute_script("arguments[0].setAttribute('style','display: True;')", elm_dptTm)
        Select(driver.find_element(By.ID, "dptTm")).select_by_visible_text(get_depart_time)

        driver.find_element(By.XPATH,"//input[@value='조회하기']").click()

        train_list=driver.find_elements(By.CSS_SELECTOR, '#result-form > fieldset > div.tbl_wrap.th_thead > table > tbody > tr')

        #print(len(train_list))

        # for i in range(1, (get_number_of_trains + 1)):
        #     for j in range(3, 8):
        #         text=driver.find_element(By.CSS_SELECTOR, f"#result-form > fieldset > div.tbl_wrap.th_thead > table > tbody > tr:nth-child({i}) > td:nth-child({j})").text.replace("\n", " ")
        #         print(text, end="")
        #     print()

        is_booked=False
        want_reserve=False
        is_not_booked_count=0
        while True:
            for i in range(1, 5): # 예약이 1~5번쨰 칸에 활성화 되있으면 예약
                standard_seat=driver.find_element(By.CSS_SELECTOR, f"#result-form > fieldset > div.tbl_wrap.th_thead > table > tbody > tr:nth-child({i}) > td:nth-child(7)").text
                reservation = driver.find_element(By.CSS_SELECTOR,
                                                    f"#result-form > fieldset > div.tbl_wrap.th_thead > table > tbody > tr:nth-child({i}) > td:nth-child(8)").text
                if "예약하기" in standard_seat:
                    print("예약 가능")
                    driver.find_element(By.CSS_SELECTOR, f"#result-form > fieldset > div.tbl_wrap.th_thead > table > tbody > tr:nth-child({i}) > td:nth-child(7) > a").click()
                    driver.implicitly_wait(2)

                    if driver.find_elements(By.ID, 'isFalseGotoMain'):
                        sendmail.main(get_recevied_email)
                        is_booked=True
                        print("예약 성공")
                        break

                    else:
                        print("잔여석 없음. 다시 검색")
                        driver.back()
                        driver.implicitly_wait(2)
                if want_reserve:
                    if "신청하기" in reservation:
                        print("예약 대기 완료")
                        driver.find_element(By.CSS_SELECTOR, f"#result-form > fieldset > div.tbl_wrap.th_thead > table > tbody > tr:nth-child({i}) > td:nth-child(8) > a").click()
                        is_booked=True
                        break

            if not is_booked: # 예약 활성화가 되어있지 않은경우 새로고침
                time.sleep(2)

                submit = driver.find_element(By.XPATH, "//input[@value='조회하기']")
                driver.execute_script("arguments[0].click();", submit)
                is_not_booked_count+=1

                print("새로고침 ", is_not_booked_count, "회")
                driver.implicitly_wait(2)
                time.sleep(0.5)

            else:
                break

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
