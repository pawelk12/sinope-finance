from tkinter import *
from time import *
import os



def update():
    time_str = strftime("%H:%M:%S   %d-%m-%Y")
    timeLabel.config(text=time_str)
    timeLabel.after(1000,update)

def createMainWindow():
    mainWindow = Tk()
    mainWindow.title("Bank App")
    mainWindow.geometry("800x600")
    mainWindow.config(background="#F9F7E6")

    global timeLabel
    timeLabel = Label(mainWindow,font=('Arial',20),fg="black",bg="#F9F7E6")
    timeLabel.grid(row=0,column=3)

    #labels and buttons

    update()
    mainWindow.mainloop()


     

def Login():
    data_from_file = []
    username = usernameEntry.get()
    password = passwordEntry.get()

    try:
        with open('login_data.txt') as file:
            for line in file:
                data_from_file.append(line.strip("\n"))
            if(username==data_from_file[0] and password==data_from_file[1]):
                    statusLabel.config(text="Login was successful",fg = 'green')
                    loginWindow.destroy()
                    createMainWindow()

            else:
                    statusLabel.config(text="Wrong username or password",fg = 'red')
                    usernameEntry.delete(0, END)
                    passwordEntry.delete(0, END)
    except FileNotFoundError:
        print("file not found")

def Register():
    data_to_file = []
    username = usernameEntry.get()
    password = passwordEntry.get()

    try:
        with open('login_data.txt') as file:
            for line in file:
                data_to_file.append(line.strip("\n"))
        if(username!=data_to_file[0]):
            with open('login_data.txt', 'w') as file:
                file.write(username)
                file.write("\n")
                file.write(password)
                statusLabel.config(text="Registration was successful. Log in",fg = 'green')
                usernameEntry.delete(0, END)
                passwordEntry.delete(0, END)
        else:
                statusLabel.config(text="Username is already in use",fg = 'red')
                usernameEntry.delete(0, END)
                passwordEntry.delete(0, END)
    except FileNotFoundError:
        print("file not found")


loginWindow = Tk()

loginWindow.geometry("370x180")
loginWindow.title("login")
loginWindow.config(background="#F9F7E6")

titleLabel = Label(loginWindow, text="Login to your bank account",font=("Arial",20),bg="#F9F7E6")
titleLabel.grid(row=0,column=2,columnspan=2,padx=20)

usernameLabel = Label(loginWindow,text="Username: ",width=20,bg="#F9F7E6")
usernameLabel.grid(row=1,column=2)
usernameEntry = Entry(loginWindow)
usernameEntry.grid(row=1,column=3)

passwordLabel = Label(loginWindow,text="Password: ",width=20,bg="#F9F7E6")
passwordLabel.grid(row=2,column=2)
passwordEntry = Entry(loginWindow, show="*")
passwordEntry.grid(row=2,column=3)

loginButton = Button(loginWindow, text="Login",command=Login)
loginButton.grid(row=3,column=2,columnspan=2)
registerButton = Button(loginWindow, text="Register",command=Register)
registerButton.grid(row=4,column=2,columnspan=2)

statusLabel = Label(loginWindow,bg="#F9F7E6")
statusLabel.grid(row=5,column=2,columnspan=2,padx=20)


loginWindow.mainloop()