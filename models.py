from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Goal(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    Goal = db.Column(db.String(300), nullable = False)
    completed = db.Column(db.Boolean , default = False)

class Task(db.Model):
    pass