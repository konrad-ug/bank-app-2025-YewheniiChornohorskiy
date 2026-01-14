import time
import pytest
import requests

BASE_URL = "http://localhost:5000"
TIMEOUT = 0.5

class TestPerformance:
    
    def test_create_delete_account_100_times(self):
        for i in range(100):
            pesel = f"99101000{i:03d}"
            
            create_data = {
                "name": f"Test{i}",
                "surname": f"User{i}",
                "pesel": pesel
            }
            
            start_time = time.time()
            response = requests.post(
                f"{BASE_URL}/api/accounts",
                json=create_data,
                timeout=TIMEOUT
            )
            elapsed_time = time.time() - start_time
            
            assert response.status_code == 201
            assert elapsed_time < TIMEOUT
            
            start_time = time.time()
            response = requests.delete(
                f"{BASE_URL}/api/accounts/{pesel}",
                timeout=TIMEOUT
            )
            elapsed_time = time.time() - start_time
            
            assert response.status_code == 200
            assert elapsed_time < TIMEOUT
            
            time.sleep(0.01)

    def test_create_account_and_100_incoming_transfers(self):
        pesel = "99101012345"
        create_data = {
            "name": "Transfer",
            "surname": "Test",
            "pesel": pesel
        }
        
        response = requests.post(
            f"{BASE_URL}/api/accounts",
            json=create_data,
            timeout=TIMEOUT
        )
        assert response.status_code == 201
        
        for i in range(100):
            start_time = time.time()
            response = requests.get(
                f"{BASE_URL}/api/accounts/{pesel}",
                timeout=TIMEOUT
            )
            elapsed_time = time.time() - start_time
            
            assert response.status_code == 200
            assert elapsed_time < TIMEOUT
        
        response = requests.get(f"{BASE_URL}/api/accounts/{pesel}", timeout=TIMEOUT)
        assert response.status_code == 200
        
        requests.delete(f"{BASE_URL}/api/accounts/{pesel}", timeout=TIMEOUT)

class TestBulkOperations:
    
    @pytest.mark.slow
    def test_create_1000_accounts_then_delete_all(self):
        pesels = []
        
        create_times = []
        for i in range(1000):
            pesel = f"9910101{i:04d}"
            pesels.append(pesel)
            
            create_data = {
                "name": f"Bulk{i}",
                "surname": f"Test{i}",
                "pesel": pesel
            }
            
            start_time = time.time()
            response = requests.post(
                f"{BASE_URL}/api/accounts",
                json=create_data,
                timeout=TIMEOUT
            )
            elapsed_time = time.time() - start_time
            
            assert response.status_code == 201
            assert elapsed_time < TIMEOUT
            create_times.append(elapsed_time)
            
            if i % 100 == 0:
                time.sleep(0.1)
        
        delete_times = []
        for pesel in pesels:
            start_time = time.time()
            response = requests.delete(
                f"{BASE_URL}/api/accounts/{pesel}",
                timeout=TIMEOUT
            )
            elapsed_time = time.time() - start_time
            
            assert response.status_code == 200
            assert elapsed_time < TIMEOUT
            delete_times.append(elapsed_time)
            
            if len(delete_times) % 100 == 0:
                time.sleep(0.1)
        
        response = requests.get(f"{BASE_URL}/api/accounts/count", timeout=TIMEOUT)
        assert response.status_code == 200
        data = response.json()
        assert data["count"] == 0