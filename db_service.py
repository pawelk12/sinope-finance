import mysql.connector
import hashlib

db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="BankingAppDB"
)

mycursor = db.cursor()

def Register(values):
    sqlRegister = "INSERT INTO ACCOUNTS (LOGIN, PASSWD, FIRST_NAME, LAST_NAME, EMAIL, DATE_OF_BIRTH, ACCOUNT_NUM)\
          VALUES (%s, %s, %s, %s, %s, %s, %s)"
    

    mycursor.execute(sqlRegister, values)
    db.commit()


def GetSecrets():
    mycursor.execute("SELECT LOGIN, PASSWD FROM ACCOUNTS;")
    secrets = mycursor.fetchall()   #tuples('login', 'passwd')
    for secret in secrets:
        print(secret)       


def IfLoginExists(login):
    sqlIfLoginExists = "SELECT 1 FROM ACCOUNTS WHERE LOGIN = %s"
    mycursor.execute(sqlIfLoginExists, (login,))
    if mycursor.fetchone():
        return True  # if login exists
    else:
        return False  # if login does not exist

def Login(login, hashed_passwd):
    sqlLogin = "SELECT ID FROM ACCOUNTS\
                WHERE LOGIN = %s AND PASSWD = %s"
    mycursor.execute(sqlLogin, (login, hashed_passwd))
    account_id = mycursor.fetchone()
    if account_id:
        return account_id[0]
    else:
        return None


def GetData(account_id):
    sqlGetData = "SELECT * FROM ACCOUNTS\
                  WHERE ID = %s"
    mycursor.execute(sqlGetData, (account_id,))
    data = mycursor.fetchall()
    return data



#########
# + condition if user did not enter his own account numer
def TransferMoney(sender_id, receiver_accnum, amount):

    # if receiver exist
    sqlIfAccountNumExists = "SELECT ID FROM ACCOUNTS WHERE ACCOUNT_NUM = %s"
    mycursor.execute(sqlIfAccountNumExists, (receiver_accnum,))
    receiver_id = mycursor.fetchone()

    sqlCheckSenderBalance = "SELECT BALANCE FROM ACCOUNTS WHERE ID = %s"
    mycursor.execute(sqlCheckSenderBalance, (sender_id,))
    sender_balance = mycursor.fetchone()[0]

    if(float(amount)<= 0.00):
        status = "Incorrect transfer amount value was provided"
        return status

    if(sender_balance < float(amount) and receiver_id != None):
        status = "You do not have enough funds in your account"
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
        return status
    else:
        status = "Invalid bank number"
        return status


def GetTransferHistory(accNumber):
    mycursor.execute(("SELECT * FROM FUND_TRANSFERS\
                      WHERE SENDER_NUM = %s OR RECEIVER_NUM = %s\
                      GROUP BY DATE_OF_TRANSFER DESC"),(accNumber, accNumber,))
    history = mycursor.fetchall()
    return history

def EditPersonalInfo(account_id, new_login, new_email):
    mycursor.execute(("UPDATE ACCOUNTS\
                      SET LOGIN = %s,\
                      EMAIL = %s\
                      WHERE ID = %s"), (new_login, new_email, account_id))
    db.commit()