import datetime
class Account:

    def __init__(self, accountId, username, firstName, lastName, email, birthDate, balance, startBonus, lastLogin, bankAccNum):
        
        self.__id = accountId
        self.__username = username
        self.__firstName = firstName
        self.__lastName = lastName
        self.__email = email
        self.__birthDate = birthDate
        self.__balance = balance
        self.__startBonus = startBonus
        self.__lastLogin = lastLogin
        self.__bankAccNum = bankAccNum

    @property
    def Id(self):
        return self.__id

    @Id.setter
    def Id(self, accountId):
        self.__id = accountId

    @property
    def Username(self):
        return self.__username
    
    @Username.setter
    def Username(self, username):
        self.__username = username

    @property
    def FirstName(self):
        return self.__firstName
    
    @FirstName.setter
    def FirstName(self, firstName):
        self.__firstName = firstName

    @property
    def LastName(self):
        return self.__lastName
    
    @LastName.setter
    def LastName(self, lastName):
        self.__lastName = lastName

    @property
    def Email(self):
        return self.__email
    
    @Email.setter
    def Email(self, email):
        self.__email = email

    @property
    def BirthDate(self):
        return self.__birthDate
    
    @BirthDate.setter
    def BirthDate(self, birthDate):
        self.__birthDate = birthDate

    @property
    def Balance(self):
        return self.__balance
    
    @Balance.setter
    def Balance(self, balance):
        self.__balance = balance

    @property
    def StartBonus(self):
        return self.__startBonus
    
    @StartBonus.setter
    def StartBonus(self, startBalance):
        self.__startBonus = startBalance

    @property
    def LastLogin(self):
        return self.__lastLogin
    
    @LastLogin.setter
    def LastLogin(self, lastLogin):
        self.__lastLogin = lastLogin

    @property
    def BankAccNum(self):
        return self.__bankAccNum
    
    @BankAccNum.setter
    def BankAccNum(self, bankAccNum):
        self.__bankAccNum = bankAccNum


    def update(self, accountId, login, firstName, lastName, email, birthDate, balance, startBonus, lastLogin, bankAccNum):
        self.__id = accountId
        self.__username = login
        self.__firstName = firstName
        self.__lastName = lastName
        self.__email = email
        self.__birthDate = birthDate
        self.__balance = balance
        self.__startBonus = startBonus
        self.__lastLogin = lastLogin
        self.__bankAccNum = bankAccNum
