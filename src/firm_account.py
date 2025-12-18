from src.account import Account
import requests
from datetime import datetime
import os
class Firm_Account(Account):
    def __init__(self, company_name, nip):
        super().__init__()
        self.company_name = company_name 
        if not self.is_nip_valid (nip):
            self.nip = "Invalid"
            self.balance = 0.0
            self.fee = 5.0
            return
        if not self.validate_nip_with_mf(nip):
            raise ValueError("Company not registered!!")
        self.nip = nip
        self.balance = 0.0
        self.fee = 5.0

    def is_nip_valid(self, nip):
        if isinstance(nip, str) and (len(nip) == 10):
            return True
        return False
    def validate_nip_with_mf(self, nip): 
        mf_url = os.getenv('BANK_APP_MF_URL', 'https://wl-test.mf.gov.pl/')
         
        if mf_url.endswith('/'):
            mf_url = mf_url.rstrip('/')
         
        today_date = datetime.now().strftime("%Y-%m-%d")
         
        endpoint_url = f"{mf_url}/api/search/nip/{nip}?date={today_date}"
        
        try: 
            response = requests.get(endpoint_url, timeout=10)
             
            print(f"MF API Response for NIP {nip}: Status {response.status_code}")
            if response.status_code == 200:
                print(f"Response data: {response.text}")
             
            if response.status_code == 200:
                data = response.json()
                 
                if 'result' in data and 'subject' in data['result']:
                    subject = data['result']['subject']
                     
                    if subject.get('statusVat') == 'Czynny':
                        return True
             
            elif response.status_code == 404:
                print(f"Company with NIP {nip} not found in MF registry")
                return False
             
            else:
                print(f"MF API returned status code: {response.status_code}")
                return False
                
        except requests.exceptions.Timeout:
            print(f"Timeout when validating NIP {nip}")
            return False
        except requests.exceptions.ConnectionError:
            print(f"Connection error when validating NIP {nip}")
            return False
        except Exception as e:
            print(f"Error validating NIP {nip}: {str(e)}")
            return False
        
        return False
    def take_loan(self, amount): 
        if self.balance < amount * 2:
            return False
         
        has_zus_payment = any(transaction == -1775.0 for transaction in self.history)
        if not has_zus_payment:
            return False
         
        self.balance += amount
        self.history.append(float(amount))
        return True