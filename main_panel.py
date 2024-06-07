import time
import customtkinter as ctk
from account import Account

class MainWidgets(ctk.CTkFrame):
    def __init__(self,master, account):
        super().__init__(master)
        self.mainFrame = ctk.CTkFrame(self)
        self.balanceLabel = ctk.CTkLabel(self.mainFrame, text="Balance: "+ "{:.2f}".format(account.balance) ,font=("Arial",20))
        self.balanceLabel.pack(side=ctk.LEFT)

        self.testLabel = ctk.CTkLabel(self.mainFrame, text="123")
        self.testLabel.pack(side=ctk.RIGHT)
        #self.timeLabel = tkinter.Label(self.mainFrame,font=('Arial',20),fg="black",bg="#F9F7E6")
        #self.timeLabel.grid(row=1,column=0)

        #loginButton = ctk.CTkButton(self.mainFrame, text="show info",command=acc.listProfile)
        #loginButton.pack()

        #getBonusButton = ctk.CTkButton(self.mainFrame, text="Receive Start Bonus",command=acc.receiveStartBonus)
        #getBonusButton.pack()

        ############### Bar frame for pages
        #self.barFrame = ctk.CTkFrame(self,width=200,height=700)


        ############### Date frame
        #self.dateFrame = ctk.CTkFrame(self,width=1200,height=50)
        #self.timeLabel = ctk.CTkLabel(self.dateFrame,font=('Arial',15),text_color="black")
        #self.timeLabel.pack(side=ctk.RIGHT)




        ############### Packing frames and stuff
        #self.dateFrame.place(x=0,y=0)
        #self.barFrame.place(x=0,y=50)
        #self.dateFrame.place(x=0,y=0)
        self.mainFrame.pack(side=ctk.RIGHT)
        self.pack(expand = True)
        #self.update()

    def update(self):
        time_str = time.strftime("%H:%M:%S   %d-%m-%Y")
        self.timeLabel.configure(text=time_str)
        self.timeLabel.after(1000,self.update)