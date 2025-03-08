import sqlalchemy as db
from sqlalchemy import ForeignKey, Column, Integer, String, DateTime
from sqlalchemy.orm import DeclarativeBase, relationship
from datetime import datetime, timezone

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(120), unique=True)
    password = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False)  # user, manager, admin

    def __init__(self, username=None, email=None, password=None, role=None):
        self.username = username
        self.email = email
        self.password = password
        self.role = role

    def __repr__(self):
        return f'<User {self.username!r}>'

class Asset(Base):
    __tablename__ = 'assets'
    id = Column(Integer, primary_key=True, autoincrement=True)
    tag = Column(String(50), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    category = Column(String(50), nullable=False)
    owner_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    owner = relationship('User', backref='assets')

    def __repr__(self):
        return f'<Asset {self.tag}, Name {self.name}, Owner {self.owner_id}>'

class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    asset_tag = Column(Integer, ForeignKey('assets.tag'), nullable=False)
    from_user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    to_user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    date_transaction = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    comments = Column(String(255), default=None)

    def __repr__(self):
        return f'<Transaction Asset {self.asset_id}, From {self.from_user_id}, To {self.to_user_id}>'
