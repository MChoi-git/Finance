from tkinter import *
from tkinter import ttk

class Login:
    def __init__(self, master):
        #Initialize tkinter
        self.master = master
        master.title("Login")
        
        self.username = Label(master, text="Username").place(x=40, y=60)
        self.pwd = Label(master, text="Password").place(x=40, y=100)
        self.loginButton = Button(master, text="Login").place(x=40,y=140)
        self.usernameInput = Entry(master, width=30).place(x=110, y=60)
        self.pwdInput = Entry(master, width=30).place(x=110, y=100)

