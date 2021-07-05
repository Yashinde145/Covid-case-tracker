# do all the imports
import requests
from bs4 import BeautifulSoup
import pandas as pd
from time import strftime
import tkinter as tk
import plyer
import time
import datetime as dt
import threading
from colored import fg,bg,attr
reset=attr('reset')




# parsing html and extracting data of India
def get_corona_detail_of_india():
    headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:32.0) Gecko/20100101 Firefox/32.0'}
    URL = 'https://covidindia.org/'
    page = requests.get(URL,headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    #print(soup)
    total_cases = soup.find("div",class_="elementor-element elementor-element-aceece0 elementor-widget elementor-widget-heading").get_text()
    tc=(total_cases.strip())
    #print(tc)
    
    update = soup.find("div", class_="elementor-element elementor-element-f032d3d elementor-widget elementor-widget-text-editor").get_text().strip()
    up=('\n'+update+'\n\n')

    active_cases = soup.find("div", class_="elementor-element elementor-element-1801ce0 elementor-widget elementor-widget-text-editor").get_text()
    active_cases24 = soup.find("div", class_="elementor-element elementor-element-0ac43cf elementor-widget elementor-widget-text-editor").get_text()
    
    ac=('\n\nTotal active cases: '+active_cases.strip()+' ('+active_cases24.strip()+')')
    #print(ac)

    deaths = soup.find("div", class_="elementor-element elementor-element-578f531 elementor-widget elementor-widget-text-editor").get_text()
    deaths24 = soup.find("div", class_="elementor-element elementor-element-0093072 elementor-widget elementor-widget-text-editor").get_text()
    d=('\n\nTotal deaths: '+deaths.strip()+' ('+deaths24.strip()+')')
    
    cure = soup.find("div", class_="elementor-element elementor-element-d112f0a elementor-widget elementor-widget-text-editor").get_text()
    cure24 = soup.find("div", class_="elementor-element elementor-element-0fc4aa0 elementor-widget elementor-widget-text-editor").get_text()
    c=('\n\nTotal recovered till date: '+cure.strip()+' ('+cure24.strip()+')')

    test = soup.find("div", class_="elementor-element elementor-element-700a9e3 elementor-widget elementor-widget-text-editor").get_text()
    test24 = soup.find("div", class_="elementor-element elementor-element-2df2689 elementor-widget elementor-widget-text-editor").get_text()
    t=('\n\nTotal tests done: '+test.strip()+' ('+test24.strip()+')\n')

    z=up+tc+ac+d+c+t
    #print(len(z))
    return z
#get_corona_detail_of_india()

# parsing html and extracting data of State-wise in India
def get_corona_detail_of_states():
    headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:32.0) Gecko/20100101 Firefox/32.0'}
    URL = 'https://covidindia.org/'
    html_page = requests.get(URL,headers=headers).text
    soup = BeautifulSoup(html_page, 'lxml')
    get_table=soup.find("table",id="tablepress-96")
    get_table_data=get_table.tbody.find_all("tr")
    #print(get_table_data)
    dic={}
    for i in range(len(get_table_data)):
        try:
            key=get_table_data[i].find+all("a",href=True)[0].string
        except:
            key=get_table_data[i].find_all("td")[0].string    
        values=[j.string for j in get_table_data[i].find_all("td")]
        print(key,values)
        dic[key]=values
    
    column_names=["Confirmed Cases","Recoveries","Deaths"]
    df=pd.DataFrame(dic).T.iloc[:,1:4]
    df.index.name="State/Union Territory"
    df.columns=column_names
    df.to_csv(r"D:\SEM-5\OSTC\ostcp\Corona_State-wise_India.csv")
    print("done")
#get_corona_detail_of_states()

# function use to  reload the data from website
def refresh():
    plyer.notification.notify(
            title="COVID 19 cases of INDIA",
            message=get_corona_detail_of_india(),
            timeout=10,
            app_icon=r'D:\SEM-5\OSTC\ostcp\icon.ico')
    newdata = get_corona_detail_of_india()
    print("Refreshing..")
    mainLabel['text'] = newdata


# function for notifying...
def notify_me():
    while True:
        plyer.notification.notify(
            title="COVID 19 cases of INDIA",
            message=get_corona_detail_of_india(),
            timeout=10,
            app_icon=r'D:\SEM-5\OSTC\ostcp\icon.ico'
        )
        time.sleep(30)

# creating gui:
root = tk.Tk()
root.geometry("900x800")
root.iconbitmap(r"D:\SEM-5\OSTC\ostcp\icon.ico")
root.title("CORONA DATA TRACKER - INDIA")
root.configure(background='light blue')
f = ("poppins", 14, "bold")
banner = tk.PhotoImage(file=r"D:\SEM-5\OSTC\ostcp\banner.png")
bannerLabel = tk.Label(root, image=banner)
bannerLabel.pack()
mainLabel = tk.Label(root, text=get_corona_detail_of_india(), font=f, bg='light blue',fg='red')
mainLabel.pack()

reBtn = tk.Button(root, text="REFRESH", font=f, relief='solid', command=refresh)
reBtn.pack()
print('\n\n\n')
reBtn = tk.Button(root, text="Click here to get State-wise data", font=f, relief='solid', command=get_corona_detail_of_states())
reBtn.pack()

'''string = strftime('%H:%M:%S %p')  
root.after(1000, time) 
reBtn = tk.Button(root, text=string, font=f, relief='solid')
reBtn.pack()'''

# create a new thread
th1 = threading.Thread(target=notify_me)
th1.setDaemon(True)
th1.start()
root.mainloop()