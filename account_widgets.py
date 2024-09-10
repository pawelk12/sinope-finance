import customtkinter as ctk
from personal_info import PersonalInfoWidgets
from login_records import LoginRecords
from db_service import getLoginRecords
from tkinter import PhotoImage

class AccountWidgets(ctk.CTkFrame):
    def __init__(self,master, mainframe):
        super().__init__(master)

        self.parent = mainframe

        self.master.bind('<Escape>',self.goBack)

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
        goBackButton.pack(anchor="nw",pady=3)

        titleLabel = ctk.CTkLabel(self, text="Account Widgets",font=("Arial",32))
        titleLabel.pack(anchor="n",pady=20)

        self.mainFrameButtons = ctk.CTkFrame(self, fg_color="transparent")

        editInfoButton = ctk.CTkButton(self.mainFrameButtons, text="Edit personal information",
                                        fg_color="transparent",
                                        corner_radius=30,
                                        border_width=2,
                                        border_spacing=6,
                                        border_color="#3d9bd7",
                                        command=self.editInfo)
        editInfoButton.pack(side=ctk.LEFT,expand=True,anchor="ne",padx=20)

        showLoginRecordsButton = ctk.CTkButton(self.mainFrameButtons,
                                        text="Show your login history",
                                        fg_color="transparent",
                                        corner_radius=30,
                                        border_width=2,
                                        border_spacing=6,
                                        border_color="#3d9bd7",
                                        command=self.showLoginRecords)
        showLoginRecordsButton.pack(side=ctk.LEFT,expand=True,anchor="nw",padx=20)
        self.mainFrameButtons.pack()

        pathToAccountWidgetsPicture = "resources/accountWidgets/accountWidgets.png"
        accountWidgetsImage = PhotoImage(file=pathToAccountWidgetsPicture)

        pictureLabel = ctk.CTkLabel(self, text="",image=accountWidgetsImage)
        pictureLabel.pack(side=ctk.BOTTOM,expand=True)


        self.pack(expand = True,fill=ctk.BOTH)

    def goBack(self,event=None):
        self.master.unbind('<Escape>')
        self.pack_forget()
        self.parent.master.createMainPanel(self.parent.account.Id)

    def showLoginRecords(self):
        login_history = getLoginRecords(self.parent.account.Id)
        self.master.unbind('<Escape>')
        self.pack_forget()
        LoginRecordsFrame = LoginRecords(self.master, self.parent, login_history)

    def editInfo(self):
        self.master.unbind('<Escape>')
        self.pack_forget()
        editInfoFrame = PersonalInfoWidgets(self.master, self.parent)