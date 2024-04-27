import tkinter
from tkinter import ttk
from account import Account


class PersonalDetails(ttk.Frame):

    def __init__(self, master):
        super().__init__(master)
        
        self.title = tkinter.Label(self,text="Please enter your personal details to finish registration").grid(row=0,column=0,columnspan=2)

        firstnameLabel = tkinter.Label(self, text="Frist Name:")
        firstnameLabel.grid(row=1,column=0)
        self.firstnameEntry = tkinter.Entry(self)
        self.firstnameEntry.grid(row=1,column=1)

        lastnameLabel = tkinter.Label(self, text="Last name:")
        lastnameLabel.grid(row=2,column=0)
        self.lastnameEntry = tkinter.Entry(self)
        self.lastnameEntry.grid(row=2,column=1)

        emailLabel = tkinter.Label(self, text="E-mail:")
        emailLabel.grid(row=3,column=0)
        self.emailEntry = tkinter.Entry(self)
        self.emailEntry.grid(row=3,column=1)

        dateOfBirthLabel = tkinter.Label(self, text="Date of birthday(dd-mm-yyyy):")
        dateOfBirthLabel.grid(row=4,column=0)
        self.dateOfBirthEntry = tkinter.Entry(self)
        self.dateOfBirthEntry.grid(row=4,column=1)

        self.detailStatusLabel = tkinter.Label(self)
        self.detailStatusLabel.grid(row=5,column=0,columnspan=2)

        submitButton= tkinter.Button(self, text="submit", command=self.submit)
        submitButton.grid(row=6,column=0,columnspan=2)
        self.pack(expand=True)

    def submit(self):
        date = self.dateOfBirthEntry.get()
        # if text boxes are empty
        if(not self.firstnameEntry.get() or not self.lastnameEntry.get() or not self.emailEntry.get() or not self.dateOfBirthEntry.get()):
            self.detailStatusLabel.config(text="Ensure all fields are filled",fg="red")
        
        #check if name and surname contains only letters
        elif(not self.firstnameEntry.get().isalpha() or not self.lastnameEntry.get().isalpha()):
            self.detailStatusLabel.config(text="In the first and last name fields, you can only use letters",fg="red")
        # check if there are @ and . in email
        elif(not ('@' in self.emailEntry.get() and '.' in self.emailEntry.get())):
            self.detailStatusLabel.config(text="Invalid Email",fg="red")
            
        #check format dd-mm-yyyy 
        elif(not(date[2] == "-" and date[5] == "-"and date[:2].isdigit() and date[3:5].isdigit() 
                and date[6:10].isdigit() and len(date) == 10)):
            self.detailStatusLabel.config(text="Enter the date according to the format",fg="red")
        #check if date is reliable
        #
        #
        #
        #

        else:
            try:
                with open('data.txt', 'a') as file:
                    file.write(self.firstnameEntry.get() + "\n")
                    file.write(self.lastnameEntry.get() + "\n")
                    file.write(self.emailEntry.get() + "\n")
                    file.write(self.dateOfBirthEntry.get() + "\n")
                    

                    self.detailStatusLabel.config(text="Personal details filled successfuly.",fg = 'green')

                account = Account()
                self.master.createMainPanel(account)
                self.destroy()
                    
            except FileNotFoundError:
                    print("file not found")