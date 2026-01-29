from abc import ABC, abstractmethod
from typing import List

class AccountsRepository(ABC):
    @abstractmethod
    def save_all(self, accounts: List) -> bool:
        """Save all accounts to database"""
        pass
    
    @abstractmethod
    def load_all(self) -> List:
        """Load all accounts from database"""
        pass