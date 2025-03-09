from flask import Flask #, jsonify, request
from flask_jwt_extended import JWTManager
import os
from app.models import db
from app.routes import api_bp
# from sqlalchemy import inspect


app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'stockr.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["JWT_SECRET_KEY"] = "super-secret-key" 
jwt = JWTManager(app)

# Register Blueprint
app.register_blueprint(api_bp, url_prefix="/api")

@app.route("/")
def home():
    return "Stockr is running!"

db.init_app(app)
# print(app.config['SQLALCHEMY_DATABASE_URI'])

with app.app_context():
    # print("Creating database...")
    db.create_all()
    # print("Tables created")
    # app.run(debug=True)

if __name__ == "__main__":
    app.run(debug=True)
    home()
    # print(app.config['SQLALCHEMY_DATABASE_URI'])
    # Create tables if they don't exist
    # with app.app_context():
    #     print("Creating database...")
    #     db.create_all()
    #     # print("Tables created:", db.engine.table_names())
    #     inspector = inspect(db.engine)
    #     print(inspector.get_table_names())
    #     app.run(debug=True)
    #     home()
