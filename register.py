import customtkinter as ctk
from db_service import IfLoginExists
from db_service import Register as WriteToDB
import hashlib
import random
import time

seed = int(time.time())
random.seed(seed)

class RegisterWidgets(ctk.CTkFrame):
    def __init__(self,master):
        super().__init__(master)
        titleLabel = ctk.CTkLabel(self,text="Please enter your personal details")
        titleLabel.grid(row=0,column=0,columnspan=2,padx=20)

        usernameLabel = ctk.CTkLabel(self,text="Login: ",width=20)
        usernameLabel.grid(row=1,column=0)
        self.usernameEntry = ctk.CTkEntry(self)
        self.usernameEntry.grid(row=1,column=1)

        passwordLabel = ctk.CTkLabel(self,text="Password: ",width=20)
        passwordLabel.grid(row=2,column=0)
        self.passwordEntry = ctk.CTkEntry(self, show="*")
        self.passwordEntry.grid(row=2,column=1)

        firstnameLabel = ctk.CTkLabel(self, text="Frist Name:")
        firstnameLabel.grid(row=3,column=0)
        self.firstnameEntry = ctk.CTkEntry(self)
        self.firstnameEntry.grid(row=3,column=1)

        lastnameLabel = ctk.CTkLabel(self, text="Last name:")
        lastnameLabel.grid(row=4,column=0)
        self.lastnameEntry = ctk.CTkEntry(self)
        self.lastnameEntry.grid(row=4,column=1)

        emailLabel = ctk.CTkLabel(self, text="E-mail:")
        emailLabel.grid(row=5,column=0)
        self.emailEntry = ctk.CTkEntry(self)
        self.emailEntry.grid(row=5,column=1)

        dateOfBirthLabel = ctk.CTkLabel(self, text="Date of birthday(yyyy-mm-dd):")
        dateOfBirthLabel.grid(row=6,column=0)
        self.dateOfBirthEntry = ctk.CTkEntry(self)
        self.dateOfBirthEntry.grid(row=6,column=1)

        self.statusLabel = ctk.CTkLabel(self, text="")
        self.statusLabel.grid(row=7,column=2,columnspan=2,padx=20)

        registerButton = ctk.CTkButton(self, text="Register",command=self.Register)
        registerButton.grid(row=8,column=0,columnspan=2)

        self.pack(expand = True)

    def Register(self):
        ##############
        # check if data is correct (correct format especially)
        # and check if account number is not taken by other user
        
        if not IfLoginExists(self.usernameEntry.get()): #login is available
            #write atributes to database
            #INSERT INTO ACCOUNTS (LOGIN, PASSWD, FIRST_NAME, LAST_NAME, EMAIL, DATE_OF_BIRTH, ACCOUNT_NUM)
            values = (self.usernameEntry.get(),
                      hashlib.sha256(self.passwordEntry.get().encode()).hexdigest(),
                      self.firstnameEntry.get(),
                      self.lastnameEntry.get(),
                      self.emailEntry.get(),
                      self.dateOfBirthEntry.get(),
                      random.randint(100000000000000000,999999999999999999)
                      )
            #############
            # update status label

            self.pack_forget()
            self.master.createLoginPanel()

            WriteToDB(values)
        else:
            print("This login is unavailable")
            #clear login entry
            self.usernameEntry.delete(0, ctk.END)