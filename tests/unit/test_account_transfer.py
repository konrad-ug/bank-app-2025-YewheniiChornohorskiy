import pytest
from src.personal_account import Personal_Account

@pytest.fixture
def personal_account():
    return Personal_Account("John", "Doe")

class TestAccount:
    def test_incoming_transfer(self, personal_account):
        personal_account.incoming_transfer(100)
        assert personal_account.balance == 100 
    def test_outgoing_transfer(self, personal_account):
        personal_account.balance = 200
        personal_account.outgoing_transfer(50)
        assert personal_account.balance == 150 
    def test_no_money(self, personal_account):
        personal_account.outgoing_transfer(1000)
        assert personal_account.balance == 0 
    def test_express_transfer(self, personal_account):
        personal_account.balance = 200
        personal_account.outgoing_transfer(100, "express")
        assert personal_account.balance == 99