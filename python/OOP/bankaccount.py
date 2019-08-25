class BankAccount:
    def __init__(self, int_rate, balance):
        self.int_rate = int_rate
        self.balance = balance
    
    def deposit(self, amount):
        self.balance += amount
        return self
    
    def withdrawal(self, amount):
        self.balance -= amount
        return self

    def display_account_info(self):
        print(self.balance)
        return self
    
    def yield_interest(self):
        self.balance = (self.int_rate * self.balance) + self.balance
        return self


account1 = BankAccount(0.01, 0)
account1.deposit(1000).deposit(1500).deposit(300).withdrawal(250).display_account_info().yield_interest().display_account_info()


account2 = BankAccount(0.01, 0)
account2.deposit(1250).deposit(750).withdrawal(40).withdrawal(16).withdrawal(9).withdrawal(250).display_account_info().yield_interest().display_account_info()