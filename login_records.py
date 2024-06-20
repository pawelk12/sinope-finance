import customtkinter as ctk
from db_service import Login


class LoginRecords(ctk.CTkScrollableFrame):
    def __init__(self,master, mainframe, login_history):
        super().__init__(master)
        
        self.parent = mainframe

        goBackButton = ctk.CTkButton(self, text="<-Back",command=self.goBack)
        goBackButton.grid(row=0,column=0,sticky="w")

        titleLabel = ctk.CTkLabel(self, text="Login history",font=("Arial",20))
        titleLabel.grid(row=1,column=0,padx=20)

        i = 0
        for record in login_history:
            recordLabel = ctk.CTkLabel(self,text=record[0],padx=20)
            recordLabel.grid(row=2+i,column=0)
            i = i + 1

        self.pack(expand = True) 

    def goBack(self):
        self.pack_forget()
        self.parent.accountWidgets()