import mysql.connector
import datetime
import requests


try:
    db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="")
    mycursor = db.cursor()
    mycursor.execute("CREATE DATABASE IF NOT EXISTS BankingAppDB;")
    mycursor.execute("USE BankingAppDB;")


    mycursor.execute("CREATE TABLE IF NOT EXISTS ACCOUNTS (\
        ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,\
        LOGIN VARCHAR(255) NOT NULL,\
        PASSWD VARCHAR(255) NOT NULL,\
        FIRST_NAME VARCHAR(255) NOT NULL,\
        LAST_NAME VARCHAR(255) NOT NULL,\
        EMAIL VARCHAR(255) NOT NULL,\
        DATE_OF_BIRTH DATE NOT NULL,\
        BALANCE DOUBLE NOT NULL DEFAULT 0.00,\
        START_BONUS BOOLEAN NOT NULL DEFAULT FALSE,\
        JOIN_DATE DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,\
        ACCOUNT_NUM BIGINT NOT NULL,\
        UNIQUE(ACCOUNT_NUM));")

    mycursor.execute("CREATE TABLE IF NOT EXISTS FUND_TRANSFERS (\
        TRANSFER_ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,\
        SENDER_NUM BIGINT NOT NULL,\
        RECEIVER_NUM BIGINT NOT NULL,\
        AMOUNT FLOAT NOT NULL,\
        DATE_OF_TRANSFER DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,\
        FOREIGN KEY (SENDER_NUM) REFERENCES ACCOUNTS(ACCOUNT_NUM),\
        FOREIGN KEY (RECEIVER_NUM) REFERENCES ACCOUNTS(ACCOUNT_NUM));")
    
    mycursor.execute("CREATE TABLE IF NOT EXISTS LOGIN_RECORDS (\
        LOG_ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,\
        USER_ID INT NOT NULL,\
        DATE_OF_LOGIN DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,\
        FOREIGN KEY (USER_ID) REFERENCES ACCOUNTS(ID));")

    mycursor.execute("CREATE TABLE IF NOT EXISTS DEPOSIT_OFFERS (\
        ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,\
        CURRENCY VARCHAR(255) NOT NULL,\
        MIN_AMOUNT FLOAT NOT NULL,\
        MAX_AMOUNT FLOAT NOT NULL,\
        DURATION VARCHAR(255) NOT NULL,\
        INTEREST_RATE FLOAT NOT NULL,\
        TYPE_OF_INTEREST_RATE VARCHAR(255) NOT NULL,\
        INTEREST_CAPITALIZATION VARCHAR(255) NOT NULL);")

    mycursor.execute("CREATE TABLE IF NOT EXISTS SAVINGS_DEPOSITS (\
        ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,\
        ACCOUNT_ID INT NOT NULL,\
        OFFER_ID INT NOT NULL,\
        AMOUNT FLOAT NOT NULL,\
        END_DATE DATETIME NOT NULL,\
        FOREIGN KEY (ACCOUNT_ID) REFERENCES ACCOUNTS(ID),\
        FOREIGN KEY (OFFER_ID) REFERENCES DEPOSIT_OFFERS(ID));")
    
    db.commit()
    mycursor.close()
    
except mysql.connector.Error:
    print("Error: " + str(mysql.connector.Error))
    quit()

def disconnect():
    db.close()


def Register(values):
    mycursor = db.cursor()
    sqlRegister = "INSERT INTO ACCOUNTS (LOGIN, PASSWD, FIRST_NAME, LAST_NAME, EMAIL, DATE_OF_BIRTH, ACCOUNT_NUM)\
          VALUES (%s, %s, %s, %s, %s, %s, %s)"
    

    mycursor.execute(sqlRegister, values)
    db.commit()
    mycursor.close()

def IfAccNumExists(accNum):
    mycursor = db.cursor()
    sqlIfAccNumExists = "SELECT 1 FROM ACCOUNTS WHERE ACCOUNT_NUM = %s"
    mycursor.execute(sqlIfAccNumExists, (accNum,))
    if mycursor.fetchone():
        mycursor.close()
        return True  #account number exists
    else:
        mycursor.close()
        return False #account number does not exist


def IfLoginExists(login):
    mycursor = db.cursor()
    sqlIfLoginExists = "SELECT 1 FROM ACCOUNTS WHERE LOGIN = %s"
    mycursor.execute(sqlIfLoginExists, (login,))
    if mycursor.fetchone():
        mycursor.close()
        return True  # if login exists
    else:
        mycursor.close()
        return False  # if login does not exist

def Login(login, hashed_passwd):
    mycursor = db.cursor()
    sqlLogin = "SELECT ID FROM ACCOUNTS\
                WHERE LOGIN = %s AND PASSWD = %s"
    mycursor.execute(sqlLogin, (login, hashed_passwd))
    account_id = mycursor.fetchone()
    if account_id:
        mycursor.close()
        return account_id[0]
    else:
        mycursor.close()
        return None


def GetData(account_id):
    mycursor = db.cursor()
    sqlGetData = "SELECT * FROM ACCOUNTS\
                  WHERE ID = %s"
    mycursor.execute(sqlGetData, (account_id,))
    data = mycursor.fetchall()
    mycursor.close()
    return data

def UpdateData(account_id):
    mycursor = db.cursor()
    sqlGetData = "SELECT LOGIN, EMAIL, BALANCE\
                  FROM ACCOUNTS\
                  WHERE ID = %s"
    mycursor.execute(sqlGetData, (account_id,))
    data = mycursor.fetchall()
    mycursor.close()
    return data


def TransferMoney(sender_id, receiver_accnum, amount):

    # if receiver exist
    mycursor = db.cursor()
    sqlIfAccountNumExists = "SELECT ID FROM ACCOUNTS WHERE ACCOUNT_NUM = %s"
    mycursor.execute(sqlIfAccountNumExists, (receiver_accnum,))
    receiver_id = mycursor.fetchone()

    sqlCheckSenderBalance = "SELECT BALANCE FROM ACCOUNTS WHERE ID = %s"
    mycursor.execute(sqlCheckSenderBalance, (sender_id,))
    sender_balance = mycursor.fetchone()[0]

    if(float(amount)<= 0.00):
        status = "Incorrect transfer amount value was provided"
        mycursor.close()
        return status

    if(sender_balance < float(amount) and receiver_id != None):
        status = "You do not have enough funds in your account"
        mycursor.close()
        return status
    elif(sender_balance > float(amount) and receiver_id != None):

        # transferring money
        mycursor.execute(("UPDATE ACCOUNTS\
                        SET BALANCE = BALANCE - %s\
                        WHERE ID = %s"), (float(amount), sender_id,))
        
        mycursor.execute(("UPDATE ACCOUNTS\
                        SET BALANCE = BALANCE + %s\
                        WHERE ACCOUNT_NUM = %s"), (float(amount), receiver_accnum,))
        
        db.commit()
        

        # adding transfer to transfer history table
        mycursor.execute(("SELECT ACCOUNT_NUM FROM ACCOUNTS\
                          WHERE ID = %s"), (sender_id,))
        sender_accnum = mycursor.fetchone()[0]

        mycursor.execute(("INSERT INTO FUND_TRANSFERS (SENDER_NUM, RECEIVER_NUM, AMOUNT)\
                          VALUES (%s, %s, %s )"), (sender_accnum, receiver_accnum, float(amount)))
        db.commit()

        status = "The transfer was successful"
        mycursor.close()
        return status
    else:
        status = "Invalid bank number"
        mycursor.close()
        return status


def GetTransferHistory(accNumber):
    mycursor = db.cursor()
    mycursor.execute(("SELECT * FROM FUND_TRANSFERS\
                      WHERE SENDER_NUM = %s OR RECEIVER_NUM = %s\
                      GROUP BY DATE_OF_TRANSFER DESC"),(accNumber, accNumber,))
    history = mycursor.fetchall()
    mycursor.close()
    return history

def EditPersonalInfo(account_id, new_login, new_email):
    mycursor = db.cursor()
    mycursor.execute(("UPDATE ACCOUNTS\
                      SET LOGIN = %s,\
                      EMAIL = %s\
                      WHERE ID = %s"), (new_login, new_email, account_id))
    db.commit()
    mycursor.close()

def addLoginRecord(account_id):
    mycursor = db.cursor()
    mycursor.execute("INSERT INTO LOGIN_RECORDS (USER_ID)\
                     VALUES (%s)",(account_id,))
    db.commit()
    mycursor.close()

def getLoginRecords(account_id):
    mycursor = db.cursor()
    mycursor.execute("SELECT DATE_OF_LOGIN\
                     FROM LOGIN_RECORDS\
                     WHERE USER_ID = %s\
                     ORDER BY DATE_OF_LOGIN DESC;", (account_id,))
    history = mycursor.fetchall()
    mycursor.close()
    return history

def setDepositsOffers():
    mycursor = db.cursor()
    mycursor.execute("SELECT COUNT(ID) AS NUMBER_OF_OFFERS FROM DEPOSIT_OFFERS;")
    numberOfOffers = mycursor.fetchone()[0]
    if numberOfOffers < 3:
        mycursor.execute("INSERT INTO DEPOSIT_OFFERS (CURRENCY,MIN_AMOUNT,MAX_AMOUNT,DURATION,INTEREST_RATE,TYPE_OF_INTEREST_RATE,\
                         INTEREST_CAPITALIZATION)\
                         VALUES ('EUR', 500.00, 10000.00, '90 days', 2.5, 'fixed rate', 'end of the period' );")
        mycursor.execute("INSERT INTO DEPOSIT_OFFERS (CURRENCY,MIN_AMOUNT,MAX_AMOUNT,DURATION,INTEREST_RATE,TYPE_OF_INTEREST_RATE,\
                         INTEREST_CAPITALIZATION)\
                         VALUES ('CHF', 2000.00, 50000.00, '180 days', 2.7, 'fixed rate', 'end of the period' );")
        mycursor.execute("INSERT INTO DEPOSIT_OFFERS (CURRENCY,MIN_AMOUNT,MAX_AMOUNT,DURATION,INTEREST_RATE,TYPE_OF_INTEREST_RATE,\
                         INTEREST_CAPITALIZATION)\
                         VALUES ('USD', 10000.00, 200000.00, '365 days', 3.3, 'fixed rate', 'end of the period' );")
        db.commit()
        mycursor.close()
    else:
        mycursor.close()

    
def getSavingsDepositOffers():
    mycursor = db.cursor()
    mycursor.execute("SELECT * FROM DEPOSIT_OFFERS")
    depositOffers = mycursor.fetchall()
    mycursor.close()
    return depositOffers


def getSavingsDepositTakenIds(accountId):
    try:
        dbcon = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        buffered=True)
        mycursor = dbcon.cursor()
        mycursor.execute("USE BankingAppDB;")
        mycursor.execute("SELECT DISTINCT OFFER_ID FROM SAVINGS_DEPOSITS\
                     WHERE ACCOUNT_ID = %s", (accountId,))
        ids = mycursor.fetchall()
        idList = [element[0] for element in ids]
        mycursor.close()
        return idList
    except mysql.connector.Error:
        print("Error: " + str(mysql.connector.Error))
        quit()
    finally:
        dbcon.close()

def getSavingsDepositOffersIds():
    mycursor = db.cursor()
    mycursor.execute("SELECT ID FROM DEPOSIT_OFFERS;")
    ids = mycursor.fetchall()
    idList = [element[0] for element in ids]
    mycursor.close()
    return idList

def acceptSavingDeposit(accountId, offerId, amount, exchangedAmount):
    #(account_id, offer_id, amount in exchanged currency)
    mycursor = db.cursor()
    # find duration of deposit from offer table
    mycursor.execute("SELECT DURATION FROM DEPOSIT_OFFERS\
                     WHERE ID = %s;", (offerId,))
    text = mycursor.fetchone()[0]
    durationList = text.split()
    duration = int(durationList[0])
    startDate = datetime.date.today()
    endDate = startDate + datetime.timedelta(days=duration)
    mycursor.execute("INSERT INTO SAVINGS_DEPOSITS (ACCOUNT_ID, OFFER_ID, AMOUNT, END_DATE)\
                     VALUES (%s, %s, %s, %s);", (accountId, offerId, exchangedAmount, endDate))
    mycursor.execute(("UPDATE ACCOUNTS\
                SET BALANCE = BALANCE - %s\
                WHERE ID = %s"), (float(amount), accountId,))
    db.commit()
    mycursor.close()


def getMySavingsDeposits(accountId):
    try:
        con = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        buffered=True)
        mycursor = con.cursor()
        mycursor.execute("USE BankingAppDB;")
        mycursor.execute("SELECT OFFER_ID, AMOUNT, END_DATE\
                     FROM SAVINGS_DEPOSITS\
                     WHERE ACCOUNT_ID = %s", (accountId,))
        output = mycursor.fetchall()
        mycursor.close()
        return output
    except mysql.connector.Error:
        print("Error: " + str(mysql.connector.Error))
        quit()
    finally:
        con.close()

def getCurrencyOfMyOffers(offerId):
    mycursor = db.cursor()
    mycursor.execute("SELECT CURRENCY\
                     FROM DEPOSIT_OFFERS\
                     WHERE ID = %s", (offerId,))
    currency = mycursor.fetchone()
    mycursor.close()
    return currency

def GetBalance(accountId):
    try:
        dbcon = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        buffered=True)
        mycursor = dbcon.cursor()
        mycursor.execute("USE BankingAppDB;")
        mycursor.execute("SELECT BALANCE FROM ACCOUNTS\
                     WHERE ID = %s", (accountId,))
        balance = mycursor.fetchone()
        mycursor.close()
        return balance
    except mysql.connector.Error:
        print("Error: " + str(mysql.connector.Error))
        quit()
    finally:
        dbcon.close()

def CheckSavings(accountId):
    try:
        dbcon = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        buffered=True)
        mycursor = dbcon.cursor()
        mycursor.execute("USE BankingAppDB;")
        mycursor.execute("SELECT * FROM SAVINGS_DEPOSITS\
                     WHERE ACCOUNT_ID = %s", (accountId,))
        myDeposits = mycursor.fetchall()
        for deposit in myDeposits:
            if deposit[4].date()<= datetime.date.today():
                #getting currency from deposit offer
                offerId = deposit[2]
                cursor = dbcon.cursor()
                cursor.execute("SELECT CURRENCY, INTEREST_RATE FROM DEPOSIT_OFFERS\
                               WHERE ID = %s", (offerId,))
                data = cursor.fetchall()[0]
                currency = data[0]
                interestRate = data[1]/100 + 1
                cursor.close()
                # currency, amount, saving depositId
                # + interest rate
                depositId = deposit[0]
                amountToExchangeToPLN = round(deposit[3]*interestRate,2)

                #exchange
                exchangedAmount = None
                host = 'api.frankfurter.app'
                try:    
                    response = requests.get(f'https://{host}/latest?amount={amountToExchangeToPLN}&from={currency}&to=PLN')
                    exchangedAmount = float(response.json()['rates'][f'PLN'])
                except requests.ConnectionError:
                    print("Connection error")
                # delete saving deposit and transfer money
                if exchangedAmount != None:
                    mycursor.execute("DELETE FROM SAVINGS_DEPOSITS\
                                     WHERE ID = %s", (depositId,))
                    dbcon.commit()
                    # transfer PLN to main deposit
                    mycursor.execute(("UPDATE ACCOUNTS\
                    SET BALANCE = BALANCE + %s\
                    WHERE ID = %s"),(exchangedAmount, accountId))
                    dbcon.commit()
        mycursor.close()
        return myDeposits
    except mysql.connector.Error:
        print("Error: " + str(mysql.connector.Error))
        quit()
    finally:
        dbcon.close()


def ResignDeposit(accountId, depositId, amount):
    try:
        dbcon = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        buffered=True)
        mycursor = dbcon.cursor()
        mycursor.execute("USE BankingAppDB;")
        mycursor.execute("DELETE FROM SAVINGS_DEPOSITS\
                            WHERE ACCOUNT_ID = %s AND OFFER_ID = %s", (accountId, depositId))
        mycursor.execute(("UPDATE ACCOUNTS\
                    SET BALANCE = BALANCE + %s\
                    WHERE ID = %s"),(amount, accountId))
        dbcon.commit()
        mycursor.close()
    except mysql.connector.Error:
        print("Error: " + str(mysql.connector.Error))
        quit()
    finally:
        dbcon.close()