import customtkinter as ctk
from db_service import TransferMoney

class TransferWidgets(ctk.CTkFrame):
    def __init__(self,master, mainframe):
        super().__init__(master)

        self.parent = mainframe

        goBackButton = ctk.CTkButton(self, text="<-Back to Home",command=self.goBack)
        goBackButton.grid(row=0,column=0,sticky="w")

        titleLabel = ctk.CTkLabel(self, text="Fund transfer",font=("Arial",20))
        titleLabel.grid(row=1,column=0,columnspan=4,padx=20)

        accountNumberLabel = ctk.CTkLabel(self,text="Enter bank account number: ",padx=20)
        accountNumberLabel.grid(row=2,column=0,columnspan=2)
        self.accountNumberEntry = ctk.CTkEntry(self)
        self.accountNumberEntry.grid(row=2,column=2)

        amountLabel = ctk.CTkLabel(self,text="Enter amount: ",padx=20)
        amountLabel.grid(row=3,column=0,columnspan=2)
        self.amountEntry = ctk.CTkEntry(self)
        self.amountEntry.grid(row=3,column=2)

        currencyLabel = ctk.CTkLabel(self,text="PLN",padx=10)
        currencyLabel.grid(row=3,column=3)

        self.statusLabel = ctk.CTkLabel(self, text="", font=("arial", 12))
        self.statusLabel.grid(row=4,column=0,columnspan=4,padx=20)

        transferButton = ctk.CTkButton(self, text="Transfer",command=self.Transfer)
        transferButton.grid(row=5,column=0,columnspan=4)


        self.pack(expand = True)

    def Transfer(self):

        # if user entered his own account number
        if(self.accountNumberEntry.get() == str(self.parent.account.BankAccNum)):
            self.statusLabel.configure(text="Invalid bank number", text_color="#ff6633")
            return

        try:
            invalidValue = "Incorrect transfer amount value was provided"
            transferSuccess = "The transfer was successful"
            notEnoughFunds = "You do not have enough funds in your account"
            invalidNumber = "Invalid bank number"

            result = TransferMoney(self.parent.account.Id, self.accountNumberEntry.get(), self.amountEntry.get())
            if(result == invalidValue):
                self.statusLabel.configure(text=invalidValue, text_color="#ff6633")
            elif(result == notEnoughFunds):
                self.statusLabel.configure(text=notEnoughFunds, text_color="#ff6633")
            elif(result == invalidNumber):
                self.statusLabel.configure(text=invalidNumber, text_color="#ff6633")
            elif(result == transferSuccess):
                self.accountNumberEntry.delete(0, ctk.END)
                self.amountEntry.delete(0, ctk.END)
                self.statusLabel.configure(text=transferSuccess, text_color="#009900")

                # update account object created in MainWidgets 
                self.parent.account.Update()

            else:
                self.statusLabel.configure(text="Unexpected error", text_color="#ff6633")
        except ValueError:
            self.statusLabel.configure(text="Please enter a valid value", text_color="#ff6633")

    def goBack(self):
        self.pack_forget()
        self.parent.master.createMainPanel(self.parent.account.Id)
