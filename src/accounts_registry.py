 
class AccountsRegistry:
    def __init__(self):
        self.accounts = []

    def add_account(self, account): 
        self.accounts.append(account)

    def find_account_by_pesel(self, pesel): 
        for account in self.accounts:
            if account.pesel == pesel:
                return account
        return None

    def get_all_accounts(self): 
        return self.accounts.copy()  

    def get_accounts_count(self): 
        return len(self.accounts)