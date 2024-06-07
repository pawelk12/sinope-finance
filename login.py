import customtkinter as ctk
from db_service import Login as ReadFromDB
from db_service import GetData
import hashlib
from account import Account


class LoginWidgets(ctk.CTkFrame):
    def __init__(self,master):
        super().__init__(master)
        titleLabel = ctk.CTkLabel(self, text="Login to your bank account",font=("Arial",20))
        titleLabel.grid(row=0,column=2,columnspan=2,padx=20)

        usernameLabel = ctk.CTkLabel(self,text="Username: ",width=20)
        usernameLabel.grid(row=1,column=2)
        self.usernameEntry = ctk.CTkEntry(self)
        self.usernameEntry.grid(row=1,column=3)

        passwordLabel = ctk.CTkLabel(self,text="Password: ",width=20)
        passwordLabel.grid(row=2,column=2)
        self.passwordEntry = ctk.CTkEntry(self, show="*")
        self.passwordEntry.grid(row=2,column=3)

        loginButton = ctk.CTkButton(self, text="Login",command=self.Login)
        loginButton.grid(row=3,column=2,columnspan=2)

        self.statusLabel = ctk.CTkLabel(self, text="")
        self.statusLabel.grid(row=5,column=2,columnspan=2,padx=20)

        self.pack(expand = True)



    def Login(self):
        if(ReadFromDB(self.usernameEntry.get(), hashlib.sha256(self.passwordEntry.get().encode()).hexdigest())):
            data = GetData(ReadFromDB(self.usernameEntry.get(), hashlib.sha256(self.passwordEntry.get().encode()).hexdigest()))

            # in order to remove password
            data_list = list(data[0])
            data_list.pop(2)
            account = Account(*data_list)
            print("Logged in successfully")
            ################
            # LATER
            # update the last login time
            
            self.pack_forget()
            self.master.createMainPanel(account)

            # else
            # update status label login failed