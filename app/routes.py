from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.models import db, User, Asset, Transaction
from werkzeug.security import generate_password_hash, check_password_hash

api_bp = Blueprint('api', __name__)

@api_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed_pw = generate_password_hash(data['password'])
    user = User(username=data['username'], password=hashed_pw, role='user')
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User registered"}), 201

@api_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and check_password_hash(user.password, data['password']):
        token = create_access_token(identity=user.id)
        return jsonify({"access_token": token})
    return jsonify({"error": "Invalid credentials"}), 401

@api_bp.route('/assets', methods=['GET'])
@jwt_required()
def get_assets():
    assets = Asset.query.all()
    return jsonify([{"id": a.id, "name": a.name, "owner": a.owner.username} for a in assets])

@api_bp.route('/assign', methods=['POST'])
@jwt_required()
def assign_asset():
    data = request.get_json()
    user_id = get_jwt_identity()
    asset = Asset.query.get(data['asset_id'])
    if asset:
        asset.owner_id = user_id
        db.session.commit()
        return jsonify({"message": "Asset assigned"})
    return jsonify({"error": "Asset not found"}), 404
