from bank_application import BankApp
from db_service import disconnect, setDepositsOffers

def main():
    try:
        setDepositsOffers()
        app = BankApp("SinopeFinance", "1200x800", "resources/icon.png")
    finally:
        disconnect()


if __name__ == "__main__":
    main()