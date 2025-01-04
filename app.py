from flask import Flask, jsonify, request, abort, render_template
import json
import os
import re

app = Flask(__name__)
DATA_FILE = "data/ip_list.json"



def validate_ip(ip):
    ip_regex = r"^\d{1,3}(\.\d{1,3}){3}$"
    return re.match(ip_regex, ip) is not None

# Route pour la page d'accueil
@app.route('/')
def home():
    return render_template('index.html')

def load_data():
    if not os.path.exists(DATA_FILE):
        return {"ipam": []}
    with open(DATA_FILE, "r") as file:
        return json.load(file)

def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

@app.route('/ipam', methods=['GET'])
def get_all():
    data = load_data()
    return jsonify(data)

# Route pour ajouter une nouvelle entrée
@app.route('/ipam', methods=['POST'])
def add_data():
    new_entry = request.json
    ip = new_entry.get('ip')

    # Valider l'adresse IP
    if not validate_ip(ip):
        return jsonify({"message": "Adresse IP invalide"}), 400

    # Vérifier si l'adresse IP existe déjà
    data = load_data()

    for entry in data["ipam"]:
        if entry["ip"] == ip:
            return jsonify({"message": "L'adresse IP existe déjà"}), 400
    for i in data["ipam"]:
        if i["hostname"] == new_entry["hostname"]:
            return jsonify({"message": "le hostname existe deja"}), 400
    # Ajouter la nouvelle entrée
    data["ipam"].append(new_entry)
    save_data(data)
    return jsonify({"message": "Entry added successfully"}), 201

@app.route('/ipam/<ip>', methods=['PUT'])
def update_data(ip):
    updated_entry = request.json
    data = load_data()
    for entry in data["ipam"]:
        if entry["ip"] == ip:
            entry.update(updated_entry)
            save_data(data)
            return jsonify({"message": "Entry updated successfully"}), 200
    abort(404, description="Entry not found")

@app.route('/ipam/<ip>', methods=['DELETE'])
def delete_data(ip):
    data = load_data()
    data["ipam"] = [entry for entry in data["ipam"] if entry["ip"] != ip]
    save_data(data)
    return jsonify({"message": "Entry deleted successfully"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)