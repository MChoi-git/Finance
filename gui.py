from tkinter import *
from tkinter import ttk
import time

def startLogin(realUser, realPwd):
    #Event handlers
    def close():
        root.destroy()
    def mouseClick():
            print("Logging in...")
            userInput = loginScreen.userInput.get()
            pwdInput = loginScreen.pwdInput.get()
            print(f"USER:{userInput}")
            print(f"PASSWORD:{pwdInput}")
            if realUser == userInput and realPwd == pwdInput:
                print("GUI:Login successfu1.")
                loginScreen.loginTry = (True)
                close()
            else:
                print("GUI:Login unsuccessful. Please try again.")

    #Login window initialization
    class Login:
        def __init__(self, master):
            #Initialize tkinter
            self.master = master
            master.title("Login")
            self.loginTry = False

            #Initialize window variables
            self.userInput = StringVar(master,'')
            self.pwdInput = StringVar(master,'')
            
            #Setup UI widgets
            #Labels
            self.username = Label(master, text="Username")
            self.username.place(x=40, y=60)
            self.pwd = Label(master, text="Password")
            self.pwd.place(x=40, y=100)
            
            #Buttons
            self.loginButton = Button(master, text="Login", command=mouseClick)
            self.loginButton.place(x=40,y=140)
            self.usernameInput = Entry(master, width=30, textvariable = self.userInput)
            self.usernameInput.place(x=110, y=60)
            self.passwordInput = Entry(master, width=30, textvariable = self.pwdInput)  
            self.passwordInput.place(x=110, y=100)
            
            #Event bindings
            #self.loginButton.bind("<Button>", mouseClick)   
    
    #Start the window loop
    root = Tk()
    root.geometry('500x500')
    loginScreen = Login(root)
    root.mainloop()
    return loginScreen.loginTry

