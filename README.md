# Banking-System
import sqlite3
from sqlite3 import Error

class BankAccount:
    def __init__(self, account_number, name, initial_balance=0):
        self.account_number = account_number
        self.name = name
        self.balance = initial_balance
        self.transaction_history = []

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            self.transaction_history.append(f"Deposited: ₹{amount}")
            print(f"₹{amount} has been deposited. New balance: ₹{self.balance}")
        else:
            print("Invalid deposit amount")

    def withdraw(self, amount):
        if 0 < amount <= self.balance:
            self.balance -= amount
            self.transaction_history.append(f"Withdrew: ₹{amount}")
            print(f"₹{amount} has been withdrawn. New balance: ₹{self.balance}")
        else:
            print("Insufficient balance or invalid amount")

    def check_balance(self):
        print(f"Account Balance: ₹{self.balance}")

    def show_transaction_history(self):
        print("Transaction History:")
        for transaction in self.transaction_history:
            print(transaction)

class BankingSystem:
    def __init__(self):
        self.accounts = {}
        self.database = "banking_system.db"
        self.create_connection()
        self.create_table()

    def create_connection(self):
        try:
            self.conn = sqlite3.connect(self.database)
            self.cursor = self.conn.cursor()
            print("Database connected.")
        except Error as e:
            print(f"Error: {e}")

    def create_table(self):
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS accounts (
            account_number TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            balance REAL NOT NULL
        );
        """
        self.cursor.execute(create_table_sql)
        self.conn.commit()

    def add_account_to_db(self, account):
        sql = 'INSERT INTO accounts(account_number, name, balance) VALUES(?,?,?)'
        self.cursor.execute(sql, (account.account_number, account.name, account.balance))
        self.conn.commit()

    def update_account_in_db(self, account):
        """Update account balance in the database after deposit/withdraw."""
        sql = 'UPDATE accounts SET balance=? WHERE account_number=?'
        self.cursor.execute(sql, (account.balance, account.account_number))
        self.conn.commit()

    def remove_account_from_db(self, account_number):
        sql = 'DELETE FROM accounts WHERE account_number=?'
        self.cursor.execute(sql, (account_number,))
        self.conn.commit()

    def load_account_from_db(self, account_number):
        sql = 'SELECT * FROM accounts WHERE account_number=?'
        self.cursor.execute(sql, (account_number,))
        account_data = self.cursor.fetchone()
        if account_data:
            return BankAccount(account_data[0], account_data[1], account_data[2])
        return None

    def create_account(self, account_number, name, initial_balance=0):
        if account_number in self.accounts:
            print("Account number already exists!")
        else:
            account = BankAccount(account_number, name, initial_balance)
            self.accounts[account_number] = account
            self.add_account_to_db(account)
            print(f"Account for {name} created successfully with account number: {account_number}")

    def delete_account(self, account_number):
        if account_number in self.accounts:
            del self.accounts[account_number]
            self.remove_account_from_db(account_number)
            print(f"Account number {account_number} has been deleted.")
        else:
            print("Account not found!")

def main():
    system = BankingSystem()

    while True:
        print("\n--- Banking System ---")
        print("1. Create a new account")
        print("2. Deposit money")
        print("3. Withdraw money")
        print("4. Check balance")
        print("5. Show transaction history")
        print("6. Delete account")
        print("7. Exit")

        choice = input("Choose an option: ")

        if choice == '1':
            account_number = input("Enter account number: ")
            name = input("Enter account holder's name: ")
            initial_balance = float(input("Enter initial balance: "))
            system.create_account(account_number, name, initial_balance)

        elif choice == '2':
            account_number = input("Enter account number: ")
            account = system.load_account_from_db(account_number)
            if account:
                amount = float(input("Enter deposit amount: "))
                account.deposit(amount)
                system.update_account_in_db(account)  # Update balance in DB
                system.accounts[account_number] = account  # Update in memory
            else:
                print("Account not found!")

        elif choice == '3':
            account_number = input("Enter account number: ")
            account = system.load_account_from_db(account_number)
            if account:
                amount = float(input("Enter withdrawal amount: "))
                account.withdraw(amount)
                system.update_account_in_db(account)  # Update balance in DB
                system.accounts[account_number] = account  # Update in memory
            else:
                print("Account not found!")

        elif choice == '4':
            account_number = input("Enter account number: ")
            account = system.load_account_from_db(account_number)
            if account:
                account.check_balance()
            else:
                print("Account not found!")

        elif choice == '5':
            account_number = input("Enter account number: ")
            account = system.load_account_from_db(account_number)
            if account:
                account.show_transaction_history()
            else:
                print("Account not found!")

        elif choice == '6':
            account_number = input("Enter account number: ")
            system.delete_account(account_number)

        elif choice == '7':
            print("Exiting...")
            break

        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()
