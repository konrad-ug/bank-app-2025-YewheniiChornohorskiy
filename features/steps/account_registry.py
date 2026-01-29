from behave import *
import requests

URL = "http://localhost:5000"

@given('Account registry is empty')
def step_impl(context):
    response = requests.get(URL + "/api/accounts")
    accounts = response.json()
    
    for account in accounts:
        pesel = account["pesel"]
        requests.delete(URL + f"/api/accounts/{pesel}")

@given('Acoount registry is empty')
def step_impl(context):
    clear_account_registry(context)
 
@given('I create an account using name: "{name}", last name: "{last_name}", pesel: "{pesel}"')
@when('I create an account using name: "{name}", last name: "{last_name}", pesel: "{pesel}"')
@step('I create an account using name: "{name}", last name: "{last_name}", pesel: "{pesel}"')
def create_account(context, name, last_name, pesel):
    json_body = {
        "name": name,
        "surname": last_name,
        "pesel": pesel
    }
    create_resp = requests.post(URL + "/api/accounts", json=json_body)
    assert create_resp.status_code == 201

@then('Number of accounts in registry equals: "{count}"')
def step_impl(context, count):
    response = requests.get(URL + "/api/accounts/count")
    assert response.status_code == 200
    actual_count = response.json()["count"]
    assert actual_count == int(count), f"Expected {count} accounts, but got {actual_count}"

@then('Account with pesel "{pesel}" exists in registry')
def step_impl(context, pesel):
    response = requests.get(URL + f"/api/accounts/{pesel}")
    assert response.status_code == 200
    account_data = response.json()
    assert account_data["pesel"] == pesel

@then('Account with pesel "{pesel}" does not exist in registry')
def step_impl(context, pesel):
    response = requests.get(URL + f"/api/accounts/{pesel}")
    assert response.status_code == 404

@when('I delete account with pesel: "{pesel}"')
def step_impl(context, pesel):
    response = requests.delete(URL + f"/api/accounts/{pesel}")
    assert response.status_code == 200

@when('I update "{field}" of account with pesel: "{pesel}" to "{value}"')
def step_impl(context, field, pesel, value):
    if field not in ["name", "surname"]:
        raise ValueError(f"Invalid field: {field}. Must be 'name' or 'surname'.")
    
    json_body = {field: value}
    response = requests.patch(URL + f"/api/accounts/{pesel}", json=json_body)
    assert response.status_code == 200

@then('Account with pesel "{pesel}" has "{field}" equal to "{value}"')
def step_impl(context, pesel, field, value):
    response = requests.get(URL + f"/api/accounts/{pesel}")
    assert response.status_code == 200
    account_data = response.json()
    
    field_mapping = {
        "name": "name",
        "surname": "surname",
        "pesel": "pesel",
        "balance": "balance"
    }
    
    api_field = field_mapping.get(field, field)
    
    if api_field == "balance":
        actual_value = float(account_data[api_field])
        expected_value = float(value)
        assert abs(actual_value - expected_value) < 0.001, \
            f"Expected {field}={expected_value}, but got {actual_value}"
    else:
        assert str(account_data[api_field]) == value, \
            f"Expected {field}='{value}', but got '{account_data[api_field]}'"
 
def clear_account_registry(context):
    response = requests.get(URL + "/api/accounts")
    accounts = response.json()
    
    for account in accounts:
        pesel = account["pesel"]
        requests.delete(URL + f"/api/accounts/{pesel}")