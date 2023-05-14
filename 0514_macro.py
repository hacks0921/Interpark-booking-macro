import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time
import schedule
import datetime
import threading

stop_flag = threading.Event() # 이벤트 처리

Interpark_ID= "hacks09210921"
Interpark_PW= "1q2w3e4r5t"
BirthDay = "850921"
wantDate = 20230523  # input year month dat
BookingDay = 1  # 1: 2 days 1 night, 2: 3 days 2 nights, 3: 4 days 3 nights
BookingArea = "A구역"
BookingSeat = "2"
BookingTime = "09:00"  # 09:03


def stop_task():  # 시작
    stop_flag.set()   # set() : 내부 플래그를 True로 설정
    output_text.insert(tk.END, "---------Thread Stop--------- \n")
    print("Thread stop")

def start_task():  # 중지
    stop_flag.clear() # 내부 플래그를 False로 설정
    if not stop_flag.is_set():
        thread = threading.Thread(target=long_running_task)
        thread.start()

def long_running_task(): # thread 처리 
    output_text.insert(tk.END, "---------Thread Start--------- \n")
    print("Thread Start")
    Interpark_ID = entry_id.get()
    Interpark_PW = entry_pw.get()
    BirthDay = entry_BirthDay.get()
    wantDate = int(entry_date.get())
    BookingDay = int(combobox_booking_day.get().split()[0])
    BookingArea = combobox_booking_area.get()
    BookingSeat = combobox_booking_seat.get()
    BookingTime = entry_booking_time.get()

    print("Interpark ID:", Interpark_ID)
    print("Interpark Password:", Interpark_PW)
    print("BirthDay:", BirthDay)
    print("Desired Date:", wantDate)
    print("Booking Day:", BookingDay)
    print("Booking Area:", BookingArea)
    print("Booking Seat:", BookingSeat)
    print("Booking Time:", BookingTime)

    #Display the print output in the text widget
    #output_text.configure(state='normal')
    #output_text.delete('1.0', tk.END)
    output_text.insert(tk.END, "Interpark ID: {}\n".format(Interpark_ID))
    output_text.insert(tk.END, "Interpark Password: {}\n".format(Interpark_PW))
    output_text.insert(tk.END, "BirthDay: {}\n".format(BirthDay))
    output_text.insert(tk.END, "wantDate Date: {}\n".format(wantDate))
    output_text.insert(tk.END, "Booking Day: {}\n".format(BookingDay))
    output_text.insert(tk.END, "Booking Area: {}\n".format(BookingArea))
    output_text.insert(tk.END, "Booking Seat: {}\n".format(BookingSeat))
    output_text.insert(tk.END, "Booking Time: {}\n".format(BookingTime))
    output_text.insert(tk.END, "[준비] Chorme Browser Open(3sec after) \n")
    output_text.see(tk.END)
    #output_text.configure(state='disabled')

    # Prevent browser shutdown option
    options = Options()
    options.add_experimental_option("detach", True)
    service = Service(ChromeDriverManager().install())
    browser = webdriver.Chrome(service=service, options=options)

    ############################################################################################
    # 예약 사이트 오픈
    print("[준비] Interpark Interpark 파주시 조리읍 공릉 캠핑장 예약 사이트 오픈")
    output_text.insert(tk.END, "[준비] Interpark Interpark 파주시 조리읍 공릉 캠핑장 예약 사이트 Open\n")
    url = 'https://tickets.interpark.com/goods/20008285'
    browser.get(url)
    time.sleep(1)
    # 예약 버튼 클릭
    button_element = browser.find_element(By.CSS_SELECTOR, "a.sideBtn.is-primary").click() # 예약 버튼 클릭

    # 아이디 비번 입력
    print("[준비] ID, PW 입력")
    output_text.insert(tk.END, "[준비] ID,PW 입력\n")
    browser.switch_to.frame(browser.find_element(By.XPATH, "//div[@class='leftLoginBox']/iframe[@title='login']"))  # 아이디/비번 입력 프레임 이동
    id_input = browser.find_element(By.ID, "userId")  # 아이디
    id_input.send_keys(Interpark_ID)
    pw_input = browser.find_element(By.ID, "userPwd") # 비번
    pw_input.send_keys(Interpark_PW)
    pw_input.send_keys(Keys.ENTER)
    time.sleep(1)

    # 예약 시작~!~!
    while not stop_flag.is_set():
        now = datetime.datetime.now()
        reservation_dely = "예약 대기중...." + str(now.hour) +":"+ str(now.minute) +":"+ str(now.second)
        output_text.insert(tk.END, "{}\n".format(reservation_dely))
        output_text.see(tk.END)  # Scroll to the end

        print(reservation_dely) 
        time.sleep(1)
        
        if now.hour >= int(BookingTime[:2]) and  now.minute >= int(BookingTime[-2:]):  # BookingTime과 같거나 넘어가면
        #if 1+1 == 2:
            try:
                # 다시 예약 버튼 클릭
                button_element = browser.find_element(By.CSS_SELECTOR, "a.sideBtn.is-primary").click() # 예약 버튼 클릭
                time.sleep(1)  # 딜레이 줘야 안죽음

                # "닫기" 팝업 화면 닫기
                browser.switch_to.window(browser.window_handles[1])  # 팝업 화면으로 이동
                browser.find_element(By.CSS_SELECTOR, ".btn02").click() # "닫기" 버튼 나오면 클릭
                time.sleep(1)

                # 01_기간/위치선택 (일자 -> 숙박 기간 -> 구역, 카라반/텐트 - 다음 단계 클릭)\
                # 01-1 일자

                print("[1단계] 기간/위치선택 시작")
                output_text.see(tk.END)
                output_text.insert(tk.END, "{}\n".format("[1단계] 기간/위치선택 시작"))
                

                CellPlayDate = browser.find_elements(By.NAME, "CellPlayDate")  # 선택 가능한 날짜 모두 불러오기
                for cell in CellPlayDate:
                    if cell.get_attribute("onclick").split("'")[1]== str(wantDate):	# wantDate  예매 원하는 일  (ex: 230524)
                        cell.click()
                        break
                # 01-2 숙박기간            
                Select(browser.find_element(By.ID,"SelectCheckIn")).options[BookingDay].click() #기간 선택
                browser.switch_to.frame(browser.find_element(By.XPATH, "//div[@class='map']/iframe[@id='ifrmSeat']"))  # 프레임 이동
                
                # 01-3 구역, 카라반,텐트
                browser.find_element(By.XPATH,"//*[@id='Map']/area[3]").click()  # 구역 선택 (아무곳이나 선택)
                StySeats = browser.find_elements(By.CSS_SELECTOR, ".stySeat") # 선택 가능 구역 모두 불러오기 

                # 잔여 위치  = 선택 위치 같을 경우 클릭 
                for StySeat in StySeats:
                    Area = StySeat.get_attribute("onclick").split("'")[7]  # Area 정보 불러오기 
                    Seat = StySeat.get_attribute("onclick").split("'")[9]  # 위치 정보 불러오기
                    if Area == BookingArea and Seat == BookingSeat:	# BookingArea, BooingSeat 원하는 위치 지정(Ex: A구역-5번)
                        StySeat.click()
                        output_text.see(tk.END)
                        output_text.insert(tk.END, "{}\n".format("Booking Area, Site: " + Area +"-"+ Seat))
                        break
                else:
                    # 잔여 위치  ≠ 선택 위치 매칭되지 않을 경우 가까운 싸이트 예약
                    for StySeat in StySeats:
                        Area = StySeat.get_attribute("onclick").split("'")[7]  # Area 정보 불러오기 
                        Seat = StySeat.get_attribute("onclick").split("'")[9]  # 위치 정보 불러오기
                        StySeat.click()
                        output_text.see(tk.END)
                        output_text.insert(tk.END, "{}\n".format("Next_Booking Area, Site: " + Area +"-"+ Seat))
                        break

                time.sleep(1)
                browser.find_element(By.ID,"NextStepImage").click()  # 다음 단계 클릭
                time.sleep(1)

                # 02_이용물품선택 
                print("[2단계] 이용물품선택/위치선택 시작")
                output_text.see(tk.END)
                output_text.insert(tk.END, "{}\n".format("[2단계] 이용물품선택/위치선택 시작"))
                browser.switch_to.window(browser.window_handles[1])  # 화면 이동
                browser.switch_to.frame(browser.find_element(By.ID, "ifrmBookStep"))  # 택은 추가
                browser.find_elements(By.ID,"PriceType")[0].click() # 파주 시민 주중 30% 적용
                browser.find_element(By.ID,"NextStepImage").click()  # 다음 단계 클릭
                time.sleep(1)

                # 03_결제하기 (생년월일 입력, 다음단계)
                print("[3단계] 생년월일 → 무통장 선택(신한)")
                output_text.see(tk.END)
                output_text.insert(tk.END, "{}\n".format("[3단계] 생년월일 → 무통장 선택(신한)"))
                browser.find_element(By.XPATH, "//*[@id='YYMMDD']").send_keys(BirthDay)
                #Select(browser.find_element(By.ID,"DiscountCard")).options[2].click() #카드 선택  
                browser.find_element(By.CSS_SELECTOR,"input[type='radio'][value='22004']").click()  # 무통장 입금
                Select(browser.find_element(By.ID,"BankCode")).options[5].click() #은행 선택  5번 신한은행
                browser.find_element(By.ID,"NextStepImage").click()  # 다음 단계 클릭
                time.sleep(1)

                # 04_모두 동의 하기 
                print("[4단계] 모두 동의 하기")
                output_text.see(tk.END)
                output_text.insert(tk.END, "{}\n".format("[4단계] 모두 동의 하기"))
                browser.find_element(By.ID,"checkAll").click()  #모두 동의 하기 
                browser.find_element(By.ID,"btn_Default").click()  # 결제 하기 클릭
                print("[5단계]완료 → 무통장 입금 하세요")
                output_text.insert(tk.END, "{}\n".format("[5단계]완료 → 무통장 입금 하세요"))
                output_text.see(tk.END)
                break
            except:
                break
    print("Thread 중단")
def main():

    global Interpark_ID, Interpark_PW, BirthDay, wantDate, BookingDay ,BookingArea,BookingSeat, BookingTime
    global entry_id, entry_pw, entry_BirthDay, entry_date, combobox_booking_day,combobox_booking_area, combobox_booking_seat, entry_booking_time
    global output_text

    root = tk.Tk()
    root.title("Interpark 파주시 조리읍 공릉 캠핑장 Booking")
    # root.geometry("610x450")
    root.geometry("610x760+50+50")
    root.resizable(width=False, height=False)
    
    label_imformation  = tk.Label(root, text="■ Please enter your Booking information" ,anchor='w')
    label_imformation.grid(row=0, column=0, sticky = tk.W+tk.E+tk.N+tk.S)
    label_imformation.configure(foreground="red")
    
    label_id = tk.Label(root, text="Interpark ID:")
    label_id.grid(row=1, column=0, sticky="e")
    entry_id = tk.Entry(root)
    entry_id.insert(tk.END, Interpark_ID)
    entry_id.grid(row=1, column=1,sticky = tk.W+tk.E+tk.N+tk.S)

    label_pw = tk.Label(root, text="Interpark PW:")
    label_pw.grid(row=2, column=0, sticky="e")
    entry_pw = tk.Entry(root, show="*")
    entry_pw.insert(tk.END, Interpark_PW)
    entry_pw.grid(row=2, column=1,sticky = tk.W+tk.E+tk.N+tk.S)

    label_BirthDay = tk.Label(root, text="BirthDay(YYMMDD):")
    label_BirthDay.grid(row=3, column=0, sticky="e")
    entry_BirthDay = tk.Entry(root)
    entry_BirthDay.insert(tk.END, BirthDay)
    entry_BirthDay.grid(row=3, column=1,sticky = tk.W+tk.E+tk.N+tk.S)

    label_date = tk.Label(root, text="예약일(YYYYMMDD):")
    label_date.grid(row=4, column=0, sticky="e")
    entry_date = tk.Entry(root)
    entry_date.insert(tk.END, wantDate)
    entry_date.grid(row=4, column=1,sticky = tk.W+tk.E+tk.N+tk.S)

    label_booking_day = tk.Label(root, text="Booking Day:")
    label_booking_day.grid(row=5, column=0, sticky="e")
    combobox_booking_day = ttk.Combobox(root, values=["1 night 2 days", "2 night 3 days", "3 night 4 days", "4 night 5 days"])
    combobox_booking_day.set("1 night 2 day")
    combobox_booking_day.grid(row=5, column=1,sticky = tk.W+tk.E+tk.N+tk.S)

    label_booking_area = tk.Label(root, text="Booking Area:")
    label_booking_area.grid(row=6, column=0, sticky="e")
    combobox_booking_area = ttk.Combobox(root, values=["A구역", "B구역"])
    combobox_booking_area.set(BookingArea)
    combobox_booking_area.grid(row=6, column=1,sticky = tk.W+tk.E+tk.N+tk.S)

    label_booking_seat = tk.Label(root, text="Booking Seat:")
    label_booking_seat.grid(row=7, column=0, sticky="e")
    combobox_booking_seat = ttk.Combobox(root, values=list(range(1, 21)))
    combobox_booking_seat.set(BookingSeat)
    combobox_booking_seat.grid(row=7, column=1,sticky = tk.W+tk.E+tk.N+tk.S)

    label_booking_time = tk.Label(root, text="Booking Time(23:59):")
    label_booking_time.grid(row=8, column=0, sticky="e")
    entry_booking_time = tk.Entry(root)
    entry_booking_time.insert(tk.END, BookingTime)
    entry_booking_time.grid(row=8, column=1,sticky = tk.W+tk.E+tk.N+tk.S)

    label_booking_seat = tk.Label(root, text="■ Booking Area, SeatMap" ,anchor='w')
    label_booking_seat.grid(row=9, column=0, sticky = tk.W+tk.E+tk.N+tk.S)
    label_booking_seat.configure(foreground="green")

    # Load the image
    # image_path = "C:\\\\Code\\공릉캠핑장.png"
    image_path = ".\\CampingSiteArea.png"
    image = Image.open(image_path)
    #image = image.resize((600, 300), Image.ANTIALIAS)  # Adjust the size as per your requirement
    image = image.resize((600, 300), resample=Image.LANCZOS)  # Adjust the size and resampling method as per your requirement
    photo = ImageTk.PhotoImage(image)

    # Create a label to display the image
    image_label = tk.Label(root, image=photo)
    image_label.grid(row=10, column=0, columnspan=3, sticky = tk.W+tk.E+tk.N+tk.S)

    # 진행사항 표시
    output_text_name = tk.Label(root, text="■ Process Log" ,anchor='w')
    output_text_name.grid(row=11, column=0, sticky = tk.W+tk.E+tk.N+tk.S)
    output_text_name.configure(foreground="blue")
    output_text = tk.Text(root, height=15, width=50)
    # output_text.insert(tk.END, "{}\n".format("1. 실행파일이 있는 폴더에 chromedriver.exe, LICENSE.chromedriver 파일이 있어야 함"))
    # output_text.insert(tk.END, "{}\n".format("2. 예약 정보 입력(booking site에서 선택)"))
    # output_text.insert(tk.END, "{}\n".format("3. Start 버튼 클릭")
    # output_text.insert(tk.END, "{}\n".format("4. Booking 시간이 되면 자동으로 예약 진행")

    output_text.grid(row=12, column=0, columnspan=3, sticky = tk.W+tk.E+tk.N+tk.S)

    message_label = tk.Label(root, text="※ Make Day : 202305 / 서홍박" ,anchor='w')
    message_label.grid(row=13, column=0, sticky = tk.W+tk.E+tk.N+tk.S)
    message_label.configure(foreground="black")

    # start click button
    start_button = tk.Button(root, text="Start", command=start_task, bg="#00ffff")
    start_button.grid(row=1, column=2, rowspan=4,sticky = tk.W+tk.E+tk.N+tk.S)
    # stop click button
    stop_button = tk.Button(root, text="Stop", command=stop_task, bg="#FF99FF")
    stop_button.grid(row=5, column=2, rowspan=4,sticky = tk.W+tk.E+tk.N+tk.S)

    root.mainloop()

if __name__ == "__main__":
    main()
