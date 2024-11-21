import logging
import sys

class InsufficientFundsError(Exception):
    def __init__(self, message="Insufficient funds in the account."):
        super().__init__(message)

class BankAccount:
    def __init__(self, initial_balance=0):
        self.balance = initial_balance

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self.balance += amount
        logging.info(f"Deposited {amount}. New balance: {self.balance}")

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if amount > self.balance:
            logging.error(f"Attempted to withdraw {amount} but only {self.balance} available.")
            raise InsufficientFundsError()
        self.balance -= amount
        logging.info(f"Withdrew {amount}. New balance: {self.balance}")

    def get_balance(self):
        logging.info(f"Balance requested. Current balance: {self.balance}")
        return self.balance

# Set up logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1].lower() == "help":
        print("Usage: python bank_program.py [deposit|withdraw|balance] [amount]")
        sys.exit(0)

    action = sys.argv[1].lower()
    try:
        amount = float(sys.argv[2]) if len(sys.argv) > 2 else 0
    except ValueError:
        logging.error("Invalid amount provided.")
        print("Please provide a valid numeric amount.")
        sys.exit(1)

    account = BankAccount(100)  # Initial balance of 100

    try:
        if action == "deposit":
            account.deposit(amount)
            print(f"Deposited {amount}. New balance: {account.get_balance()}")
        elif action == "withdraw":
            account.withdraw(amount)
            print(f"Withdrew {amount}. New balance: {account.get_balance()}")
        elif action == "balance":
            balance = account.get_balance()
            print(f"Current balance: {balance}")
        else:
            logging.error(f"Invalid action: {action}")
            print("Invalid action. Use 'deposit', 'withdraw', or 'balance'.")
    except InsufficientFundsError as e:
        print(f"Error: {e}")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        print("An unexpected error occurred. Please check the logs.")