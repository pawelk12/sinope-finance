import tkinter
from tkinter import ttk

class LoginWidgets(ttk.Frame):
    def __init__(self,master):
        super().__init__(master)
        titleLabel = tkinter.Label(self, text="Login to your bank account",font=("Arial",20),bg="#F9F7E6")
        titleLabel.grid(row=0,column=2,columnspan=2,padx=20)

        usernameLabel = tkinter.Label(self,text="Username: ",width=20,bg="#F9F7E6")
        usernameLabel.grid(row=1,column=2)
        self.usernameEntry = tkinter.Entry(self)
        self.usernameEntry.grid(row=1,column=3)

        passwordLabel = tkinter.Label(self,text="Password: ",width=20,bg="#F9F7E6")
        passwordLabel.grid(row=2,column=2)
        self.passwordEntry = tkinter.Entry(self, show="*")
        self.passwordEntry.grid(row=2,column=3)

        loginButton = tkinter.Button(self, text="Login",command=self.Login)
        loginButton.grid(row=3,column=2,columnspan=2)
        registerButton = tkinter.Button(self, text="Register",command=self.Register)
        registerButton.grid(row=4,column=2,columnspan=2)

        self.statusLabel = tkinter.Label(self,bg="#F9F7E6")
        self.statusLabel.grid(row=5,column=2,columnspan=2,padx=20)

        self.pack(expand = True)



    def Login(self):
        data_from_file = []

        try:
            with open('data.txt') as file:
                for line in file:
                    data_from_file.append(line.strip("\n"))
                if(data_from_file and self.usernameEntry.get()==data_from_file[0] and self.passwordEntry.get()==data_from_file[1]):
                    self.statusLabel.config(text="Login was successful",fg = 'green')
                    self.destroy()
                    # check if personal details are written to file
                    if(len(data_from_file)>=3):
                        #just for test
                        print("Welcome")
                    else:
                        self.master.runPersonalDetails()
                else:
                    self.statusLabel.config(text="Wrong username or password",fg = 'red')
                    self.usernameEntry.delete(0, tkinter.END)
                    self.passwordEntry.delete(0, tkinter.END)
        except FileNotFoundError:
            print("file not found")

    #To add: epmty strings check
    def Register(self):
        data_to_file = []

        try:
            with open('data.txt') as file:
                for line in file:
                    data_to_file.append(line.strip("\n"))
            if(not data_to_file):
                try:
                    with open('data.txt', 'w') as file:
                        file.write(self.usernameEntry.get() + "\n")
                        file.write(self.passwordEntry.get() + "\n")
                        self.statusLabel.config(text="Registration was successful. Log in",fg = 'green')
                        self.usernameEntry.delete(0, tkinter.END)
                        self.passwordEntry.delete(0, tkinter.END)
                except FileNotFoundError:
                    print("file not found")
            elif(self.usernameEntry.get()!=data_to_file[0]):
                try:
                    with open('data.txt', 'w') as file:
                        file.write(self.usernameEntry.get() + "\n")
                        file.write(self.passwordEntry.get() + "\n")
                        self.statusLabel.config(text="Registration was successful. Log in",fg = 'green')
                        self.usernameEntry.delete(0, tkinter.END)
                        self.passwordEntry.delete(0, tkinter.END)
                except FileNotFoundError:
                    print("file not found")
            else:
                self.statusLabel.config(text="Username is already in use",fg = 'red')
                self.usernameEntry.delete(0, tkinter.END)
                self.passwordEntry.delete(0, tkinter.END)
        except FileNotFoundError:
            print("file not found")