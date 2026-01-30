import pytest
import requests
import json

BASE_URL = "http://127.0.0.1:5000/api/accounts"

@pytest.fixture
def cleanup(): 
    response = requests.get(BASE_URL)
    if response.status_code == 200:
        accounts = response.json()
        for account in accounts:
            requests.delete(f"{BASE_URL}/{account['pesel']}")
     
    try: 
        requests.post(f"{BASE_URL}/save")
    except:
        pass
    
    yield 
    response = requests.get(BASE_URL)
    if response.status_code == 200:
        accounts = response.json()
        for account in accounts:
            requests.delete(f"{BASE_URL}/{account['pesel']}")

class TestSaveLoadEndpoints:
    
    def test_save_single_account(self, cleanup): 
        account_data = {"name": "Save", "surname": "Test", "pesel": "11111111111"}
        create_resp = requests.post(BASE_URL, json=account_data)
        assert create_resp.status_code == 201
         
        save_resp = requests.post(f"{BASE_URL}/save")
        assert save_resp.status_code == 200
        
        save_json = save_resp.json()
        assert save_json["count"] == 1
        assert "Successfully saved" in save_json["message"]
    
    def test_save_multiple_accounts(self, cleanup): 
        accounts = [
            {"name": "A1", "surname": "B1", "pesel": "22222222221"},
            {"name": "A2", "surname": "B2", "pesel": "22222222222"},
            {"name": "A3", "surname": "B3", "pesel": "22222222223"}
        ]
        
        for acc in accounts:
            resp = requests.post(BASE_URL, json=acc)
            assert resp.status_code == 201
         
        save_resp = requests.post(f"{BASE_URL}/save")
        assert save_resp.status_code == 200
        assert save_resp.json()["count"] == 3
    
    def test_save_empty_registry(self, cleanup): 
        save_resp = requests.post(f"{BASE_URL}/save")
        assert save_resp.status_code == 200
        assert save_resp.json()["count"] == 0
    
    def test_load_accounts(self, cleanup): 
        account_data = {"name": "Load", "surname": "Test", "pesel": "33333333333"}
        requests.post(BASE_URL, json=account_data)
        requests.post(f"{BASE_URL}/save")
         
        requests.delete(f"{BASE_URL}/33333333333")
         
        count_resp = requests.get(f"{BASE_URL}/count")
        assert count_resp.json()["count"] == 0
         
        load_resp = requests.post(f"{BASE_URL}/load")
        assert load_resp.status_code == 200
        assert load_resp.json()["count"] == 1 
        get_resp = requests.get(f"{BASE_URL}/33333333333")
        assert get_resp.status_code == 200
        assert get_resp.json()["name"] == "Load"
    
    def test_load_empty_database(self, cleanup): 
        response = requests.get(BASE_URL)
        if response.status_code == 200:
            accounts = response.json()
            for account in accounts:
                requests.delete(f"{BASE_URL}/{account['pesel']}")
         
        load_resp = requests.post(f"{BASE_URL}/load")
        assert load_resp.status_code == 200
        
        count = load_resp.json()["count"]
        assert count in [0, 1], f"Unexpected count: {count}"
    
    def test_save_and_load_preserves_data(self, cleanup): 
        account_data = {"name": "Full", "surname": "Cycle", "pesel": "44444444444"}
        create_resp = requests.post(BASE_URL, json=account_data)
        initial_data = create_resp.json()["account"]
         
        requests.post(f"{BASE_URL}/save")
         
        update_data = {"name": "Updated", "surname": "Name"}
        requests.patch(f"{BASE_URL}/44444444444", json=update_data)
         
        requests.post(f"{BASE_URL}/load")
         
        get_resp = requests.get(f"{BASE_URL}/44444444444")
        loaded_data = get_resp.json()
         
        assert loaded_data["name"] == "Full"
        assert loaded_data["surname"] == "Cycle"
    
    def test_save_twice_overwrites(self, cleanup): 
        acc1 = {"name": "First", "surname": "Save", "pesel": "55555555555"}
        requests.post(BASE_URL, json=acc1)
        requests.post(f"{BASE_URL}/save")
         
        update_data = {"name": "Updated"}
        requests.patch(f"{BASE_URL}/55555555555", json=update_data)
         
        requests.post(f"{BASE_URL}/save") 
        requests.delete(f"{BASE_URL}/55555555555")
        requests.post(f"{BASE_URL}/load")
        
        get_resp = requests.get(f"{BASE_URL}/55555555555")
        assert get_resp.json()["name"] == "Updated"