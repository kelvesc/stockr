from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.models import db, Team, Subteam, Type, User, Asset, Transaction
# from werkzeug.security import generate_password_hash, check_password_hash


api_bp = Blueprint('api', __name__)

# # Error handler for custom excaptons
# @app.errorhandler(GeneralException)
# def exception_raised(e):
#     return jsonify(e.message), e.status_code

# # Error handler for 404: resource not found
# @app.errorhandler(404)
# def resource_not_found(e):
#     return jsonify(error=str(e)), 404

# # Error handler for 405: method not allowed
# @app.errorhandler(405)
# def method_not_allowed(e):
#     return jsonify(error=str(e)), 405

# @api_bp.route('/register', methods=['POST'])
# def register():
#     data = request.get_json()
#     hashed_pw = generate_password_hash(data['password'])
#     user = User(username=data['username'], password=hashed_pw, role='user')
#     db.session.add(user)
#     db.session.commit()
#     return jsonify({"message": "User registered"}), 201


# @api_bp.route('/login', methods=['POST'])
# def login():
#     data = request.get_json()
#     user = User.query.filter_by(username=data['username']).first()
#     if user and check_password_hash(user.password, data['password']):
#         token = create_access_token(identity=user.id)
#         return jsonify({"access_token": token})
#     return jsonify({"error": "Invalid credentials"}), 401

# Fetch teams
@api_bp.route("/teams", methods=["GET"])
def get_teams():
    teams = Team.query.all()
    return jsonify([{"id": t.id, "name": t.name, "location": t.location } for t in teams])

# Fetch subteams
@api_bp.route("/subteams", methods=["GET"])
def get_subteams():
    subteams = Subteam.query.all()
    return jsonify([{"id": u.id, "name": u.name, "team_id": u.team_id} for u in subteams])

# Fetch types
@api_bp.route("/types", methods=["GET"])
def get_types():
    types = Type.query.all()
    return jsonify([{"id": t.id, "name": t.name} for t in types])


# Fetch users
@api_bp.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    return jsonify([{"id": u.id, "coreid": u.coreid, "name": u.name, "last_name": u.last_name, "email": u.email, "team_id": u.team_id, "subteam": u.subteam_id} for u in users])

# Fetch assets
@api_bp.route("/assets", methods=["GET"])
def get_assets():
    assets = Asset.query.all()
    return jsonify([{"id": a.id, "tag": a.tag, "name": a.name, "serial_number": a.serial_number, "owner": a.owner.coreid, "status": a.status, "type": a.type.name, "comments": a.comments} for a in assets])
# return jsonify([{"id": a.id, "tag": a.tag, "name": a.name, "serial_number": a.serial_number, "status": a.status, "comments": a.comments, "type": a.type, "owner": a.owner.coireid} for a in assets])

# Fetch transactions
@api_bp.route("/transactions", methods=["GET"])
def get_transactions():
    transactions = Transaction.query.all()
    return jsonify([{
        "id": t.id,
        # "responsible_id": t.responsible_id,
        "responsible_coreid": t.responsible.coreid,
        "asset_tag": t.asset.tag,
        "date_transaction": t.date_transaction
    } for t in transactions])

# @api_bp.route('/assign', methods=['POST'], endpoint="assign_asset_new")
# @jwt_required()
# def assign_asset():
#     data = request.get_json()
#     user_id = get_jwt_identity()

#     asset = Asset.query.filter_by(tag=data.get('asset_tag')).first()
#     new_owner = User.query.filter_by(coreid=data.get('new_owner_coreid')).first()

#     if not asset:
#         return jsonify({"error": "Asset not found"}), 404
#     if not new_owner:
#         return jsonify({"error": "User not found"}), 404

#     asset.owner_id = new_owner.id
#     db.session.commit()

#     return jsonify({"message": "Asset assigned successfully"}), 200

# Assign asset to a new owner
@api_bp.route("/assign", methods=["POST"])
# @jwt_required()
def assign_asset():
    data = request.get_json()
    asset_tag = data.get("asset_tag")
    new_owner_coreid = data.get("new_owner_coreid")

    if not asset_tag or not new_owner_coreid:
        return jsonify({"error": "Missing asset_tag or new_owner_coreid"}), 400

    new_owner = User.query.filter_by(coreid=new_owner_coreid).first()
    if not new_owner:
        return jsonify({"error": "User not found"}), 404

    asset = Asset.query.filter_by(tag=asset_tag).first()
    if not asset:
        return jsonify({"error": "Asset not found"}), 404

    asset.owner_id = new_owner.id

    # Register transaction
    transaction = Transaction(responsible_id=new_owner.id, asset_tag=asset_tag)
    db.session.add(transaction)

    db.session.commit()
    return jsonify({"message": "Asset assigned successfully"}), 200

