import logging
import sys


class InsufficientFunds(Exception):
    def __init__(self, message="Insufficient funds in the account."):
        super().__init__(message)


class BankAccount:
    def __init__(self, initial_balance=100):
        try:
            with open('balance.txt', 'r') as f:
                self.balance = float(f.read())
            logging.info(f"Initial balance loaded: {self.balance}")
        except (FileNotFoundError, ValueError):
            self.balance = initial_balance
            logging.info(f"Using initial balance: {self.balance}")

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self.balance += amount
        self._save_balance()
        logging.info(f"Deposited {amount}. New balance: {self.balance}")

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if amount > self.balance:
            logging.error(f"Attempted to withdraw {amount}, but only {self.balance} available.")
            raise InsufficientFunds()
        self.balance -= amount
        self._save_balance()
        logging.info(f"Withdrew {amount}. New balance: {self.balance}")

    def get_balance(self):
        logging.info(f"Balance requested. Current balance: {self.balance}")
        return self.balance

    def _save_balance(self):
        with open('balance.txt', 'w') as f:
            f.write(str(self.balance))
        logging.info(f"Balance saved: {self.balance}")


# Configure logging to output to file with timestamps
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filename='bank_account.log',
                    filemode='a')

if __name__ == "__main__":
    logging.info("Program started.")

    if len(sys.argv) < 2 or sys.argv[1].lower() == "help":
        help_message = """
Usage: python bank_program.py [action] [amount]

Actions:
  deposit [amount]: Add the specified amount to the account balance. [amount] is required.
  withdraw [amount]: Subtract the specified amount from the account balance if sufficient funds are available. [amount] is required.
  balance: Display the current account balance. No amount needed.

Examples:
  Deposit: python bank_program.py deposit 100
  Withdraw: python bank_program.py withdraw 50
  Check Balance: python bank_program.py balance

Error Handling:
  - Raises InsufficientFundsError if attempting to withdraw more than the available balance.
  - Logs errors and invalid inputs with timestamps.

Logging:
  - All actions and errors are logged to 'bank_account.log' with timestamps.

Balance Persistence:
  - Balance is saved to 'balance.txt' after each operation.
  - If 'balance.txt' is not found or contains invalid data, the initial balance is set to 100.
"""
        print(help_message)
        logging.info("Help requested. Program exiting.")
        sys.exit(0)

    action = sys.argv[1].lower()
    try:
        amount = float(sys.argv[2]) if len(sys.argv) > 2 else 0
    except ValueError:
        logging.error("Invalid amount provided.")
        print("Please provide a valid numeric amount.")
        sys.exit(1)

    account = BankAccount()  # Initial balance of 100 if balance.txt not found

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
    except InsufficientFunds as e:
        print(f"Error: {e}")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        print("An unexpected error occurred. Please check the logs.")

    logging.info("Program ended.")