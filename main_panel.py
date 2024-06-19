import time
import customtkinter as ctk
from account import Account
from fund_transfer import TransferWidgets
from transfer_history import TransferHistoryWidgets
from personal_info import PersonalInfoWidgets
from db_service import GetData, GetTransferHistory
from account_widgets import AccountWidgets
class MainWidgets(ctk.CTkFrame):
    def __init__(self,master, account_id):
        super().__init__(master)
        
        data = GetData(account_id)
        # in order to remove password
        data_list = list(data[0])
        data_list.pop(2)
        self.account = Account(*data_list)
        self.mainFrame = ctk.CTkFrame(self, fg_color="transparent")
        self.balanceLabel = ctk.CTkLabel(self.mainFrame, text="{:.2f}".format(self.account.balance) ,font=("Arial",80),
                                         fg_color="transparent")
        self.currencyLabel = ctk.CTkLabel(self.mainFrame, text="PLN" ,font=("Arial",40),
                                         fg_color="transparent")
        self.balanceLabel.pack()
        self.currencyLabel.pack()
        

        #self.timeLabel = tkinter.Label(self.mainFrame,font=('Arial',20),fg="black",bg="#F9F7E6")
        #self.timeLabel.grid(row=1,column=0)

        ############### Bar frame for pages

        self.barFrame = ctk.CTkFrame(self)

        transferButton = ctk.CTkButton(self.barFrame, text="Transfer of funds",command=self.fundTransfer)
        transferButton.grid(row=0,column=0)

        historyButton = ctk.CTkButton(self.barFrame, text="Transfer history",command=self.transferHistory)
        historyButton.grid(row=1,column=0)

        accountButton = ctk.CTkButton(self.barFrame, text="My account",command=self.accountWidgets)
        accountButton.grid(row=2,column=0)

        ############### Packing frames and stuff
        self.barFrame.pack(side=ctk.LEFT, fill=ctk.Y)
        self.mainFrame.pack(side=ctk.LEFT, expand=True, fill=ctk.X) #fill=ctk.BOTH, 
        self.pack(fill=ctk.BOTH, expand=True)

    def update(self):
        time_str = time.strftime("%H:%M:%S   %d-%m-%Y")
        self.timeLabel.configure(text=time_str)
        self.timeLabel.after(1000,self.update)

    def fundTransfer(self):
        self.pack_forget()
        transferFrame = TransferWidgets(self.master, self)

    def transferHistory(self):
        self.pack_forget()
        history = GetTransferHistory(self.account.bankAccNum) #list of tuples
        transferHistoryFrame = TransferHistoryWidgets(self.master, self, history)

    def accountWidgets(self):
        self.pack_forget()
        accountFrame = AccountWidgets(self.master, self)