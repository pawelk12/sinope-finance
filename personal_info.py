import customtkinter as ctk
import hashlib
from db_service import Login
from db_service import IfLoginExists
from db_service import EditPersonalInfo
from tkinter import PhotoImage

class PersonalInfoWidgets(ctk.CTkFrame):
    def __init__(self,master, mainframe):
        super().__init__(master)
        
        self.parent = mainframe

        pathToArrow = "resources/arrowLeft.png"
        arrowImage = PhotoImage(file=pathToArrow)

        goBackButton = ctk.CTkButton(self, text="Back   ",
                                    image=arrowImage,
                                    fg_color="transparent",
                                    corner_radius=30,
                                    border_width=2,
                                    border_spacing=6,
                                    border_color="#3d9bd7",
                                    command=self.goBack)
        goBackButton.grid(row=0,column=0,sticky="w",pady=3)

        titleLabel = ctk.CTkLabel(self,text="Edit your personal details",font=("Arial",32))
        titleLabel.grid(row=1,column=0,columnspan=2,pady=20)

        self.grid_columnconfigure(0,weight=1)
        self.grid_columnconfigure(1,weight=1)


        self.editFrame = ctk.CTkFrame(self, fg_color="transparent")

        firstnameLabel = ctk.CTkLabel(self.editFrame, text="Frist Name: " + self.parent.account.FirstName,font=("Arial",18))
        firstnameLabel.grid(row=0,column=0,sticky = "w")

        lastnameLabel = ctk.CTkLabel(self.editFrame, text="Last name: " + self.parent.account.LastName,font=("Arial",18))
        lastnameLabel.grid(row=1,column=0,sticky = "w")

        dateOfBirthLabel = ctk.CTkLabel(self.editFrame, text="Date of Birth: " + str(self.parent.account.BirthDate),font=("Arial",18))
        dateOfBirthLabel.grid(row=2,column=0,sticky = "w")

        bankAccNumLabel = ctk.CTkLabel(self.editFrame, text="Acct. No.: " + str(self.parent.account.BankAccNum),font=("Arial",18))
        bankAccNumLabel.grid(row=3,column=0,sticky = "w")

        # entry boxes

        usernameLabel = ctk.CTkLabel(self.editFrame,text="Login: ",width=20,font=("Arial",18))
        usernameLabel.grid(row=4,column=0,sticky = "w")

        loginStartValue = ctk.StringVar()
        self.usernameEntry = ctk.CTkEntry(self.editFrame, textvariable=loginStartValue,
                                          fg_color="transparent",
                                          border_width=2,
                                          border_color="#3d9bd7",
                                          font=("Arial",16))
        loginStartValue.set(self.parent.account.Username)
        self.usernameEntry.grid(row=4,column=1)


        usernameLabel = ctk.CTkLabel(self.editFrame,text="E-mail: ",width=20,font=("Arial",18))
        usernameLabel.grid(row=5,column=0,sticky = "w")

        emailStartValue = ctk.StringVar()
        self.emailEntry = ctk.CTkEntry(self.editFrame, textvariable=emailStartValue,
                                          fg_color="transparent",
                                          border_width=2,
                                          border_color="#3d9bd7",
                                          font=("Arial",16))
        emailStartValue.set(self.parent.account.Email)
        self.emailEntry.grid(row=5,column=1,pady=3)

        confirmLabel = ctk.CTkLabel(self.editFrame,text="Confirm changes with your password ",font=("Arial",18))
        confirmLabel.grid(row=6,column=0,columnspan=2)

        passwordLabel = ctk.CTkLabel(self.editFrame,text="Password: ",width=20,font=("Arial",18))
        passwordLabel.grid(row=7,column=0,sticky="w")
        self.passwordEntry = ctk.CTkEntry(self.editFrame, show="*",
                                          fg_color="transparent",
                                          border_width=2,
                                          border_color="#3d9bd7",
                                          font=("Arial",16))
        self.passwordEntry.grid(row=7,column=1)

        self.statusLabel = ctk.CTkLabel(self.editFrame, text="")
        self.statusLabel.grid(row=8,column=0,columnspan=2,padx=20)
        
        saveButton = ctk.CTkButton(self.editFrame, text="Save",
                                           fg_color="transparent",
                                           corner_radius=30,
                                           border_width=2,
                                           border_spacing=6,
                                           border_color="#3d9bd7",command=self.SaveChanges)
        saveButton.grid(row=9,column=0,columnspan=2,pady=20)


        self.editFrame.grid(row=2,column=0,columnspan=2)
        self.pack(expand = True,fill=ctk.BOTH)


    def SaveChanges(self):
        hashed_passwd = hashlib.sha256(self.passwordEntry.get().encode()).hexdigest()
        username = self.parent.account.Username
        email = self.parent.account.Email

        if(Login(username,hashed_passwd)== None):
            self.statusLabel.configure(text="Incorrect password",text_color="#ff6633")
            self.passwordEntry.delete(0, ctk.END)
            return

        if(self.usernameEntry.get() == self.parent.account.Username and self.emailEntry.get() == email):
            self.statusLabel.configure(text="You have not changed anything",text_color="#ff6633")
            return

        if(IfLoginExists(self.usernameEntry.get()) and self.usernameEntry.get()!=username):
            self.statusLabel.configure(text="This username is already taken",text_color="#ff6633")
            self.passwordEntry.delete(0, ctk.END)
            return

        if(Login(username,hashed_passwd)!= None and #user changes email
           self.usernameEntry.get() == username and self.emailEntry.get()!=email):
            
            EditPersonalInfo(self.parent.account.Id, self.usernameEntry.get(), self.emailEntry.get())
            self.parent.account.Update()
            self.statusLabel.configure(text="Changes have been saved",text_color="#009900")
            self.passwordEntry.delete(0, ctk.END)

        elif(Login(username,hashed_passwd)!=None and #user changes login
             not IfLoginExists(self.usernameEntry.get()) and
             self.usernameEntry.get()!=username and self.emailEntry.get()==email):
            
            EditPersonalInfo(self.parent.account.Id, self.usernameEntry.get(), self.emailEntry.get())
            self.parent.account.Update()
            self.statusLabel.configure(text="Changes have been saved",text_color="#009900")
            self.passwordEntry.delete(0, ctk.END)
            
        elif(Login(username,hashed_passwd)!= None and #user changes login and email
             not IfLoginExists(self.usernameEntry.get()) and
             self.usernameEntry.get()!=username and self.emailEntry.get()!=email):

            EditPersonalInfo(self.parent.account.Id, self.usernameEntry.get(), self.emailEntry.get())
            self.parent.account.Update()
            self.statusLabel.configure(text="Changes have been saved",text_color="#009900")
            self.passwordEntry.delete(0, ctk.END)

        elif(Login(username,hashed_passwd)!= None and
             self.usernameEntry.get()==username and self.emailEntry.get()==email):

            self.statusLabel.configure(text="No changes have been made",text_color="#ff6633")
            self.passwordEntry.delete(0, ctk.END)


    def goBack(self):
        self.pack_forget()
        self.parent.accountWidgets()
