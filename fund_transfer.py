import customtkinter as ctk
from db_service import TransferMoney
from db_service import GetData

class TransferWidgets(ctk.CTkFrame):
    def __init__(self,master, mainframe):
        super().__init__(master)

        self.parent = mainframe

        titleLabel = ctk.CTkLabel(self, text="Fund transfer",font=("Arial",20))
        titleLabel.grid(row=0,column=1,columnspan=4,padx=20)

        accountNumberLabel = ctk.CTkLabel(self,text="Enter bank account number: ",padx=20)
        accountNumberLabel.grid(row=1,column=2)
        self.accountNumberEntry = ctk.CTkEntry(self)
        self.accountNumberEntry.grid(row=1,column=3)

        amountLabel = ctk.CTkLabel(self,text="Enter amount: ",padx=20)
        amountLabel.grid(row=2,column=2)
        self.amountEntry = ctk.CTkEntry(self)
        self.amountEntry.grid(row=2,column=3)

        currencyLabel = ctk.CTkLabel(self,text="PLN",padx=10)
        currencyLabel.grid(row=2,column=4)

        transferButton = ctk.CTkButton(self, text="Transfer",command=self.Transfer)
        transferButton.grid(row=3,column=1,columnspan=4)

        self.statusLabel = ctk.CTkLabel(self, text="", font=("arial", 10))
        self.statusLabel.grid(row=4,column=1,columnspan=4,padx=20)

        self.pack(expand = True)

    def Transfer(self):

        invalidValue = "Incorrect transfer amount value was provided."
        transferSuccess = "The transfer was successful."
        notEnoughFunds = "You do not have enough funds in your account."
        invalidNumber = "Invalid bank number."

        result = TransferMoney(self.parent.account.id, self.accountNumberEntry.get(), self.amountEntry.get())
        if(result == invalidValue):
            self.statusLabel.configure(text=invalidValue, text_color="#ff6633")
        elif(result == notEnoughFunds):
            self.statusLabel.configure(text=notEnoughFunds, text_color="#ff6633")
        elif(result == invalidNumber):
            self.statusLabel.configure(text=invalidNumber, text_color="#ff6633")
        elif(result == transferSuccess):
            self.statusLabel.configure(text=transferSuccess, text_color="#009900")

            # update account object created in MainWidgets 
            data = GetData(self.parent.account.id)
            data_list = list(data[0])
            data_list.pop(2)
            self.parent.account.update(*data_list)

        else:
            print("transfer error")
