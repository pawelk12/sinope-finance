import customtkinter as ctk
from login import LoginWidgets
from register import RegisterWidgets
from welcome import WelcomeWidgets
from main_panel import MainWidgets



class BankApp(ctk.CTk):

    def __init__(self,title,geometry):
        super().__init__()
        self.title(title)
        self.geometry(geometry)
        self.minsize(600,400)
        self.maxsize(1200,800)
        
        self.createWelcomWingets()
        self.mainloop()


    def createWelcomWingets(self):
        welcomeFrame = WelcomeWidgets(self)

    def createLoginPanel(self):
        loginFrame = LoginWidgets(self)

    def createRegisterPanel(self):
        registerFrame = RegisterWidgets(self)

    def createMainPanel(self, account_id):
        mainPanel = MainWidgets(self, account_id)

