import time
class Account:
    balance = 0.00
    startBonReceived =  False

    def __init__(self, username, firstName, lastName, email, dateOfBirth):
        self.username = username
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.dateOfBirth = dateOfBirth
        # Bank account number


    
    #def updateProfile() - maybe email

    def receiveStartBonus(self):
        if(not self.startBonReceived):
            self.balance += 300.0
            self.startBonReceived = True
            print("You received bonus")
        else:
            print("The starting bonus cannot be claimed again")
           

    def getLastLoginDate():
        pass


    def listProfile(self):
        print(self.balance)
        print(self.username)
        print(self.firstName)
        print(self.lastName)
        print(self.email)
        print(self.dateOfBirth)


    def transferMoney(self, amount, name, lastname, bankAccNum):

        if(self.balance>=amount):
            self.balance -= amount
            try:
                with open('login_data.txt', 'a') as file:
                    file.write("-" + str(amount) + " " + name + " " + lastname + " " + bankAccNum + " " + time.strftime("%d-%m-%Y") + "\n")
            except FileNotFoundError:
                print("file not found")
            print("Transferred "+ "{:.2f}".format(self.balance) + "PLN to " + name + " " + lastname)
            print("Current balance: " + "{:.2f}".format(self.balance))


        else:
            print("You do not have sufficient funds to make transfer")


    def showHistory():
        pass


    def showBalance(self):
        print("{:.2f}".format(self.balance))


    def deposit(self,amount):
        if(amount > 0.0):
            self.balance += amount
        else:
            pass # clear entry box, show message

    # def withdraw()

    def generateBankAccNum():
        pass


    def getBankAccNum():
        pass
