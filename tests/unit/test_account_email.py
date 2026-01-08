from unittest.mock import Mock, patch, MagicMock
from src.personal_account import Personal_Account
from src.firm_account import Firm_Account
from datetime import datetime

class TestAccountEmail:
    
    @patch('src.personal_account.SMTPClient')
    def test_personal_account_send_history_success(self, mock_smtp_class): 
        mock_smtp_instance = Mock()
        mock_smtp_instance.send.return_value = True
        mock_smtp_class.return_value = mock_smtp_instance
        
        account = Personal_Account("John", "Doe", "12345678901")
        account.history = [100.0, -1.0, 500.0]
        email_address = "test@example.com"
         
        today_date = "2025-12-10"
        with patch('src.personal_account.datetime') as mock_datetime:
            mock_datetime.now.return_value.strftime.return_value = today_date
             
            result = account.send_history_via_email(email_address)
         
        assert result is True
        mock_smtp_class.assert_called_once()
        mock_smtp_instance.send.assert_called_once_with(
            f"Account Transfer History {today_date}",
            f"Personal account history: {[100.0, -1.0, 500.0]}",
            email_address
        )
    
    @patch('src.personal_account.SMTPClient')
    def test_personal_account_send_history_failure(self, mock_smtp_class): 
        mock_smtp_instance = Mock()
        mock_smtp_instance.send.return_value = False
        mock_smtp_class.return_value = mock_smtp_instance
        
        account = Personal_Account("Jane", "Smith", "98765432109")
        account.history = [200.0, -50.0]
        email_address = "test2@example.com"
         
        result = account.send_history_via_email(email_address)
         
        assert result is False
        mock_smtp_instance.send.assert_called_once()
    
    @patch('src.firm_account.SMTPClient')
    @patch.object(Firm_Account, 'validate_nip_with_mf', return_value=True)
    def test_firm_account_send_history_success(self, mock_validate_nip, mock_smtp_class): 
        mock_smtp_instance = Mock()
        mock_smtp_instance.send.return_value = True
        mock_smtp_class.return_value = mock_smtp_instance
        
        account = Firm_Account("Test Company", "1234567890")
        account.history = [5000.0, -1000.0, 500.0]
        email_address = "company@example.com"
         
        today_date = "2025-12-10"
        with patch('src.firm_account.datetime') as mock_datetime:
            mock_datetime.now.return_value.strftime.return_value = today_date
             
            result = account.send_history_via_email(email_address)
         
        assert result is True
        mock_smtp_class.assert_called_once()
        mock_smtp_instance.send.assert_called_once_with(
            f"Account Transfer History {today_date}",
            f"Company account history: {[5000.0, -1000.0, 500.0]}",
            email_address
        )
    
    @patch('src.firm_account.SMTPClient')
    @patch.object(Firm_Account, 'validate_nip_with_mf', return_value=True)
    def test_firm_account_send_history_empty_history(self, mock_validate_nip, mock_smtp_class): 
        mock_smtp_instance = Mock()
        mock_smtp_instance.send.return_value = True
        mock_smtp_class.return_value = mock_smtp_instance
        
        account = Firm_Account("New Company", "1234567890")
        account.history = []
        email_address = "new@example.com"
         
        result = account.send_history_via_email(email_address) 
        assert result is True
        mock_smtp_instance.send.assert_called_once()
        call_args = mock_smtp_instance.send.call_args
        assert "Company account history: []" in call_args[0][1]
    
    @patch('src.personal_account.SMTPClient')
    def test_personal_account_send_history_with_transactions(self, mock_smtp_class): 
        mock_smtp_instance = Mock()
        mock_smtp_instance.send.return_value = True
        mock_smtp_class.return_value = mock_smtp_instance
        
        account = Personal_Account("John", "Doe", "12345678901") 
        account.incoming_transfer(1000)
        account.outgoing_transfer(200)
        account.incoming_transfer(500)
        
        email_address = "transaction@example.com"
         
        result = account.send_history_via_email(email_address)
         
        assert result is True
        mock_smtp_instance.send.assert_called_once()
        call_args = mock_smtp_instance.send.call_args
        assert "Personal account history:" in call_args[0][1]
        assert "[1000.0, -200.0, 500.0]" in call_args[0][1]
    
    @patch('src.firm_account.SMTPClient')
    @patch.object(Firm_Account, 'validate_nip_with_mf', return_value=True)
    def test_firm_account_send_history_with_express_fee(self, mock_validate_nip, mock_smtp_class): 
        mock_smtp_instance = Mock()
        mock_smtp_instance.send.return_value = True
        mock_smtp_class.return_value = mock_smtp_instance
        
        account = Firm_Account("Test Company", "1234567890") 
        account.incoming_transfer(10000)
        account.outgoing_transfer(2000, express=True)
        
        email_address = "firm@example.com"
         
        result = account.send_history_via_email(email_address)
         
        assert result is True
        mock_smtp_instance.send.assert_called_once()
        call_args = mock_smtp_instance.send.call_args
        assert "Company account history:" in call_args[0][1] 
        assert "-5.0" in call_args[0][1]
 