from datetime import datetime
from time import time
from app import app, db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

"""-----------------DATABASE MODELS------------------"""

class Blogpost(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(64))
    subtitle = db.Column(db.String(128))
    author = db.Column(db.String(64))
    date_posted = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    content = db.Column(db.Text)
    editor_id = db.Column(db.Integer, db.ForeignKey('editors.id')) #when creating pass editor=(Editors object)

class Editors(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), index=True, unique=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    posts = db.relationship('Blogpost', backref='editor', lazy='dynamic')
    logins = db.relationship('Logins', backref='login', lazy='dynamic')

    #defines how to print objects of this class
    def __repr__(self):
        return '<Editor {}>'.format(self.name)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(id):
    return Editors.query.get(int(id))

class Messages(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64))
    email = db.Column(db.String(64))
    date_posted = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    message = db.Column(db.Text)

class Logins(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    editor_id = db.Column(db.Integer, db.ForeignKey('editors.id')) #when creating pass login=(Editors object)
