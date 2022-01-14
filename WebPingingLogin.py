from tkinter import *
from tkinter import messagebox
from tkinter import Image
import sqlite3
from tkinter import font
import requests
import time
import os


con = sqlite3.connect('webpinginguserdata.db')
cur = con.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS record(
                    username text, 
                    password text,
                    email text, 
                    company text
                    
                )
            ''')
con.commit()
con.close()


def insert_user():
    check_counter=0
    warn = ""
    if username_entry.get() == "":
        warn = "Name can't be empty"
    else:
        check_counter +=1
    
    if password_entry.get() == "":
        warn = "Password can't be empty"
    else:
        check_counter +=1
    
    if email_entry.get() == "":
        warn = "Email can't be empty"
    else:
        check_counter +=1
    
    if company_entry.get() == "":
        warn = "Please enter your company name"
    else:
        check_counter +=1    
    
    if check_counter == 4:
        with sqlite3.connect('webpinginguserdata.db') as db:
            con = db.cursor()
        find_user = ('SELECT username FROM record WHERE username = ?')
        con.execute(find_user,[username_entry.get()])
        if con.fetchall():
            messagebox.showerror('Error','Username has been taken, try a different username.')
        else:
            try:
                con = sqlite3.connect('webpinginguserdata.db')
                cur = con.cursor()
                cur.execute("INSERT INTO record VALUES (:username,:password,:email, :company)", {
                                        'username': username_entry.get(),
                                        'password': password_entry.get(),
                                        'email': email_entry.get(),
                                        'company': company_entry.get()
                })
                con.commit()
                messagebox.showinfo('confirmation', 'Registration Successful')
            except Exception as ep:
                messagebox.showerror('', ep)
    else:
        messagebox.showerror('Error', warn) 

def login_response():
    try:
        con = sqlite3.connect('webpinginguserdata.db')
        c = con.cursor()
        
        find_user = ('SELECT * FROM record WHERE username = ? and password = ?')
        c.execute(find_user,[username_entry1.get(),password_entry1.get()])
        result = c.fetchall()
        # for row in c.execute("Select * from record"):
        #     username = row[0]
        #     pwd = row[1]
    except Exception as ep:
        messagebox.showerror('',ep)
    
    uname = username_entry1.get()
    upwd = password_entry1.get()
    check_counter =0
    if uname == "":
        warn = "Username can't be empty"
    else:
        check_counter +=1
    if upwd == "":
        warn = "Password can't be empty"
    else:
        check_counter +=1
    if (uname == "" and upwd == ""):
        warn = "Username and Password can't be empty"
    else:
        check_counter +=1
    if check_counter == 3:
            if result:
                messagebox.showinfo('Login Status', username_entry1.get() +'\n Logged in Successfully!')
                loginScreen.withdraw()
                from subprocess import call
                call(["python","WebPingingPremium.py", uname ])
                
                
            else:
                    messagebox.showerror('Login Status', 'invalid username or password')
    else:
        messagebox.showerror('',warn)
        

    
def register():
    global registerScreen
    screen.withdraw()
    registerScreen = Toplevel(screen)
    registerScreen.title("WebPinging Register")
    registerScreen.iconbitmap('webpinging.ico')
    registerScreen.geometry("500x500")
    registerScreen.configure(bg='snow') 
    Label(registerScreen,text="WebPinging System Register", bg="thistle4",width="500",height="2", font=("Calibri",13,'bold')).pack()
    Label(registerScreen,text="").pack()
    
    global username
    global password
    global email
    global company
    global username_entry
    global password_entry
    global email_entry
    global company_entry
    username = StringVar()
    password = StringVar()
    email = StringVar()
    company = StringVar()
    
    def closeTestScreen():
        registerScreen.withdraw()
        screen.deiconify()
        #os.system("WebPingingLogin.py")
    
    Label(registerScreen,text="Please enter the following details",bg='snow', font=("Calibri",13,'bold')).pack()
    Label(registerScreen,text="",bg='snow').pack()
    
    Label(registerScreen,text="Username *",bg='snow',font=("Aharoni",13,'bold')).pack()
    username_entry = Entry(registerScreen,textvariable = username,width="50",borderwidth=4)
    username_entry.pack()
    
    Label(registerScreen,text="Password *",bg='snow',font=("Aharoni",13,'bold')).pack()
    password_entry = Entry(registerScreen,show="*",textvariable = password,width="50",borderwidth=4 )
    password_entry.pack()
    
    Label(registerScreen,text="Email *",bg='snow',font=("Aharoni",13,'bold')).pack()
    email_entry = Entry(registerScreen,textvariable = email,width="50",borderwidth=4)
    email_entry.pack()
    
    Label(registerScreen,text="Company *",bg='snow',font=("Aharoni",13,'bold')).pack()
    company_entry = Entry(registerScreen,textvariable = company,width="50",borderwidth=4)
    company_entry.pack()
    Label(registerScreen,text="",bg='snow').pack()
    registerButton=Button(registerScreen, text = "Register",bg='lightgreen', width="20",height="2",command= insert_user,borderwidth=4)
    registerButton.pack()
    Label(registerScreen,text="",bg='snow').pack()
    homeTest_button=Button(registerScreen, text = "Back to Home",bg='lightblue', width="20",height="2",command =closeTestScreen,borderwidth=4)
    homeTest_button.pack(side = TOP, padx=7,pady=7)
    Label(registerScreen,text="Created by Gauthaman & James Chia",fg='black',bg ='thistle4',font=("Calibri",10)).place(x=0,y=480)
    Label(registerScreen,text="© 2021 WebPinging All Rights Reserved",fg='black',bg ='thistle4',font=("Calibri",10)).place(x=278,y=480)
    
    
def login():
    global loginScreen
    screen.withdraw()
    loginScreen = Toplevel(screen)
    loginScreen.title("WebPinging Login")
    loginScreen.iconbitmap('webpinging.ico')
    loginScreen.geometry("500x500")
    loginScreen.configure(bg='snow') 
    #Label(loginScreen,text="WebPinging System", bg="grey",width="500",height="2", font=("Calibri",13)).pack()
    #Label(loginScreen,text="").pack()
    Label(loginScreen,text="WebPinging System Login", bg="thistle4",width="500",height="2", font=("Calibri",13,'bold')).pack()
    Label(loginScreen,text="", bg='snow').pack()
    Label(loginScreen,text="").pack()
    #Label(loginScreen,text="").pack()
    Label(loginScreen,text="Please enter your login details",bg='snow', font=("Calibri",13,'bold')).pack()
    Label(loginScreen,text="",bg='snow').pack()
    
    global username_verify
    global password_verify
    
    username_verify = StringVar()
    password_verify = StringVar()
    
    global username_entry1
    global password_entry1
    
    def closeTestScreen():
        loginScreen.withdraw()
        
        # os.chdir("D:\WebPinging System")
        # os.system('python3' +filename)
        screen.deiconify()
        #os.system("WebPingingLogin.py")
    
    Label(loginScreen,text="Username *",bg='snow', font=("Aharoni",13,'bold')).pack()
    username_entry1 = Entry(loginScreen,width="40", textvariable = username_verify,borderwidth=4)
    username_entry1.pack()
    Label(loginScreen,text="",bg='snow').pack()
    Label(loginScreen,text="Password *",bg='snow', font=("Aharoni",13,'bold')).pack()
    password_entry1 = Entry(loginScreen,show="*",width="40", textvariable = password_verify,borderwidth=4)
    password_entry1.pack()
    Label(loginScreen,text="",bg='snow').pack()
   
    loginButton = Button(loginScreen, text="Login",height="2",width="20",bg='lightgreen',font=("Aharoni",10,'bold') ,command=login_response,borderwidth=4)
    loginButton.pack(side=TOP,padx=7,pady=7)
    homeTest_button = Button(loginScreen, text="Home",bg='lightblue',fg='black',height="2",width="20",font=("Aharoni",10,'bold'), command =closeTestScreen,borderwidth=4)
    homeTest_button.pack(side = TOP, padx=7,pady=7)
    Label(loginScreen,text="Created by Gauthaman & James Chia",fg='black',bg ='thistle4',font=("Calibri",10)).place(x=0,y=480)
    Label(loginScreen,text="© 2021 WebPinging All Rights Reserved",fg='black',bg ='thistle4',font=("Calibri",10)).place(x=278,y=480)
    


def start():
    global startScreen
    labelhttp = Label
    screen.withdraw()
    userUrl = StringVar()
    #labelhttp = StringVar()
    startScreen = Toplevel(screen)
    startScreen.title("Basic Functional Testing")
    startScreen.iconbitmap('webpinging.ico')
    startScreen.geometry("500x500")
    startScreen.configure(bg='snow') 
    
    Label(text="",bg='snow').pack()
    my_label=Label(startScreen,text="WebPinging System Functional Testing", bg="thistle4",width="500",height="2", font=("Calibri",13,'bold'))
    my_label.pack(pady=5)
    Label(text="", bg='snow').pack()
    my_label2 = Label(startScreen, text= "Here we have our URL HTTP test function for you to try out.",bg='snow')
    my_label2.pack(pady=5)
    Label(startScreen,text="",bg='snow').pack()
    # my_label3 = Label(startScreen, text= "Test Your Website Performance Here NOW! Enter Your URL to Get Started and See the Results!",bg='snow')
    # my_label3.pack(pady=5)

    test_entry = Entry(startScreen,textvariable=userUrl, width = 50,borderwidth=4)
    test_entry.pack(pady=5)
    Label(startScreen,text="",bg='snow').pack()
    
    def closeTestScreen():
        startScreen.withdraw()
        screen.deiconify()
        #os.system("WebPingingLogin.py")
    
    
        
    def statusCode():
        start = time.time()
        response = requests.get(userUrl.get())
        response.status_code
        end = time.time()
        #response.status_code == requests.codes.ok
        if response.status_code == 200:
            result = userUrl.get()
            time1 = str(end - start)
            messagebox.showinfo("Result","The http status result for "+result+" "+"\n is 200 'All OK'"+"\n Time taken (/s): "+time1)
            #my_label = Label(startScreen,text="The http status result for "+result+" "+"\n is 200 'All OK'")
            #my_label.pack()
            # my_label5 = Label(startScreen,text="%s: Time taken (/s): %0.3f ")
            # my_label5.pack()
            # my_label8 = Label(startScreen,text=time1)
            # my_label8.pack()
            
        elif response.status_code == 301:
            result = userUrl.get()
            time1 = str(end - start)
            messagebox.showinfo("Result","The http status result for "+result+" "+"\n is 301 'Moved Permanently'"+"\n Time taken (/s): "+time1)
            # my_label = Label(startScreen,text="The http status result for "+result+" "+"\n is 301 'Moved Permanently'")
            # my_label.pack()
            #messagebox.showinfo("Status",'301 Moved Permanently')
            # my_label5 = Label(startScreen,text="Time taken (/s): ")
            # my_label5.pack()
            # my_label8 = Label(startScreen,text=time1)
            # my_label8.pack()

        elif response.status_code == 302:
            result = userUrl.get()
            time1 = str(end - start)
            messagebox.showinfo("Result","The http status result for "+result+" "+"\n is 302 'Moved Temporarily'"+"\n Time taken (/s): "+time1)
            # my_label = Label(startScreen,text="The http status result for "+result+" "+"\n is 302 'Moved Temporarily'")
            # my_label.pack()
            #messagebox.showinfo("Status",'302 Moved Temporarily')
            # my_label5 = Label(startScreen,text="Time taken (/s): ")
            # my_label5.pack()
            # my_label8 = Label(startScreen,text=time1)
            # my_label8.pack()
            #labelhttp = Label(startScreen, text="Status Code 302: Moved Temporarily",bg='snow')#.pack()
            #labelhttp.pack()
        elif response.status_code == 403:
            result = userUrl.get()
            time1 = str(end - start)
            messagebox.showinfo("Result","The http status result for "+result+" "+"\n is 403 'Forbidden'"+"\n Time taken (/s): "+time1)
            # my_label = Label(startScreen,text="The http status result for "+result+" "+"\n is 403 'Forbidden'")
            # my_label.pack()
            # my_label5 = Label(startScreen,text="Time taken (/s): ")
            # my_label5.pack()
            # my_label8 = Label(startScreen,text=time1)
            # my_label8.pack()

        elif response.status_code == 404:
            result = userUrl.get()
            time1 = str(end - start)
            messagebox.showinfo("Result","The http status result for "+result+" "+"\n is 404 'Not Found'"+"\n Time taken (/s): "+time1)
            # my_label = Label(startScreen,text="The http status result for "+result+" "+"\n is 404 'Not Found'")
            # my_label.pack()
            # my_label5 = Label(startScreen,text="Time taken (/s): ")
            # my_label5.pack()
            # my_label8 = Label(startScreen,text=time1)
            # my_label8.pack()

        elif response.status_code == 500:
            result = userUrl.get()
            time1 = str(end - start)
            messagebox.showinfo("Result","The http status result for "+result+" "+"\n is 500 'Internal Server Error'"+"\n Time taken (/s): "+time1)
            # my_label = Label(startScreen,text="The http status result for "+result+" "+"\n is 500 'Internal Server Error'")
            # my_label.pack()
            #messagebox.showinfo("Status",'500 Internal Server Error')
            # my_label5 = Label(startScreen,text="Time taken (/s): ")
            # my_label5.pack()
            # my_label8 = Label(startScreen,text=time1)
            # my_label8.pack()

        elif response.status_code == 503:
            result = userUrl.get()
            time1 = str(end - start)
            messagebox.showinfo("Result","The http status result for "+result+" "+"\n is 503 'Service Unavailable'"+"\n Time taken (/s): "+time1)
            # my_label = Label(startScreen,text="The http status result for "+result+" "+"\n is 503 'Service Unavailable'")
            # my_label.pack()
            #messagebox.showinfo("Status",'503 Service Unavailable')
            # my_label5 = Label(startScreen,text="Time taken (/s): ")
            # my_label5.pack()
            # my_label8 = Label(startScreen,text=time1)
            # my_label8.pack()



    #if len(test_entry.get()) == 0:
        #labelhttp = Label(startScreen, text="umbe",bg='snow')#.pack()
        #labelhttp.pack()
        #messagebox.showinfo("Warning!", "Box is empty! Write something")
            
    def clear_text():
        test_entry.delete(0, END)
        #labelhttp.config(text = "")
        return None
    Label(startScreen,text="",bg='snow').pack()
    test_button = Button(startScreen, text= "START THE TEST", fg = 'white', bg = 'red',height="2",width="20",font=("Aharoni",10,'bold'), command =statusCode,borderwidth=4)
    test_button.pack(side = TOP, padx=7,pady=5)
    Label(startScreen,text="",bg='snow').pack()
    #Label(text="",bg='snow').pack()
    #Label(text="", bg='snow').pack()
    #Label(text="", bg='snow').pack()
    clear_button = Button(startScreen, text="New Website", bg ='snow',height="2",width="20",font=("Aharoni",10,'bold'), command =clear_text,borderwidth=4)
    clear_button.pack(side = TOP, padx=7,pady=7)
    Label(startScreen,text="",bg='snow').pack()
    homeTest_button = Button(startScreen, text="Home",bg='lightblue',height="2",width="20",font=("Aharoni",10,'bold'), command =closeTestScreen,borderwidth=4)
    homeTest_button.pack(side = TOP, padx=7,pady=7)
    Label(startScreen,text="",bg='snow').pack()
    Label(startScreen,text="Created by Gauthaman & James Chia",fg='black',bg ='thistle4',font=("Calibri",10)).place(x=0,y=480)
    Label(startScreen,text="© 2021 WebPinging All Rights Reserved",fg='black',bg ='thistle4',font=("Calibri",10)).place(x=278,y=480)
    


def main_screen():
    global main_screen
    global screen
    #startScreen.withdraw()
    screen = Tk()
    screen.title('WebPinging Basic')
    screen.iconbitmap('webpinging.ico')
    screen.geometry("500x500")
    screen.configure(bg='snow')
            
    
    # Label(screen,image=logo)
    # Label.pack()
    Label(text="",bg='snow').pack()
    image = PhotoImage(file='D:\WebPinging System\WebPingingLogo.png')   
    Lab = Label(text="Welcome to WebPinging System")
    Lab.pack()
    Lab["image"] = image
    Label(text="",bg='snow').pack()
    Label(text="",bg='snow').pack()
    # Label(text="Welcome to WebPinging System", bg="thistle4",width="500",height="2", font=("Calibri",13)).pack()
    # Label(text="", bg='snow').pack()
    Button(text="Login as Premium User",height="2",width="30",bg ='thistle4',font=("Aharoni",9,'bold'),command = login, borderwidth=4).pack()
    Label(text="",bg='snow').pack()
    Button(text="Register to be Premium User",height="2",width="30",bg ='thistle4',font=("Aharoni",9,'bold'), command = register, borderwidth=4).pack()
    Label(text="",bg='snow').pack()
    Button(text="Click Here To Test Single URL",height="2",width="30",bg ='thistle4',font=("Aharoni",9,'bold'), command = start, borderwidth=4).pack()
    Label(text="",bg='snow').pack()
    #Button(text="View Test Report",height="2",width="30",command=test_screen).pack()
    #Label(text="",bg='snow').pack()
    Button(text="Exit to desktop",fg = 'white', bg = 'red',height="2",width="30",font=("Aharoni",9,'bold'), command= screen.destroy, borderwidth=4).pack()
    Label(text="",bg='snow').pack()
    Label(text="",bg='snow').pack()
    Label(text="",bg='snow').pack()
    Label(text="",bg='snow').pack()
    Label(text="Created by Gauthaman & James Chia",fg='black',bg ='thistle4',font=("Calibri",10)).place(x=0,y=480)
    Label(text="© 2021 WebPinging All Rights Reserved",fg='black',bg ='thistle4',font=("Calibri",10)).place(x=278,y=480)
    
    screen.mainloop()
    

main_screen()