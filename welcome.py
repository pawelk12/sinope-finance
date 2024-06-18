import customtkinter as ctk
from tkinter import PhotoImage

class WelcomeWidgets(ctk.CTkFrame):
    def __init__(self,master):
        super().__init__(master)

        self.master.geometry("476x573")
        self.configure(fg_color="#021639")
        pathToJupiter = "resources/welcome/picture.png"
        jupiterImage = PhotoImage(file=pathToJupiter)
        imageLabel = ctk.CTkLabel(self,text="",image=jupiterImage)
        imageLabel.pack(side=ctk.LEFT)

        self.buttonFrame = ctk.CTkFrame(self, fg_color="transparent")

        pathToUserIcon = "resources/welcome/user.png"
        userIconImage = PhotoImage(file=pathToUserIcon)
        userImageLabel = ctk.CTkLabel(self.buttonFrame,text="",image=userIconImage)
        userImageLabel.grid(row=0,column=0,sticky="n")

        loginButton = ctk.CTkButton(self.buttonFrame, text="Login",command=self.Login)
        loginButton.grid(row=1,column=0,padx=5,pady=5)
        
        registerButton = ctk.CTkButton(self.buttonFrame, text="Register",command=self.Register)
        registerButton.grid(row=2,column=0,padx=5,pady=5)
        

        self.buttonFrame.pack(side=ctk.LEFT, expand=True, fill=ctk.X)
        self.pack(expand = True)


    def Login(self):
        self.pack_forget()
        self.master.createLoginPanel()


    def Register(self):
        self.pack_forget()
        self.master.createRegisterPanel()