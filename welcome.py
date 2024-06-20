import customtkinter as ctk
from tkinter import PhotoImage

class WelcomeWidgets(ctk.CTkFrame):
    def __init__(self,master):
        super().__init__(master)

        self.master.resizeAndCenter(476,575)
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

        loginButton = ctk.CTkButton(self.buttonFrame,
                                    text="Login",
                                    font=("Helvetica",13),
                                    fg_color="transparent",
                                    corner_radius=30,
                                    border_width=2,
                                    border_spacing=6,
                                    border_color="#3d9bd7",
                                    command=self.Login)
        loginButton.grid(row=1,column=0,padx=5,pady=3)
        
        registerButton = ctk.CTkButton(self.buttonFrame, 
                                       text="Register",
                                       font=("Helvetica",13),
                                       fg_color="transparent",
                                       corner_radius=30,
                                       border_width=2,
                                       border_spacing=6,
                                       border_color="#3d9bd7",
                                       command=self.Register)
        registerButton.grid(row=2,column=0,padx=5,pady=3)
        

        self.buttonFrame.pack(side=ctk.LEFT, expand=True, fill=ctk.X)
        self.pack(expand = True)


    def Login(self):
        self.pack_forget()
        self.master.createLoginPanel()


    def Register(self):
        self.pack_forget()
        self.master.createRegisterPanel()