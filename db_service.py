import mysql.connector


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
        BALANCE FLOAT NOT NULL DEFAULT 0.00,\
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