from src.accounts_repository import AccountsRepository
from pymongo import MongoClient
from typing import List
import os

class MongoAccountsRepository(AccountsRepository):
    def __init__(self): 
        mongo_host = os.getenv('MONGO_HOST', 'localhost')
        mongo_port = int(os.getenv('MONGO_PORT', 27017))
        database_name = os.getenv('MONGO_DB', 'bank_app')
        collection_name = os.getenv('MONGO_COLLECTION', 'accounts')
         
        self.client = MongoClient(f'mongodb://{mongo_host}:{mongo_port}/')
        self.db = self.client[database_name]
        self.collection = self.db[collection_name]
         
        self.collection.create_index("pesel", unique=True)
    
    def save_all(self, accounts: List) -> bool: 
        try: 
            self.collection.delete_many({})
             
            for account in accounts:
                account_dict = {
                    "name": account.first_name,
                    "surname": account.last_name,
                    "pesel": account.pesel,
                    "balance": account.balance,
                    "history": account.history,
                    "fee": account.fee
                }
                self.collection.update_one(
                    {"pesel": account.pesel},
                    {"$set": account_dict},
                    upsert=True
                )
            return True
        except Exception as e:
            print(f"Error saving accounts to MongoDB: {e}")
            return False
    
    def load_all(self) -> List: 
        try:
            from src.personal_account import Personal_Account
            
            accounts = []
            for account_data in self.collection.find(): 
                account = Personal_Account(
                    account_data["name"],
                    account_data["surname"],
                    account_data["pesel"]
                )
                account.balance = account_data["balance"]
                account.history = account_data.get("history", [])
                account.fee = account_data.get("fee", 1.0)
                accounts.append(account)
            
            return accounts
        except Exception as e:
            print(f"Error loading accounts from MongoDB: {e}")
            return []
    
    def close(self): 
        if self.client:
            self.client.close()