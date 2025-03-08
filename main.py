from flask import Flask, jsonify, request
import sqlite3
import app.routes

app = Flask(__name__)

# Helper function for DB connection
def get_db_connection():
    conn = sqlite3.connect("stockr.db")
    conn.row_factory = sqlite3.Row
    return conn

# # User login
# @app.route("/login", methods=["POST"])
# def login():
#     data = request.json
#     conn = get_db_connection()
#     user = conn.execute("SELECT * FROM users WHERE username = ? AND password = ?", 
#                         (data["username"], data["password"])).fetchone()
#     conn.close()
#     if user:
#         return jsonify({"message": "Login successful"}), 200
#     return jsonify({"error": "Invalid credentials"}), 401

# Fetch assets
@app.route("/assets", methods=["GET"])
def get_assets():
    conn = get_db_connection()
    assets = conn.execute("SELECT * FROM assets").fetchall()
    conn.close()
    return jsonify([dict(asset) for asset in assets])

# Fetch users
@app.route("/users", methods=["GET"])
def get_users():
    conn = get_db_connection()
    users = conn.execute("SELECT * FROM users").fetchall()
    conn.close()
    return jsonify([dict(user) for user in users])

# Fetch users
@app.route("/transactions", methods=["GET"])
def get_transactions():
    conn = get_db_connection()
    transactions = conn.execute("SELECT * FROM transactions").fetchall()
    conn.close()
    return jsonify([dict(transaction) for transaction in transactions])

# Assing an asset
# @app.route("/assign", methods=["POST"])
# def assign_asset():
#     data = request.get_json()
#     asset_id = data.get("asset_id")
#     new_owner = data.get("new_owner")

#     if not asset_id or not new_owner:
#         return jsonify({"error": "Missing asset_id or new_owner"}), 400

#     conn = get_db_connection()
#     cursor = conn.cursor()

#     cursor.execute('''
#         UPDATE assets 
#         SET owner = ? 
#         WHERE id = ?
#     ''', (new_owner, asset_id))

#     if cursor.rowcount == 0:
#         conn.close()
#         return jsonify({"error": "Asset not found"}), 404

#     conn.commit()
#     conn.close()
#     return jsonify({"message": "Asset assigned successfully"}), 200
@app.route("/assign", methods=["POST"])
def assign_asset():
    data = request.get_json()
    asset_tag = data.get("asset_tag")
    new_owner_coreid = data.get("new_owner_coreid")

    if not asset_tag or not new_owner_coreid:
        return jsonify({"error": "Missing asset_tag or new_owner_coreid"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch user ID using coreid
    cursor.execute("SELECT id FROM users WHERE coreid = ?", (new_owner_coreid,))
    user = cursor.fetchone()
    
    if not user:
        conn.close()
        return jsonify({"error": "User not found"}), 404

    new_owner_id = user[0]

    # Update asset ownership using tag
    cursor.execute('''
        UPDATE assets 
        SET owner = ? 
        WHERE tag = ?
    ''', (new_owner_id, asset_tag))

    if cursor.rowcount == 0:
        conn.close()
        return jsonify({"error": "Asset not found"}), 404

    # Update transactions
    cursor.execute('''
        INSERT INTO transactions (responsible_id, asset_tag, date_transaction) 
        VALUES (?, ?, datetime('now'))
    ''', (new_owner_id, asset_tag))


    conn.commit()
    conn.close()
    return jsonify({"message": "Asset assigned successfully"}), 200



@app.route("/")
def home():
    return "Stockr is running!"


if __name__ == "__main__":
    app.run(debug=True)
