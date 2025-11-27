import pytest
from src.personal_account import Personal_Account
from src.accounts_registry import AccountsRegistry

@pytest.fixture
def registry():
    return AccountsRegistry()

@pytest.fixture
def sample_accounts():
    return [
        Personal_Account("John", "Doe", "12345678901"),
        Personal_Account("Jane", "Smith", "98765432109"),
        Personal_Account("Bob", "Johnson", "55566677788")
    ]

class TestAccountsRegistry:
    def test_add_account(self, registry):
        account = Personal_Account("John", "Doe", "12345678901")
        
        registry.add_account(account)
        
        assert registry.get_accounts_count() == 1
        assert registry.get_all_accounts() == [account]

    def test_find_account_by_pesel(self, registry, sample_accounts):
        for account in sample_accounts:
            registry.add_account(account)
        
        found_account = registry.find_account_by_pesel("98765432109")
        
        assert found_account is not None
        assert found_account.pesel == "98765432109"
        assert found_account.first_name == "Jane"
        assert found_account.last_name == "Smith"

    def test_find_account_by_pesel_not_found(self, registry, sample_accounts):
        for account in sample_accounts:
            registry.add_account(account)
        
        found_account = registry.find_account_by_pesel("00000000000")
        
        assert found_account is None

    def test_get_all_accounts(self, registry, sample_accounts):
        for account in sample_accounts:
            registry.add_account(account)
        
        all_accounts = registry.get_all_accounts()
        
        assert len(all_accounts) == 3
        assert all(account in all_accounts for account in sample_accounts)

    def test_get_accounts_count(self, registry, sample_accounts):
        assert registry.get_accounts_count() == 0
        
        registry.add_account(sample_accounts[0])
        assert registry.get_accounts_count() == 1
        
        registry.add_account(sample_accounts[1])
        assert registry.get_accounts_count() == 2

    def test_add_multiple_accounts_same_pesel(self, registry):
        account1 = Personal_Account("John", "Doe", "12345678901")
        account2 = Personal_Account("John", "Doe", "12345678901") 
        
        registry.add_account(account1)
        registry.add_account(account2) 
        assert registry.get_accounts_count() == 2