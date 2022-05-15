import email
from enum import unique
from . import db
from werkzeug.security import generate_password_hash,check_password_hash

class Quote:
    def __init__(self,quote,author):
        self.quote=quote
        self.author=author

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255))
    email = db.Column(db.String(255),unique = True,nullable = False)
    secure_password = db.Column(db.String(255),nullable = False)
    blogs = db.relationship('Blog',backref='user',lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.secure_password = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.secure_password,password)

    def __repr__(self):
        return f'User {self.username}'

class Blog(db.Model):
    __tablename__='blogs'

    id = db.Column(db.Integer,primary_key = True)
    title = db.Column(db.String(255),nullable = False)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    
    def __repr__(self):
        return f'Blog {self.title}'

