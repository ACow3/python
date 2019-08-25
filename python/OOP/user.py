class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.account_balance = 0

    def make_deposit(self, amount):
        self.account_balance += amount

    def make_withdrawl(self,amount):
        self.account_balance -= amount

    def display_user_balance(self):
        self.account_balance

guido = User("Guido van Rossum", "guido@python.com")
guido.make_deposit(1000)
guido.make_deposit(500)
guido.make_deposit(125)
guido.make_withdrawl(200)


alex = User("Alex Dojo", "alex@python.com")
alex.make_deposit(2000)
alex.make_deposit(300)
alex.make_withdrawl(100)
alex.make_withdrawl(75)


shawn = User("Shawn Dojo", "shawn@python.com")
shawn.make_deposit(475)
shawn.make_withdrawl(50)
shawn.make_withdrawl(70)
shawn.make_withdrawl(25)


print("user:", guido.name, "balance:", guido.account_balance)

print("user:", alex.name, "balance:", alex.account_balance)

print("user:", shawn.name, "balance:", shawn.account_balance)


