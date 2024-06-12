from bank_application import BankApp
from db_service import disconnect

def main():
    try:
        app = BankApp("MyBankApp", "1200x800")
    finally:
        disconnect()


if __name__ == "__main__":
    main()