class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.account_balance = 0

    def make_deposit(self, amount):
        self.account_balance += amount
        return self

    def make_withdrawl(self,amount):
        self.account_balance -= amount
        return self

    def display_user_balance(self):
        self.account_balance
        return self

    
guido = User("Guido van Rossum", "guido@python.com")
guido.make_deposit(1000).make_deposit(500).make_deposit(125).make_withdrawl(200)


alex = User("Alex Dojo", "alex@python.com")
alex.make_deposit(2000).make_deposit(300).make_withdrawl(100).make_withdrawl(75)


shawn = User("Shawn Dojo", "shawn@python.com")
shawn.make_deposit(475).make_withdrawl(50).make_withdrawl(70).make_withdrawl(25)


print("user:", guido.name, "balance:", guido.account_balance)

print("user:", alex.name, "balance:", alex.account_balance)

print("user:", shawn.name, "balance:", shawn.account_balance)