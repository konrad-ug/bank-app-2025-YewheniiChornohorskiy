from flask import Flask, request, jsonify
from src.accounts_registry import AccountsRegistry
from src.personal_account import Personal_Account

app = Flask(__name__)
registry = AccountsRegistry()

@app.route("/api/accounts", methods=['POST'])
def create_account():
    data = request.get_json()
     
    if not data or 'name' not in data or 'surname' not in data or 'pesel' not in data:
        return jsonify({"error": "Missing required fields: name, surname, pesel"}), 400
     
    existing_account = registry.find_account_by_pesel(data["pesel"])
    if existing_account:
        return jsonify({"error": "Account with this PESEL already exists"}), 409
     
    account = Personal_Account(data["name"], data["surname"], data["pesel"])
    registry.add_account(account)
    
    return jsonify({
        "message": "Account created",
        "account": {
            "name": account.first_name,
            "surname": account.last_name,
            "pesel": account.pesel,
            "balance": account.balance
        }
    }), 201

@app.route("/api/accounts", methods=['GET'])
def get_all_accounts():
    accounts = registry.get_all_accounts()
    accounts_data = []
    
    for acc in accounts:
        accounts_data.append({
            "name": acc.first_name,
            "surname": acc.last_name,
            "pesel": acc.pesel,
            "balance": acc.balance
        })
    
    return jsonify(accounts_data), 200

@app.route("/api/accounts/count", methods=['GET'])
def get_account_count():
    count = registry.get_accounts_count()
    return jsonify({"count": count}), 200

@app.route("/api/accounts/<pesel>", methods=['GET'])
def get_account_by_pesel(pesel):
    account = registry.find_account_by_pesel(pesel)
    
    if not account:
        return jsonify({"error": "Account not found"}), 404
    
    return jsonify({
        "name": account.first_name,
        "surname": account.last_name,
        "pesel": account.pesel,
        "balance": account.balance
    }), 200

@app.route("/api/accounts/<pesel>", methods=['PATCH'])
def update_account(pesel):
    account = registry.find_account_by_pesel(pesel)
    
    if not account:
        return jsonify({"error": "Account not found"}), 404
    
    data = request.get_json() 
    if not data or ('name' not in data and 'surname' not in data):
        return jsonify({"error": "No fields to update provided"}), 400
     
    if 'name' in data:
        account.first_name = data['name']
    
    if 'surname' in data:
        account.last_name = data['surname']
    
    return jsonify({
        "message": "Account updated",
        "account": {
            "name": account.first_name,
            "surname": account.last_name,
            "pesel": account.pesel,
            "balance": account.balance
        }
    }), 200

@app.route("/api/accounts/<pesel>", methods=['DELETE'])
def delete_account(pesel):
    account = registry.find_account_by_pesel(pesel) 

    if not account:
        return jsonify({"error": "Account not found"}), 404 
    
    registry.accounts.remove(account) 
    return jsonify({"message": "Account deleted"}), 200

if __name__ == '__main__':
    app.run(debug=True)