import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import json
from settings import DATABASE_NAME, DATABASE_PORT, DATABASE_OWNER, DATABASE_PASSWORD

database_name = DATABASE_NAME
database_path = f'postgresql://{DATABASE_OWNER}:{DATABASE_PASSWORD}@localhost:{DATABASE_PORT}/{database_name}'

db = SQLAlchemy()

"""
setup_db(app)
    binds a flask application and a SQLAlchemy service
"""


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    # migrate = Migrate(app, db)
    db.create_all()


"""
Question

"""


class Question(db.Model):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True)
    question = Column(String)
    answer = Column(String)
    category = Column(String)
    difficulty = Column(Integer)
    rating = Column(Integer, default=3)

    def __init__(self, question, answer, category, difficulty, rating):
        self.question = question
        self.answer = answer
        self.category = category
        self.difficulty = difficulty
        self.rating = rating

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'question': self.question,
            'answer': self.answer,
            'category': self.category,
            'difficulty': self.difficulty,
            'rating': self.rating
        }


"""
Category

"""


class Category(db.Model):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    type = Column(String)

    def __init__(self, type):
        self.type = type

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'type': self.type
        }
