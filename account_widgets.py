import customtkinter as ctk
from personal_info import PersonalInfoWidgets
from login_records import LoginRecords
from db_service import getLoginRecords

class AccountWidgets(ctk.CTkFrame):
    def __init__(self,master, mainframe):
        super().__init__(master)

        self.parent = mainframe
        self.account = self.parent.account

        goBackButton = ctk.CTkButton(self, text="<-Back to Home",command=self.goBack)
        goBackButton.grid(row=0,column=0,sticky="w")

        editInfoButton = ctk.CTkButton(self, text="Edit personal information",command=self.editInfo)
        editInfoButton.grid(row=1,column=0)

        showLoginRecordsButton = ctk.CTkButton(self, text="Show account login history",command=self.showLoginRecords)
        showLoginRecordsButton.grid(row=1,column=1)


        self.pack(expand = True)

    def goBack(self):
        self.pack_forget()
        self.parent.master.createMainPanel(self.parent.account.id)

    def showLoginRecords(self):
        login_history = getLoginRecords(self.account.id)
        self.pack_forget()
        LoginRecordsFrame = LoginRecords(self.master, self, login_history)

    def editInfo(self):
        self.pack_forget()
        editInfoFrame = PersonalInfoWidgets(self.master, self)