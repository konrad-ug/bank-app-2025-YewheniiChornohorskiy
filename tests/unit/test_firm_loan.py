import pytest
from src.firm_account import Firm_Account
from unittest.mock import patch
@pytest.fixture
def firm_account_with_balance(): 
    with patch.object(Firm_Account, 'validate_nip_with_mf', return_value=True):
        return Firm_Account("Test Company", "1234567890")

@pytest.fixture
def firm_account_with_zus(): 
    with patch.object(Firm_Account, 'validate_nip_with_mf', return_value=True):
        account = Firm_Account("Test Company", "1234567890")
        account.incoming_transfer(5000) 
        account.outgoing_transfer(1775)  
        return account

class TestFirmLoan:
    @pytest.mark.parametrize("balance, loan_amount, has_zus, expected_result", [ 
        (5000, 2000, True, True),
        (5000, 2500, True, True), 
        (3000, 2000, True, False),
        (1000, 1000, True, False), 
        (5000, 2000, False, False),
        (6000, 3000, False, False), 
        (1000, 1000, False, False),
        (1500, 1000, False, False),
    ])
    def test_take_loan_conditions(self, firm_account_with_balance, balance, loan_amount, has_zus, expected_result): 
        firm_account_with_balance.balance = balance
        if has_zus: 
            firm_account_with_balance.history.append(-1775.0)
         
        result = firm_account_with_balance.take_loan(loan_amount)
         
        assert result == expected_result
        if expected_result:
            assert firm_account_with_balance.balance == balance + loan_amount
            assert firm_account_with_balance.history[-1] == float(loan_amount)
        else:
            assert firm_account_with_balance.balance == balance

    def test_take_loan_adds_to_history(self, firm_account_with_zus):
        initial_balance = firm_account_with_zus.balance
        loan_amount = 1000
        
        result = firm_account_with_zus.take_loan(loan_amount)
        
        assert result is True
        assert firm_account_with_zus.balance == initial_balance + loan_amount
        assert firm_account_with_zus.history[-1] == float(loan_amount)

    def test_take_loan_exact_balance_condition(self, firm_account_with_zus): 
        firm_account_with_zus.balance = 4000
        loan_amount = 2000
        
        result = firm_account_with_zus.take_loan(loan_amount)
        
        assert result is True
        assert firm_account_with_zus.balance == 4000 + 2000

    def test_take_loan_no_zus_payment(self, firm_account_with_balance):
        firm_account_with_balance.balance = 10000 
        firm_account_with_balance.balance -= 1000
        firm_account_with_balance.history.append(-1000.0)
        
        result = firm_account_with_balance.take_loan(2000)
        
        assert result is False
        assert firm_account_with_balance.balance == 9000

    def test_take_loan_multiple_zus_payments(self, firm_account_with_balance):
        firm_account_with_balance.balance = 5000 
        firm_account_with_balance.history.append(-1775.0)
        firm_account_with_balance.history.append(-1775.0)
        
        result = firm_account_with_balance.take_loan(2000)
        
        assert result is True  

    def test_take_loan_with_express_fee_in_history(self, firm_account_with_balance): 
        firm_account_with_balance.balance = 5000 
        firm_account_with_balance.incoming_transfer(1780)   
        firm_account_with_balance.outgoing_transfer(1775, express=True)
        
        result = firm_account_with_balance.take_loan(2000)
        
        assert result is True  