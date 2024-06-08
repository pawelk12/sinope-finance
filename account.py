import datetime
class Account:

    def __init__(self, account_id, login, firstName, lastName, email, birthDate, balance, startBonus, lastLogin, bankAccNum):
        
        self.id = account_id
        self.username = login
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.birthDate = birthDate
        self.balance = balance
        self.startBonus = startBonus
        self.lastLogin = lastLogin
        self.bankAccNum = bankAccNum

    def update(self, account_id, login, firstName, lastName, email, birthDate, balance, startBonus, lastLogin, bankAccNum):
        self.id = account_id
        self.username = login
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.birthDate = birthDate
        self.balance = balance
        self.startBonus = startBonus
        self.lastLogin = lastLogin
        self.bankAccNum = bankAccNum
