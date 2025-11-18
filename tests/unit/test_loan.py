import pytest
from src.personal_account import Personal_Account

@pytest.fixture
def personal_account():
    return Personal_Account("John", "Doe", "12345678901")

class TestLoan:
    @pytest.mark.parametrize("history, loan_amount, expected_result, expected_balance", [
        ([100, 200, 50], 1000, True, 1000), 
        ([100, -10, 50], 100, False, 0), 
        ([10, 40, -30, 40, 50], 100, True, 100),  
        ([10, 20, 30, 40, 50], 200, True, 200), 
        ([100, 200], 50, False, 0), 
    ])
    def test_submit_for_loan(self, personal_account, history, loan_amount, expected_result, expected_balance):
        personal_account.history = history
        result = personal_account.submit_for_loan(loan_amount)
        assert result == expected_result
        assert personal_account.balance == expected_balance
        if result:
            assert personal_account.history[-1] == float(loan_amount) 
    def test_loan_adds_to_balance_and_history(self, personal_account):
        personal_account.history = [100, 200, 300]
        result = personal_account.submit_for_loan(500)
        assert result is True
        assert personal_account.balance == 500
        assert personal_account.history == [100, 200, 300, 500.0] 
    def test_loan_not_granted_when_conditions_not_met(self, personal_account):
        personal_account.history = [100, -50, 200]
        result = personal_account.submit_for_loan(100)
        assert result is False
        assert personal_account.balance == 0
        assert personal_account.history == [100, -50, 200]