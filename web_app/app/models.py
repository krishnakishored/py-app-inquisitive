from app import db
from datetime import datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)  
        
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)

class Verb(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    german = db.Column(db.String(128),unique=True, nullable=False, index=True)
    english = db.Column(db.String(128),nullable=False)
    partsofspeech = db.Column(db.String(32))
    
    def __repr__(self):
        return '{0} : {1}'.format(self.german, self.english)