from src.account import Account

class Firm_Account(Account):
    def __init__(self, company_name, nip):
        super().__init__()
        self.company_name = company_name
        self.nip = nip if self.is_nip_valid(nip) else "Invalid"  
        self.balance = 0.0
        self.fee = 5.0

    def is_nip_valid(self, nip):
        if isinstance(nip, str) and (len(nip) == 10):
            return True
        return False

    def take_loan(self, amount): 
        if self.balance < amount * 2:
            return False
         
        has_zus_payment = any(transaction == -1775.0 for transaction in self.history)
        if not has_zus_payment:
            return False
         
        self.balance += amount
        self.history.append(float(amount))
        return True