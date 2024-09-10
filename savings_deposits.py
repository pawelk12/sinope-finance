import customtkinter as ctk
from db_service import getSavingsDepositOffers, getSavingsDepositOffersIds, acceptSavingDeposit, getSavingsDepositTakenIds,\
getMySavingsDeposits, getInfoOfMyOffers, ResignDeposit
import requests
from tkinter import PhotoImage

class SavingsDepositsWidgets(ctk.CTkFrame):
    def __init__(self,master, mainframe):
        super().__init__(master)

        self.parent = mainframe

        self.master.bind('<Escape>',self.goBackHome)

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

        goBackButton.grid(row=0,column=0,pady=3,sticky="w")

        titleLabel = ctk.CTkLabel(self.myDeposits, text="Active Deposits",font=("Arial",32))
        titleLabel.grid(row=1,column=0,columnspan=2,pady=20)
        #get my savings deposits from db
        self.mySavingsDeposits = getMySavingsDeposits(self.parent.account.Id)
        if self.mySavingsDeposits:
            self.myDepositsInfoFrame = ctk.CTkFrame(self.myDeposits, fg_color="transparent")
            endingDateLabel= ctk.CTkLabel(self.myDepositsInfoFrame, text="End Date",font=("Arial",22))
            amountLabel= ctk.CTkLabel(self.myDepositsInfoFrame, text="Amount",font=("Arial",22))
            interestRate=ctk.CTkLabel(self.myDepositsInfoFrame, text="Interest Rate",font=("Arial",22))
            interestCap=ctk.CTkLabel(self.myDepositsInfoFrame, text="Interest Capitalization",font=("Arial",22))
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
                depositAmountLabel = ctk.CTkLabel(self.myDepositsInfoFrame, text=text,font=("Arial",18))
                depositAmountLabel.grid(row=i,column=1,pady=5)

                endDate=deposit[2].date()
                depositEndingDateLabel = ctk.CTkLabel(self.myDepositsInfoFrame, text=endDate,font=("Arial",18))
                depositEndingDateLabel.grid(row=i,column=0,pady=1)

                interestRate= str(currDeposit[5]) + "% " + str(currDeposit[6])
                depositInterestRateLabel = ctk.CTkLabel(self.myDepositsInfoFrame, text=interestRate,font=("Arial",18))
                depositInterestRateLabel.grid(row=i,column=2,pady=1)

                interestCapitalization = str(currDeposit[7])
                depositInterestCapLabel = ctk.CTkLabel(self.myDepositsInfoFrame, text=interestCapitalization,font=("Arial",18))
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
        self.resignFrame.grid_columnconfigure(0, weight=1)
        self.resignFrame.grid_columnconfigure(1, weight=1)
        
        placeholderLabel = ctk.CTkLabel(self.resignFrame, text="",font=("Arial",32))
        placeholderLabel.grid(row=0,column=0)

        titleLabel = ctk.CTkLabel(self.resignFrame, text="Early Withdrawal",font=("Arial",32))
        titleLabel.grid(row=1,column=0,columnspan=2,pady=20)
    
        self.myDepositLabel = ctk.CTkLabel(self.resignFrame, text=self.myDeposit,font=("Arial",20))
        confirmationLabel = ctk.CTkLabel(self.resignFrame, text="Are you sure you want to cancel the deposit?",font=("Arial",20))
        confirmationLabel.grid(row=2,column=0,columnspan = 2)
        penaltyLabel = ctk.CTkLabel(self.resignFrame, text="Canceling early will result in a loss of interest and a 1% fee.",font=("Arial",20))
        penaltyLabel.grid(row=3,column=0,columnspan = 2)

        placeholerLabel = ctk.CTkLabel(self.resignFrame, text="",font=("Arial",20))
        placeholerLabel.grid(row=4,column=0)
        self.myDepositStatusLabel = ctk.CTkLabel(self.resignFrame, text="",font=("Arial",20))
        self.myDepositStatusLabel.grid(row=5,column=0,columnspan=2)
        goBackButton = ctk.CTkButton(self.resignFrame, text="Cancel",
                                     fg_color="transparent",
                                     corner_radius=30,
                                     border_width=2,
                                     border_spacing=6,
                                     border_color="#3d9bd7",
                                     command=lambda: self.goBackFromResign())
        goBackButton.grid(row=6,column=0,sticky="e",padx=4)
        confirmResignation = ctk.CTkButton(self.resignFrame, text="Confirm resignation",
                                           fg_color="transparent",
                                           corner_radius=30,
                                           border_width=2,
                                           border_spacing=6,
                                           border_color="#ed460e",
                                           hover_color="#632410",
                                           command=lambda: self.confirmResignation(self.parent.account.Id, self.myDepositId))
        confirmResignation.grid(row=6,column=1,sticky="w",padx=4)

        #savings deposits offers frame
        self.depositOffers = ctk.CTkFrame(self, fg_color="transparent")
        goBackButton = ctk.CTkButton(self.depositOffers,
                                    text="Back   ",
                                    image=arrowImage,
                                    fg_color="transparent",
                                    corner_radius=30,
                                    border_width=2,
                                    border_spacing=6,
                                    border_color="#3d9bd7",
                                    command=lambda: self.goBack(self.depositOffers))
        goBackButton.grid(row=0,column=0,pady=3,sticky="w")
        titleLabel = ctk.CTkLabel(self.depositOffers, text="Saving Deposit Offers",font=("Arial",32))
        titleLabel.grid(row=1,column=0,columnspan=2,pady=20)

        balance = self.parent.account.Balance
        balanceLabel = ctk.CTkLabel(self.depositOffers, text="Balance: {:.2f} PLN".format(balance),font=("Arial",18))
        myDepositOffers=getSavingsDepositOffers()
        takenIdList = getSavingsDepositTakenIds(self.parent.account.Id)
        takenIdList.sort()
        allIdList = getSavingsDepositOffersIds()

        self.availableOffersFrame = ctk.CTkFrame(self.depositOffers, fg_color="transparent")
        currencyLabel= ctk.CTkLabel(self.availableOffersFrame, text="Currency",font=("Arial",22))
        minmaxLabel= ctk.CTkLabel(self.availableOffersFrame, text="Min-Max",font=("Arial",22))
        durationLabel= ctk.CTkLabel(self.availableOffersFrame, text="Duration",font=("Arial",22))
        interestRate=ctk.CTkLabel(self.availableOffersFrame, text="Interest Rate",font=("Arial",22))
        interestCap=ctk.CTkLabel(self.availableOffersFrame, text="Interest Capitalization",font=("Arial",22))
        currencyLabel.grid(row=0,column=0,padx=15,pady=10)
        minmaxLabel.grid(row=0,column=1,padx=15,pady=10)
        durationLabel.grid(row=0,column=2,padx=15,pady=10)
        interestRate.grid(row=0,column=3,padx=15,pady=10)
        interestCap.grid(row=0,column=4,padx=15,pady=10)

        for i,offer in enumerate(myDepositOffers, start=1):
            if(takenIdList == allIdList):
                infoLabel = ctk.CTkLabel(self.depositOffers, text="Unfortunately, we do not have an available deposit offer for you.",font=("Arial",20))
                infoLabel.grid(row=2,column=0,columnspan=2)
                break
            elif(i in takenIdList):
                pass
            else:
                currency = offer[1]
                offerCurrencyLabel = ctk.CTkLabel(self.availableOffersFrame, text=currency,font=("Arial",18))
                offerCurrencyLabel.grid(row=i,column=0,pady=1)
                minmax=str(int(offer[2]))+"-"+str(int(offer[3]))+" PLN"
                offerMinmaxLabel = ctk.CTkLabel(self.availableOffersFrame, text=minmax,font=("Arial",18))
                offerMinmaxLabel.grid(row=i,column=1,pady=1)
                duration = offer[4] 
                offerDurationLabel = ctk.CTkLabel(self.availableOffersFrame, text=duration,font=("Arial",18))
                offerDurationLabel.grid(row=i,column=2,pady=1)
                interestRate=str(offer[5])+"% "+str(offer[6])
                offerInterestRateLabel= ctk.CTkLabel(self.availableOffersFrame, text=interestRate,font=("Arial",18))
                offerInterestRateLabel.grid(row=i,column=3,pady=1)
                interestCap = offer[7]
                offerInterestCap = ctk.CTkLabel(self.availableOffersFrame, text=interestCap,font=("Arial",18))
                offerInterestCap.grid(row=i,column=4,pady=1)

                selectButton = ctk.CTkButton(self.availableOffersFrame,text="Select Offer",
                                            fg_color="transparent",
                                            corner_radius=30,
                                            border_width=2,
                                            border_spacing=6,
                                            border_color="#0ec41d",
                                            hover_color="#16631c",
                                            command=lambda offerId=i :self.selectOffer(offerId))
                selectButton.grid(row=i,column=5,pady=1)
                self.availableOffersFrame.grid(row=2,column=0,columnspan=2)
                balanceLabel.grid(row=3,column=0,columnspan=2,pady=30)

        self.depositOffers.grid_columnconfigure(0, weight=1)
        self.depositOffers.grid_columnconfigure(1, weight=1)

        #confirm your offer
        self.confirmOffer = ctk.CTkFrame(self, fg_color="transparent")
        self.confirmOffer.grid_columnconfigure(0, weight=1)
        self.confirmOffer.grid_columnconfigure(1, weight=1)

        goBackButton = ctk.CTkButton(self.confirmOffer,
                                     text="Back   ",
                                     image=arrowImage,
                                     fg_color="transparent",
                                     corner_radius=30,
                                     border_width=2,
                                     border_spacing=6,
                                     border_color="#3d9bd7",
                                     command=lambda :self.goBackFromConfirmation())
        goBackButton.grid(row=0,column=0,sticky="w",pady=3)

        titleLabel = ctk.CTkLabel(self.confirmOffer, text="Confirm Offer",font=("Arial",32))
        titleLabel.grid(row=1,column=0,columnspan=6,pady=20)

        self.offerInfo = ctk.CTkFrame(self.confirmOffer, fg_color="transparent")
        self.offerInfo.grid(row=2,column=0,columnspan=2)


        self.exchangeFrame = ctk.CTkFrame(self.confirmOffer, fg_color="transparent")
        self.exchangeFrame._border_width = 3
        self.exchangeFrame._border_color = "#3d9bd7"
        self.exchangeFrame._corner_radius = 32

        self.exchangeFrame.grid(row=3,column=0,columnspan=2,pady=10)

        amountLabel = ctk.CTkLabel(self.exchangeFrame, text="Please enter amount:",font=("Arial",18))
        amountLabel.grid(row=0,column=0,sticky="e",padx=15,pady=10)

        self.amountEntry = ctk.CTkEntry(self.exchangeFrame,
                                          fg_color="transparent",
                                          border_width=2,
                                          border_color="#3d9bd7",font=("Arial",16))
        self.amountEntry.grid(row=0,column=1,padx=5)

        self.statusLabel = ctk.CTkLabel(self.exchangeFrame, text="",text_color="#ff6633")
        self.statusLabel.grid(row=2,column=0,columnspan=3)
        self.exchangeRate = ctk.CTkLabel(self.exchangeFrame, text="",font=("Arial",18))
        self.exchangeRate.grid(row=3,column=0,pady=10,columnspan=3)
        self.acceptOfferButton = ctk.CTkButton(self.exchangeFrame, text="Accept Offer",
                                               fg_color="transparent",
                                                corner_radius=30,
                                                border_width=2,
                                                border_spacing=6,
                                                border_color="#0ec41d",
                                                hover_color="#16631c",)


        #packing stuff

        self.mainFrame.pack(fill=ctk.BOTH, expand=True)
        self.pack(fill=ctk.BOTH, expand=True)

    def goBackHome(self,event=None):
        self.master.unbind('<Escape>')
        self.pack_forget()
        self.parent.master.createMainPanel(self.parent.account.Id)

    def showMyDeposits(self):
        self.master.unbind('<Escape>')
        self.master.bind('<Escape>',lambda event: self.goBack(self.myDeposits))
        self.mainFrame.pack_forget()
        self.myDeposits.pack(fill=ctk.BOTH, expand=True)

    def showDepositOffers(self):
        self.master.unbind('<Escape>')
        self.master.bind('<Escape>',lambda event: self.goBack(self.depositOffers))
        self.mainFrame.pack_forget()
        self.depositOffers.pack(fill=ctk.BOTH, expand=True)


    def selectOffer(self, newId):
        self.setId(newId)
        self.depositOffers.pack_forget()
        self.master.unbind('<Escape>')
        self.master.bind('<Escape>',self.goBackFromConfirmation)

        currencyTitleLabel= ctk.CTkLabel(self.offerInfo, text="Currency",font=("Arial",22))
        minmaxLabel= ctk.CTkLabel(self.offerInfo, text="Min-Max",font=("Arial",22))
        durationLabel= ctk.CTkLabel(self.offerInfo, text="Duration",font=("Arial",22))
        interestRate=ctk.CTkLabel(self.offerInfo, text="Interest Rate",font=("Arial",22))
        interestCap=ctk.CTkLabel(self.offerInfo, text="Interest Capitalization",font=("Arial",22))
        currencyTitleLabel.grid(row=0,column=0,padx=15,pady=10)
        minmaxLabel.grid(row=0,column=1,padx=15,pady=10)
        durationLabel.grid(row=0,column=2,padx=15,pady=10)
        interestRate.grid(row=0,column=3,padx=15,pady=10)
        interestCap.grid(row=0,column=4,padx=15,pady=10)

        tupleId = self.offerId - 1
        offer = getSavingsDepositOffers()[tupleId]
        currency = offer[1]
        self.offerCurrencyLabel = ctk.CTkLabel(self.offerInfo, text=currency,font=("Arial",18))
        self.offerCurrencyLabel.grid(row=1,column=0,pady=1)
        minmax=str(int(offer[2]))+"-"+str(int(offer[3]))+" PLN"
        self.offerMinmaxLabel = ctk.CTkLabel(self.offerInfo, text=minmax,font=("Arial",18))
        self.offerMinmaxLabel.grid(row=1,column=1,pady=1)
        duration = offer[4] 
        self.offerDurationLabel = ctk.CTkLabel(self.offerInfo, text=duration,font=("Arial",18))
        self.offerDurationLabel.grid(row=1,column=2,pady=1)
        interestRate=str(offer[5])+"% "+str(offer[6])
        self.offerInterestRateLabel= ctk.CTkLabel(self.offerInfo, text=interestRate,font=("Arial",18))
        self.offerInterestRateLabel.grid(row=1,column=3,pady=1)
        interestCap = offer[7]
        self.offerInterestCap = ctk.CTkLabel(self.offerInfo, text=interestCap,font=("Arial",18))
        self.offerInterestCap.grid(row=1,column=4,pady=1)


        self.currencyLabel = ctk.CTkLabel(self.exchangeFrame, text='PLN',font=("Arial",18))
        self.currencyLabel.grid(row=0,column=2,sticky="w",padx=15,pady=10)
        self.confirmOffer.pack(fill=ctk.BOTH,expand=True)
        self.update()


    def update(self):
        host = 'api.frankfurter.app'
        tupleId = self.offerId - 1
        to = getSavingsDepositOffers()[tupleId][1]
        self.statusLabel.configure(text="")
        self.acceptOfferButton.grid_forget()
        self.master.unbind('<Return>')
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
                self.acceptOfferButton.grid(row=4,column=0,columnspan=3,pady=10)
                self.master.bind('<Return>',lambda event:self.acceptOffer(mysqlOfferId,float(self.amountEntry.get()),
                                                                          response.json()['rates'][f'{to}']))
            elif(float(self.amountEntry.get())<getSavingsDepositOffers()[tupleId][2] or
                 float(self.amountEntry.get())>getSavingsDepositOffers()[tupleId][3]):
                minAmount = getSavingsDepositOffers()[tupleId][2]
                maxAmount = getSavingsDepositOffers()[tupleId][3]
                self.statusLabel.configure(text=f"min amount: {minAmount}, max amount: {maxAmount}")
                self.exchangeRate.configure(text="")
                self.acceptOfferButton.grid_forget()
                self.master.unbind('<Return>')
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
            exchangedAmountAfterFee=(amount*0.99)
            exchangedAmountAfterFee=round(exchangedAmountAfterFee,2)
            self.myDepositStatusLabel.configure(text="You will get back: "+str(exchangedAmountAfterFee) + " " + f'PLN')
            self.exchangedAmountPLN = exchangedAmountAfterFee
        except requests.ConnectionError:
            self.statusLabel.configure(text="Connection error")
        self.updateExhangeProcessId = self.after(100000, lambda: self.updateExchangeLabel(amount,fromCurrency))

    def goBackFromConfirmation(self,event=None):
        self.master.unbind('<Escape>')
        self.master.unbind('<Return>')
        self.master.bind('<Escape>',self.goBackHome)
        self.amountEntry.delete(0, ctk.END)
        self.exchangeRate.configure(text="")
        self.acceptOfferButton.grid_forget()
        self.offerCurrencyLabel.grid_forget()
        self.offerCurrencyLabel.grid_forget()
        self.offerMinmaxLabel.grid_forget()
        self.offerDurationLabel.grid_forget()
        self.offerInterestRateLabel.grid_forget()
        self.offerInterestCap.grid_forget()
        self.currencyLabel.grid_forget()
        self.confirmOffer.pack_forget()
        self.mainFrame.pack(fill=ctk.BOTH,expand=True)
        self.after_cancel(self.updateProcessId)


    def acceptOffer(self, offerId, amount, exchangedAmount, event=None):
        self.master.unbind('<Escape>')
        self.master.unbind('<Return>')
        acceptSavingDeposit(self.parent.account.Id, offerId, amount, exchangedAmount)
        self.after_cancel(self.updateProcessId)
        self.parent.account.Update()
        self.goBackHome()

    def goBack(self, frame,event=None):
        self.master.unbind('<Escape>')
        self.master.bind('<Escape>',self.goBackHome)
        frame.pack_forget()
        self.mainFrame.pack(fill=ctk.BOTH,expand=True)

    def setId(self, newId):
        self.offerId = newId

    def resign(self, text, depositId, amount, fromCurrency):
        self.master.unbind('<Escape>')
        self.master.bind('<Escape>',self.goBackFromResign)
        self.myDeposit = text
        self.myDepositId = depositId
        self.myDepositLabel.configure(text=self.myDeposit)
        self.myDeposits.pack_forget()
        self.updateExchangeLabel(amount, fromCurrency)
        self.resignFrame.pack(fill=ctk.BOTH,expand=True)

    # stop updating process 
    def goBackFromResign(self, event=None):
        self.master.unbind('<Escape>')
        self.master.bind('<Escape>',lambda event: self.goBack(self.myDeposits))
        self.after_cancel(self.updateExhangeProcessId)
        self.resignFrame.pack_forget()
        self.myDeposits.pack(fill=ctk.BOTH,expand=True)


    def confirmResignation(self, accountId, depositId):
        # get exchanged value and add it to balance in db, then refresh account 
        ResignDeposit(accountId, depositId, self.exchangedAmountPLN)
        self.master.unbind('<Escape>')
        self.resignFrame.pack_forget()
        self.myDeposits.destroy()
        self.parent.account.Update()
        self.goBackHome()
        self.after_cancel(self.updateExhangeProcessId)