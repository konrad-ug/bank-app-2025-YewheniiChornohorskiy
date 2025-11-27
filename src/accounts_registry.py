from typing import List, Optional
from src.personal_account import Personal_Account

class AccountsRegistry:
    def __init__(self):
        self.accounts: List[Personal_Account] = []

    def add_account(self, account: Personal_Account): 
        self.accounts.append(account)

    def find_account_by_pesel(self, pesel: str) -> Optional[Personal_Account]: 
        for account in self.accounts:
            if account.pesel == pesel:
                return account
        return None

    def get_all_accounts(self) -> List[Personal_Account]: 
        return self.accounts.copy()  

    def get_accounts_count(self) -> int: 
        return len(self.accounts)