import time
class Account:
    balance = 0.00
    startBonReceived =  False

    def __init__(self):
        
        data = self.getData()
        
        self.username = data[0]
        self.firstName = data[2]
        self.lastName = data[3]
        self.email = data[4]
        self.dateOfBirth = data[5]
        # Bank account number

    def getData(self):
        data = []
        try:
            with open('data.txt') as file:
                for line in file:
                    data.append(line.strip("\n"))
        except FileNotFoundError:
            print("file not found")
        return data
    
    #def updateProfile() - maybe email


    def receiveStartBonus(self):
        data = self.getData()
        # to be completed (write to file that bonus has been received and then button is disappearing or user gets message
        # that he cannot reclaim it
        #
        #
        #
        #
        '''if(not self.startBonReceived):
            self.balance += 300.0
            self.startBonReceived = True
            print("You received bonus")
        else:
            print("The starting bonus cannot be claimed again")'''
           

    def getLastLoginDate():
        pass


    def listProfile(self):

        print(str(self.balance) + "\n" + self.username + "\n" + self.firstName + "\n" + self.lastName + "\n" 
              + self.email + "\n" + self.dateOfBirth)
        

    def transferMoney(self, amount, name, lastname, bankAccNum):

        if(self.balance>=amount):
            self.balance -= amount
            try:
                with open('login_data.txt', 'a') as file:
                    file.write("-" + str(amount) + " " + name + " " + lastname + " " + bankAccNum + " " + time.strftime("%d-%m-%Y") + "\n")
            except FileNotFoundError:
                print("file not found")
            print("Transferred "+ "{:.2f}".format(self.amount) + "PLN to " + name + " " + lastname)
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

    # if not exists in file
    def generateBankAccNum():
        pass


    def getBankAccNum():
        pass
