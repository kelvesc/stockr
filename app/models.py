from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
from sqlalchemy.orm import DeclarativeBase

# db = SQLAlchemy()

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)

class Team(db.Model):
    __tablename__ = "teams"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    location = db.Column(db.String(50), unique=False, nullable=False)

class Subteam(db.Model):
    __tablename__ = "subteams"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), unique=False, nullable=False)
    team = db.relationship('Team', backref='subteams')

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    coreid = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(50), unique=False, nullable=False)
    last_name = db.Column(db.String(50), unique=False, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    psw = db.Column(db.String(50), unique=False, nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), unique=False, nullable=False)
    subteam_id = db.Column(db.Integer, db.ForeignKey('subteams.id'), unique=False, nullable=False)
    team = db.relationship('Team', backref='users')
    subteam = db.relationship('Subteam', backref='users')


class Type(db.Model):
    __tablename__ = "types"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

class Asset(db.Model):
    __tablename__ = "assets"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tag = db.Column(db.Integer, unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    serial_number = db.Column(db.String(100), unique=True, nullable=False)
    status = db.Column(db.String(50), nullable=False)
    comments = db.Column(db.String(200), nullable=False)
    type_id = db.Column(db.Integer, db.ForeignKey('types.id'), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=False)
    type = db.relationship('Type', backref='assets')
    team = db.relationship('Team', backref='assets')
    owner = db.relationship('User', backref='assets')

class Transaction(db.Model):
    __tablename__ = "transactions"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    responsible_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    asset_tag = db.Column(db.Integer, db.ForeignKey('assets.tag'), nullable=False)
    date_transaction = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    responsible = db.relationship('User', backref='transactions')
    asset = db.relationship('Asset', backref='transactions')
