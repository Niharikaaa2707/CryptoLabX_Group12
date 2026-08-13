# secure_application/src/banking.py

import os
from datetime import datetime

# Path for secure_application log file
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_FILE = os.path.join(BASE_DIR, "outputs", "banking_execution.log")

# In-memory user database
USERS = {
    "acc101": {"name": "Alice", "password": "password123", "pin": "1234", "balance": 1000.0, "beneficiaries": []},
    "acc102": {"name": "Bob", "password": "securepass456", "pin": "5678", "balance": 500.0, "beneficiaries": []}
}

# --- VULNERABILITY 1: SENSITIVE DATA EXPOSURE IN LOGS ---
def log_action(message):
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    with open(LOG_FILE, "a") as f:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Intentionally logging raw credentials/sensitive data
        f.write(f"[{timestamp}] {message}\n")


def login():
    print("\n--- LOGIN ---")
    acc_id = input("Enter Account ID (e.g., acc101): ")
    password = input("Enter Password: ")
    
    # VULNERABILITY 1 IN ACTION: Exposing plaintext password in log files
    log_action(f"LOGIN TRY - Account: {acc_id}, Plaintext Password: {password}")

    if acc_id in USERS and USERS[acc_id]["password"] == password:
        print(f"Welcome back, {USERS[acc_id]['name']}!")
        return acc_id
    else:
        print("Invalid credentials!")
        return None

# --- VULNERABILITY 2: BROKEN ACCESS CONTROL (IDOR) ---
def check_balance(current_user_id):
    print("\n--- CHECK BALANCE ---")
    # Vulnerability: Prompts for any account ID instead of restricting to current_user_id
    target_acc = input("Enter Account ID to inspect balance: ")
    
    if target_acc in USERS:
        print(f"Account {target_acc} ({USERS[target_acc]['name']}) Balance: ${USERS[target_acc]['balance']:.2f}")
        log_action(f"User {current_user_id} viewed balance for {target_acc}")
    else:
        print("Account not found.")

# --- VULNERABILITY 3: INSUFFICIENT INPUT VALIDATION ---
def transfer_funds(current_user_id):
    print("\n--- TRANSFER FUNDS ---")
    recipient_id = input("Enter Recipient Account ID: ")
    
    if recipient_id not in USERS:
        print("Recipient account does not exist.")
        return

    try:
        amount = float(input("Enter amount to transfer: "))
        # Vulnerability: No check to ensure amount > 0.
        # Sending a negative number increases sender balance and decreases recipient balance!
        if USERS[current_user_id]["balance"] < amount:
            print("Insufficient funds!")
            return

        USERS[current_user_id]["balance"] -= amount
        USERS[recipient_id]["balance"] += amount
        print(f"Successfully transferred ${amount:.2f} to {USERS[recipient_id]['name']}.")
        log_action(f"TRANSFER - {current_user_id} sent ${amount} to {recipient_id}")
    except ValueError:
        print("Invalid amount entered.")


def manage_beneficiaries(current_user_id):
    print("\n--- MANAGE BENEFICIARIES ---")
    print("1. Add Beneficiary")
    print("2. List Beneficiaries")
    choice = input("Choice: ")

    if choice == "1":
        b_name = input("Enter Beneficiary Name: ")
        b_acc = input("Enter Beneficiary Account ID: ")
        USERS[current_user_id]["beneficiaries"].append({"name": b_name, "account": b_acc})
        print("Beneficiary added successfully!")
        log_action(f"BENEFICIARY ADDED - User {current_user_id} added {b_name} ({b_acc})")
    elif choice == "2":
        print("\nYour Beneficiaries:")
        for b in USERS[current_user_id]["beneficiaries"]:
            print(f"- {b['name']} (Acc: {b['account']})")


def banking_menu():
    logged_in_user = None

    while True:
        if not logged_in_user:
            logged_in_user = login()
            if not logged_in_user:
                retry = input("Try again? (y/n): ")
                if retry.lower() != 'y':
                    break
                continue

        print("\n===================================")
        print("     Online Banking Dashboard")
        print("===================================")
        print("1. Check Balance")
        print("2. Transfer Funds")
        print("3. Manage Beneficiaries")
        print("4. Logout")
        print("5. Exit Application")

        choice = input("\nSelect Option: ")

        if choice == "1":
            check_balance(logged_in_user)
        elif choice == "2":
            transfer_funds(logged_in_user)
        elif choice == "3":
            manage_beneficiaries(logged_in_user)
        elif choice == "4":
            print(f"Logged out user {logged_in_user}.")
            log_action(f"LOGOUT - User {logged_in_user}")
            logged_in_user = None
        elif choice == "5":
            print("Exiting Banking Module...")
            break
        else:
            print("Invalid Option!")

if __name__ == "__main__":
    banking_menu()