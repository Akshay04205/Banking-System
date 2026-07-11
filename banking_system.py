import tkinter as tk
from tkinter import messagebox, scrolledtext
import sqlite3

DB="banking_system.db"

class Bank:
    def __init__(self):
        self.conn=sqlite3.connect(DB)
        self.cur=self.conn.cursor()
        self.cur.execute("""CREATE TABLE IF NOT EXISTS accounts(
            account_number TEXT PRIMARY KEY,
            name TEXT,
            balance REAL)""")
        self.cur.execute("""CREATE TABLE IF NOT EXISTS transactions(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_number TEXT,
            details TEXT)""")
        self.conn.commit()

    def create(self,acc,name,balance):
        self.cur.execute("INSERT INTO accounts VALUES(?,?,?)",(acc,name,balance))
        self.conn.commit()

    def get(self,acc):
        self.cur.execute("SELECT * FROM accounts WHERE account_number=?",(acc,))
        return self.cur.fetchone()

    def update(self,acc,bal):
        self.cur.execute("UPDATE accounts SET balance=? WHERE account_number=?",(bal,acc))
        self.conn.commit()

    def delete(self,acc):
        self.cur.execute("DELETE FROM accounts WHERE account_number=?",(acc,))
        self.cur.execute("DELETE FROM transactions WHERE account_number=?",(acc,))
        self.conn.commit()

    def log(self,acc,msg):
        self.cur.execute("INSERT INTO transactions(account_number,details) VALUES(?,?)",(acc,msg))
        self.conn.commit()

    def history(self,acc):
        self.cur.execute("SELECT details FROM transactions WHERE account_number=?",(acc,))
        return [x[0] for x in self.cur.fetchall()]

bank=Bank()

root=tk.Tk()
root.title("Banking System")
root.geometry("500x600")

def val():
    return acc.get().strip(), name.get().strip(), amt.get().strip()

def out(msg):
    txt.insert(tk.END,msg+"\n"); txt.see(tk.END)

def parse_amount(m):
    try:
        return float(m)
    except ValueError:
        messagebox.showerror("Error","Invalid amount")
        return None

def create():
    a,n,m=val()
    if not a or not n:
        return messagebox.showerror("Error","Account number and name are required")
    m=parse_amount(m)
    if m is None: return
    try:
        bank.create(a,n,m); bank.log(a,f"Account created ₹{m}"); out("Account created.")
    except sqlite3.IntegrityError:
        messagebox.showerror("Error","Account exists")

def deposit():
    a,_,m=val()
    row=bank.get(a)
    if not row: return messagebox.showerror("Error","Account not found")
    m=parse_amount(m)
    if m is None: return
    bal=row[2]+m
    bank.update(a,bal); bank.log(a,f"Deposited ₹{m}")
    out(f"Balance: ₹{bal:.2f}")

def withdraw():
    a,_,m=val()
    row=bank.get(a)
    if not row: return messagebox.showerror("Error","Account not found")
    m=parse_amount(m)
    if m is None: return
    if m>row[2]: return messagebox.showerror("Error","Insufficient balance")
    bal=row[2]-m
    bank.update(a,bal); bank.log(a,f"Withdrew ₹{m}")
    out(f"Balance: ₹{bal:.2f}")

def balance():
    a,_,_=val(); row=bank.get(a)
    if row: out(f"Balance: ₹{row[2]:.2f}")
    else: messagebox.showerror("Error","Account not found")

def history():
    a,_,_=val()
    h=bank.history(a)
    if not h:
        out("No transaction history found.")
        return
    out("History:")
    for i in h: out(i)

def delete():
    a,_,_=val()
    if not a:
        return messagebox.showerror("Error","Enter an account number")
    if not messagebox.askyesno("Confirm","Delete this account and its history?"):
        return
    bank.delete(a); out("Account deleted")

def reset():
    acc.delete(0, tk.END)
    name.delete(0, tk.END)
    amt.delete(0, tk.END)
    txt.delete("1.0", tk.END)

for t in ("Account Number","Name","Amount"):
    tk.Label(root,text=t).pack()
    e=tk.Entry(root,width=35)
    e.pack()
    if t=="Account Number": acc=e
    elif t=="Name": name=e
    else: amt=e

for text,cmd in [("Create Account",create),("Deposit",deposit),("Withdraw",withdraw),
("Check Balance",balance),("Transaction History",history),("Delete Account",delete),
("Reset",reset)]:
    tk.Button(root,text=text,command=cmd,width=25).pack(pady=3)

txt=scrolledtext.ScrolledText(root,height=12,width=55)
txt.pack(pady=10)

root.mainloop()