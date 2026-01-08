class Account:
    def __init__(self):
        self.balance = 0.0
        self.fee = 0.0
        self.history = []  

    def incoming_transfer(self, amount):
        self.balance += amount
        self.history.append(float(amount))

    def outgoing_transfer(self, amount, express=None):
        if self.balance >= amount:
            if express:
                self.balance -= (amount + self.fee)
                self.history.append(-float(amount))
                self.history.append(-float(self.fee))
            else:
                self.balance -= amount
                self.history.append(-float(amount)) 

        
