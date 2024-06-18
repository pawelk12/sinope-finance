import customtkinter as ctk
from login import LoginWidgets
from register import RegisterWidgets
from welcome import WelcomeWidgets
from main_panel import MainWidgets
from tkinter import PhotoImage
import tkinter as tk


class BankApp(tk.Tk):

    def __init__(self,title,geometry, path_to_icon):
        super().__init__()
        self.title(title)
        self.geometry(geometry)
        self.minsize(300,400)
        self.maxsize(1200,800)
        self.path_to_icon = path_to_icon
        self.setIcon()
        self.configure(bg="#2b2b2b")
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

    def setIcon(self):
        icon = PhotoImage(file=self.path_to_icon)
        self.iconphoto(True, icon)

