# 🏦 Terminal Banking System

A simple, dependency-free **command-line banking system** built with Python and SQLite. 
It lets users create accounts, deposit and withdraw funds, check balances, view transaction 
history, and manage accounts — all persisted to a local SQLite database.

## Features

-  **Create Account** — open a new account with a unique account number and starting balance
-  **Deposit / Withdraw** — update balances with input validation (no negative or invalid amounts)
-  **Check Balance** — instantly view an account's current balance
-  **Transaction History** — every deposit, withdrawal, and account creation is logged
-  **Delete Account** — remove an account and its history (with confirmation prompt)
-  **List All Accounts** — view every account in a formatted table
-  **Persistent Storage** — all data is saved in a local SQLite `.db` file, so nothing is lost between runs

## Tech Stack

- **Python 3** (standard library only — no external dependencies)
- **SQLite3** for lightweight, file-based persistent storage


No `pip install` needed — everything uses Python's built-in libraries.

## Usage

Run the script and follow the on-screen menu:
