import customtkinter as ctk
import hashlib
from db_service import Login
from db_service import IfLoginExists
from db_service import EditPersonalInfo
from db_service import GetData

class PersonalInfoWidgets(ctk.CTkFrame):
    def __init__(self,master, mainframe):
        super().__init__(master)
        
        self.parent = mainframe

        goBackButton = ctk.CTkButton(self, text="<-Back",command=self.goBack)
        goBackButton.grid(row=0,column=0,sticky="w")

        titleLabel = ctk.CTkLabel(self,text="Edit your personal details")
        titleLabel.grid(row=1,column=0,columnspan=2,padx=20)


        firstnameLabel = ctk.CTkLabel(self, text="Frist Name: " + self.parent.account.firstName)
        firstnameLabel.grid(row=2,column=0,sticky = "w")

        lastnameLabel = ctk.CTkLabel(self, text="Last name: " + self.parent.account.lastName)
        lastnameLabel.grid(row=3,column=0,sticky = "w")

        dateOfBirthLabel = ctk.CTkLabel(self, text="Date of Birth: " + str(self.parent.account.birthDate))
        dateOfBirthLabel.grid(row=4,column=0,sticky = "w")

        bankAccNumLabel = ctk.CTkLabel(self, text="Acct. No.: " + str(self.parent.account.bankAccNum))
        bankAccNumLabel.grid(row=5,column=0,sticky = "w")

        # entry boxes

        usernameLabel = ctk.CTkLabel(self,text="Login: ",width=20)
        usernameLabel.grid(row=6,column=0,sticky = "w")

        loginStartValue = ctk.StringVar()
        self.usernameEntry = ctk.CTkEntry(self, textvariable=loginStartValue)
        loginStartValue.set(self.parent.account.username)
        self.usernameEntry.grid(row=6,column=1)


        usernameLabel = ctk.CTkLabel(self,text="E-mail: ",width=20)
        usernameLabel.grid(row=7,column=0,sticky = "w")

        emailStartValue = ctk.StringVar()
        self.emailEntry = ctk.CTkEntry(self, textvariable=emailStartValue)
        emailStartValue.set(self.parent.account.email)
        self.emailEntry.grid(row=7,column=1)

        confirmLabel = ctk.CTkLabel(self,text="Confirm changes with your password ")
        confirmLabel.grid(row=8,column=0,sticky = "w")

        passwordLabel = ctk.CTkLabel(self,text="Password: ",width=20)
        passwordLabel.grid(row=9,column=0)
        self.passwordEntry = ctk.CTkEntry(self, show="*")
        self.passwordEntry.grid(row=9,column=1)

        self.statusLabel = ctk.CTkLabel(self, text="")
        self.statusLabel.grid(row=10,column=0,columnspan=2,padx=20)
        
        saveButton = ctk.CTkButton(self, text="Save",command=self.SaveChanges)
        saveButton.grid(row=11,column=0,columnspan=2)

        self.pack(expand = True)

    def SaveChanges(self):
        hashed_passwd = hashlib.sha256(self.passwordEntry.get().encode()).hexdigest()
        if(Login(self.parent.account.username,hashed_passwd)== None):
            self.statusLabel.configure(text="You have entered an incorrect password",text_color="#ff6633")
        elif(Login(self.parent.account.username,hashed_passwd)!= None and not IfLoginExists(self.usernameEntry.get())):
            EditPersonalInfo(self.parent.account.id, self.usernameEntry.get(), self.emailEntry.get())
            # update account object
            data = GetData(self.parent.account.id)
            data_list = list(data[0])
            data_list.pop(2)
            self.parent.account.update(*data_list)
            self.statusLabel.configure(text="Changes have been saved",text_color="#009900")
        else:
            self.statusLabel.configure(text="The login you entered is already taken",text_color="#ff6633")

    def goBack(self):
        self.pack_forget()
        self.parent.accountWidgets()