import pytest
import requests 

BASE_URL = "http://127.0.0.1:5000/api/accounts"

@pytest.fixture(scope="module")
def api_server(): 
    yield BASE_URL

@pytest.fixture
def sample_account_data():
    return {
        "name": "Jan",
        "surname": "Kowalski",
        "pesel": "89092909825"
    }

@pytest.fixture
def another_account_data():
    return {
        "name": "Anna",
        "surname": "Nowak",
        "pesel": "90010112345"
    }

@pytest.fixture
def cleanup_accounts(api_server): 
    yield 
    response = requests.get(api_server)
    if response.status_code == 200:
        accounts = response.json()
        for account in accounts:
            requests.delete(f"{api_server}/{account['pesel']}")

class TestAccountCRUD:
    def test_create_account_success(self, api_server, sample_account_data, cleanup_accounts): 
        response = requests.post(api_server, json=sample_account_data)
        
        assert response.status_code == 201
        data = response.json()
        assert data["message"] == "Account created"
        assert data["account"]["name"] == sample_account_data["name"]
        assert data["account"]["surname"] == sample_account_data["surname"]
        assert data["account"]["pesel"] == sample_account_data["pesel"]
        assert "balance" in data["account"]

    def test_create_account_missing_fields(self, api_server, cleanup_accounts): 
        incomplete_data = {"name": "Jan"}
        response = requests.post(api_server, json=incomplete_data)
        
        assert response.status_code == 400
        data = response.json()
        assert "error" in data

    def test_create_account_duplicate_pesel(self, api_server, sample_account_data, cleanup_accounts): 
        response1 = requests.post(api_server, json=sample_account_data)
        assert response1.status_code == 201 
        response2 = requests.post(api_server, json=sample_account_data)
        assert response2.status_code == 409
        data = response2.json()
        assert "error" in data

    def test_get_all_accounts(self, api_server, sample_account_data, another_account_data, cleanup_accounts): 
        requests.post(api_server, json=sample_account_data)
        requests.post(api_server, json=another_account_data)
        
        response = requests.get(api_server)
        
        assert response.status_code == 200
        accounts = response.json()
        assert len(accounts) == 2
        assert isinstance(accounts, list)

    def test_get_account_count(self, api_server, sample_account_data, another_account_data, cleanup_accounts): 
        requests.post(api_server, json=sample_account_data)
        requests.post(api_server, json=another_account_data)
        
        response = requests.get(f"{api_server}/count")
        
        assert response.status_code == 200
        data = response.json()
        assert data["count"] == 2

    def test_get_account_by_pesel(self, api_server, sample_account_data, cleanup_accounts): 
        requests.post(api_server, json=sample_account_data)
        
        response = requests.get(f"{api_server}/{sample_account_data['pesel']}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == sample_account_data["name"]
        assert data["surname"] == sample_account_data["surname"]
        assert data["pesel"] == sample_account_data["pesel"]

    def test_get_account_by_pesel_not_found(self, api_server, cleanup_accounts): 
        response = requests.get(f"{api_server}/00000000000")
        
        assert response.status_code == 404
        data = response.json()
        assert "error" in data

    def test_update_account_partial(self, api_server, sample_account_data, cleanup_accounts):  
        requests.post(api_server, json=sample_account_data) 
        update_data = {"name": "Marek"}
        response = requests.patch(f"{api_server}/{sample_account_data['pesel']}", json=update_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Account updated"
        assert data["account"]["name"] == "Marek"
        assert data["account"]["surname"] == sample_account_data["surname"]  # Nazwisko bez zmian

    def test_update_account_full(self, api_server, sample_account_data, cleanup_accounts): 
        requests.post(api_server, json=sample_account_data) 
        update_data = {"name": "Marek", "surname": "Wiśniewski"}
        response = requests.patch(f"{api_server}/{sample_account_data['pesel']}", json=update_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["account"]["name"] == "Marek"
        assert data["account"]["surname"] == "Wiśniewski"
        assert data["account"]["pesel"] == sample_account_data["pesel"]  # PESEL bez zmian

    def test_update_account_no_fields(self, api_server, sample_account_data, cleanup_accounts): 
        requests.post(api_server, json=sample_account_data) 
        update_data = {}
        response = requests.patch(f"{api_server}/{sample_account_data['pesel']}", json=update_data)
        
        assert response.status_code == 400
        data = response.json()
        assert "error" in data

    def test_update_account_not_found(self, api_server, cleanup_accounts): 
        update_data = {"name": "Test"}
        response = requests.patch(f"{api_server}/00000000000", json=update_data)
        
        assert response.status_code == 404
        data = response.json()
        assert "error" in data

    def test_delete_account(self, api_server, sample_account_data, cleanup_accounts): 
        requests.post(api_server, json=sample_account_data) 
        response1 = requests.get(f"{api_server}/{sample_account_data['pesel']}")
        assert response1.status_code == 200
        
        # Usuń konto
        response2 = requests.delete(f"{api_server}/{sample_account_data['pesel']}")
        assert response2.status_code == 200
        data = response2.json()
        assert data["message"] == "Account deleted" 
        response3 = requests.get(f"{api_server}/{sample_account_data['pesel']}")
        assert response3.status_code == 404

    def test_delete_account_not_found(self, api_server, cleanup_accounts): 
        response = requests.delete(f"{api_server}/00000000000")
        
        assert response.status_code == 404
        data = response.json()
        assert "error" in data

    def test_account_balance_persistence(self, api_server, sample_account_data, cleanup_accounts):  
        response1 = requests.post(api_server, json=sample_account_data)
        initial_balance = response1.json()["account"]["balance"] 
        response2 = requests.get(f"{api_server}/{sample_account_data['pesel']}")
        retrieved_balance = response2.json()["balance"]
        
        assert initial_balance == retrieved_balance

if __name__ == "__main__":
    pytest.main([__file__, "-v"])