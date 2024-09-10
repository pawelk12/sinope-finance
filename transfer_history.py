import customtkinter as ctk
from tkinter import PhotoImage

class TransferHistoryWidgets(ctk.CTkFrame):
    def __init__(self, master, mainframe, history):
        super().__init__(master)
        self.parent = mainframe

        self.master.bind('<Escape>',self.goBack)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        pathToArrow = "resources/arrowLeft.png"

        arrowImage = PhotoImage(file=pathToArrow)
        goBackButton = ctk.CTkButton(self,
                                    text="Home   ",
                                    image=arrowImage,
                                    fg_color="transparent",
                                    corner_radius=30,
                                    border_width=2,
                                    border_spacing=6,
                                    border_color="#3d9bd7",command=self.goBack)
        goBackButton.grid(row=0,column=0,sticky="w",pady=3)

        titleLabel = ctk.CTkLabel(self, text="Transfer history",font=("Arial",32))
        titleLabel.grid(row=1,column=0,columnspan=2,pady=20)

        self.transferHistoryFrame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.transferHistoryFrame.configure(width=900, height=450)

        self.transferHistoryFrame.grid_columnconfigure(0, weight=1)
        self.transferHistoryFrame.grid_columnconfigure(1, weight=1)
        self.transferHistoryFrame.grid_columnconfigure(2, weight=1)
        self.transferHistoryFrame.grid_columnconfigure(3, weight=1)

        if not history:
            infoLabel = ctk.CTkLabel(self.transferHistoryFrame,text="    Your transfer history is empty.",font=("Arial",18),padx=20)
            infoLabel.grid(row=0,column=0,columnspan=4)

        i = 0
        for record in history:
            if (self.parent.account.BankAccNum == record[1]): # user sent money
                dateLabel = ctk.CTkLabel(self.transferHistoryFrame,text=str(record[4]),font=("Arial",18),padx=20)
                amountLabel = ctk.CTkLabel(self.transferHistoryFrame,text="-"+str("{:.2f}".format(record[3])+" PLN"),font=("Arial",18),padx=20)
                sentLabel = ctk.CTkLabel(self.transferHistoryFrame,text="sent to",font=("Arial",18),padx=20)
                receiverNumLabel = ctk.CTkLabel(self.transferHistoryFrame,text=str(record[2]),font=("Arial",18),padx=20)
                dateLabel.grid(row=i,column=0)
                amountLabel.grid(row=i,column=1)
                sentLabel.grid(row=i,column=2)
                receiverNumLabel.grid(row=i,column=3)

            elif (self.parent.account.BankAccNum == record[2]): #if user received money
                dateLabel = ctk.CTkLabel(self.transferHistoryFrame,text=str(record[4]),font=("Arial",18),padx=20)
                amountLabel = ctk.CTkLabel(self.transferHistoryFrame,text=str("{:.2f}".format(record[3])+" PLN"),font=("Arial",18),text_color = "#1a8e05",padx=20)
                receivedLabel = ctk.CTkLabel(self.transferHistoryFrame,text="received from",font=("Arial",18),padx=20)
                receiverNumLabel = ctk.CTkLabel(self.transferHistoryFrame,text=str(record[1]),font=("Arial",18),padx=20)
                dateLabel.grid(row=i,column=0)
                amountLabel.grid(row=i,column=1)
                receivedLabel.grid(row=i,column=2)
                receiverNumLabel.grid(row=i,column=3)

            i = i + 1

        self.transferHistoryFrame.grid(row=2,column=0,columnspan=2)
        self.pack(expand = True,fill=ctk.BOTH)

    def goBack(self,event=None):
        self.master.unbind('<Escape>')
        self.pack_forget()
        self.parent.master.createMainPanel(self.parent.account.Id)