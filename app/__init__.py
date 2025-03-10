from flask import Flask
from sqlalchemy import Column, Integer, String
import sqlalchemy as db
from flask_jwt_extended import JWTManager
from flask_cors import CORS
#from app.config import Config

#db = SQLAlchemy()
jwt = JWTManager()


def create_app():
    app = Flask(__name__)
#    app.config.from_object(Config)

    #db.init_app(app)
    jwt.init_app(app)
    CORS(app)

    from app.routes import api_bp
    app.register_blueprint(api_bp)

    return app
