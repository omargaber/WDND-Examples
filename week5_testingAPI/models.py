import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
import json

database_name = "bank"
database_path = "postgres://{}:{}@{}/{}".format(
    'username', 'password', 'localhost:5432', database_name)

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


class Account(db.Model):
    __tablename__ = 'user_account'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(), nullable=False)
    last_name = Column(String(), nullable=False)
    balance = Column(Integer, default=0)
