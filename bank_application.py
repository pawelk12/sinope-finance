import tkinter
from tkinter import ttk
import time
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

    def createMainPanel(self,acc):
        self.mainFrame = ttk.Frame(self)
        self.balanceLabel = tkinter.Label(self.mainFrame, text="Balance: "+ "{:.2f}".format(acc.balance) ,font=("Arial",20),bg="#F9F7E6")
        self.balanceLabel.grid(row=0,column=2,columnspan=2,padx=20)

        self.timeLabel = tkinter.Label(self.mainFrame,font=('Arial',20),fg="black",bg="#F9F7E6")
        self.timeLabel.grid(row=1,column=0)

        loginButton = tkinter.Button(self.mainFrame, text="show info",command=acc.listProfile)
        loginButton.grid(row=1,column=1,columnspan=2)

        getBonusButton = tkinter.Button(self.mainFrame, text="Receive Start Bonus",command=acc.receiveStartBonus)
        getBonusButton.grid(row=2,column=1,columnspan=2)

        self.mainFrame.pack(expand = True)
        self.update()

    def update(self):
        time_str = time.strftime("%H:%M:%S   %d-%m-%Y")
        self.timeLabel.config(text=time_str)
        self.timeLabel.after(1000,self.update)

