import pytest
import sys
import os
from unittest.mock import patch, Mock
from src.firm_account import Firm_Account
import requests 
os.environ['BANK_APP_MF_URL'] = 'https://wl-test.mf.gov.pl'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestFirmAccountNIPValidation:
    
    @pytest.mark.parametrize("nip, expected_nip", [
        ("1234567890", "Invalid"), 
        ("abcdefghij", "Invalid"), 
        ("123456789", "Invalid"),  
        ("12345678901", "Invalid"), 
        (None, "Invalid"),    
        ("", "Invalid"), 
        ("123-456-78-90", "Invalid") 
    ])
    @patch('src.firm_account.requests.get')
    def test_nip_length_validation(self, mock_get, nip, expected_nip): 
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'result': {
                'subject': None 
            }
        }
        mock_get.return_value = mock_response
         
        if nip and len(nip) == 10: 
            with pytest.raises(ValueError, match="Company not registered!!"):
                Firm_Account("Test Company", nip)
        else: 
            account = Firm_Account("Test Company", nip)
            assert account.nip == expected_nip
    
    @patch('src.firm_account.requests.get')
    def test_valid_nip_with_api_success(self, mock_get, monkeypatch): 
        monkeypatch.setenv('BANK_APP_MF_URL', 'https://wl-test.mf.gov.pl')
         
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'result': {
                'subject': {
                    'statusVat': 'Czynny'
                }
            }
        }
        mock_response.text = '{"result": {"subject": {"statusVat": "Czynny"}}}'
        mock_get.return_value = mock_response
         
        account = Firm_Account("Valid Company", "8461627563")
        assert account.nip == "8461627563"
        assert account.company_name == "Valid Company"
    
    @patch('src.firm_account.requests.get')
    def test_invalid_nip_with_api_error(self, mock_get, monkeypatch): 
        monkeypatch.setenv('BANK_APP_MF_URL', 'https://wl-test.mf.gov.pl')
        
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'result': {
                'subject': {
                    'statusVat': 'Nieczynny' 
                }
            }
        }
        mock_response.text = '{"result": {"subject": {"statusVat": "Nieczynny"}}}'
        mock_get.return_value = mock_response
         
        with pytest.raises(ValueError, match="Company not registered!!"):
            Firm_Account("Invalid Company", "8461627563")
    
    @patch('src.firm_account.requests.get')
    def test_api_not_found_response(self, mock_get, monkeypatch): 
        monkeypatch.setenv('BANK_APP_MF_URL', 'https://wl-test.mf.gov.pl')
        
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response 
        with pytest.raises(ValueError, match="Company not registered!!"):
            Firm_Account("Non-existent Company", "8461627563")
    
    @patch('src.firm_account.requests.get')
    def test_api_timeout(self, mock_get, monkeypatch): 
        monkeypatch.setenv('BANK_APP_MF_URL', 'https://wl-test.mf.gov.pl')
        
        mock_get.side_effect = requests.exceptions.Timeout("Connection timeout")
         
        with pytest.raises(ValueError, match="Company not registered!!"):
            Firm_Account("Company", "8461627563")
    
    @patch('src.firm_account.requests.get')
    def test_api_connection_error(self, mock_get, monkeypatch): 
        monkeypatch.setenv('BANK_APP_MF_URL', 'https://wl-test.mf.gov.pl')
        
        mock_get.side_effect = requests.exceptions.ConnectionError("Connection failed") 
        with pytest.raises(ValueError, match="Company not registered!!"):
            Firm_Account("Company", "8461627563")
    
    @patch('src.firm_account.requests.get')
    def test_api_different_urls(self, mock_get): 
        test_cases = [
            ('https://wl-test.mf.gov.pl', 'https://wl-test.mf.gov.pl/api/search/nip/8461627563?date='),
            ('https://wl-api.mf.gov.pl', 'https://wl-api.mf.gov.pl/api/search/nip/8461627563?date='),
            ('https://wl-test.mf.gov.pl/', 'https://wl-test.mf.gov.pl/api/search/nip/8461627563?date='),
        ]
        
        for base_url, expected_url_prefix in test_cases:
            with patch.dict(os.environ, {'BANK_APP_MF_URL': base_url}):
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
                
                Firm_Account("Test Company", "8461627563")  
                called_url = mock_get.call_args[0][0]
                assert called_url.startswith(expected_url_prefix)
                assert "?date=" in called_url
                assert len(called_url.split("?date=")[1]) == 10 
                mock_get.reset_mock()
        
    def test_invalid_nip_no_api_call(self): 
        account = Firm_Account("Invalid NIP Company", "12345")
        assert account.nip == "Invalid"
        assert account.balance == 0.0
    
    @patch('src.firm_account.requests.get')
    def test_today_date_format(self, mock_get, monkeypatch): 
        monkeypatch.setenv('BANK_APP_MF_URL', 'https://wl-test.mf.gov.pl')
        
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
        
        Firm_Account("Test Company", "8461627563") 
        called_url = mock_get.call_args[0][0]
        assert "?date=" in called_url
        date_part = called_url.split("?date=")[1]
        assert len(date_part) == 10  
    
    @patch('src.firm_account.print') 
    @patch('src.firm_account.requests.get')
    def test_api_response_logging(self, mock_get, mock_print, monkeypatch): 
        monkeypatch.setenv('BANK_APP_MF_URL', 'https://wl-test.mf.gov.pl')
        
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'result': {
                'subject': {
                    'statusVat': 'Czynny'
                }
            }
        }
        mock_response.text = 'Test response text'
        mock_get.return_value = mock_response
        
        Firm_Account("Test Company", "8461627563")
         
        mock_print.assert_any_call(f"MF API Response for NIP 8461627563: Status 200")
        mock_print.assert_any_call(f"Response data: Test response text")

if __name__ == "__main__":
    pytest.main([__file__, "-v"])