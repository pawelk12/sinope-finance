import customtkinter as ctk

class TransferHistoryWidgets(ctk.CTkScrollableFrame):
    def __init__(self, master, mainframe, history):
        super().__init__(master)
        self.configure(width=500, height=300)
        self.parent = mainframe

        goBackButton = ctk.CTkButton(self, text="<-Back to Home",command=self.goBack)
        goBackButton.grid(row=0,column=0,sticky="w")

        titleLabel = ctk.CTkLabel(self, text="Transfer history",font=("Arial",20))
        titleLabel.grid(row=1,column=0,columnspan=2,padx=20)

        i = 0
        for record in history:
            if (self.parent.account.bankAccNum == record[1]): # user sent money
                sent = str(record[4]) + "\t" +str("{:.2f}".format(record[3])) + " PLN   sent to: " + str(record[2])
                recordLabel = ctk.CTkLabel(self,text=sent,padx=20)
            else:
                received = str(record[4]) + "\t" +str("{:.2f}".format(record[3])) + " PLN   received from: " + str(record[1])
                recordLabel = ctk.CTkLabel(self,text=received,padx=20)
                recordLabel.configure(text_color = "#1a8e05")
            recordLabel.grid(row=2+i,column=0,sticky="w")
            i = i + 1


        self.pack(expand = True)

    def goBack(self):
        self.pack_forget()
        self.parent.master.createMainPanel(self.parent.account.id)