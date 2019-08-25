class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.account = BankAccount(int_rate=0.02, balance=0)

    def make_deposit(self, amount):
        self.account = amount

    def make_withdrawal(self,amount):
        self.account = amount

    def display_user_balance(self):
        self.account = amount

class BankAccount:
    def __init__(self, int_rate, balance):
        self.int_rate = int_rate
        self.account = balance
    
    def deposit(self, amount):
        self.account += amount
        return self
    
    def withdrawal(self, amount):
        self.account -= amount
        return self

    def display_account_info(self):
        print(self.account)
        return self
    
    def yield_interest(self):
        self.int_rate * self.account + self.account
        return self

guido = User("Guido van Rossum", "guido@python.com")
guido.make_deposit(1000)
guido.make_deposit(500)
guido.make_deposit(125)
guido.make_withdrawal(200)


alex = User("Alex Dojo", "alex@python.com")
alex.make_deposit(2000)
alex.make_deposit(300)
alex.make_withdrawal(100)
alex.make_withdrawal(75)


shawn = User("Shawn Dojo", "shawn@python.com")
shawn.make_deposit(475)
shawn.make_withdrawal(50)
shawn.make_withdrawal(70)
shawn.make_withdrawal(25)


print("user:", guido.name, "balance:", guido.account)

print("user:", alex.name, "balance:", alex.account)

print("user:", shawn.name, "balance:", shawn.account)