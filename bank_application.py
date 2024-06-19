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
        self.resizable(False, False)
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

    def resizeAndCenter(self, windowWidth, windowHeight):
        screenWidth = self.winfo_screenwidth()
        screenHeight = self.winfo_screenheight()

        centeredX = int(screenWidth/2 - windowWidth/2)
        centeredY = int(screenHeight/2 - windowHeight/2)

        self.geometry(f"{windowWidth}x{windowHeight}+{centeredX}+{centeredY}")

