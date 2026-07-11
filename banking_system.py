import sqlite3

DB = "banking_system.db"

class Bank:
    def __init__(self):
        self.conn = sqlite3.connect(DB)
        self.cur = self.conn.cursor()
        self.cur.execute("""CREATE TABLE IF NOT EXISTS accounts(
            account_number TEXT PRIMARY KEY,
            name TEXT,
            balance REAL)""")
        self.cur.execute("""CREATE TABLE IF NOT EXISTS transactions(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_number TEXT,
            details TEXT)""")
        self.conn.commit()

    def create(self, acc, name, balance):
        self.cur.execute("INSERT INTO accounts VALUES(?,?,?)", (acc, name, balance))
        self.conn.commit()

    def get(self, acc):
        self.cur.execute("SELECT * FROM accounts WHERE account_number=?", (acc,))
        return self.cur.fetchone()

    def update(self, acc, bal):
        self.cur.execute("UPDATE accounts SET balance=? WHERE account_number=?", (bal, acc))
        self.conn.commit()

    def delete(self, acc):
        self.cur.execute("DELETE FROM accounts WHERE account_number=?", (acc,))
        self.cur.execute("DELETE FROM transactions WHERE account_number=?", (acc,))
        self.conn.commit()

    def log(self, acc, msg):
        self.cur.execute("INSERT INTO transactions(account_number,details) VALUES(?,?)", (acc, msg))
        self.conn.commit()

    def history(self, acc):
        self.cur.execute("SELECT details FROM transactions WHERE account_number=?", (acc,))
        return [x[0] for x in self.cur.fetchall()]


def parse_amount(s):
    try:
        val = float(s)
        if val < 0:
            print("Amount cannot be negative.")
            return None
        return val
    except ValueError:
        print("Invalid amount.")
        return None


def create_account(bank):
    a = input("Account number: ").strip()
    n = input("Name: ").strip()
    if not a or not n:
        print("Account number and name are required.")
        return
    m = parse_amount(input("Initial balance: ").strip())
    if m is None:
        return
    try:
        bank.create(a, n, m)
        bank.log(a, f"Account created ₹{m}")
        print("Account created.")
    except sqlite3.IntegrityError:
        print("Account already exists.")


def deposit(bank):
    a = input("Account number: ").strip()
    row = bank.get(a)
    if not row:
        print("Account not found.")
        return
    m = parse_amount(input("Deposit amount: ").strip())
    if m is None:
        return
    bal = row[2] + m
    bank.update(a, bal)
    bank.log(a, f"Deposited ₹{m}")
    print(f"New balance: ₹{bal:.2f}")


def withdraw(bank):
    a = input("Account number: ").strip()
    row = bank.get(a)
    if not row:
        print("Account not found.")
        return
    m = parse_amount(input("Withdraw amount: ").strip())
    if m is None:
        return
    if m > row[2]:
        print("Insufficient balance.")
        return
    bal = row[2] - m
    bank.update(a, bal)
    bank.log(a, f"Withdrew ₹{m}")
    print(f"New balance: ₹{bal:.2f}")


def check_balance(bank):
    a = input("Account number: ").strip()
    row = bank.get(a)
    if row:
        print(f"Name: {row[1]} | Balance: ₹{row[2]:.2f}")
    else:
        print("Account not found.")


def show_history(bank):
    a = input("Account number: ").strip()
    h = bank.history(a)
    if not h:
        print("No transaction history found.")
        return
    print("--- History ---")
    for i in h:
        print(i)


def delete_account(bank):
    a = input("Account number: ").strip()
    if not bank.get(a):
        print("Account not found.")
        return
    confirm = input(f"Type 'yes' to confirm deleting account {a}: ").strip().lower()
    if confirm == "yes":
        bank.delete(a)
        print("Account deleted.")
    else:
        print("Cancelled.")


def list_accounts(bank):
    bank.cur.execute("SELECT account_number, name, balance FROM accounts")
    rows = bank.cur.fetchall()
    if not rows:
        print("No accounts found.")
        return
    print(f"{'Acc No':<15}{'Name':<20}{'Balance':<10}")
    print("-" * 45)
    for r in rows:
        print(f"{r[0]:<15}{r[1]:<20}₹{r[2]:.2f}")


MENU = """
==== Banking System ====
1. Create Account
2. Deposit
3. Withdraw
4. Check Balance
5. Transaction History
6. Delete Account
7. List All Accounts
8. Exit
"""

def main():
    bank = Bank()
    actions = {
        "1": create_account, "2": deposit, "3": withdraw,
        "4": check_balance, "5": show_history, "6": delete_account,
        "7": list_accounts,
    }
    while True:
        print(MENU)
        choice = input("Choose an option: ").strip()
        if choice == "8":
            print("Goodbye.")
            break
        action = actions.get(choice)
        if action:
            action(bank)
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()