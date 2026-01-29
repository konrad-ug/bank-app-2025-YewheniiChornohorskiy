from src.accounts_repository import AccountsRepository
from typing import List
import os

class MongoAccountsRepository(AccountsRepository):
    def __init__(self):
        try:
            from pymongo import MongoClient
            
            mongo_host = os.getenv('MONGO_HOST', 'localhost')
            mongo_port = int(os.getenv('MONGO_PORT', 27017))
            database_name = os.getenv('MONGO_DB', 'bank_app')
            collection_name = os.getenv('MONGO_COLLECTION', 'accounts')
            
            self.client = MongoClient(
                f'mongodb://admin:password@localhost:27017/',
                serverSelectionTimeoutMS=2000 
            )
            
            self.client.server_info()
            self.db = self.client[database_name]
            self.collection = self.db[collection_name]
            
            try:
                self.collection.create_index("pesel", unique=True)
            except:
                print("Could not create index (no permissions)")
                
            self.is_available = True
            print("MongoDB connected successfully")
            
        except Exception as e:
            print(f"MongoDB not available: {e}")
            self.is_available = False
            self.client = None
            self.collection = None
    
    def save_all(self, accounts: List) -> bool:
        if not self.is_available or self.collection is None:
            print("Mock save operation (MongoDB not available)")
            return True  
        
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
            print(f"❌ Error saving to MongoDB: {e}")
            return False
    
    def load_all(self) -> List:
        if not self.is_available or self.collection is None:
            print("Mock load operation (MongoDB not available)")
            return [] 
        
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
            print(f"Error loading from MongoDB: {e}")
            return []
    
    def close(self):
        if self.client:
            self.client.close()