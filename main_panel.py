import time
import customtkinter as ctk
from account import Account
from tkinter import PhotoImage
from fund_transfer import TransferWidgets
from transfer_history import TransferHistoryWidgets
from db_service import GetData, GetTransferHistory, CheckSavings
from account_widgets import AccountWidgets
from savings_deposits import SavingsDepositsWidgets

class MainWidgets(ctk.CTkFrame):
    def __init__(self,master, accountId):
        super().__init__(master)
        
        self.createAccount(accountId)
        self.mainFrame = ctk.CTkFrame(self, fg_color="transparent")


        self.mainFrame._border_width = 3
        self.mainFrame._border_color = "#3d9bd7"
        self.mainFrame._corner_radius = 10


        self.balanceLabel = ctk.CTkLabel(self.mainFrame, text="{:.2f}".format(self.account.Balance) ,font=("Arial",80),
                                         fg_color="transparent")
        self.currencyLabel = ctk.CTkLabel(self.mainFrame, text="PLN" ,font=("Arial",40),
                                         fg_color="transparent")
        self.timeLabel = ctk.CTkLabel(self.mainFrame,font=('Arial',20),
                                   fg_color="transparent")
        self.savingsButton = ctk.CTkButton(self.mainFrame,
                                           text="Savings Deposits",
                                           fg_color="transparent",
                                           corner_radius=30,
                                           border_width=2,
                                           border_spacing=6,
                                           border_color="#3d9bd7",
                                           command=self.savingsDeposits)

        self.updateBalance()
        self.checkSavings()
        self.updateTime()
        self.timeLabel.pack(anchor="ne",padx=15,pady=5)
        self.balanceLabel.pack(anchor="s", expand=True)
        self.currencyLabel.pack(anchor="n", expand=True)
        self.savingsButton.pack(pady=30)


        ############### Bar frame for pages

        self.barFrame = ctk.CTkFrame(self)

        pathToUserIcon = "resources/welcome/user.png"
        userIconImage = PhotoImage(file=pathToUserIcon)
        userImageLabel = ctk.CTkLabel(self.barFrame,text="",image=userIconImage)
        userImageLabel.pack()

        transferButton = ctk.CTkButton(self.barFrame, text="Transfer of funds",
                                           fg_color="transparent",
                                           corner_radius=8,
                                           border_width=2,
                                           border_spacing=8,
                                           border_color="#3d9bd7",
                                           command=self.fundTransfer)
        transferButton.pack(ipadx=30,pady=0)

        historyButton = ctk.CTkButton(self.barFrame, text="Transfer history",
                                           fg_color="transparent",
                                           corner_radius=8,
                                           border_width=2,
                                           border_spacing=8,
                                           border_color="#3d9bd7",
                                           command=self.transferHistory)
        historyButton.pack(ipadx=30,pady=0)

        accountButton = ctk.CTkButton(self.barFrame, text="My account",
                                           fg_color="transparent",
                                           corner_radius=8,
                                           border_width=2,
                                           border_spacing=8,
                                           border_color="#3d9bd7",
                                           command=self.accountWidgets)
        accountButton.pack(ipadx=30,pady=0)

        logoutButton = ctk.CTkButton(self.barFrame, text="Log out",
                                            fg_color="transparent",
                                            corner_radius=8,
                                            border_width=2,
                                            border_spacing=8,
                                            border_color="#ed460e",
                                            hover_color="#632410",
                                            command=self.logOut)
        logoutButton.pack(anchor="s",expand = True,ipadx=30)

        ############### Packing frames and stuff
        self.barFrame.pack(side=ctk.LEFT,fill=ctk.Y)
        self.mainFrame.pack(side=ctk.LEFT,fill=ctk.BOTH, expand=True)
        self.pack(fill=ctk.BOTH, expand=True)

    def updateTime(self):
        time_str = time.strftime("%H:%M:%S   %d.%m.%Y")
        self.timeLabel.configure(text=time_str)
        self.timeLabel.after(1000,self.updateTime)

    def checkSavings(self):
        CheckSavings(self.account.Id)
        # check savings and update balance
        self.checkingDeposits = self.after(1000000,self.checkSavings)

    def updateBalance(self):
        self.account.UpdateBalance()
        self.balanceLabel.configure(text="{:.2f}".format(self.account.Balance))
        self.updatingBalance = self.balanceLabel.after(10000,self.updateBalance)
    

    def fundTransfer(self):
        self.pack_forget()
        self.transition()
        transferFrame = TransferWidgets(self.master, self)

    def transferHistory(self):
        self.pack_forget()
        self.transition()
        history = GetTransferHistory(self.account.BankAccNum) #list of tuples
        transferHistoryFrame = TransferHistoryWidgets(self.master, self, history)

    def accountWidgets(self):
        self.pack_forget()
        self.transition()
        accountFrame = AccountWidgets(self.master, self)

    def createAccount(self, accountId):
        data = GetData(accountId)
        # in order to remove password
        data_list = list(data[0])
        data_list.pop(2)
        self.account = Account(*data_list)

    def logOut(self):
        del self.account
        self.pack_forget()
        self.transition()
        self.master.createWelcomWingets()

    def savingsDeposits(self):
        self.pack_forget()
        self.transition()
        savingsDepositsFrame = SavingsDepositsWidgets(self.master, self)

    def transition(self):
        for widget in self.winfo_children():
            widget.pack_forget()
            widget.destroy()
        self.after_cancel(self.updatingBalance)
        self.after_cancel(self.checkingDeposits)