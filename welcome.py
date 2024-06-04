import customtkinter as ctk


class WelcomeWidgets(ctk.CTkFrame):
    def __init__(self,master):
        super().__init__(master)

        loginButton = ctk.CTkButton(self, text="Login",command=self.Login)
        loginButton.grid(row=1,column=1,columnspan=2)
        registerButton = ctk.CTkButton(self, text="Register",command=self.Register)
        registerButton.grid(row=2,column=1,columnspan=2)

        self.pack(expand = True)


    def Login(self):
        self.pack_forget()
        self.master.createLoginPanel()


    def Register(self):
        self.pack_forget()
        self.master.createRegisterPanel()