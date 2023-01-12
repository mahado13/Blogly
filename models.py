"""Models for Blogly."""
"""
Author: Mahad Osman
Date: Jan 11th 2023
Assignment Blogly part 2
"""

from venv import create
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)


class Users(db.Model):
    __tablename__ = 'users'

    # @classmethod
    # def get_ordered_list(cls):
    #     return cls.query.order_by(cls.last_name).all()

    id = db.Column(db.Integer, primary_key =True, autoincrement =True)

    first_name = db.Column(db.String(50), nullable = False)
    last_name = db.Column(db.String(50), nullable = False)
    image_url = db.Column(db.String, nullable = True)
    # image_type = db.Column(db.String,  nullable = False)

    
    def __repr__(self) -> str:
        u = self
        return  f"<User id={u.id} Firstname ={u.first_name} LastName={u.last_name} image_url={u.image_url}"

    def get_full_name(self):
        """Simple method to retrieve a full name"""
        return f"{self.first_name} {self.last_name}"
    
class Posts(db.Model):
    __table__name = 'posts'

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    title = db.Column(db.String(50), nullable = False, unique = True)
    content = db.Column(db.String, nullable = False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = db.relationship('Users', backref='posts')




