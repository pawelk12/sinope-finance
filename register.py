import hashlib
import random
import time
import customtkinter as ctk
from db_service import IfLoginExists,IfAccNumExists
from db_service import Register as WriteToDB
from datetime import date, datetime


seed = int(time.time())
random.seed(seed)

class RegisterWidgets(ctk.CTkFrame):
    def __init__(self,master):
        super().__init__(master)

        self._fg_color= "#021639"
        self.master.configure(bg="#021639")
        self._border_width = 3
        self._border_color = "#3d9bd7"
        self._corner_radius = 32
        self.master.bind('<Return>',self.Register)

        titleLabel = ctk.CTkLabel(self,text="Please enter your personal details",font=("Arial",20))
        titleLabel.grid(row=0,column=0,columnspan=2,padx=20,pady=10)

        usernameLabel = ctk.CTkLabel(self,text="Login: ",width=20)
        usernameLabel.grid(row=1,column=0,sticky="e")
        self.usernameEntry = ctk.CTkEntry(self,
                                          fg_color="transparent",
                                          border_width=2,
                                          border_color="#3d9bd7")
        self.usernameEntry.grid(row=1,column=1,pady=1)

        passwordLabel = ctk.CTkLabel(self,text="Password: ",width=20)
        passwordLabel.grid(row=2,column=0,sticky="e")
        self.passwordEntry = ctk.CTkEntry(self,
                                          show="*",
                                          fg_color="transparent",
                                          border_width=2,
                                          border_color="#3d9bd7")
        self.passwordEntry.grid(row=2,column=1,pady=1)

        firstnameLabel = ctk.CTkLabel(self, text="Frist Name:")
        firstnameLabel.grid(row=3,column=0,sticky="e")
        self.firstnameEntry = ctk.CTkEntry(self,
                                           fg_color="transparent",
                                           border_width=2,
                                           border_color="#3d9bd7")
        self.firstnameEntry.grid(row=3,column=1,pady=1)

        lastnameLabel = ctk.CTkLabel(self, text="Last name:")
        lastnameLabel.grid(row=4,column=0,sticky="e")
        self.lastnameEntry = ctk.CTkEntry(self,
                                          fg_color="transparent",
                                          border_width=2,
                                          border_color="#3d9bd7")
        self.lastnameEntry.grid(row=4,column=1,pady=1)

        emailLabel = ctk.CTkLabel(self, text="E-mail:")
        emailLabel.grid(row=5,column=0,sticky="e")
        self.emailEntry = ctk.CTkEntry(self,
                                       fg_color="transparent",
                                       border_width=2,
                                       border_color="#3d9bd7")
        self.emailEntry.grid(row=5,column=1,pady=1)

        dateOfBirthLabel = ctk.CTkLabel(self, text="Date of Birth(yyyy-mm-dd):")
        dateOfBirthLabel.grid(row=6,column=0,sticky="e")
        self.dateOfBirthEntry = ctk.CTkEntry(self,
                                             fg_color="transparent",
                                             border_width=2,
                                             border_color="#3d9bd7")
        self.dateOfBirthEntry.grid(row=6,column=1,pady=1)

        self.statusLabel = ctk.CTkLabel(self, text="")
        self.statusLabel.grid(row=7,column=0,columnspan=2,padx=20)

        registerButton = ctk.CTkButton(self,
                                    text="Register",
                                    fg_color="transparent",
                                    corner_radius=30,
                                    border_width=2,
                                    border_spacing=6,
                                    border_color="#3d9bd7",
                                    command=self.Register)
        registerButton.grid(row=8,column=0,columnspan=2)

        switchToButton = ctk.CTkButton(self, text="Do you have an account? Click here to login",
                                        fg_color ="transparent",hover=False,command=self.SwitchToLogin)
        switchToButton.grid(row=9,column=0,columnspan=2,padx=10,pady=10)

        self.pack(expand = True)
        
    def Register(self,event=None):

        # checking if user entered date in correct format
        try:
            date.fromisoformat(self.dateOfBirthEntry.get())
        except ValueError:
            self.statusLabel.configure(text="Incorrect date entered",text_color="#ff6633")
            return

        # checking if user is adult
        currDate = datetime.today()
        date18yearsAgo = datetime(currDate.year-18, currDate.month, currDate.day)
        if(datetime.fromisoformat(self.dateOfBirthEntry.get()) > date18yearsAgo):
            self.statusLabel.configure(text="You must be at least 18 years old to register",text_color="#ff6633")
            return

        # while account number exists in database get new random account number
        accNum = random.randint(100000000000000000,999999999999999999)
        while IfAccNumExists(accNum):
            accNum = random.randint(100000000000000000,999999999999999999)


        if not IfLoginExists(self.usernameEntry.get()): #login is available
            #write atributes to database

            values = (self.usernameEntry.get(),
                      hashlib.sha256(self.passwordEntry.get().encode()).hexdigest(),
                      self.firstnameEntry.get(),
                      self.lastnameEntry.get(),
                      self.emailEntry.get(),
                      self.dateOfBirthEntry.get(),
                      accNum
                      )
            
            self.statusLabel.configure(text="Registered successfully",text_color="#009900")
            self.master.unbind('<Return>')
            self.pack_forget()
            self.master.createLoginPanel()

            WriteToDB(values)
        else:
            self.statusLabel.configure(text="This login is unavailable",text_color="#ff6633")
            #clear login entry
            self.usernameEntry.delete(0, ctk.END)
        
    def SwitchToLogin(self):
        self.master.unbind('<Return>')
        self.pack_forget()
        self.master.createLoginPanel()