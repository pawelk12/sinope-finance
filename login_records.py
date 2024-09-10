import customtkinter as ctk
from tkinter import PhotoImage

class LoginRecords(ctk.CTkFrame):
    def __init__(self,master, mainframe, login_history):
        super().__init__(master)
        
        self.parent = mainframe

        self.master.bind('<Escape>',self.goBack)

        pathToArrow = "resources/arrowLeft.png"
        arrowImage = PhotoImage(file=pathToArrow)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        goBackButton = ctk.CTkButton(self,
                                    text="Back   ",
                                    image=arrowImage,
                                    fg_color="transparent",
                                    corner_radius=30,
                                    border_width=2,
                                    border_spacing=6,
                                    border_color="#3d9bd7"
                                    ,command=self.goBack)
        goBackButton.grid(row=0,column=0,sticky="w",pady=3)

        titleLabel = ctk.CTkLabel(self, text="Login History",font=("Arial",32))
        titleLabel.grid(row=1,column=0,columnspan=2,pady=20)

        self.loginHistoryFrame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.loginHistoryFrame.configure(width=600, height=450)
        self.loginHistoryFrame.grid_columnconfigure(0,weight=1)
        self.loginHistoryFrame.grid_columnconfigure(1,weight=1)

        dateInfoLabel = ctk.CTkLabel(self.loginHistoryFrame, text="Date",font=("Arial",24),padx=20)
        deviceInfoLabel = ctk.CTkLabel(self.loginHistoryFrame, text="Device",font=("Arial",24),padx=20)
        dateInfoLabel.grid(row=0,column=0,sticky="e",pady=10)
        deviceInfoLabel.grid(row=0,column=1,sticky="w")

        i = 0
        for record in login_history:
            dateLabel = ctk.CTkLabel(self.loginHistoryFrame,text=str(record[0]),padx=20,font=("Arial",18))
            dateLabel.grid(row=i+1,column=0,sticky="e")
            deviceLabel = ctk.CTkLabel(self.loginHistoryFrame,text=record[1],padx=20,font=("Arial",18))
            deviceLabel.grid(row=i+1,column=1,sticky="w")
            i = i + 1
            if i > 49:
                break

        self.loginHistoryFrame.grid(row=2,column=0,columnspan=2)
        self.pack(expand = True,fill=ctk.BOTH) 

    def goBack(self,event=None):
        self.master.unbind('<Escape>')
        self.pack_forget()
        self.parent.accountWidgets()