from src.account import Account
from smtp.smtp import SMTPClient
from datetime import datetime
class Personal_Account(Account):
    def __init__(self, first_name, last_name, pesel = None, promo = None):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name 
        self.pesel = pesel if self.is_pesel_valid(pesel) else "Invalid" 
        self.balance = 50.0 if self.is_promo_valid(promo) and self.pesel != "Invalid" and self.get_birth_year_from_pesel() < 65 else 0.0
        self.fee = 1.0
    def is_pesel_valid(self,pesel):
        if isinstance(pesel,str) and (len(pesel) == 11):
            return True 
    def is_promo_valid(self,promo):
        if promo and promo.startswith("PROM_") and len(promo) == 8:
            return True
    def get_birth_year_from_pesel(self): 
        current_year = 2025 
        year = int(self.pesel[:2]) 
        if year > 30: 
            year += 1900 
        else: 
            year += 2000
        return current_year - year    
    def submit_for_loan(self, amount):  
        if len(self.history) >= 3: 
            last_three = self.history[-3:]
            if all(t > 0 for t in last_three):
                self.balance += amount
                self.history.append(float(amount))
                return True
 
        if len(self.history) >= 5:
            last_five = self.history[-5:] 
            if sum(last_five) > amount:
                self.balance += amount
                self.history.append(float(amount))
                return True

        return False
    def send_history_via_email(self, email_address): 
        today_date = datetime.now().strftime("%Y-%m-%d")
        subject = f"Account Transfer History {today_date}"
         
        text = f"Personal account history: {self.history}"
         
        smtp_client = SMTPClient()
        return smtp_client.send(subject, text, email_address)