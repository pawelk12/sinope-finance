import customtkinter as ctk
from db_service import getSavingsDepositOffers

class SavingsDepositsWidgets(ctk.CTkFrame):
    def __init__(self,master, mainframe):
        super().__init__(master)

        self.parent = mainframe


        #mainframe
        self.mainFrame = ctk.CTkFrame(self, fg_color="transparent")
        goBackButton = ctk.CTkButton(self.mainFrame, text="<-Back to Home",command=self.goBackHome)
        goBackButton.grid(row=0,column=0,sticky="w")

        titleLabel = ctk.CTkLabel(self.mainFrame, text="Savings Deposits in USD, CHF or EUR",font=("Arial",20))
        titleLabel.grid(row=1,column=0,columnspan=2,padx=20)

        myDepositsButton = ctk.CTkButton(self.mainFrame, text="show your deposits",command=self.showMyDeposits)
        myDepositsButton.grid(row=2,column=0,columnspan=2)

        depositsOffersButton = ctk.CTkButton(self.mainFrame, text="show available offers",command=self.showDepositOffers)
        depositsOffersButton.grid(row=2,column=1,columnspan=2)

        #my savings deposits frame

        self.myDeposits = ctk.CTkFrame(self, fg_color="transparent")
        goBackButton = ctk.CTkButton(self.myDeposits, text="<-Back",command=lambda: self.goBack(self.myDeposits))
        goBackButton.grid(row=0,column=0,sticky="w")
        titleLabel = ctk.CTkLabel(self.myDeposits, text="moje depozyty",font=("Arial",20))
        titleLabel.grid(row=1,column=0,columnspan=2,padx=20)


        #savings deposits offers frame
        self.depositOffers = ctk.CTkFrame(self, fg_color="transparent")
        goBackButton = ctk.CTkButton(self.depositOffers, text="<-Back",command=lambda: self.goBack(self.depositOffers))
        goBackButton.grid(row=0,column=0,sticky="w")
        titleLabel = ctk.CTkLabel(self.depositOffers, text="oferty depozytow",font=("Arial",20))
        titleLabel.grid(row=1,column=0,columnspan=2,padx=20)
        myDepositOffers=getSavingsDepositOffers()
        for i,offer in enumerate(myDepositOffers):
            offerLabel = ctk.CTkLabel(self.depositOffers, text=offer,font=("Arial",20))
            offerLabel.grid(row=i+2,column=0)
            selectButton = ctk.CTkButton(self.depositOffers,text="wybierz",command=lambda offerId=i+1 :self.selectOffer(offerId))
            selectButton.grid(row=i+2,column=1)


        #confirm your offer
        self.confirmOffer = ctk.CTkFrame(self, fg_color="transparent")
        goBackButton = ctk.CTkButton(self.confirmOffer, text="<-Back",command=lambda: self.goBack(self.confirmOffer))
        goBackButton.grid(row=0,column=0,sticky="w")
        amountLabel = ctk.CTkLabel(self.confirmOffer, text="Amount")
        amountLabel.grid(row=2,column=0)
        self.amountEntry = ctk.CTkEntry(self.confirmOffer,
                                          fg_color="transparent",
                                          border_width=2,
                                          border_color="#3d9bd7")
        self.amountEntry.grid(row=2,column=1)




        #packing stuff
        self.mainFrame.pack()
        self.pack(expand = True,fill=ctk.BOTH)

    def goBackHome(self):
        self.pack_forget()
        self.parent.master.createMainPanel(self.parent.account.Id)

    def showMyDeposits(self):
        self.mainFrame.pack_forget()
        self.myDeposits.pack()

    def showDepositOffers(self):
        self.mainFrame.pack_forget()
        self.depositOffers.pack()

    def selectOffer(self, offerId):
        self.depositOffers.pack_forget()
        selectedOffer = getSavingsDepositOffers()[offerId-1]
        offerLabel = ctk.CTkLabel(self.confirmOffer, text=selectedOffer,font=("Arial",20))
        offerLabel.grid(row=1,column=1)
        currencyLabel = ctk.CTkLabel(self.confirmOffer, text=selectedOffer[1],font=("Arial",20))
        currencyLabel.grid(row=2,column=3)
        self.confirmOffer.pack()

    def goBack(self, frame):
        frame.pack_forget()
        self.mainFrame.pack()
    