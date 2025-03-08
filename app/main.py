from flask import Flask #, jsonify, request
from flask_jwt_extended import JWTManager
import os
from app.models import db
from app.routes import api_bp


app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'stockr.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# print(app.url_map)

app.config["JWT_SECRET_KEY"] = "super-secret-key" 
jwt = JWTManager(app)

# Register Blueprint
app.register_blueprint(api_bp, url_prefix="/api")

@app.route("/")
def home():
    return "Stockr is running!"


if __name__ == "__main__":
    print('Running app...')
    # Create tables if they don't exist
    with app.app_context():
        print("Creating database...")
        db.create_all()
        print("Database created...")
        app.run(debug=True)
        home()
