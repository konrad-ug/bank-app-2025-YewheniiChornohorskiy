import pytest
from unittest.mock import Mock, MagicMock, patch
from src.mongo_accounts_repository import MongoAccountsRepository

class TestMongoAccountsRepository:
    
    def test_save_all_success(self): 
        with patch('pymongo.MongoClient') as mock_client: 
            mock_collection = MagicMock()
            mock_collection.delete_many.return_value = None
            mock_collection.update_one.return_value = None
            
            mock_db = MagicMock()
            mock_db.__getitem__.return_value = mock_collection
            
            mock_client_instance = MagicMock()
            mock_client_instance.__getitem__.return_value = mock_db
            mock_client.return_value = mock_client_instance
             
            repo = MongoAccountsRepository()
            
            class MockAccount:
                first_name = "Test"
                last_name = "User"
                pesel = "12345678901"
                balance = 100.0
                history = []
                fee = 1.0
            
            result = repo.save_all([MockAccount()])
            assert result is True
    
    def test_load_all_empty(self): 
        with patch('pymongo.MongoClient') as mock_client:
            mock_collection = MagicMock()
            mock_collection.find.return_value = []
            
            mock_db = MagicMock()
            mock_db.__getitem__.return_value = mock_collection
            
            mock_client_instance = MagicMock()
            mock_client_instance.__getitem__.return_value = mock_db
            mock_client.return_value = mock_client_instance
            
            repo = MongoAccountsRepository()
            accounts = repo.load_all()
            
            assert len(accounts) == 0