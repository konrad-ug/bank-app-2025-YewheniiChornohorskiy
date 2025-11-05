from src.personal_account import Personal_Account
from src.account import Account

class TestAccount:
    def test_account_creation(self):
        account = Personal_Account("John", "Doe","12345678901","PROM_XYZ")
        assert account.first_name == "John"
        assert account.last_name == "Doe" 
        assert account.balance == 50.0
        assert account.pesel == "12345678901"
    def test_krotki_pesel(self):
        account_krotki_pesel = Personal_Account("John", "Doe","1234567890")
        assert account_krotki_pesel.pesel == "Invalid"
    def test_dlugi_pesel(self):
        account_dlugi_pesel = Personal_Account("John", "Doe","123456789012")
        assert account_dlugi_pesel.pesel == "Invalid"
    def test_brak_pesel(self):
        account_brak_pesel = Personal_Account("John", "Doe")
        assert account_brak_pesel.pesel == "Invalid" 
    def test_long_promo(self):
        account_dlugi_promo = Personal_Account("John", "Doe","12345678901","PROM_XYZZ")
        assert account_dlugi_promo.balance == 0.0 
    def test_short_promo(self):
        account_krotki_promo = Personal_Account("John", "Doe","12345678901","PROM_XY") 
        assert account_krotki_promo.balance == 0.0   
    def test_promo_valid_for_young_person(self): 
        acc = Personal_Account("Jan", "Kowalski", "70010112345", "PROM_123")
        assert acc.balance == 50.0 
    def test_promo_invalid_for_old_person(self): 
        acc = Personal_Account("Anna", "Nowak","50010112345", "PROM_123")
        assert acc.balance == 0.0 
    def test_no_promo(self):
        acc = Personal_Account("Piotr", "Zieliński", "70010112345", None)
        assert acc.balance == 0.0  
    def test_invalid_promo_format(self):
        acc = Personal_Account("Kasia", "Lewandowska", pesel="70010112345", promo="BADPROMO")
        assert acc.balance == 0.0 
    def test_invalid_pesel_with_promo(self):
        acc = Personal_Account("Kasia", "Lewandowska", pesel="7001011234", promo="PROM_123")
        assert acc.balance == 0.0 
    def test_start_fee_and_balance(self):
        acc = Account()
        assert acc.balance == 0.0
        assert acc.fee == 0.0
    def test_incoming_transfer_adds_to_history(self):
        acc = Account()
        acc.incoming_transfer(500)
        assert acc.history == [500.0]
        assert acc.balance == 500.0 
    def test_outgoing_transfer_adds_to_history(self):
        acc = Account()
        acc.incoming_transfer(500)
        acc.outgoing_transfer(300)
        assert acc.history == [500.0, -300.0]
        assert acc.balance == 200.0 
    def test_express_transfer_adds_fee_to_history(self):
        acc = Account()
        acc.fee = 1
        acc.incoming_transfer(500)
        acc.outgoing_transfer(300, express=True)
        assert acc.history == [500.0, -300.0, -1.0]
        assert acc.balance == 199.0