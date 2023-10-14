class Bank:
    def __init__(self):
        self.accounts = []
        self.account_number = 0
        self.bankrupt = False


    def is_bankrupt(self, status):
        self.bankrupt = status


    def create_account(self, name, email, address, account_type):
        self.account_number += 1
        account = Account(self.account_number, name, email, address, account_type)
        self.accounts.append(account)
        return account


    def delete_account(self, account_number):
        for account in self.accounts:
            if account.account_number == account_number:
                self.accounts.remove(account)
                return True
        return False


    def all_accounts(self):
        return self.accounts


    def total_balance(self):
        total_balance = 0
        for account in self.accounts:
            total_balance += account.balance
        return total_balance


    def total_loan_amount(self):
        total_loan_amount = 0
        for account in self.accounts:
            total_loan_amount += account.loan_amount
        return total_loan_amount


    def loan_feature(self, status):
        Account.loan_feature_enabled = status


class Account:
    loan_feature_enabled = True


    def __init__(self, account_number, name, email, address, account_type):
        self.account_number = account_number
        self.name = name
        self.email = email
        self.address = address
        self.account_type = account_type
        self.balance = 0
        self.loan_amount = 0
        self.loan_taken_count = 0 
        self.transactions = []
        self.bank = bank


    def deposit(self, amount):
        if amount <= 0:
            return False
        self.balance += amount
        transaction = Transaction(amount, "Deposit")
        self.transactions.append(transaction)
        return True


    def withdraw(self, amount):
        if self.bank.bankrupt:
            print("The bank is bankrupt.")
            return False
        if amount <= 0:
            return False
        if amount > self.balance:
            if not self.bank.bankrupt:
                print("Withdrawal amount exceeded your balance.")
            return False
        self.balance -= amount
        transaction = Transaction(amount, "Withdraw")
        self.transactions.append(transaction)
        return True


    def check_balance(self):
        total_balance = self.balance + self.loan_amount
        return total_balance


    def take_loan(self, amount):
        if not Account.loan_feature_enabled or self.loan_taken_count >= 2 or amount <= 0:
            return False

        self.loan_amount += amount
        self.loan_taken_count += 1


        transaction = Transaction(amount, "Loan")
        self.transactions.append(transaction)
    
        return True




    def transfer_money(self, recipient_account, amount):
        if self.bank.bankrupt:
            print("The bank is bankrupt.")
            return False
        if amount <= 0:
            return False
        if amount > self.balance:
            if not self.bank.bankrupt:
                print("Transfer failed. Insufficient balance.")
            return False
        if recipient_account:
            recipient_account.deposit(amount)
            transaction1 = Transaction(amount, "Transfer", recipient_account)
            transaction2 = Transaction(amount, "Transfer", self)
            self.transactions.append(transaction2)
            recipient_account.transactions.append(transaction1)
            print(f"Transferred {amount} taka to the account: {recipient_account.account_number}")
        else:
            print("Recipient's account does not exist.")
            return False
        
    def check_transaction_history(self):
        return [transaction.to_dict() for transaction in self.transactions]



class Transaction:
    def __init__(self, amount, transaction_type, recipient_account=None):
        self.amount = amount
        self.type = transaction_type 
        self.recipient_account = recipient_account

    def to_dict(self):
        transaction_info = {"amount": self.amount, "transaction_type": self.type}
        if self.recipient_account:
            transaction_info["recipient_account"] = self.recipient_account.account_number
        return transaction_info


bank = Bank()

while True:
    print("Are you:")
    print("1. User")
    print("2. Admin")
    print("3. Exit")
    
    option = input("Enter your option: ")
    
    if option == "1":
        user_menu = [
            "1. Create an user account",
            "2. Deposit Money",
            "3. Withdraw Money",
            "4. Check available balance",
            "5. Transfer money",
            "6. Check transaction history",
            "7. Take loan",
            "8. Return to the main menu"
        ]
        while True:
            print("\nUser Menu:")
            for option in user_menu:
                print(option)
            
            user_option = input("Enter your option: ")
            
            if user_option == "1":
                name = input("Enter your name: ")
                email = input("Enter your email: ")
                address = input("Enter your address: ")
                account_type = input("Enter your account type (press 1 for Savings account and 2 for Current account): ")
                if account_type == "1":
                    account_type = "Savings"
                else:
                    account_type = "Current"
                account = bank.create_account(name, email, address, account_type)
                print(f" Your account is create and account number is: {account.account_number}")
            
            elif user_option == "2":
                account_number = int(input("Enter your account number: "))
                amount = int(input("Enter how much money to deposit: "))
                account = None
                for acc in bank.all_accounts():
                    if acc.account_number == account_number:
                        account = acc
                        break
                if account:
                    account.deposit(amount)
                    print(f"Deposited {amount} taka to the account number: {account_number}")
                else:
                    print("Account does not exist.")
            
            elif user_option == "3":
                account_number = int(input("Enter your account number: "))
                amount = int(input("Enter how much you want to withdraw: "))
                account = None
                for acc in bank.all_accounts():
                    if acc.account_number == account_number:
                        account = acc
                        break
                if account:
                    if account.withdraw(amount):
                        print(f"Withdrew {amount} taka from account: {account_number}")
                    else:
                        print("Withdraw amount exceeded you balance.")
                else:
                    print("Account does not exist.")
            
            elif user_option == "4":
                account_number = int(input("Enter your account number: "))
                account = None
                for acc in bank.all_accounts():
                    if acc.account_number == account_number:
                        account = acc
                        break
                if account:
                    print(f"Available balance for your account: {account_number}: {account.check_balance()} taka")
                else:
                    print("Account does not exist.")
            
            elif user_option == "5":
                account_number = int(input("Enter your account number: "))
                recipient_account_number = int(input("Enter recipient's account number: "))
                amount = int(input("Enter how much you want to transfer: "))

                sender_account = None
                recipient_account = None

                for acc in bank.all_accounts():
                    if acc.account_number == account_number:
                        sender_account = acc
                    if acc.account_number == recipient_account_number:
                        recipient_account = acc

                if sender_account and recipient_account:
                    if sender_account.withdraw(amount):
                        if recipient_account.deposit(amount):
                            print(f"Transferred {amount} taka to the account: {recipient_account_number}")
                        else:
                            sender_account.deposit(amount) 
                            print("Transfer failed. Check recipient's account.")
                    else:
                        print("Transfer failed. Check your reciever input or your account balance.")
                else:
                    print("Sender's or recipient's account does not exist.")


            
            elif user_option == "6":
                account_number = int(input("Enter your account number: "))
                account = None
                for acc in bank.all_accounts():
                    if acc.account_number == account_number:
                        account = acc
                        break
                if account:
                    history = account.check_transaction_history()
                    print(f"Transaction history for account: {account_number}:")
                    for t_history in history:
                        print(t_history)
                else:
                    print("Account does not exist.")
            
            elif user_option == "7":
                account_number = int(input("Enter your account number: "))
                amount = float(input("Enter how much you want as loan: "))
                account = None
                for acc in bank.all_accounts():
                    if acc.account_number == account_number:
                        account = acc
                        break
                if account:
                    if account.take_loan(amount):
                        print(f"Loan of {amount} approved for the account {account_number}")
                    else:
                        print("Loan request denied")
                else:
                    print("Account does not exist.")
                
            
            elif user_option == '8':
                break
            
            """ if bank.bankrupt:
                print("The bank is bankrupt.") """

    elif option == "2":
        admin_menu = [
            "1. Create an account",
            "2. Delete any user account",
            "3. See all user accounts list",
            "4. Check the total available balance of the bank",
            "5. Check the total loan amount",
            "6. Turn on/off the loan feature",
            "7. Change Bankrupt Status",
            "8. Return to the main menu"
        ]
        while True:
            print("\nAdmin Menu:")
            for option in admin_menu:
                print(option)

            admin_option = input("Enter your option: ")

            if admin_option  == "1":
                name = input("Enter user's name: ")
                email = input("Enter user's email: ")
                address = input("Enter user's address: ")
                account_type = input("Enter user's account type (press 1 for Savings and 2 for Current): ")
                if account_type == "1":
                    account_type = "Savings"
                else:
                    account_type = "Current"
                account = bank.create_account(name, email, address, account_type)
                print(f"User account created with account number: {account.account_number}")

            elif admin_option == "2":
                account_number = int(input("Enter account number which will delete: "))
                if bank.delete_account(account_number):
                    print(f"User account {account_number} has been deleted.")
                else:
                    print("Account not found.")

            elif admin_option == "3":
                accounts = bank.all_accounts()
                if accounts:
                    print("List of all user accounts:")
                    for account in accounts:
                        print(f"Account Number: {account.account_number}, Name: {account.name}")
                else:
                    print("No user accounts are found.")

            elif admin_option == "4":
                total_balance = bank.total_balance()
                if total_balance == 0:
                    print("The balance of the Bank is empty.")
                else:
                    print(f"Total available balance in the bank: {total_balance}")

            elif admin_option == "5":
                total_loan_amount = bank.total_loan_amount()
                print(f"Total loan amount in the bank: {total_loan_amount}")

            elif admin_option == "6":
                loan_feature_status = input("Turn on or off the loan feature (press 1 for On and 2 for Off): ")
                if loan_feature_status == "1":
                    bank.loan_feature(True)
                    print("Loan feature is On now.")
                elif loan_feature_status == "2":
                    bank.loan_feature(False)
                    print("Loan feature is Off now")
                else:
                    print("Your choice is invalid.")
                    
            elif admin_option == "7":
                bankrupt_status = input("Declare the bank as bankrupt (press 1 for Yes, 2 for No): ")
                if bankrupt_status == "1":
                    bank.is_bankrupt(True)
                    print("The bank is now bankrupt.")
                elif bankrupt_status == "2":
                    bank.is_bankrupt(False)
                    print("The bank is no longer bankrupt.")

                

            elif admin_option == "8":
                break  

    elif option == "3":
        break
    
    if bank.bankrupt:
        print("The bank is bankrupt.")