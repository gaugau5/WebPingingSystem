from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import subprocess
import sys
import time
import json
import getopt
import datetime
import tkinter
import js2py
import requests
import os
from time import sleep
from math import log10, pow

import sqlite3
import requests
import os


con = sqlite3.connect('webpinginguserdata.db')
cur = con.cursor()
cur.execute(
'''CREATE TABLE IF NOT EXISTS PerfTestResults(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    username TEXT, 
    testedWebsite TEXT, 
    http_reqs TEXT,
    http_req_duration TEXT,
    data_sent TEXT,
    data_received TEXT,
    vus TEXT,
    error_rate TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
)''')
con.commit()
cur.execute(
'''CREATE TABLE IF NOT EXISTS LoadTestResults(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    username text, 
    testedWebsite TEXT, 
    http_reqs text,
    iterations text,
    data_sent text,
    data_received text,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
)''')
con.commit()
cur.execute(
'''CREATE TABLE IF NOT EXISTS FunctionalityTestResults(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    username text, 
    testedWebsite TEXT, 
    http_result text,
    timeTaken text,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
)''')
con.close()

refresh_interval = 6
metrics = []
metrics1 = []
global username
username = sys.argv[1]


def main():
    print('init')
    global metrics, refresh_interval
    while True:
        print('hello here')
        metric_data = fetch2()
        # metric_data = fetch() //backup
        t = datetime.datetime.now()
        metrics.append( (t, metric_data) )
        print(len(metrics))
        if len(metrics) > 1:
            http_reqs = get_rate2("http_reqs")
            iterations = get_rate2("iterations")
            data_sent = get_rate2("data_sent")
            data_received = get_rate2("data_received")
            print ("%s: reqs/s: %0.1f  Iterations/s: %0.1f  Bytes IN/s: %0.1f  Bytes OUT/s: %0.1f") % \
                                          ( datetime.datetime.now().strftime("%H:%M:%S"), http_reqs, iterations, data_received, data_sent )

        sleep(refresh_interval)
        
def get_rate(metric_name):
    global metrics
    latest_fetch = metrics[-1][1]
    latest_timestamp = metrics[-1][0]
    previous_fetch = metrics[-2][1]
    previous_timestamp = metrics[-2][0]
    delta = latest_fetch[metric_name]['data']['attributes']['sample']['count'] - \
            previous_fetch[metric_name]['data']['attributes']['sample']['count']
    interval = metrics[-1][0] - metrics[-2][0]
    rate = float(delta) / float(interval.seconds)
    return rate

def fetch2():
        r1 = requests.get("http://localhost:6565/v1/metrics/http_reqs").json();
        r2 = requests.get("http://localhost:6565/v1/metrics/iterations").json();
        r3 = requests.get("http://localhost:6565/v1/metrics/data_sent").json();
        r4 = requests.get("http://localhost:6565/v1/metrics/data_received").json();
        return {"http_reqs": r1, "iterations":r2, "data_sent":r3, "data_received": r4}
    
def get_rate2(metric_name):
    global metrics
    latest_fetch = metrics[-1][1]
    latest_timestamp = metrics[-1][0]
    previous_fetch = metrics[-2][1]
    previous_timestamp = metrics[-2][0]
    delta = latest_fetch[metric_name]['data']['attributes']['sample']['count'] - \
            previous_fetch[metric_name]['data']['attributes']['sample']['count']
    interval = metrics[-1][0] - metrics[-2][0]
    rate = float(delta) / float(interval.seconds)
    return rate

#Testing
def main_2():
    print('init')
    global metrics1, refresh_interval
    while True:
        print('hello here')
        metric_data2 = fetch3()
        # metric_data = fetch() //backup
        t1 = datetime.datetime.now()
        metrics1.append( (t1, metric_data2) )
        print(len(metrics1))
        if len(metrics1) > 1:
            http_reqs = get_rate3("http_reqs")
            http_req_duration = get_avg("http_req_duration")
            data_sent = get_rate3("data_sent")
            data_received = get_rate3("data_received")
            vus = get_value("vus")
            error_rate = get_error_rate("error_rate")
            print ("%s: reqs/s: %0.1f  response time/s: %0.1f  Bytes IN/s: %0.1f  Bytes OUT/s: %0.1f vus/s: %0.1f  error_rate/s: %0.1f") % \
                                          ( datetime.datetime.now().strftime("%H:%M:%S"), http_reqs, http_req_duration, data_received, data_sent, vus, error_rate)
            #print ("%s: reqs/s: %0.1f  response time/s: %0.1f  Bytes IN/s: %0.1f  Bytes OUT/s: %0.1f") % \
            #                              ( datetime.datetime.now().strftime("%H:%M:%S"), http_reqs, login_time_avg, data_received, data_sent)

        sleep(refresh_interval)

    
def get_rate3(metric_name1):
    global metrics1
    latest_fetch = metrics1[-1][1]
    latest_timestamp = metrics1[-1][0]
    previous_fetch = metrics1[-2][1]
    previous_timestamp = metrics1[-2][0]
    delta = latest_fetch[metric_name1]['data']['attributes']['sample']['count'] - \
            previous_fetch[metric_name1]['data']['attributes']['sample']['count']
    interval = metrics1[-1][0] - metrics1[-2][0]
    rate = float(delta) / float(interval.seconds)
    return rate

def get_avg(metric_name1):
    global metrics1
    latest_fetch = metrics1[-1][1]
    latest_timestamp = metrics1[-1][0]
    previous_fetch = metrics1[-2][1]
    previous_timestamp = metrics1[-2][0]
    delta = latest_fetch[metric_name1]['data']['attributes']['sample']['avg'] - \
            previous_fetch[metric_name1]['data']['attributes']['sample']['avg']
    interval = metrics1[-1][0] - metrics1[-2][0]
    rate = float(delta) / float(interval.seconds)
    return rate

def get_value(metric_name1):
    global metrics1
    latest_fetch = metrics1[-1][1]
    latest_timestamp = metrics1[-1][0]
    previous_fetch = metrics1[-2][1]
    previous_timestamp = metrics1[-2][0]
    delta = latest_fetch[metric_name1]['data']['attributes']['sample']['value'] - \
            previous_fetch[metric_name1]['data']['attributes']['sample']['value']
    interval = metrics1[-1][0] - metrics1[-2][0]
    rate = float(delta) / float(interval.seconds)
    return rate
    
def get_error_rate(metric_name1):
    global metrics1
    latest_fetch = metrics1[-1][1]
    latest_timestamp = metrics1[-1][0]
    previous_fetch = metrics1[-2][1]
    previous_timestamp = metrics1[-2][0]
    delta = latest_fetch[metric_name1]['data']['attributes']['sample']['rate'] - \
            previous_fetch[metric_name1]['data']['attributes']['sample']['rate']
    interval = metrics1[-1][0] - metrics1[-2][0]
    rate = float(delta) / float(interval.seconds)
    return rate

def fetch3():
        r5 = requests.get("http://localhost:6565/v1/metrics/http_reqs").json();
        r6 = requests.get("http://localhost:6565/v1/metrics/http_req_duration").json();
        r7 = requests.get("http://localhost:6565/v1/metrics/data_sent").json();
        r8 = requests.get("http://localhost:6565/v1/metrics/data_received").json();
        r9 = requests.get("http://localhost:6565/v1/metrics/vus").json();
        r10 = requests.get("http://localhost:6565/v1/metrics/error_rate").json();
        return {"http_reqs": r5, "http_req_duration":r6, "data_sent":r7, "data_received": r8, "vus": r9, "error_rate": r10}
    

#Testing

        
def start():
    global startScreen
    labelhttp = Label
    screen.withdraw()
    userUrl = StringVar()
    Url2=StringVar()
    Url3=StringVar()
    #labelhttp = StringVar()
    startScreen = Toplevel(screen)
    startScreen.title("Premium Functional Testing")
    startScreen.iconbitmap('webpinging.ico')
    startScreen.geometry("600x750")
    startScreen.configure(bg='snow') 
    
    Label(text="",bg='snow').pack()
    my_label=Label(startScreen,text="WebPinging System Functional Testing", bg="thistle4",width="500",height="2", font=("Calibri",13,'bold'))
    my_label.pack(pady=5)
    Label(text="", bg='snow').pack()
    Label(text="",bg='snow').pack()
    my_label3 = Label(startScreen, text= "Test Your Website Status Here!",bg='snow')
    my_label3.pack(pady=5)
    Label(startScreen, text= "URL 1",bg='snow').pack()
    test_entry = Entry(startScreen,textvariable=userUrl, width = 50,borderwidth=4)
    test_entry.pack(pady=5)
    Label(startScreen, text= "URL 2",bg='snow').pack()
    test_entry1 = Entry(startScreen,textvariable=Url2, width = 50,borderwidth=4)
    test_entry1.pack(pady=5)
    Label(startScreen, text= "URL 3",bg='snow').pack()
    test_entry2 = Entry(startScreen,textvariable=Url3, width = 50,borderwidth=4)
    test_entry2.pack(pady=5)
    
    Label(text="",bg='snow').pack()
    def closeTestScreen():
        startScreen.withdraw()
        screen.deiconify()
    # @timer(1,1)
    def statusCode():
        if (userUrl.get() == "" or Url2.get() == "" or Url3.get() == ""):
            warn = "URL input can't be empty"
            messagebox.showerror('Error', warn)
        else:
            start = time.time()
            response = requests.get(userUrl.get())
            response.status_code
            http_result = response.status_code
            end = time.time()
            
            start1 = time.time()
            response1 = requests.get(Url2.get())
            response1.status_code
            http_result1 = response1.status_code
            end1 = time.time()
            
            start2 = time.time()
            response2 = requests.get(Url3.get())
            response2.status_code
            http_result2 = response2.status_code
            end2 = time.time()
            
        
            #test entry 1
            if http_result == 200:
                #messagebox.showinfo(userUrl.get(),'200 All OK')
                result = userUrl.get()
                my_label = Label(startScreen,text="The http status result for "+result+" "+"\n is 200 'All OK'")
                my_label.pack()
                time1 = end - start
                my_label5 = Label(startScreen,text="Time taken (/s): ")
                my_label5.pack()
                my_label8 = Label(startScreen,text=time1)
                my_label8.pack()
                
                con = sqlite3.connect('webpinginguserdata.db')
                cur = con.cursor()
                cur.execute(
                    "INSERT INTO FunctionalityTestResults (username, testedWebsite, http_result, timeTaken) VALUES (:username, :testedWebsite ,:http_result, :timeTaken)",
                    {
                        'username': username,
                        'testedWebsite': userUrl.get(),
                        'http_result': http_result,
                        'timeTaken': time1
                    }
                )
                con.commit()
                con.close()
                
            elif http_result == 301:
                #messagebox.showinfo("Status",'301 Moved Permanently')
                result = userUrl.get()
                my_label = Label(startScreen,text="The http status result for "+result+" "+"\n is 301 'Moved Permanently'")
                my_label.pack()
                time1 = end - start
                my_label5 = Label(startScreen,text="Time taken (/s): ")
                my_label5.pack()
                my_label8 = Label(startScreen,text=time1)
                my_label8.pack()
                
                con = sqlite3.connect('webpinginguserdata.db')
                cur = con.cursor()
                cur.execute(
                    "INSERT INTO FunctionalityTestResults (username, testedWebsite, http_result, timeTaken) VALUES (:username, :testedWebsite ,:http_result, :timeTaken)",
                    {
                        'username': username,
                        'testedWebsite': userUrl.get(),
                        'http_result': http_result,
                        'timeTaken': time1
                    }
                )
                con.commit()
                con.close()
            elif http_result == 302:
                #messagebox.showinfo("Status",'302 Moved Temporarily')
                result = userUrl.get()
                my_label = Label(startScreen,text="The http status result for "+result+" "+"\n is 302 'Moved Temporarily'")
                my_label.pack()
                time1 = end - start
                my_label5 = Label(startScreen,text="Time taken (/s): ")
                my_label5.pack()
                my_label8 = Label(startScreen,text=time1)
                my_label8.pack()
                
                con = sqlite3.connect('webpinginguserdata.db')
                cur = con.cursor()
                cur.execute(
                    "INSERT INTO FunctionalityTestResults (username, testedWebsite, http_result, timeTaken) VALUES (:username, :testedWebsite ,:http_result, :timeTaken)",
                    {
                        'username': username,
                        'testedWebsite': userUrl.get(),
                        'http_result': http_result,
                        'timeTaken': time1
                    }
                )
                con.commit()
                con.close()
            elif http_result == 403:
                #messagebox.showinfo("Status",'403 Forbidden')
                result = userUrl.get()
                my_label = Label(startScreen,text="The http status result for "+result+" "+"\n is 403 'Forbidden'")
                my_label.pack()
                time1 = end - start
                my_label5 = Label(startScreen,text="Time taken (/s): ")
                my_label5.pack()
                my_label8 = Label(startScreen,text=time1)
                my_label8.pack()
                
                con = sqlite3.connect('webpinginguserdata.db')
                cur = con.cursor()
                cur.execute(
                    "INSERT INTO FunctionalityTestResults (username, testedWebsite, http_result, timeTaken) VALUES (:username, :testedWebsite ,:http_result, :timeTaken)",
                    {
                        'username': username,
                        'testedWebsite': userUrl.get(),
                        'http_result': http_result,
                        'timeTaken': time1
                    }
                )
                con.commit()
                con.close()
            elif http_result == 404:
                #messagebox.showinfo("Status",'404 Not Found')
                result = userUrl.get()
                my_label = Label(startScreen,text="The http status result for "+result+" "+"\n is 404 'Not Found'")
                my_label.pack()
                time1 = end - start
                my_label5 = Label(startScreen,text="Time taken (/s): ")
                my_label5.pack()
                my_label8 = Label(startScreen,text=time1)
                my_label8.pack()
                
                con = sqlite3.connect('webpinginguserdata.db')
                cur = con.cursor()
                cur.execute(
                    "INSERT INTO FunctionalityTestResults (username, testedWebsite, http_result, timeTaken) VALUES (:username, :testedWebsite ,:http_result, :timeTaken)",
                    {
                        'username': username,
                        'testedWebsite': userUrl.get(),
                        'http_result': http_result,
                        'timeTaken': time1
                    }
                )
                con.commit()
                con.close()
            elif http_result == 500:
                #messagebox.showinfo("Status",'500 Internal Server Error')
                result = userUrl.get()
                my_label = Label(startScreen,text="The http status result for "+result+" "+"\n is 500 'Internal Server Error'")
                my_label.pack()
                time1 = end - start
                my_label5 = Label(startScreen,text="Time taken (/s): ")
                my_label5.pack()
                my_label8 = Label(startScreen,text=time1)
                my_label8.pack()
                
                con = sqlite3.connect('webpinginguserdata.db')
                cur = con.cursor()
                cur.execute(
                    "INSERT INTO FunctionalityTestResults (username, testedWebsite, http_result, timeTaken) VALUES (:username, :testedWebsite ,:http_result, :timeTaken)",
                    {
                        'username': username,
                        'testedWebsite': userUrl.get(),
                        'http_result': http_result,
                        'timeTaken': time1
                    }
                )
                con.commit()
                con.close()
            elif http_result == 503:
                #messagebox.showinfo("Status",'503 Service Unavailable')
                result = userUrl.get()
                my_label = Label(startScreen,text="The http status result for "+result+" "+"\n is 503 'Service Unavailable'")
                my_label.pack()
                time1 = end - start
                my_label5 = Label(startScreen,text="Time taken (/s): ")
                my_label5.pack()
                my_label8 = Label(startScreen,text=time1)
                my_label8.pack()
                
                con = sqlite3.connect('webpinginguserdata.db')
                cur = con.cursor()
                cur.execute(
                    "INSERT INTO FunctionalityTestResults (username, testedWebsite, http_result, timeTaken) VALUES (:username, :testedWebsite ,:http_result, :timeTaken)",
                    {
                        'username': username,
                        'testedWebsite': userUrl.get(),
                        'http_result': http_result,
                        'timeTaken': time1
                    }
                )
                con.commit()
                con.close()
                
            #test entry 2    
            if http_result1 == 200:
                #messagebox.showinfo(userUrl1.get(),'200 All OK')
                result = Url2.get()
                my_label = Label(startScreen,text="The http status result for "+result+" "+"\n is 200 'All OK'")
                my_label.pack()
                time1 = end1 - start1
                my_label5 = Label(startScreen,text="Time taken (/s): ")
                my_label5.pack()
                my_label8 = Label(startScreen,text=time1)
                my_label8.pack()
                
                con = sqlite3.connect('webpinginguserdata.db')
                cur = con.cursor()
                cur.execute(
                    "INSERT INTO FunctionalityTestResults (username, testedWebsite, http_result, timeTaken) VALUES (:username, :testedWebsite ,:http_result, :timeTaken)",
                    {
                        'username': username,
                        'testedWebsite': Url2.get(),
                        'http_result': http_result1,
                        'timeTaken': time1
                    }
                )
                con.commit()
                con.close()
            elif http_result1 == 301:
                #messagebox.showinfo("Status",'301 Moved Permanently')
                result = Url2.get()
                my_label = Label(startScreen,text="The http status result for "+result+" "+"\n is 301 'Moved Permanently'")
                my_label.pack()
                time1 = end1 - start1
                my_label5 = Label(startScreen,text="Time taken (/s): ")
                my_label5.pack()
                my_label8 = Label(startScreen,text=time1)
                my_label8.pack()
                
                con = sqlite3.connect('webpinginguserdata.db')
                cur = con.cursor()
                cur.execute(
                    "INSERT INTO FunctionalityTestResults (username, testedWebsite, http_result, timeTaken) VALUES (:username, :testedWebsite ,:http_result, :timeTaken)",
                    {
                        'username': username,
                        'testedWebsite': Url2.get(),
                        'http_result': http_result1,
                        'timeTaken': time1
                    }
                )
                con.commit()
                con.close()
            elif http_result1 == 302:
                #messagebox.showinfo("Status",'302 Moved Temporarily')
                result = Url2.get()
                my_label = Label(startScreen,text="The http status result for "+result+" "+"\n is 302 'Moved Temporarily'")
                my_label.pack()
                time1 = end1 - start1
                my_label5 = Label(startScreen,text="Time taken (/s): ")
                my_label5.pack()
                my_label8 = Label(startScreen,text=time1)
                my_label8.pack()
                
                con = sqlite3.connect('webpinginguserdata.db')
                cur = con.cursor()
                cur.execute(
                    "INSERT INTO FunctionalityTestResults (username, testedWebsite, http_result, timeTaken) VALUES (:username, :testedWebsite ,:http_result, :timeTaken)",
                    {
                        'username': username,
                        'testedWebsite': Url2.get(),
                        'http_result': http_result1,
                        'timeTaken': time1
                    }
                )
                con.commit()
                con.close()
            elif http_result1 == 403:
                #messagebox.showinfo("Status",'403 Forbidden')
                result = Url2.get()
                my_label = Label(startScreen,text="The http status result for "+result+" "+"\n is 403 'Forbidden'")
                my_label.pack()
                time1 = end1 - start1
                my_label5 = Label(startScreen,text="Time taken (/s): ")
                my_label5.pack()
                my_label8 = Label(startScreen,text=time1)
                my_label8.pack()
                
                con = sqlite3.connect('webpinginguserdata.db')
                cur = con.cursor()
                cur.execute(
                    "INSERT INTO FunctionalityTestResults (username, testedWebsite, http_result, timeTaken) VALUES (:username, :testedWebsite ,:http_result, :timeTaken)",
                    {
                        'username': username,
                        'testedWebsite': Url2.get(),
                        'http_result': http_result1,
                        'timeTaken': time1
                    }
                )
                con.commit()
                con.close()
            elif http_result1 == 404:
                #messagebox.showinfo("Status",'404 Not Found')
                result = Url2.get()
                my_label = Label(startScreen,text="The http status result for "+result+" "+"\n is 404 'Not Found'")
                my_label.pack()
                time1 = end1 - start1
                my_label5 = Label(startScreen,text="Time taken (/s): ")
                my_label5.pack()
                my_label8 = Label(startScreen,text=time1)
                my_label8.pack()
                
                con = sqlite3.connect('webpinginguserdata.db')
                cur = con.cursor()
                cur.execute(
                    "INSERT INTO FunctionalityTestResults (username, testedWebsite, http_result, timeTaken) VALUES (:username, :testedWebsite ,:http_result, :timeTaken)",
                    {
                        'username': username,
                        'testedWebsite': Url2.get(),
                        'http_result': http_result1,
                        'timeTaken': time1
                    }
                )
                con.commit()
                con.close()
            elif http_result1 == 500:
                #messagebox.showinfo("Status",'500 Internal Server Error')
                result = Url2.get()
                my_label = Label(startScreen,text="The http status result for "+result+" "+"\n is 500 'Internal Server Error'")
                my_label.pack()
                time1 = end1 - start1
                my_label5 = Label(startScreen,text="Time taken (/s): ")
                my_label5.pack()
                my_label8 = Label(startScreen,text=time1)
                my_label8.pack()
                
                con = sqlite3.connect('webpinginguserdata.db')
                cur = con.cursor()
                cur.execute(
                    "INSERT INTO FunctionalityTestResults (username, testedWebsite, http_result, timeTaken) VALUES (:username, :testedWebsite ,:http_result, :timeTaken)",
                    {
                        'username': username,
                        'testedWebsite': Url2.get(),
                        'http_result': http_result1,
                        'timeTaken': time1
                    }
                )
                con.commit()
                con.close()
            elif http_result1 == 503:
                #messagebox.showinfo("Status",'503 Service Unavailable')
                result = Url2.get()
                my_label = Label(startScreen,text="The http status result for "+result+" "+"\n is 503 'Service Unavailable'")
                my_label.pack()
                time1 = end1 - start1
                my_label5 = Label(startScreen,text="Time taken (/s): ")
                my_label5.pack()
                my_label8 = Label(startScreen,text=time1)
                my_label8.pack()
                
                con = sqlite3.connect('webpinginguserdata.db')
                cur = con.cursor()
                cur.execute(
                    "INSERT INTO FunctionalityTestResults (username, testedWebsite, http_result, timeTaken) VALUES (:username, :testedWebsite ,:http_result, :timeTaken)",
                    {
                        'username': username,
                        'testedWebsite': Url2.get(),
                        'http_result': http_result1,
                        'timeTaken': time1
                    }
                )
                con.commit()
                con.close()
                
            #test entry 3
                
            if http_result2 == 200:
                #messagebox.showinfo(userUrl1.get(),'200 All OK')
                result = Url3.get()
                my_label = Label(startScreen,text="The http status result for "+result+" "+"\n is 200 'All OK'")
                my_label.pack()
                time2 = end2 - start2
                my_label5 = Label(startScreen,text="Time taken (/s): ")
                my_label5.pack()
                my_label8 = Label(startScreen,text=time2)
                my_label8.pack()
                
                con = sqlite3.connect('webpinginguserdata.db')
                cur = con.cursor()
                cur.execute(
                    "INSERT INTO FunctionalityTestResults (username, testedWebsite, http_result, timeTaken) VALUES (:username, :testedWebsite ,:http_result, :timeTaken)",
                    {
                        'username': username,
                        'testedWebsite': Url3.get(),
                        'http_result': http_result2,
                        'timeTaken': time2
                    }
                )
                con.commit()
                con.close()
            elif http_result2 == 301:
                #messagebox.showinfo("Status",'301 Moved Permanently')
                result = Url3.get()
                my_label = Label(startScreen,text="The http status result for "+result+" "+"\n is 301 'Moved Permanently'")
                my_label.pack()
                time2 = end2 - start2
                my_label5 = Label(startScreen,text="Time taken (/s): ")
                my_label5.pack()
                my_label8 = Label(startScreen,text=time2)
                my_label8.pack()
                
                con = sqlite3.connect('webpinginguserdata.db')
                cur = con.cursor()
                cur.execute(
                    "INSERT INTO FunctionalityTestResults (username, testedWebsite, http_result, timeTaken) VALUES (:username, :testedWebsite ,:http_result, :timeTaken)",
                    {
                        'username': username,
                        'testedWebsite': Url3.get(),
                        'http_result': http_result2,
                        'timeTaken': time2
                    }
                )
                con.commit()
                con.close()
            elif http_result2 == 302:
                #messagebox.showinfo("Status",'302 Moved Temporarily')
                result = Url3.get()
                my_label = Label(startScreen,text="The http status result for "+result+" "+"\n is 302 'Moved Temporarily'")
                my_label.pack()
                time2 = end2 - start2
                my_label5 = Label(startScreen,text="Time taken (/s): ")
                my_label5.pack()
                my_label8 = Label(startScreen,text=time2)
                my_label8.pack()
                
                con = sqlite3.connect('webpinginguserdata.db')
                cur = con.cursor()
                cur.execute(
                    "INSERT INTO FunctionalityTestResults (username, testedWebsite, http_result, timeTaken) VALUES (:username, :testedWebsite ,:http_result, :timeTaken)",
                    {
                        'username': username,
                        'testedWebsite': Url3.get(),
                        'http_result': http_result2,
                        'timeTaken': time2
                    }
                )
                con.commit()
                con.close()
            elif http_result2 == 403:
                #messagebox.showinfo("Status",'403 Forbidden')
                result = Url3.get()
                my_label = Label(startScreen,text="The http status result for "+result+" "+"\n is 403 'Forbidden'")
                my_label.pack()
                time2 = end2 - start2
                my_label5 = Label(startScreen,text="Time taken (/s): ")
                my_label5.pack()
                my_label8 = Label(startScreen,text=time2)
                my_label8.pack()
                
                con = sqlite3.connect('webpinginguserdata.db')
                cur = con.cursor()
                cur.execute(
                    "INSERT INTO FunctionalityTestResults (username, testedWebsite, http_result, timeTaken) VALUES (:username, :testedWebsite ,:http_result, :timeTaken)",
                    {
                        'username': username,
                        'testedWebsite': Url3.get(),
                        'http_result': http_result2,
                        'timeTaken': time2
                    }
                )
                con.commit()
                con.close()
            elif http_result2 == 404:
                #messagebox.showinfo("Status",'404 Not Found')
                result = Url3.get()
                my_label = Label(startScreen,text="The http status result for "+result+" "+"\n is 404 'Not Found'")
                my_label.pack()
                time2 = end2 - start2
                my_label5 = Label(startScreen,text="Time taken (/s): ")
                my_label5.pack()
                my_label8 = Label(startScreen,text=time2)
                my_label8.pack()
                
                con = sqlite3.connect('webpinginguserdata.db')
                cur = con.cursor()
                cur.execute(
                    "INSERT INTO FunctionalityTestResults (username, testedWebsite, http_result, timeTaken) VALUES (:username, :testedWebsite ,:http_result, :timeTaken)",
                    {
                        'username': username,
                        'testedWebsite': Url3.get(),
                        'http_result': http_result2,
                        'timeTaken': time2
                    }
                )
                con.commit()
                con.close()
            elif http_result2 == 500:
                #messagebox.showinfo("Status",'500 Internal Server Error')
                result = Url3.get()
                my_label = Label(startScreen,text="The http status result for "+result+" "+"\n is 500 'Internal Server Error'")
                my_label.pack()
                time2 = end2 - start2
                my_label5 = Label(startScreen,text="Time taken (/s): ")
                my_label5.pack()
                my_label8 = Label(startScreen,text=time2)
                my_label8.pack()
                
                con = sqlite3.connect('webpinginguserdata.db')
                cur = con.cursor()
                cur.execute(
                    "INSERT INTO FunctionalityTestResults (username, testedWebsite, http_result, timeTaken) VALUES (:username, :testedWebsite ,:http_result, :timeTaken)",
                    {
                        'username': username,
                        'testedWebsite': Url3.get(),
                        'http_result': http_result2,
                        'timeTaken': time2
                    }
                )
                con.commit()
                con.close()
            elif http_result2 == 503:
                #messagebox.showinfo("Status",'503 Service Unavailable')
                result = Url3.get()
                my_label = Label(startScreen,text="The http status result for "+result+" "+"\n is 503 'Service Unavailable'")
                my_label.pack()
                time2 = end2 - start2
                my_label5 = Label(startScreen,text="Time taken (/s): ")
                my_label5.pack()
                my_label8 = Label(startScreen,text=time2)
                my_label8.pack()
                
                con = sqlite3.connect('webpinginguserdata.db')
                cur = con.cursor()
                cur.execute(
                    "INSERT INTO FunctionalityTestResults (username, testedWebsite, http_result, timeTaken) VALUES (:username, :testedWebsite ,:http_result, :timeTaken)",
                    {
                        'username': username,
                        'testedWebsite': Url3.get(),
                        'http_result': http_result2,
                        'timeTaken': time2
                    }
                )
                con.commit()
                con.close()
            
            
    def clear_text():
        test_entry.delete(0, END)
        test_entry1.delete(0,END)
        test_entry2.delete(0,END)
        #labelhttp.config(text = "")
        return None
    
    test_button = Button(startScreen, text= "START THE TEST", fg = 'white', bg = 'red',height="2",width="20",font=("Aharoni",10,'bold'), command =statusCode,borderwidth=4)
    test_button.pack(side = TOP, padx=7,pady=5)
    #Label(text="",bg='snow').pack()
    #Label(text="", bg='snow').pack()
    #Label(text="", bg='snow').pack()
    clear_button = Button(startScreen, text="New Website", bg ='snow',height="2",width="20",font=("Aharoni",10,'bold'),command =clear_text,borderwidth=4)
    clear_button.pack(side = TOP, padx=7,pady=7)
    homeTest_button = Button(startScreen, text="Home",bg='lightblue',height="2",width="20",font=("Aharoni",10,'bold'), command =closeTestScreen,borderwidth=4)
    homeTest_button.pack(side = TOP, padx=7,pady=7)
    Label(text="",bg='snow').pack()
    

def loadtest_screen():
    global testScreen
    screen.withdraw()
    testScreen = Toplevel(screen)
    testScreen.title("Load Test")
    testScreen.iconbitmap('webpinging.ico')
    testScreen.geometry("900x600")
    testScreen.configure(bg='snow') 
    
    # load_canvas = Canvas(testScreen)
    # load_canvas.pack(side = LEFT, fill=BOTH, expand= 1)
    # load_scroll = ttk.Scrollbar(testScreen, orient = VERTICAL, command= load_canvas.yview)
    # load_scroll.pack(side=RIGHT,fill=Y)
    
    # load_canvas.configure(yscrollcommand=load_scroll.set)
    # load_canvas.bind('<Configure>', lambda e: load_canvas.configure(scrollregion=load_canvas.bbox("all")))

    global r1
    labelhttp = Label
    screen.withdraw()
    userUrl = StringVar()
    #labelhttp = StringVar()
        
    my_label=Label(testScreen,text="WebPinging System Load Testing", bg="thistle4",width="500",height="2", font=("Calibri",13))
    my_label.pack(pady=5)
    Label(text="", bg='snow').pack()
    #my_label2 = Label(testScreen, text= "Here we have our URL test function for you to try out.",bg='snow')
    #my_label2.pack(pady=5)
    Label(testScreen,text="",bg='snow').pack()
    Label(testScreen,text="",bg='snow').pack()
    Label(testScreen,text="",bg='snow').pack()
    #my_label3 = Label(testScreen, text= "Test Your Website Performance Here NOW! Enter Your URL to Get Started and See the Results!",bg='snow')
    #my_label3.pack(pady=5)
    #my_label4 = Label(testScreen, text= username)
    Label(testScreen,text="Enter URL",bg='snow').pack()
    test_entry = Entry(testScreen,textvariable=userUrl, width = 50,borderwidth=4)
    test_entry.pack(pady=5)
    
    
    Label(text="",bg='snow').pack()


    def closeTestScreen():
        testScreen.withdraw()
        os.system("WebPingingLogin.py")
        
        
        
    def load_test():
        if (userUrl.get() == ""):
            warn = "URL input can't be empty"
            messagebox.showerror('Error', warn)
        else:
            print('init')
            global metrics, refresh_interval
            r1 = ("Load Test Result of ", userUrl.get())
            print(r1)
            info_message02 = { r1 }
            my_label9 = Label(testScreen,text=info_message02)
            my_label9.pack()
            req_sum = 0
            iter_sum = 0
            data_sent_sum = 0
            data_received_sum = 0
            #new change added to make them literal value
            Final_reqsum = "";
            Final_itersum = "";
            Final_datasentsum = "";
            Final_datareceived = "";
            
            http_reqs = "";
            iterations = "";
            data_sent = "";
            data_received = "";
            try:
                while True:
                    print('hello here')
                    metric_data = fetch2()
                    # metric_data = fetch() //backup
                    t = datetime.datetime.now()
                    metrics.append((t, metric_data))
                    print(len(metrics))            
                    if len(metrics) > 2:
                        http_reqs = get_rate2("http_reqs")
                        iterations = get_rate2("iterations")
                        data_sent = get_rate2("data_sent")
                        data_received = get_rate2("data_received") #add
                        req_sum = req_sum + http_reqs
                        iter_sum = iter_sum + iterations
                        data_sent_sum = data_sent_sum + data_sent
                        data_received_sum = data_received_sum + data_received                    
                        print(http_reqs)
                        print(iterations)
                        print(data_sent)
                        print(data_received)                    
                        print(req_sum)
                        print(iter_sum)
                        print(data_sent_sum)
                        print(data_received_sum)             
                        print("%s: http reqs/s: %0.2f  Iterations/s: %0.1f  Bytes IN/s: %0.1f  Bytes OUT/s: %0.1f"  % ( datetime.datetime.now().strftime("%H:%M:%S"), http_reqs, iterations, data_received, data_sent ))
                        info_message01 = {"%s: http reqs/s: %0.2f  Iterations/s: %0.1f  Bytes IN/s: %0.1f  Bytes OUT/s: %0.1f" % ( datetime.datetime.now().strftime("%H:%M:%S"), http_reqs, iterations, data_received, data_sent )}
                        my_label8 = Label(testScreen,text=info_message01)
                        my_label8.pack()
            except:                   
                print("%s: Total reqs/s: %0.3f  Total Iterations/s: %0.1f  Total Bytes IN/s: %0.1f  Total Bytes OUT/s: %0.1f"  % ( datetime.datetime.now().strftime("%H:%M:%S"), req_sum, iter_sum, data_received_sum, data_sent_sum ))
                info_message03 = {"%s: Total reqs/s: %0.3f  Total Iterations/s: %0.1f  Total Bytes IN/s: %0.1f  Total Bytes OUT/s: %0.1f"  % ( datetime.datetime.now().strftime("%H:%M:%S"), req_sum, iter_sum, data_received_sum, data_sent_sum )}
                my_label10 = Label(testScreen,text=info_message03)
                my_label10.pack()
                print("_________________________________________________________________________________________________________________________")
                info_message04 = "_________________________________________________________________________________________________________________________"
                my_label11 = Label(testScreen,text=info_message04)
                my_label11.pack()
                    
        
            #new change to turn them back to string value
            Final_reqsum = str(req_sum)
            Final_itersum = str(iter_sum)
            Final_datasentsum = str(data_sent_sum)
            Final_datareceived = str(data_received_sum)
            
            #print (Final_reqsum, Final_itersum, Final_datasentsum, Final_datareceived)
            #info_message20 = {Final_reqsum, Final_itersum, Final_datasentsum, Final_datareceived}
            #my_label22 = Label(testScreen,text=info_message20)
            #my_label22.pack()
            
            # new change from line 517 to 531 
            con = sqlite3.connect('webpinginguserdata.db')
            cur = con.cursor()
            cur.execute(
                "INSERT INTO LoadTestResults (username, testedWebsite, http_reqs, iterations, data_sent, data_received) VALUES (:username, :testedWebsite, :http_reqs, :iterations, :data_sent, :data_received)",
                {
                    'username': username,
                    'testedWebsite': userUrl.get(),
                    'http_reqs': Final_reqsum,
                    'iterations': Final_itersum,
                    'data_sent': Final_datasentsum,
                    'data_received': Final_datareceived
                }
            ) 
            con.commit()
            con.close()
                
            sleep(refresh_interval)
        
    
    def closeTestScreen():
        testScreen.withdraw()
        screen.deiconify()
        #os.system("WebPingingLogin.py")

    test_button = Button(testScreen, text= "START THE TEST", fg = 'white', bg = 'red',height="2",width="20",font=("Aharoni",10,'bold'), command =load_test,borderwidth=4)
    test_button.pack(side = TOP, padx=7,pady=5)
    homeTest_button = Button(testScreen, text="Home",bg='snow',height="2",width="20",font=("Aharoni",10,'bold'), command =closeTestScreen,borderwidth=4)
    homeTest_button.pack(side = TOP, padx=10,pady=7)
    
def performancetest_screen():
    global performancetestScreen
    screen.withdraw()
    performancetestScreen = Toplevel(screen)
    performancetestScreen.title("Performance Test")
    performancetestScreen.iconbitmap('webpinging.ico')
    performancetestScreen.geometry("900x600")
    performancetestScreen.configure(bg='snow') 
    

    global r1
    labelhttp = Label
    screen.withdraw()
    userPerformanceUrl = StringVar()
    #labelhttp = StringVar()
        
    my_label12=Label(performancetestScreen,text="WebPinging System Performance Testing", bg="thistle4",width="500",height="2", font=("Calibri",13))
    my_label12.pack(pady=5)
    Label(performancetestScreen,text="", bg='snow').pack()
    Label(performancetestScreen,text="", bg='snow').pack()
    Label(performancetestScreen,text="", bg='snow').pack()
    # my_label13 = Label(performancetestScreen, text= "Here we have our URL test function for you to try out.",bg='snow')
    # my_label13.pack(pady=5)
    Label(text="",bg='snow').pack()
    # my_label14 = Label(performancetestScreen, text= "Test Your Website Performance Here NOW! Enter Your URL to Get Started and See the Results!",bg='snow')
    # my_label14.pack(pady=5)
    Label(performancetestScreen,text="Enter URL",bg='snow').pack()
    test_entry1 = Entry(performancetestScreen,textvariable=userPerformanceUrl, width = 50,borderwidth=4)
    test_entry1.pack(pady=5)
    Label(performancetestScreen,text="", bg='snow').pack()
    Label(performancetestScreen,text="", bg='snow').pack()
    
    Label(text="",bg='snow').pack()


    def closePerformanceTestScreen():
        performancetestScreen.withdraw()
        os.system("WebPingingLogin.py")
        
        
        
    def performance_test():
        if (userPerformanceUrl.get() == ""):
            warn = "URL input can't be empty"
            messagebox.showerror('Error', warn)
        else:
            print('init')
            global metrics1, refresh_interval
            r01 = ("Performance Test Result of ", userPerformanceUrl.get())
            print(r01)
            info_message05 = { r01 }
            my_label15 = Label(performancetestScreen,text=info_message05)
            my_label15.pack()
            req_sum = 0
            response_sum = 0
            data_sent_sum = 0
            data_received_sum = 0
            vus_sum = 0
            error_rate_sum = 0
            req_avg = 0
            response_avg = 0
            data_sent_avg = 0
            data_received_avg = 0
            vus_avg = 0
            error_rate_avg = 0
            http_reqs = "";
            http_req_duration = "";
            data_sent = "";
            data_received = "";
            vus = "";
            error_rate = "";
            count = 0
            try:
                while True:
                    print('hello here')
                    metric_data2 = fetch3()
                    # metric_data = fetch() //backup
                    t1 = datetime.datetime.now()
                    metrics1.append((t1, metric_data2))
                    print(len(metrics1))            
                    if len(metrics1) > 2:
                        count  +=1
                        http_reqs = get_rate3("http_reqs")
                        http_req_duration = get_avg("http_req_duration")
                        data_sent = get_rate3("data_sent")
                        data_received = get_rate3("data_received")
                        vus = get_value("vus")
                        error_rate = get_error_rate("error_rate") #add
                        req_sum = req_sum + http_reqs
                        response_sum = response_sum + http_req_duration
                        data_sent_sum = data_sent_sum + data_sent
                        data_received_sum = data_received_sum + data_received  
                        vus_sum = vus_sum + vus
                        error_rate_sum = error_rate_sum + error_rate
                        # req_avg = req_sum / http_req_duration
                        # response_avg = response_sum /http_req_duration
                        # data_sent_avg = data_sent_sum / data_sent
                        # data_received_avg = data_received_sum / data_received
                        # vus_avg = vus_sum / vus
                        # error_rate_avg = error_rate_sum / error_rate                   
                        print(http_reqs)
                        print(http_req_duration)
                        print(data_sent)
                        print(data_received)
                        print(vus)
                        print(error_rate)                     
                        print(req_sum)
                        print(response_sum)
                        print(data_sent_sum)
                        print(data_received_sum) 
                        print(vus_sum)
                        print(error_rate_sum)
                        # print(req_avg)
                        # print(response_avg)
                        # print(data_sent_avg)
                        # print(data_received_avg) 
                        # print(vus_avg)
                        # print(error_rate_avg)               
                        print("%s: reqs/s: %0.3f  response time/s: %0.3f  Bytes IN/s: %0.3f  Bytes OUT/s: %0.3f vus/s: %0.3f  error_rate/s: %0.3f"  % ( datetime.datetime.now().strftime("%H:%M:%S"), http_reqs, http_req_duration, data_received, data_sent, vus, error_rate ))
                        info_message08 = {"%s: reqs/s: %0.3f  response time/s: %0.3f  Bytes IN/s: %0.3f  Bytes OUT/s: %0.3f vus/s: %0.3f  error_rate/s: %0.3f" % ( datetime.datetime.now().strftime("%H:%M:%S"), http_reqs, http_req_duration, data_received, data_sent, vus, error_rate )}
                        my_label16 = Label(performancetestScreen,text=info_message08)
                        my_label16.pack()
            
            #sleep(refresh_interval)
            except:
                
                req_avg = req_sum/ count
                response_avg = response_sum/count
                data_sent_avg = data_sent_sum / count
                data_received_avg = data_received_sum / count
                vus_avg = vus_sum / count
                error_rate_avg = error_rate_sum / count
                print(req_avg)
                print(response_avg)
                print(data_sent_avg)
                print(data_received_avg) 
                print(vus_avg)
                print(error_rate_avg)                    
                print("%s: Average reqs/s: %0.3f  Average response time/s: %0.3f  Average Bytes IN/s: %0.3f  Average Bytes OUT/s: %0.3f Average vus/s: %0.3f  Average error_rate/s: %0.3f"  % ( datetime.datetime.now().strftime("%H:%M:%S"), req_avg, response_avg, data_received_avg, data_sent_avg, vus_avg, error_rate_avg ))
                info_message06 = {"%s: Average reqs/s: %0.3f  Average response time/s: %0.3f  Average Bytes IN/s: %0.3f  Average Bytes OUT/s: %0.3f Average vus/s: %0.3f  Average error_rate/s: %0.3f"  % ( datetime.datetime.now().strftime("%H:%M:%S"), req_avg, response_avg, data_received_avg, data_sent_avg, vus_avg, error_rate_avg )}
                #print("%s: Average reqs/s: %0.1f  Average response time/s: %0.1f  Average Bytes IN/s: %0.1f  Average Bytes OUT/s: %0.1f Average vus/s: %0.1f  Average error_rate/s: %0.1f"  % ( datetime.datetime.now().strftime("%H:%M:%S"), req_sum, response_sum, data_received_sum, data_sent_sum, vus_sum, error_rate_sum ))
                #info_message06 = {"%s: Average reqs/s: %0.1f  Average response time/s: %0.1f  Average Bytes IN/s: %0.1f  Average Bytes OUT/s: %0.1f Average vus/s: %0.1f  Average error_rate/s: %0.1f"  % ( datetime.datetime.now().strftime("%H:%M:%S"), req_sum, response_sum, data_received_sum, data_sent_sum, vus_sum, error_rate_sum )}
                #print("%s: Average reqs/s: %0.1f  Average response time/s: %0.1f  Average Bytes IN/s: %0.1f  Average Bytes OUT/s: %0.1f "  % ( datetime.datetime.now().strftime("%H:%M:%S"), req_sum, response_sum, data_received_sum, data_sent_sum ))
                #info_message06 = {"%s: Average reqs/s: %0.1f  Average response time/s: %0.1f  Average Bytes IN/s: %0.1f  Average Bytes OUT/s: %0.1f "  % ( datetime.datetime.now().strftime("%H:%M:%S"), req_sum, response_sum, data_received_sum, data_sent_sum )}
                my_label17 = Label(performancetestScreen,text=info_message06)
                my_label17.pack()
                print("_________________________________________________________________________________________________________________________")
                info_message07 = "_________________________________________________________________________________________________________________________"
                my_label11 = Label(performancetestScreen,text=info_message07)
                my_label11.pack()
                
            con = sqlite3.connect('webpinginguserdata.db')
            cur = con.cursor()
            cur.execute(
                "INSERT INTO PerfTestResults (username, testedWebsite,http_reqs, http_req_duration, data_sent, data_received, vus, error_rate) VALUES (:username, :testedWebsite,:http_reqs, :http_req_duration, :data_sent, :data_received, :vus, :error_rate)",
                {
                    'username': username,
                    'testedWebsite': userPerformanceUrl.get(),
                    'http_reqs': req_avg,
                    'http_req_duration': response_avg,
                    'data_sent': data_sent_avg,
                    'data_received': data_received_avg,
                    'vus': vus_avg, 
                    'error_rate': error_rate_avg
                }
            )
            con.commit()
            con.close()
                    
            sleep(refresh_interval)
        
    
    def closePerformanceTestScreen():
        performancetestScreen.withdraw()
        screen.deiconify()
        #os.system("WebPingingLogin.py")

    performance_test_button = Button(performancetestScreen, text= "START THE TEST", fg = 'white', bg = 'red',height="2",width="20",font=("Aharoni",10,'bold'), command = performance_test,borderwidth=4)
    performance_test_button.pack(side = TOP, padx=7,pady=5)
    homeTest_button = Button(performancetestScreen, text="Home",bg='snow',height="2",width="20",font=("Aharoni",10,'bold'), command =closePerformanceTestScreen,borderwidth=4)
    homeTest_button.pack(side = TOP, padx=10,pady=7)#end
    
def performanceHistory_screen():
    global performanceHistoryScreen
    screen.withdraw()
    performanceHistoryScreen = Toplevel(screen)
    performanceHistoryScreen.title("Performance Test History Screen")
    performanceHistoryScreen.iconbitmap('webpinging.ico')
    performanceHistoryScreen.geometry("1000x500")
    performanceHistoryScreen.configure(bg='snow')
    Label(performanceHistoryScreen,text= sys.argv[1]+"'s Performance Test History", bg="thistle4",width="500",height="2", font=("Calibri",13,'bold')).pack()
    Label(performanceHistoryScreen,text="", bg='snow').pack()
    
    #table style
    style = ttk.Style()
    #table theme
    style.theme_use('default')
    #table color
    style.configure("Treeview",
                    background = '#D3D3D3',
                    foreground = 'black',
                    rowheight = 25,
                    fieldbackground = "D3D3D3")
    
    #on select color
    style.map("Treeview",
              background =[('selected', "#347083")])
    
    #frame for table
    table_frame = Frame(performanceHistoryScreen)
    table_frame.pack(pady=10)
    
    #scrollbar
    table_scroll = Scrollbar(table_frame)
    table_scroll.pack(side=RIGHT,fill=Y)
    table_scroll1 = Scrollbar(table_frame,orient='horizontal')
    table_scroll1.pack(side=BOTTOM,fill=X)
    
    #create table
    tree = ttk.Treeview(table_frame,yscrollcommand=table_scroll.set,xscrollcommand=table_scroll1.set,selectmode="extended")
    tree.pack()
    
    #scrollbar function
    table_scroll.config(command=tree.yview)
    table_scroll1.config(command=tree.xview)
    #define column
    tree['column'] = ("No.","Username","Website","Average HTTP Request/s","Average response time","Average Data Sent/s","Average Data Received/s","Average Vus/s","Average Error Rate/s","Date & Time")
    
    #format column
    tree.column("#0", width=0, stretch=NO)
    tree.column("No.", anchor=W, width=140)
    tree.column("Username", anchor=W, width=140)
    tree.column("Website", anchor=CENTER, width=140)
    tree.column("Average HTTP Request/s", anchor=CENTER, width=140)
    tree.column("Average response time", anchor=CENTER, width=140)
    tree.column("Average Data Sent/s", anchor=CENTER, width=140)
    tree.column("Average Data Received/s", anchor=CENTER, width=140)
    #tree.column("Average Data Sent/s", anchor=CENTER, width=140)
    tree.column("Average Vus/s", anchor=CENTER, width=140)
    tree.column("Average Error Rate/s", anchor=CENTER, width=140)
    tree.column("Date & Time", anchor=CENTER, width=140)
    
    #heading
    tree.heading("#0", text="", anchor=W)
    tree.heading("No.", text="No.", anchor=W)
    tree.heading("Username", text="Username", anchor=W)
    tree.heading("Website", text="Website", anchor=CENTER)
    tree.heading("Average HTTP Request/s", text="Average HTTP Request/s", anchor=CENTER)
    tree.heading("Average response time", text="Average response time", anchor=CENTER)
    tree.heading("Average Data Sent/s", text="Average Data Sent/s", anchor=CENTER)
    tree.heading("Average Data Received/s", text="Average Data Received/s", anchor=CENTER)
    #tree.heading("Average Data Sent/s", text="Average Data Sent/s", anchor=CENTER)
    tree.heading("Average Vus/s", text="Average Vus/s", anchor=CENTER)
    tree.heading("Average Error Rate/s", text="Average error_rate/s", anchor=CENTER)
    tree.heading("Date & Time", text="Date & Time", anchor=CENTER)
    
    #stripping
    tree.tag_configure('oddrow', background="white")
    tree.tag_configure('evenrow', background="lightblue")
    
    con = sqlite3.connect('webpinginguserdata.db')
    cur = con.cursor()
    cur.execute( "SELECT * FROM PerfTestResults WHERE username= :username", {'username': username})
    rows = cur.fetchall()
    
    global count
    count = 0
    
    for row in rows:
        if count % 2 == 0:
            tree.insert(parent='', index='end', iid=count, text='', values=(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9]),tags=('evenrow',))
        else:
            tree.insert(parent='', index='end', iid=count, text='', values=(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9]),tags=('oddrow',))
        count += 1
    con.commit()
    con.close()
    
    def closeTestScreen():
        performanceHistoryScreen.withdraw()
        testScreen.deiconify()
        #os.system("WebPingingLogin.py")
    homeTest_button = Button(performanceHistoryScreen, text="Back",bg='thistle4',height="2",width="30",font=("Aharoni",10,'bold'), command =closeTestScreen)
    homeTest_button.pack(side = TOP, padx=10,pady=7)   
    # Label(performanceHistoryScreen,text="Created by Gauthaman & James Chia",fg='black',bg ='thistle4',font=("Calibri",10)).place(x=0,y=480)
    # Label(performanceHistoryScreen,text="© 2021 WebPinging All Rights Reserved",fg='black',bg ='thistle4',font=("Calibri",10)).place(x=1318,y=480)
    

    

def loadHistory_screen():
    global loadHistoryScreen
    screen.withdraw()
    loadHistoryScreen = Toplevel(screen)
    loadHistoryScreen.title("Load Test History Screen")
    loadHistoryScreen.iconbitmap('webpinging.ico')
    loadHistoryScreen.geometry("1000x500")
    loadHistoryScreen.configure(bg='snow')
    Label(loadHistoryScreen,text= sys.argv[1]+"'s Load Test History", bg="thistle4",width="500",height="2", font=("Calibri",13,'bold')).pack()
    Label(loadHistoryScreen,text="", bg='snow').pack()
    
    #table style
    style = ttk.Style()
    #table theme
    style.theme_use('default')
    #table color
    style.configure("Treeview",
                    background = '#D3D3D3',
                    foreground = 'black',
                    rowheight = 25,
                    fieldbackground = "D3D3D3")
    
    #on select color
    style.map("Treeview",
              background =[('selected', "#347083")])
    
    #frame for table
    table_frame = Frame(loadHistoryScreen)
    table_frame.pack(pady=10)
    
    #scrollbar
    table_scroll = Scrollbar(table_frame)
    table_scroll.pack(side=RIGHT,fill=Y)
    table_scroll1 = Scrollbar(table_frame,orient='horizontal')
    table_scroll1.pack(side=BOTTOM,fill=X)
    #create table
    tree = ttk.Treeview(table_frame,yscrollcommand=table_scroll.set,xscrollcommand=table_scroll1.set,selectmode="extended")
    tree.pack()
    
    #scrollbar function
    table_scroll.config(command=tree.yview)
    table_scroll1.config(command=tree.xview)
    
    #define column
    tree['column'] = ("No.","Username","Website","HTTP Request/s","Iterations/s","Data Sent/s","Data Received/s","Date & Time")
    
    #format column
    tree.column("#0", width=0, stretch=NO)
    tree.column("No.", anchor=W, width=140)
    tree.column("Username", anchor=W, width=140)
    tree.column("Website", anchor=CENTER, width=140)
    tree.column("HTTP Request/s", anchor=CENTER, width=140)
    tree.column("Iterations/s", anchor=CENTER, width=140)
    tree.column("Data Sent/s", anchor=CENTER, width=140)
    tree.column("Data Received/s", anchor=CENTER, width=140)
    tree.column("Date & Time", anchor=CENTER, width=140)
    
    #heading
    tree.heading("#0", text="", anchor=W)
    tree.heading("No.", text="No.", anchor=W)
    tree.heading("Username", text="Username", anchor=W)
    tree.heading("Website", text="Website", anchor=CENTER)
    tree.heading("HTTP Request/s", text="HTTP Request/s", anchor=CENTER)
    tree.heading("Iterations/s", text="Iterations/s", anchor=CENTER)
    tree.heading("Data Sent/s", text="Data Sent/s", anchor=CENTER)
    tree.heading("Data Received/s", text="Data Received/s", anchor=CENTER)
    tree.heading("Date & Time", text="Date & Time", anchor=CENTER)
    
    #stripping
    tree.tag_configure('oddrow', background="white")
    tree.tag_configure('evenrow', background="lightblue")
    
    con = sqlite3.connect('webpinginguserdata.db')
    cur = con.cursor()
    cur.execute( "SELECT * FROM LoadTestResults WHERE username= :username", {'username': username})
    rows = cur.fetchall()
    
    global count
    count = 0
    
    for row in rows:
        if count % 2 == 0:
            tree.insert(parent='', index='end', iid=count, text='', values=(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7]),tags=('evenrow',))
        else:
            tree.insert(parent='', index='end', iid=count, text='', values=(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7]),tags=('oddrow',))
        count += 1
    con.commit()
    con.close()
    
    def closeTestScreen():
        loadHistoryScreen.withdraw()
        testScreen.deiconify()
        #os.system("WebPingingLogin.py")
    homeTest_button = Button(loadHistoryScreen, text="Back",bg='thistle4',height="2",width="30",font=("Aharoni",10,'bold'), command =closeTestScreen)
    homeTest_button.pack(side = TOP, padx=10,pady=7)   
    # Label(loadHistoryScreen,text="Created by Gauthaman & James Chia",fg='black',bg ='thistle4',font=("Calibri",10)).place(x=0,y=480)
    # Label(loadHistoryScreen,text="© 2021 WebPinging All Rights Reserved",fg='black',bg ='thistle4',font=("Calibri",10)).place(x=975,y=480)  

def functionalHistory_screen():
    global functionalHistoryscreen
    testScreen.withdraw()
    functionalHistoryscreen = Toplevel(screen)
    functionalHistoryscreen.title("Functionality Test History Screen")
    functionalHistoryscreen.iconbitmap('webpinging.ico')
    functionalHistoryscreen.geometry("1000x500")
    functionalHistoryscreen.configure(bg='snow')
    Label(functionalHistoryscreen,text= sys.argv[1]+"'s Functionality Test History", bg="thistle4",width="500",height="2", font=("Calibri",13,'bold')).pack()
    Label(functionalHistoryscreen,text="", bg='snow').pack()
    
    #table style
    style = ttk.Style()
    #table theme
    style.theme_use('default')
    #table color
    style.configure("Treeview",
                    background = '#D3D3D3',
                    foreground = 'black',
                    rowheight = 25,
                    fieldbackground = "D3D3D3")
    
    #on select color
    style.map("Treeview",
              background =[('selected', "#347083")])
    
    #frame for table
    table_frame = Frame(functionalHistoryscreen)
    table_frame.pack(pady=10)
    
    #scrollbar
    table_scroll = Scrollbar(table_frame)
    table_scroll.pack(side=RIGHT,fill=Y)
    
    #create table
    tree = ttk.Treeview(table_frame,yscrollcommand=table_scroll.set,selectmode="extended")
    tree.pack()
   
    #scrollbar function
    table_scroll.config(command=tree.yview)
    
    #define column
    tree['column'] = ("No.","Username","Website","HTTP Result","Time Taken","Date")
    
    #format column
    tree.column("#0", width=0, stretch=NO)
    tree.column("No.", anchor=W, width=140)
    tree.column("Username", anchor=W, width=140)
    tree.column("Website", anchor=CENTER, width=140)
    tree.column("HTTP Result", anchor=CENTER, width=140)
    tree.column("Time Taken", anchor=CENTER, width=140)
    tree.column("Date", anchor=CENTER, width=140)
    
    #heading
    tree.heading("#0", text="", anchor=W)
    tree.heading("No.", text="No.", anchor=W)
    tree.heading("Username", text="Username", anchor=W)
    tree.heading("Website", text="Website", anchor=CENTER)
    tree.heading("HTTP Result", text="HTTP Result", anchor=CENTER)
    tree.heading("Time Taken", text="Time Taken /s", anchor=CENTER)
    tree.heading("Date", text="Date", anchor=CENTER)
    
    #stripping
    tree.tag_configure('oddrow', background="white")
    tree.tag_configure('evenrow', background="lightblue")
    
    #data
    con = sqlite3.connect('webpinginguserdata.db')
    cur = con.cursor()
    cur.execute( "SELECT * FROM FunctionalityTestResults WHERE username= :username", {'username': username})
    rows = cur.fetchall()
    
    global count
    count = 0
    
    for row in rows:
        if count % 2 == 0:
            tree.insert(parent='', index='end', iid=count, text='', values=(row[0],row[1],row[2],row[3],row[4],row[5]),tags=('evenrow',))
        else:
            tree.insert(parent='', index='end', iid=count, text='', values=(row[0],row[1],row[2],row[3],row[4],row[5]),tags=('oddrow',))
        count += 1
    con.commit()
    con.close() 
    
    def closeTestScreen():
        functionalHistoryscreen.withdraw()
        testScreen.deiconify()
        #os.system("WebPingingLogin.py")
    homeTest_button = Button(functionalHistoryscreen, text="Back",bg='thistle4',height="2",width="30",font=("Aharoni",10,'bold'), command =closeTestScreen)
    homeTest_button.pack(side = TOP, padx=10,pady=7)   
    # Label(functionalHistoryscreen,text="Created by Gauthaman & James Chia",fg='black',bg ='thistle4',font=("Calibri",10)).place(x=0,y=480)
    # Label(functionalHistoryscreen,text="© 2021 WebPinging All Rights Reserved",fg='black',bg ='thistle4',font=("Calibri",10)).place(x=779,y=480)    
    
def test_screen():
    global testScreen
    screen.withdraw()
    testScreen = Toplevel(screen)
    testScreen.title("Test Report")
    testScreen.iconbitmap('webpinging.ico')
    testScreen.geometry("500x500")
    testScreen.configure(bg='snow') 
    Label(testScreen,text="View History of Your Tests", bg="thistle4",width="500",height="2", font=("Calibri",13)).pack()
    Label(testScreen,text="", bg='snow').pack()
    
    def closeTestScreen():
        testScreen.withdraw()
        screen.deiconify()
    
    Label(testScreen, text="", bg='snow').pack()
    Button(testScreen,text="Performance Test History",bg='light green',height="2",width="30",font=("Aharoni",10,'bold'),command=performanceHistory_screen,borderwidth=4).pack()
    Label(testScreen,text="", bg='snow').pack()
    Button(testScreen,text="Load Test History",bg='light blue',height="2",width="30",font=("Aharoni",10,'bold'),command=loadHistory_screen,borderwidth=4).pack()
    Label(testScreen,text="", bg='snow').pack()
    Button(testScreen,text="Functional Test History",bg='light yellow',height="2",width="30",font=("Aharoni",10,'bold'),command=functionalHistory_screen,borderwidth=4).pack()
    Label(testScreen,text="", bg='snow').pack()
    homeTest_button = Button(testScreen, text="Back",bg='thistle4',height="2",width="30",font=("Aharoni",10,'bold'), command =closeTestScreen)
    homeTest_button.pack(side = TOP, padx=10,pady=7)     
    Label(testScreen,text="Created by Gauthaman & James Chia",fg='black',bg ='thistle4',font=("Calibri",10)).place(x=0,y=480)
    Label(testScreen,text="© 2021 WebPinging All Rights Reserved",fg='black',bg ='thistle4',font=("Calibri",10)).place(x=278,y=480)
    
def logout():
    screen.withdraw()
    from subprocess import call
    call(["python","WebPingingLogin.py"])    

def main_screen():
    global screen
    #startScreen.withdraw()
    screen = Tk()
    screen.title('WebPinging Premium')
    screen.iconbitmap('webpinging.ico')
    screen.geometry("500x500")
    screen.configure(bg='snow')        
    
    Label(text="",bg='snow').pack()
    image = PhotoImage(file='D:\WebPinging System\WebPingingLogo.png')   
    Lab = Label(text="Welcome to WebPinging System")
    Lab.pack()
    Lab["image"] = image
    # Label(text="Welcome to WebPinging System", bg="thistle4",width="500",height="2", font=("Calibri",13)).pack()
    # Label(text="", bg='snow').pack()
    Label(text="Welcome "+sys.argv[1],font=("Aharoni",10,'bold'),bg='snow').pack()
    Label(text="",bg='snow').pack()
    Button(text="Premium Functional Testing",height="2",width="30",bg ='thistle4',font=("Aharoni",9,'bold'), command = start,borderwidth=4).pack()
    Label(text="",bg='snow').pack()
    Button(text="Performance Testing",height="2",width="30",bg ='thistle4',font=("Aharoni",9,'bold'),command=performancetest_screen,borderwidth=4).pack()
    Label(text="",bg='snow').pack()
    Button(text="Load Testing",height="2",width="30",bg ='thistle4',font=("Aharoni",9,'bold'),command=loadtest_screen,borderwidth=4).pack()
    Label(text="",bg='snow').pack()
    Button(text="View Test Report",height="2",width="30",bg ='thistle4',font=("Aharoni",9,'bold'),command=test_screen,borderwidth=4).pack()
    Label(text="",bg='snow').pack()
    Button(text="Log Out",fg = 'white', bg = 'red',height="2",width="30",font=("Aharoni",9,'bold'), command= logout,borderwidth=4).pack()
    Label(text="Created by Gauthaman & James Chia",fg='black',bg ='thistle4',font=("Calibri",10)).place(x=0,y=480)
    Label(text="© 2021 WebPinging All Rights Reserved",fg='black',bg ='thistle4',font=("Calibri",10)).place(x=278,y=480)
    screen.mainloop()

main_screen()