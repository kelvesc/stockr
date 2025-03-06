import sqlalchemy as db
from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from datetime import datetime, timezone

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(120), unique=True)
    password = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False)  # user, manager, admin

    def __init__(self, username=None, email=None, password=None, role=None):
        self.name = username
        self.mail = email
        self.password = password
        self.role = role

    def __repr__(self):
        return f'<User {self.name!r}>'

class Asset(Base):
    __tablename__ = 'assets'
    id = Column(Integer, primary_key=True)
    tag = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    category = Column(String(50), nullable=False)
    owner_id = Column(Integer, ForeignKey('user.id'))
    owner = relationship('User', backref='assets')

    def __init__():
        pass

    def __repr__(self):
        return f'<Asset {self.tag}, Name {self.name} Owner {self.owner}'

class Transaction(Base):
    __tablename__ = 'transaction'
    id = Column(Integer, primary_key=True)
    asset_id = Column(Integer, ForeignKey('asset.id'))
    from_user_id = Column(Integer, ForeignKey('user.id'))
    to_user_id = Column(Integer, ForeignKey('user.id'))
    timestamp = Column(DateTime, default=datetime.now(timezone.utc))
