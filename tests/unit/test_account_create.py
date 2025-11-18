import pytest
from src.personal_account import Personal_Account
from src.account import Account

@pytest.fixture
def default_account():
    return Account()

@pytest.fixture
def personal_account_with_promo():
    return Personal_Account("John", "Doe", "12345678901", "PROM_XYZ")

class TestAccount:
    @pytest.mark.parametrize("pesel, expected", [
        ("12345678901", "12345678901"),
        ("1234567890", "Invalid"),
        ("123456789012", "Invalid"),
        (None, "Invalid"),
    ])
    def test_pesel_validation(self, pesel, expected):
        account = Personal_Account("John", "Doe", pesel)
        assert account.pesel == expected

    @pytest.mark.parametrize("promo, expected_balance", [
        ("PROM_XYZ", 50.0),
        ("PROM_XYZZ", 0.0),
        ("PROM_XY", 0.0),
        (None, 0.0),
        ("BADPROMO", 0.0),
    ])
    def test_promo_validation(self, promo, expected_balance):
        account = Personal_Account("John", "Doe", "12345678901", promo)
        assert account.balance == expected_balance 
    @pytest.mark.parametrize("pesel, promo, expected_balance", [
        ("70010112345", "PROM_123", 50.0),
        ("50010112345", "PROM_123", 0.0),
        ("70010112345", None, 0.0),
        ("7001011234", "PROM_123", 0.0),
    ])
    def test_age_promo_combination(self, pesel, promo, expected_balance):
        account = Personal_Account("Test", "User", pesel, promo)
        assert account.balance == expected_balance 
    def test_start_fee_and_balance(self, default_account):
        assert default_account.balance == 0.0
        assert default_account.fee == 0.0 
    def test_incoming_transfer_adds_to_history(self, default_account):
        default_account.incoming_transfer(500)
        assert default_account.history == [500.0]
        assert default_account.balance == 500.0 
    def test_outgoing_transfer_adds_to_history(self, default_account):
        default_account.incoming_transfer(500)
        default_account.outgoing_transfer(300)
        assert default_account.history == [500.0, -300.0]
        assert default_account.balance == 200.0 
    def test_express_transfer_adds_fee_to_history(self, default_account):
        default_account.fee = 1
        default_account.incoming_transfer(500)
        default_account.outgoing_transfer(300, express=True)
        assert default_account.history == [500.0, -300.0, -1.0]
        assert default_account.balance == 199.0