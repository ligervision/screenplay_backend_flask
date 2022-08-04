# from datetime import datetime
from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.dialects.postgresql import JSON


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    screenplays = db.relationship('Screenplay', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)
        
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
        
        
@login.user_loader
def load_user(id):
    return User.query.get(int(id))
        

class Screenplay(db.Model):
    screenplay_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(140))
    total_scenes = db.Column(db.String(140))
    logline = db.Column(db.String(255))
    dramatic_question = db.Column(db.String(255))
    genre1 = db.Column(db.String(140))
    genre2 = db.Column(db.String(140))
    genre3 = db.Column(db.String(140))
    narrative_type = db.Column(db.String(140))
    # timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<Screenplay {}>'.format(self.title)
