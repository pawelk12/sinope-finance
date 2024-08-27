import customtkinter as ctk
from db_service import getSavingsDepositOffers, getSavingsDepositOffersIds, acceptSavingDeposit, getSavingsDepositTakenIds,\
getMySavingsDeposits, getInfoOfMyOffers, ResignDeposit
import requests
from tkinter import PhotoImage

class SavingsDepositsWidgets(ctk.CTkFrame):
    def __init__(self,master, mainframe):
        super().__init__(master)

        self.parent = mainframe
        self.offerId = None
        self.myDeposit = None
        self.myDepositId = None

        #mainframe
        self.mainFrame = ctk.CTkFrame(self, fg_color="transparent")

        pathToArrow = "resources/arrowLeft.png"
        arrowImage = PhotoImage(file=pathToArrow)

        goBackButton = ctk.CTkButton(self.mainFrame,
                                    text="Home   ",
                                    image=arrowImage,
                                    fg_color="transparent",
                                    corner_radius=30,
                                    border_width=2,
                                    border_spacing=6,
                                    border_color="#3d9bd7",
                                    command=self.goBackHome)
        goBackButton.pack(anchor="nw",pady=3)

        titleLabel = ctk.CTkLabel(self.mainFrame, text="Savings Deposits",font=("Arial",32))
        titleLabel.pack(anchor="n",pady=20)

        self.mainFrameButtons = ctk.CTkFrame(self.mainFrame, fg_color="transparent")


        myDepositsButton = ctk.CTkButton(self.mainFrameButtons,
                                        text="  My Savings Deposits  ",
                                        fg_color="transparent",
                                        corner_radius=30,
                                        border_width=2,
                                        border_spacing=6,
                                        border_color="#3d9bd7",
                                        command=self.showMyDeposits)
        myDepositsButton.pack(side=ctk.LEFT,expand=True,anchor="ne",padx=20)

        depositsOffersButton = ctk.CTkButton(self.mainFrameButtons,
                                        text="Available Savings Offers",
                                        fg_color="transparent",
                                        corner_radius=30,
                                        border_width=2,
                                        border_spacing=6,
                                        border_color="#3d9bd7",
                                        command=self.showDepositOffers)
        depositsOffersButton.pack(side=ctk.LEFT,expand=True,anchor="nw",padx=20)
        self.mainFrameButtons.pack()

        pathToDepositsPicture = "resources/deposits/mainframe.png"
        depositsImage = PhotoImage(file=pathToDepositsPicture)

        pictureLabel = ctk.CTkLabel(self.mainFrame, text="",image=depositsImage)
        pictureLabel.pack(side=ctk.BOTTOM,expand=True)


        #my savings deposits frame
        self.myDeposits = ctk.CTkFrame(self, fg_color="transparent")
        goBackButton = ctk.CTkButton(self.myDeposits,
                                    text="Back   ",
                                    image=arrowImage,
                                    fg_color="transparent",
                                    corner_radius=30,
                                    border_width=2,
                                    border_spacing=6,
                                    border_color="#3d9bd7",
                                    command=lambda: self.goBack(self.myDeposits))
        #goBackButton.grid(row=0,column=0,sticky="w",pady=3)
        goBackButton.grid(row=0,column=0,pady=3,sticky="w")

        titleLabel = ctk.CTkLabel(self.myDeposits, text="Active Deposits",font=("Arial",32))
        titleLabel.grid(row=1,column=0,columnspan=2,pady=20)
        #get my savings deposits from db
        self.mySavingsDeposits = getMySavingsDeposits(self.parent.account.Id)
        if self.mySavingsDeposits:
            self.myDepositsInfoFrame = ctk.CTkFrame(self.myDeposits, fg_color="transparent")
            endingDateLabel= ctk.CTkLabel(self.myDepositsInfoFrame, text="End Date",font=("Arial",24))
            amountLabel= ctk.CTkLabel(self.myDepositsInfoFrame, text="Amount",font=("Arial",24))
            interestRate=ctk.CTkLabel(self.myDepositsInfoFrame, text="Interest Rate",font=("Arial",24))
            interestCap=ctk.CTkLabel(self.myDepositsInfoFrame, text="Interest Capitalization",font=("Arial",24))
            endingDateLabel.grid(row=0,column=0,padx=15,pady=10)
            amountLabel.grid(row=0,column=1,padx=15,pady=10)
            interestRate.grid(row=0,column=2,padx=15,pady=10)
            interestCap.grid(row=0,column=3,padx=15,pady=10)

            for i,deposit in enumerate(self.mySavingsDeposits, start=1):
                currDeposit=getInfoOfMyOffers(deposit[0])[0]
                curr = str(getInfoOfMyOffers(deposit[0])[0][1])
                text = str(deposit[1]) +" "+curr
                myDepositId = deposit[0]
                amount = deposit[1]
                depositAmountLabel = ctk.CTkLabel(self.myDepositsInfoFrame, text=text,font=("Arial",20))
                depositAmountLabel.grid(row=i,column=1,pady=5)

                endDate=deposit[2].date()
                depositEndingDateLabel = ctk.CTkLabel(self.myDepositsInfoFrame, text=endDate,font=("Arial",20))
                depositEndingDateLabel.grid(row=i,column=0,pady=1)

                interestRate= str(currDeposit[5]) + "% " + str(currDeposit[6])
                depositInterestRateLabel = ctk.CTkLabel(self.myDepositsInfoFrame, text=interestRate,font=("Arial",20))
                depositInterestRateLabel.grid(row=i,column=2,pady=1)

                interestCapitalization = str(currDeposit[7])
                depositInterestCapLabel = ctk.CTkLabel(self.myDepositsInfoFrame, text=interestCapitalization,font=("Arial",20))
                depositInterestCapLabel.grid(row=i,column=3,pady=1)

                resignButton = ctk.CTkButton(self.myDepositsInfoFrame,text="Resign",
                                            fg_color="transparent",
                                            corner_radius=30,
                                            border_width=2,
                                            border_spacing=6,
                                            border_color="#ed460e",
                                            hover_color="#632410",
                                            command = lambda mydeposit = text,
                                            depositId = myDepositId,
                                            amount = amount,
                                            currency = curr:self.resign(mydeposit,depositId,amount,currency))
                resignButton.grid(row=i,column=5,pady=1)
                self.myDepositsInfoFrame.grid(row=2,column=0,columnspan=2)
        else:
            infoLabel = ctk.CTkLabel(self.myDeposits, text="You currently do not have any funds placed in savings deposits.\nYou can explore our offers in the adjacent tab."
                                     ,font=("Arial",20))
            infoLabel.grid(row=2,column=0,columnspan=2)

        self.myDeposits.grid_columnconfigure(0, weight=1)
        self.myDeposits.grid_columnconfigure(1, weight=1)

        # confirm resignation frame
        self.resignFrame = ctk.CTkFrame(self, fg_color="transparent")
        self.myDepositLabel = ctk.CTkLabel(self.resignFrame, text=self.myDeposit,font=("Arial",20))
        self.myDepositLabel.grid(row=0,column=0, columnspan = 2)
        confirmationLabel = ctk.CTkLabel(self.resignFrame, text="Are you sure you want to cancel the deposit? Early cancellation will result in the loss of interest.+fee 1%",
                                         font=("Arial",20))
        confirmationLabel.grid(row=1,column=0,columnspan = 2)
        self.myDepositStatusLabel = ctk.CTkLabel(self.resignFrame, text="",font=("Arial",20))
        self.myDepositStatusLabel.grid(row=2,column=0,columnspan=2)
        goBackButton = ctk.CTkButton(self.resignFrame, text="Cancel",command=lambda: self.goBackFromResign())
        goBackButton.grid(row=3,column=0,sticky="e")
        confirmResignation = ctk.CTkButton(self.resignFrame, text="Confirm resignation", command=lambda: self.confirmResignation(self.parent.account.Id, self.myDepositId))
        confirmResignation.grid(row=3,column=1,sticky="w")

        #savings deposits offers frame
        self.depositOffers = ctk.CTkFrame(self, fg_color="transparent")
        goBackButton = ctk.CTkButton(self.depositOffers, text="<-Back",command=lambda: self.goBack(self.depositOffers))
        goBackButton.grid(row=0,column=0,sticky="w")
        titleLabel = ctk.CTkLabel(self.depositOffers, text="oferty depozytow",font=("Arial",20))
        titleLabel.grid(row=1,column=0,columnspan=2,padx=20)
        balance = self.parent.account.Balance
        balanceLabel = ctk.CTkLabel(self.depositOffers, text=f"Your balance: {balance} PLN")
        balanceLabel.grid(row=2,column=0,columnspan=2,padx=20)
        myDepositOffers=getSavingsDepositOffers()
        takenIdList = getSavingsDepositTakenIds(self.parent.account.Id)
        takenIdList.sort()
        allIdList = getSavingsDepositOffersIds()
        for i,offer in enumerate(myDepositOffers, start=1):
            if(takenIdList == allIdList):
                infoLabel = ctk.CTkLabel(self.depositOffers, text="Unfortunately we do not have deposit offer available for you",font=("Arial",20))
                infoLabel.grid(row=i+3,column=0)
                break
            elif(i in takenIdList):
                pass
            else:
                offerLabel = ctk.CTkLabel(self.depositOffers, text=offer,font=("Arial",20))
                offerLabel.grid(row=i+3,column=0)
                selectButton = ctk.CTkButton(self.depositOffers,text="wybierz",command=lambda offerId=i :self.selectOffer(offerId))
                selectButton.grid(row=i+3,column=1)

        #confirm your offer
        self.confirmOffer = ctk.CTkFrame(self, fg_color="transparent")
        goBackButton = ctk.CTkButton(self.confirmOffer, text="<-Back",command=lambda :self.goBackFromConfirmation())
        goBackButton.grid(row=0,column=0,sticky="w")

        balance = self.parent.account.Balance
        balanceLabel = ctk.CTkLabel(self.confirmOffer, text=f"Your balance: {balance} PLN")
        balanceLabel.grid(row=2,column=0,columnspan=2,padx=20)

        amountLabel = ctk.CTkLabel(self.confirmOffer, text="Amount")
        amountLabel.grid(row=3,column=0)
        self.amountEntry = ctk.CTkEntry(self.confirmOffer,
                                          fg_color="transparent",
                                          border_width=2,
                                          border_color="#3d9bd7")
        self.amountEntry.grid(row=3,column=1)

        self.statusLabel = ctk.CTkLabel(self.confirmOffer, text="",text_color="#ff6633")
        self.statusLabel.grid(row=4,column=0)
        self.exchangeRate = ctk.CTkLabel(self.confirmOffer, text="")
        self.exchangeRate.grid(row=5,column=0)
        self.acceptOfferButton = ctk.CTkButton(self.confirmOffer, text="Accept offer")


        #packing stuff
        #self.mainFrame.pack(expand = True,fill=ctk.BOTH)
        self.mainFrame.pack(fill=ctk.BOTH, expand=True)
        #self.pack(expand = True,fill=ctk.BOTH)
        self.pack(fill=ctk.BOTH, expand=True)

    def goBackHome(self):
        self.pack_forget()
        self.parent.master.createMainPanel(self.parent.account.Id)

    def showMyDeposits(self):
        self.mainFrame.pack_forget()
        self.myDeposits.pack(fill=ctk.BOTH, expand=True)

    def showDepositOffers(self):
        self.mainFrame.pack_forget()
        self.depositOffers.pack()


    def selectOffer(self, newId):
        self.setId(newId)
        self.depositOffers.pack_forget()
        tupleId = self.offerId - 1
        selectedOffer = getSavingsDepositOffers()[tupleId]
        self.offerLabel = ctk.CTkLabel(self.confirmOffer, text=selectedOffer,font=("Arial",20))
        self.offerLabel.grid(row=1,column=1)
        currencyLabel = ctk.CTkLabel(self.confirmOffer, text='PLN',font=("Arial",20))
        currencyLabel.grid(row=3,column=2)
        self.confirmOffer.pack()
        self.update()


    def update(self):
        host = 'api.frankfurter.app'
        tupleId = self.offerId - 1
        to = getSavingsDepositOffers()[tupleId][1]
        self.statusLabel.configure(text="")
        if(self.amountEntry.get()==''):
            self.exchangeRate.configure(text='0.00 '+f'{to}')
        try:
            if(float(self.amountEntry.get())>=getSavingsDepositOffers()[tupleId][2] and
                     float(self.amountEntry.get())<=getSavingsDepositOffers()[tupleId][3] and
                     float(self.amountEntry.get())<=self.parent.account.Balance):
                self.statusLabel.configure(text="")
                response = requests.get(f'https://{host}/latest?amount={float(self.amountEntry.get())}&from=PLN&to={to}')
                self.exchangeRate.configure(text=str(float(response.json()['rates'][f'{to}'])) + " " + f'{to}')
                mysqlOfferId=self.offerId
                self.acceptOfferButton.configure(command=lambda:self.acceptOffer(mysqlOfferId,float(self.amountEntry.get()),
                                                                          response.json()['rates'][f'{to}']))
                self.acceptOfferButton.grid(row=6,column=0)
            elif(float(self.amountEntry.get())<getSavingsDepositOffers()[tupleId][2] or
                 float(self.amountEntry.get())>getSavingsDepositOffers()[tupleId][3]):
                minAmount = getSavingsDepositOffers()[tupleId][2]
                maxAmount = getSavingsDepositOffers()[tupleId][3]
                self.statusLabel.configure(text=f"min amount: {minAmount} max amount: {maxAmount}")
                self.exchangeRate.configure(text="")
                self.acceptOfferButton.grid_forget()
            else:
                self.statusLabel.configure(text="You do not have enough funds in your account")
        except requests.ConnectionError:
            self.statusLabel.configure(text="Connection error")
        except ValueError:
            if not self.amountEntry.get() == '':
                self.statusLabel.configure(text="You have to enter a number")
        self.updateProcessId = self.after(1000, self.update)

    def updateExchangeLabel(self, amount, fromCurrency):
        host = 'api.frankfurter.app'
        self.myDepositStatusLabel.configure(text="")
        try:
            self.myDepositStatusLabel.configure(text="")
            response = requests.get(f'https://{host}/latest?amount={amount}&from={fromCurrency}&to=PLN')
            amount=float(response.json()['rates'][f'PLN'])
            exchangedAmountAfterFee=amount*0.99
            self.myDepositStatusLabel.configure(text=str(exchangedAmountAfterFee) + " " + f'PLN')
            self.exchangedAmountPLN = exchangedAmountAfterFee
        except requests.ConnectionError:
            self.statusLabel.configure(text="Connection error")
        self.updateExhangeProcessId = self.after(100000, lambda: self.updateExchangeLabel(amount,fromCurrency))

    def goBackFromConfirmation(self):
        self.amountEntry.delete(0, ctk.END)
        self.exchangeRate.configure(text="")
        self.acceptOfferButton.grid_forget()
        self.offerLabel.grid_forget()
        self.confirmOffer.pack_forget()
        self.mainFrame.pack()
        self.after_cancel(self.updateProcessId)


    def acceptOffer(self, offerId, amount, exchangedAmount):
        acceptSavingDeposit(self.parent.account.Id, offerId, amount, exchangedAmount)
        self.after_cancel(self.updateProcessId)
        self.parent.account.Update()
        self.goBackHome()

    def goBack(self, frame):
        frame.pack_forget()
        self.mainFrame.pack()

    def setId(self, newId):
        self.offerId = newId

    def resign(self, text, depositId, amount, fromCurrency):
        self.myDeposit = text
        self.myDepositId = depositId
        self.myDepositLabel.configure(text=self.myDeposit)
        self.myDeposits.pack_forget()
        self.updateExchangeLabel(amount, fromCurrency)
        self.resignFrame.pack()

    # stop updating process 
    def goBackFromResign(self):
        self.after_cancel(self.updateExhangeProcessId)
        self.resignFrame.pack_forget()
        self.myDeposits.pack(fill=ctk.BOTH,expand=True)


    def confirmResignation(self, accountId, depositId):
        # get exchanged value and add it to balance in db, then refresh account 
        ResignDeposit(accountId, depositId, self.exchangedAmountPLN)
        self.resignFrame.pack_forget()
        self.myDeposits.destroy()
        self.parent.account.Update()
        self.goBackHome()
        self.after_cancel(self.updateExhangeProcessId)