import pytest
from src.firm_account import Firm_Account
from unittest.mock import patch, Mock 

@pytest.fixture
def firm_account_valid_nip(): 
    with patch.object(Firm_Account, 'validate_nip_with_mf', return_value=True):
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
    
    def test_constructor_raises_error_for_invalid_nip(self): 
        with patch.object(Firm_Account, 'validate_nip_with_mf', return_value=False):
            with pytest.raises(ValueError, match="Company not registered!!"):
                Firm_Account("Fake Company", "1234567890")
    
    def test_nip_format_validation_no_api_call_for_invalid_format(self): 
        with patch.object(Firm_Account, 'validate_nip_with_mf') as mock_validate:
            account = Firm_Account("Short NIP", "123")
            assert account.nip == "Invalid"
            mock_validate.assert_not_called()
    
    @patch('requests.get')
    def test_validate_nip_with_mf_success(self, mock_get): 
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'result': {
                'subject': {
                    'statusVat': 'Czynny'
                }
            }
        }
        mock_get.return_value = mock_response
         
        with patch('src.firm_account.datetime') as mock_datetime:
            mock_datetime.now.return_value.strftime.return_value = "2025-12-09"
             
            with patch.dict('os.environ', {'BANK_APP_MF_URL': 'https://wl-api.mf.gov.pl'}):
                account = Firm_Account("Test Company", "8461627563")
                
                mock_get.assert_called_once()
                assert account.nip == "8461627563"
    
    @patch('requests.get')
    def test_validate_nip_with_mf_not_active(self, mock_get): 
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'result': {
                'subject': {
                    'statusVat': 'Zwolniony' 
                }
            }
        }
        mock_get.return_value = mock_response
        
        with patch('src.firm_account.datetime') as mock_datetime:
            mock_datetime.now.return_value.strftime.return_value = "2025-12-09"
            
            with patch.dict('os.environ', {'BANK_APP_MF_URL': 'https://wl-api.mf.gov.pl'}):
                with pytest.raises(ValueError, match="Company not registered!!"):
                    Firm_Account("Test Company", "8461627563")
    
    @patch('requests.get')
    def test_validate_nip_with_mf_404(self, mock_get): 
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        
        with patch('src.firm_account.datetime') as mock_datetime:
            mock_datetime.now.return_value.strftime.return_value = "2025-12-09"
            
            with patch.dict('os.environ', {'BANK_APP_MF_URL': 'https://wl-api.mf.gov.pl'}):
                with pytest.raises(ValueError, match="Company not registered!!"):
                    Firm_Account("Test Company", "8461627563")