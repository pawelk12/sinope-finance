import customtkinter as ctk
from db_service import Login as ReadFromDB, addLoginRecord
import hashlib

class LoginWidgets(ctk.CTkFrame):
    def __init__(self,master):
        super().__init__(master)

        self._fg_color= "#021639"
        self.master.configure(bg="#021639")
        self._border_width = 3
        self._border_color = "#3d9bd7"
        self._corner_radius = 32

        titleLabel = ctk.CTkLabel(self, text="Login to your bank account",font=("Arial",20))
        titleLabel.grid(row=0,column=2,columnspan=2,padx=20,pady=10)

        usernameLabel = ctk.CTkLabel(self,text="Username: ",width=20)
        usernameLabel.grid(row=1,column=2)
        self.usernameEntry = ctk.CTkEntry(self,
                                          fg_color="transparent",
                                          border_width=2,
                                          border_color="#3d9bd7")
        self.usernameEntry.grid(row=1,column=3)

        passwordLabel = ctk.CTkLabel(self,text="Password: ",width=20)
        passwordLabel.grid(row=2,column=2)
        self.passwordEntry = ctk.CTkEntry(self,
                                          show="*",
                                          fg_color="transparent",
                                          border_width=2,
                                          border_color="#3d9bd7")
        self.passwordEntry.grid(row=2,column=3,pady=5)

        self.statusLabel = ctk.CTkLabel(self, text="")
        self.statusLabel.grid(row=3,column=2,columnspan=2,padx=20)

        loginButton = ctk.CTkButton(self,
                                    text="Login",
                                    fg_color="transparent",
                                    corner_radius=30,
                                    border_width=2,
                                    border_spacing=6,
                                    border_color="#3d9bd7",
                                    command=self.Login)
        loginButton.grid(row=4,column=2,columnspan=2)

        SwitchToRegisterButton = ctk.CTkButton(self, text="Don't you have an account? Click here to register",
                                        fg_color ="transparent",hover=False,command=self.SwitchToRegister)
        SwitchToRegisterButton.grid(row=5,column=2,columnspan=2,padx=20,pady=10)

        self.pack(expand = True)


    def Login(self):
        
        account_id = ReadFromDB(self.usernameEntry.get(), hashlib.sha256(self.passwordEntry.get().encode()).hexdigest())
        if(account_id):
            self.statusLabel.configure(text="Logged successfully",text_color="#009900")
            addLoginRecord(account_id)
            self.pack_forget()

            # configuring window
            self.master.createMainPanel(ReadFromDB(self.usernameEntry.get(), hashlib.sha256(self.passwordEntry.get().encode()).hexdigest()))
            self.master.resizeAndCenter(1200,750)
            self.master.resizable(True, True)
            self.master.minsize(600,400)

        else:
            self.statusLabel.configure(text="Failed to log in",text_color="#ff6633")

    def SwitchToRegister(self):
        self.pack_forget()
        self.master.createRegisterPanel()