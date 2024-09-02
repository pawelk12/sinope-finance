import customtkinter as ctk
from db_service import TransferMoney
from tkinter import PhotoImage

class TransferWidgets(ctk.CTkFrame):
    def __init__(self,master, mainframe):
        super().__init__(master)

        self.parent = mainframe

        pathToArrow = "resources/arrowLeft.png"
        arrowImage = PhotoImage(file=pathToArrow)

        goBackButton = ctk.CTkButton(self,
                                    text="Home   ",
                                    image=arrowImage,
                                    fg_color="transparent",
                                    corner_radius=30,
                                    border_width=2,
                                    border_spacing=6,
                                    border_color="#3d9bd7",
                                    command=self.goBack)
        
        goBackButton.grid(row=0,column=0,sticky="w",pady=3)

        titleLabel = ctk.CTkLabel(self, text="Transfer Funds",font=("Arial",32))
        titleLabel.grid(row=1,column=0,columnspan=2,pady=20)


        self.transferFrame = ctk.CTkFrame(self, fg_color="transparent")
        self.transferFrame._border_width = 3
        self.transferFrame._border_color = "#3d9bd7"
        self.transferFrame._corner_radius = 32

        self.transferFrame.grid(row=2,column=0,columnspan=2,pady=10)

        accountNumberLabel = ctk.CTkLabel(self.transferFrame,text="Please enter bank account number: ",font=("Arial",18))
        accountNumberLabel.grid(row=0,column=0,sticky="e",padx=15,pady=10)

        self.accountNumberEntry = ctk.CTkEntry(self.transferFrame,
                                          fg_color="transparent",
                                          border_width=2,
                                          border_color="#3d9bd7",
                                          font=("Arial",16),
                                          width=200)
        self.accountNumberEntry.grid(row=0,column=1,pady=10)

        amountLabel = ctk.CTkLabel(self.transferFrame,text="Please enter amount: ",font=("Arial",18))
        amountLabel.grid(row=1,column=0,sticky="e",padx=10)
        self.amountEntry = ctk.CTkEntry(self.transferFrame,
                                          fg_color="transparent",
                                          border_width=2,
                                          border_color="#3d9bd7",
                                          font=("Arial",16),
                                          width=200)
        self.amountEntry.grid(row=1,column=1)

        currencyLabel = ctk.CTkLabel(self.transferFrame,text="PLN",font=("Arial",18))
        currencyLabel.grid(row=1,column=2,sticky="w",padx=15)

        self.statusLabel = ctk.CTkLabel(self.transferFrame, text="", font=("Arial", 12))
        self.statusLabel.grid(row=2,column=0,columnspan=3,padx=20)

        transferButton = ctk.CTkButton(self.transferFrame, text="Transfer",
                                        fg_color="transparent",
                                        corner_radius=30,
                                        border_width=2,
                                        border_spacing=6,
                                        border_color="#3d9bd7",command=self.Transfer)
        transferButton.grid(row=3,column=0,columnspan=3,pady=10)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)


        self.pack(fill=ctk.BOTH, expand = True)

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
