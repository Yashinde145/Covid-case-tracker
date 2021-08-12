# do all the imports
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
import csv
import json
import pandas as pd
import tkinter as tk
import plyer
import time
import datetime as dt
import threading
from colored import fg,bg,attr
from colorama import Fore
reset=attr('reset')




# parsing html and extracting data of India
def get_corona_detail_of_india():
    headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:32.0) Gecko/20100101 Firefox/32.0'}
    URL = 'https://www.mygov.in/covid-19/'
    page = requests.get(URL,headers=headers)
    soup=BeautifulSoup(page.text,'html.parser')
    #span=soup.findAll('span',class_='icount')
    #print(soup)  

    global new_cases,active_casesg,dis_cases24,d_cases24
    t_case = soup.select_one(".t_case")
    total_cases = t_case.select_one(".icount").get_text(strip=True)
    new_cases = t_case.select_one(".color-red, .color-green").get_text(strip=True)
    #print(total_cases)
    total_cases = '\n Total cases till today:  '+total_cases
    #print(new_cases)
    new_cases = '\n Cases in last 24 hours:  '+new_cases
    #print()


    a_case = soup.select_one(".active-case")
    active_cases = a_case.select_one(".icount").get_text(strip=True)
    active_cases24 = a_case.select_one(".color-red, .color-green").get_text(strip=True)
    active_cases24_per = a_case.select_one(".per_block").get_text(strip=True)
    #print(active_cases)
    active_casesg = '\n Active cases:  '+active_cases+active_cases24_per
    active_cases = '\n\n Active cases:  '+active_cases+active_cases24_per
    #print(active_cases24)
    #print(active_cases24_per)
    active_cases24 = '\n Difference in last 24 hours:  '+active_cases24
    #print()


    dis_case = soup.select_one(".iblock.discharge")
    dis_cases = dis_case.select_one(".icount").get_text(strip=True)
    dis_cases24 = dis_case.select_one(".increase_block").get_text(strip=True)
    dis_cases_per = dis_case.select_one(".per_block").get_text(strip=True)
    #print(dis_cases)
    dis_cases = '\n\n Total discharged till today:  '+dis_cases+dis_cases_per
    #print(dis_cases24)
    #print(dis_cases_per)
    dis_cases24 = '\n Discharged in last 24 hours:  '+dis_cases24
    #print()


    d_case = soup.select_one(".iblock.death_case")
    d_cases = d_case.select_one(".icount").get_text(strip=True)
    d_cases24 = d_case.select_one(".color-red").get_text(strip=True)
    d_cases_per = d_case.select_one(".per_block").get_text(strip=True)
    #print(d_cases)
    d_cases = '\n\n Total deaths till today:  '+d_cases+d_cases_per
    #print(d_cases24)
    #print(d_cases_per)
    d_cases24 = '\n Deaths in last 24 hours:  '+d_cases24
    #print()


    test_case = soup.select_one(".test_box")
    test_cases = test_case.select_one(".testing_count").get_text(strip=True)
    test_cases24 = soup.select_one(".testing_result").select_one(".testing_count").get_text(strip=True)
    #print(test_cases)
    #print(test_cases24)
    test_cases = '\n\n Total tests till today:  '+test_cases
    test_cases24 = '\n Tests in last 24 hours:  '+test_cases24
    #print()

    
    vac24, vac24_s = (soup.select_one(".yday-vcount").get_text(strip=True, separator="|").split("|"))
    vac_all, vac_all_s = (soup.select_one(".total-vcount").get_text(strip=True, separator="|").split("|"))
    #print(vac_all)
    vac_all = '\n\n Total Vaccinations done: '+vac_all
    #print(vac24)
    vac24 = '\n Vaccinations done in last 24 hours: '+vac24+'\n'
    #print()
    

    z = total_cases+new_cases+active_cases+active_cases24+d_cases+dis_cases+dis_cases24+test_cases+test_cases24+vac_all+vac24
    #print(len(z))
    return z
#get_corona_detail_of_india()




# parsing html and extracting data of State-wise in India
def get_corona_detail_of_states():
    url = "https://www.mohfw.gov.in/data/datanew.json"

    # store the response of URL
    response = urlopen(url)

    # storing the JSON response
    # from url in data
    data_json = json.loads(response.read())
    # print the json response
    #print(data_json)

    f_data=open(r"C:\Users\Yash\Desktop\Covid19_Tracker\Statewise_data.csv",'w')
    csvw = csv.writer(f_data)

    count=0

    for f in data_json:

        if count==0:
            header=f.keys()
            csvw.writerow(header)
            count+=1

        csvw.writerow(f.values())

    f_data.close()
#get_corona_detail_of_states()


# function use to  reload the data from website
def refresh():
    plyer.notification.notify(
            title="COVID 19 cases of INDIA",
            message=get_corona_detail_of_india(),
            timeout=10,
            app_icon=r'C:\Users\Yash\Desktop\Covid19_Tracker\icon.ico')
    newdata = get_corona_detail_of_india()
    print("Refreshing..")
    mainLabel['text'] = newdata


# function for notifying...
def notify_me():
    while True:
        plyer.notification.notify(
            title="COVID 19 cases of INDIA",
            message= new_cases+active_casesg+dis_cases24+d_cases24,
            timeout=10,
            app_icon=r'C:\Users\Yash\Desktop\Covid19_Tracker\icon.ico'
        )
        time.sleep(30)


# creating gui:
root = tk.Tk()
root.geometry("1920x1800")
root.iconbitmap(r"C:\Users\Yash\Desktop\Covid19_Tracker\icon.ico")
root.title("CORONA DATA TRACKER - INDIA")
root.configure(background='light blue')
f = ("poppins", 14, "bold")
banner = tk.PhotoImage(file=r"C:\Users\Yash\Desktop\Covid19_Tracker\banner.png")
bannerLabel = tk.Label(root, image=banner)
bannerLabel.pack()
mainLabel = tk.Label(root, text=get_corona_detail_of_india(), font=f, bg='light blue',fg='red')
mainLabel.pack()

reBtn = tk.Button(root, text="REFRESH", font=f, relief='solid', command=refresh)
reBtn.pack()
#reBtn = tk.Button(root, text="Click here to get State-wise data", font=f, relief='solid', command=get_corona_detail_of_states())
reBtn.pack()


reBtn = tk.Button(root, text="Click Here to get State-wise List", font=f, relief='solid', command=get_corona_detail_of_states())
reBtn.pack()
#reBtn = tk.Button(root, text="Click here to get State-wise data", font=f, relief='solid', command=get_corona_detail_of_states())
reBtn.pack()



# create a new thread
th1 = threading.Thread(target=notify_me)
th1.setDaemon(True)
th1.start()
root.mainloop()

if __name__ == '__main__':
    get_corona_detail_of_india()
    #get_corona_detail_of_states()
