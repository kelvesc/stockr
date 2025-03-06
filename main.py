from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Helper function for DB connection
def get_db_connection():
    conn = sqlite3.connect("stockr.db")
    conn.row_factory = sqlite3.Row
    return conn

# User login
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE username = ? AND password = ?", 
                        (data["username"], data["password"])).fetchone()
    conn.close()
    if user:
        return jsonify({"message": "Login successful"}), 200
    return jsonify({"error": "Invalid credentials"}), 401

# Fetch assets
@app.route("/assets", methods=["GET"])
def get_assets():
    conn = get_db_connection()
    assets = conn.execute("SELECT * FROM assets").fetchall()
    conn.close()
    return jsonify([dict(asset) for asset in assets])

# Add an asset (for testing)
@app.route("/add_asset", methods=["POST"])
def add_asset():
    data = request.json
    conn = get_db_connection()
    conn.execute("INSERT INTO assets (name, owner) VALUES (?, ?)", 
                 (data["name"], data["owner"]))
    conn.commit()
    conn.close()
    return jsonify({"message": "Asset added"}), 201



@app.route("/")
def home():
    return "Stockr is running!"


if __name__ == "__main__":
    app.run(debug=True)
