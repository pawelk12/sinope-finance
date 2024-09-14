# Sinope Finance banking app

## Description
A simple desktop application for managing money, allowing users to transfer funds to other bank accounts and allocate their money into savings deposits in various currencies. 
The app includes key features inseparably linked to the account, such as updating personal details and viewing transfer history. 
It also offers a log list with dates and devices used for login.
Savings deposits provide an opportunity to protect savings from inflation and earn profit depending on currency exchange rates. However, early withdrawal will result in a loss of interest and a fee.

## Technologies Used
The project is built using:
- GUI: CustomTkinter, Tkinter
- Database: MySQL
- API: frankfurter

## Preparation
In order to use the application, an user must set up a local server environment, such as XAMPP, which includes Apache and MySQL. I recomend also creating a new virtual environment in Python for this project to avoid dependency conflicts.
After completing the steps mentioned above, and once the server and environment are started, you can install the required libraries by running the command:
```bash
pip install -r requirements.txt
```
## How to Run
To run the app, execute the following command:
```bash
python -u main.py
```
