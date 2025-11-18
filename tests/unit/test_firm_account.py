import pytest
from src.firm_account import Firm_Account

@pytest.fixture
def firm_account_valid_nip():
    return Firm_Account("Google", "1234567890")

@pytest.fixture
def firm_account_invalid_nip():
    return Firm_Account("Coca Cola", "123456789")

class TestFirmAccount:
    def test_incorrect_nip(self, firm_account_invalid_nip):
        assert firm_account_invalid_nip.nip == "Invalid" 
    def test_incoming_transfer(self, firm_account_valid_nip):
        firm_account_valid_nip.incoming_transfer(100)
        assert firm_account_valid_nip.balance == 100 
    def test_outgoing_transfer(self, firm_account_valid_nip):
        firm_account_valid_nip.balance = 200
        firm_account_valid_nip.outgoing_transfer(50)
        assert firm_account_valid_nip.balance == 150 
    def test_no_money(self, firm_account_valid_nip):
        firm_account_valid_nip.outgoing_transfer(1000)
        assert firm_account_valid_nip.balance == 0 
    def test_express_transfer(self, firm_account_valid_nip):
        firm_account_valid_nip.balance = 200
        firm_account_valid_nip.outgoing_transfer(100, "express")
        assert firm_account_valid_nip.balance == 95