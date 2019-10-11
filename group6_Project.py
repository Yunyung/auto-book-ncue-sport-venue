# -*- coding: utf-8 -*-
"""
Created on Sun Jan  6 14:59:53 2019

@author: jason
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

from time import sleep

import time
import getpass
import sys
import datetime
import threading
import os



# webdriver
def WebSpyder():
    driver = webdriver.Chrome()    
    login_url = "https://aps.ncue.edu.tw/court/index.php"
    driver.get(login_url)
    # 填入帳號密碼
    driver.find_element_by_name('p_usr').send_keys(username)
    driver.find_element_by_name('p_pwd').send_keys(password)
    driver.find_element_by_name('log').click()
    if (choice == "1"):
        Booking(driver)
    elif (choice == "2"):
        CancelReservation(driver)
    driver.quit()

#檢查有無alert產生 將alert排除
def CloseAlert(driver):
    try:
        a1 = driver.switch_to.alert
        #print (a1.text+" "+date)
        a1.accept()
    except Exception as e:
        # if no alert occur will throw an exception
        pass

#預約
    
    
def Booking(driver):
    #進入控制日期的frame
    driver.switch_to.frame('ContentS')
    
    # 修改借用日期
    try:
        cleardate = driver.find_element_by_name('sel_date') 
        cleardate.send_keys(Keys.CONTROL + "a")             # 此網頁有某些自動refresh特性，無法調用clear()方法清除，改用模擬DELETE
        cleardate.send_keys(Keys.DELETE)
        driver.find_element_by_name('sel_date').send_keys(usedate) #填入日期
        driver.find_element_by_name('form1').submit()           #確定送出日期    
    except Exception as e:
        print ("Exception found, Selecting date Error", format(e))

    # 借用場地
    for session in crt_time_order_list:
        # 點選要借用的節次
        print("*************************************")
        print("開始執行搶場動作...........")
        try:
            driver.get('https://aps.ncue.edu.tw/court/apply.php?useday='+urldate+'&sec='+str(session)+'&court_id=BMT04')
        except Exception as e:
            CloseAlert(driver)
            print("Error Occur", format(e))
            sys.exit()
        # 取得此場地還有哪些空場
        try:
            Booking_target_success = 0
            court_selectBar = Select(driver.find_element_by_name('court_id'))   # 得到 selectbar
            all_crt_remain = court_selectBar.options                            # 讀取所有 selectbar的 option物件(list存之)   
        except Exception as e:
            CloseAlert(driver)
            print("可能是選擇日期錯誤 請重試!!")
            sys.exit()
            
        print("---------------------------------------------")
        print("節次 - %s" % (session))
        for option in all_crt_remain:                       # 查看剩餘的所有場地有哪些 若其中要借的場地相符，則申請
#            print(option.text, end = " ")                   # option.text會回傳option裡顯示的內容  Ex:羽球場A ..
            for crt in crt_tag_order_list:
                target_crt = "羽球場" + crt              # 改變格式 與option相符，方便比對
                if (target_crt == option.text):
                    court_selectBar.select_by_visible_text(target_crt)
                    driver.find_element_by_name('crs_name').send_keys(crs_name)
                    driver.find_element_by_name('tel').send_keys(tel)
                    driver.find_element_by_name('email').send_keys(email)
                    driver.find_element_by_name('form1').submit()
                    Booking_target_success = 1
                    break;
            if (Booking_target_success == 1):
                break;
                    

        if (Booking_target_success == 1):
            print("成功借到場地: {}".format(target_crt))
        else:
            print("想申請的場地皆已額滿!".format(session))
            print("剩餘場地 : ", end = "")
            if not all_crt_remain:         #若 option 的 list 為空
                print("無", end = "")
            for option in all_crt_remain:
                print(option.text, end = "   ")                   # option.text會回傳option裡顯示的內容  Ex:羽球場A ..
            print()
        print("---------------------------------------------")        
        CloseAlert(driver)
#       sleep(2)
        
        
 # 搶場
def StartReservation(TargetDate):     
    #### 利用申請的時間，用來決定是否要馬上做，或者可申請的時間到後才開始做
    target_month = int(TargetDate[4:6])
    target_Date = int(TargetDate[6:8])
    
    localtime = time.localtime()
    current_day = str(localtime.tm_mday)
    if (target_Date - int(current_day) < 8): # 7天內可以直接申請
        WebSpyder()    
        print("已完成所有搶場動作...........")
    else: #大於7天 需要等待
        # 計算兩個date 時間差距
        Time_target = datetime.datetime(2019, target_month, target_Date - 7, 0, 1, 30)
        Time_current = datetime.datetime(localtime.tm_year, localtime.tm_mon, localtime.tm_mday, localtime.tm_hour, localtime.tm_min, localtime.tm_sec)
        diffSeconds = (Time_target - Time_current).total_seconds() # 總時間(秒)
        print("將在 2019年", target_month,"月", target_Date - 7,"日 0 時 1 分 30 秒開始自動搶場!")
        print("離目標時間還剩 ", int(diffSeconds / 3600) ," 時 ", int((diffSeconds % 3600) / 60),"分",int(diffSeconds % 60) , "秒", " 後自動執行搶場動作")
        print("若要時間到自動搶場則請勿關閉視窗.....................")
        timer = threading.Timer(diffSeconds, WebSpyder)
        timer.start()
        timer.join()
        print("已完成所有搶場動作.........\n")
        
# 取消預約
def CancelReservation(driver):
    try:
        book_url = "https://aps.ncue.edu.tw/court/my_book.php"
        driver.get(book_url)
        while(1):
            #continue_link = driver.find_element_by_partial_link_text('2019/01/16')
            continue_link = driver.find_element_by_link_text(usedate)
            continue_link.click()
            driver.find_element_by_name('form1').submit()
            CloseAlert(driver)
            sleep(1)
    except Exception as e:
        print("取消完成")
        #print ("Exception found", format(e))
        
        
        
        
        
        
###############################################################################
print('######彰化師範大學運動場地借用系統#####')
userModal = input("請選擇 - (1)新的申請 (2)已建檔 : ")

# 使用者選擇 (1)申請新的搶場表單
if userModal == "1":
    
    username = input('請輸入學號 : ')
    password = getpass.getpass('請輸入密碼 : ')
        
    choice = input('請選擇功能 - (1)申請場地 (2)取消場地 (3)exit : ')
    
    while(choice!= "1" and choice != "2" and choice != "3"):
        print('輸入格式錯誤, 請重新選擇(鍵入"1"-"3"之選擇)!!')
        choice = input('請選擇功能 - (1)搶場 (2)取消場地 (3)exit : ')
    
    if choice == "3":
        print('結束程式')
        sys.exit()
    
    #輸入時 1 要輸入成01 後面格式化才不會出錯 
    date = input('請輸入目標日期，格式為 -> 月/日(Ex: 1月28號 -> 01/28) : ') # 設定日期
    localtime = time.localtime()                    # 取得現在時間
    urldate = str(localtime.tm_year) + date[0:2] + date[3:5]               # Ex : 格式化Date => 20190103 用在url中
    usedate = str(localtime.tm_year) + "/" + date[0:2] + "/" + date[3:5]   # Ex : 格式化Date => 2019/01/03
    
    
    # 搶場
    if choice == "1":
        print("請決定借用的時間節次(1~14) (格式: 3 5 7 8 14) : ")
        input_str = sys.stdin.readline()   # 讀入一整串字串
        crt_time_order_list = input_str.split() # 切成串列
        
        print("請決定要申請場地優先次序(一個節次只能申請一個場地) (場地A~J) (格式: A B D J)")
        input_str = sys.stdin.readline() 
        crt_tag_order_list = input_str.split()
    
        crs_name = input('請輸入借場事由 :')
        tel = input('請輸入手機號碼 :')
        email = input('請輸入E-mail:')
        
        
        
        ## 詢問使用者是否建立檔案 ##
        is_saveFile = input("是否將此資料存檔，以便下次可快速使用? (Y/N) : ")
        if (is_saveFile == "Y"):
            file_saveName = input("請輸入此存檔的檔名 : ")
            if not (os.path.exists("userRecord")): #若userRecrod此目錄不存在則創造一個
                os.mkdir("userRecord")
            try:
                f = open("userRecord/" + file_saveName + ".txt", 'w')
                f.write(username + "\n")
                f.write(password + "\n")
                f.write(urldate + "\n")
                f.write(usedate + "\n")
                for item in crt_time_order_list:
                    f.write("%s " % item)
                f.write("\n")
                for item in crt_tag_order_list:
                    f.write("%s " % item)  
                f.write("\n")
                f.write(crs_name + "\n")
                f.write(tel + "\n")
                f.write(email + "\n")
                f.close()
            except Exception as e:
                print("Write file error", format(e))
            print("!!!!!!!已建好資料存檔!!!!!!!")
            
        ## 開始搶場
        StartReservation(urldate)
        
    
    # 取消場地
    if choice == "2":
        print("*************************************")
        print("開始執行取消場地作業................")
        WebSpyder()

# 使用者選擇 (2)已建檔  使用已建立過檔案
elif userModal == "2":
    print("已建檔的檔案列表如下")
    print("-----------------------------------------------------")
    user_file_list = os.listdir("userRecord")
    number = 1;
    for file in user_file_list:
        print(str(number) + ". " + file)
        number = number + 1
    print("-----------------------------------------------------")
    pickFileNumber = input("請選擇你要使用的紀錄的號碼 : ")
    print()
    
    
    content = []
    with open("userRecord/" + user_file_list[int(pickFileNumber) - 1]) as file_Obj:  #開啟檔案
        content = file_Obj.readlines()
    content = [x.strip() for x in content]    # 讀進來會有'\n' 去除 '\n'  
    
    # 寫入檔案內容
    username = content[0]
    password = content[1]
    urldate = content[2]
    usedate = content[3]
    crt_time_order_list = content[4].split()
    crt_tag_order_list = content[5].split()
    crs_name = content[6]
    tel = content[7]
    email = content[8]
    
    while (1):
        print()
        print("學號 : " + username)
        print("搶/取消 日期 : " + usedate)
        print("決定借用的時間節次(1~14) : ", crt_time_order_list)
        print("決定要申請場地優先次序(一個節次只能申請一個場地) (場地A~J) : ", crt_tag_order_list)
        print("借場事由 : ", crs_name)
        print("手機號碼 : ", tel)
        print("Email : ", email)
        print()
        choice = input("(1)搶場 (2)取消借場 (3)更改日期 : ")
        if choice == "1":
            ## 開始搶場
            StartReservation(urldate)
        elif choice == "2":
            print("*************************************")
            print("開始執行取消場地作業................")
            WebSpyder()
        elif choice == "3":
            date = input("請輸入目標日期，格式為 -> 月/日(Ex: 1月28號 -> 01/28) :")
            localtime = time.localtime()    
            urldate = str(localtime.tm_year) + date[0:2] + date[3:5]               # Ex : 格式化Date => 20190103 用在url中
            usedate = str(localtime.tm_year) + "/" + date[0:2] + "/" + date[3:5]   # Ex : 格式化Date => 2019/01/03
            f = open("userRecord/" + user_file_list[int(pickFileNumber) - 1], 'w')
            f.write(username + "\n")
            f.write(password + "\n")
            f.write(urldate + "\n")
            f.write(usedate + "\n")
            for item in crt_time_order_list:
                f.write("%s " % item)
            f.write("\n")
            for item in crt_tag_order_list:
                f.write("%s " % item)  
            f.write("\n")
            f.write(crs_name + "\n")
            f.write(tel + "\n")
            f.write(email + "\n")
            f.close()
            
            print("!!!!!!!更改日期->{} 成功!!!!!".format(usedate))
            sleep(1)        
    
        
    
