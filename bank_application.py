import tkinter
from tkinter import ttk
from login import LoginWidgets
from personal_details import PersonalDetails

class BankApp(tkinter.Tk):
    def __init__(self,title,geometry):
        super().__init__()
        self.title(title)
        self.geometry(geometry)
        
        loginFrame = LoginWidgets(self)
        self.mainloop()

        
    def runPersonalDetails(self):

        accountDetails = PersonalDetails(self)
