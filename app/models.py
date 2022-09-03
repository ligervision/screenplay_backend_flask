# from datetime import datetime
from app import db, login
from flask_login import UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.sql import func


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    screenplay = db.relationship('Screenplay', backref='author', lazy='dynamic')

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password_hash = self.set_password(password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        return generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
        
        
@login.user_loader
def load_user(id):
    return User.query.get(int(id))
        

class Screenplay(db.Model):
    screenplay_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(140), nullable=False)
    total_scenes = db.Column(db.Integer)
    logline = db.Column(db.String(8000))
    dramatic_question = db.Column(db.String(8000))
    genre1 = db.Column(db.String(140))
    genre2 = db.Column(db.String(140))
    genre3 = db.Column(db.String(140))
    narrative_type = db.Column(db.String(255))
    description = db.Column(db.String(8000))
    scene = db.relationship('Scene', backref='screenplay', lazy='dynamic')

    def __init__(self, user_id, title, total_scenes, logline, dramatic_question, genre1, genre2, genre3, narrative_type, description):
        self.user_id = user_id
        self.title = title
        self.total_scenes = total_scenes # THIS STARTS AT 0
        self.logline = logline
        self.dramatic_question = dramatic_question
        self.genre1 = genre1
        self.genre2 = genre2
        self.genre3 = genre3
        self.narrative_type = narrative_type
        self.description = description

    def __repr__(self):
        return '<Screenplay {}>'.format(self.title)


class Scene(db.Model):
    scene_id = db.Column(db.Integer, primary_key=True)
    screenplay_id = db.Column(db.Integer, db.ForeignKey('screenplay.screenplay_id'), nullable=False)
    scene_index = db.Column(db.Integer)
    scene_sequence = db.Column(db.Integer)
    slugline = db.Column(db.String(500), nullable=False)
    content = db.Column(db.String(65535))
    description = db.Column(db.String(8000))
    plot_section = db.Column(db.String(140))

    def __init__(self, screenplay_id, scene_index, scene_sequence, slugline, content, description, plot_section):

        self.scene_id = 129
        self.screenplay_id = screenplay_id
        self.scene_index = scene_index
        self.scene_sequence = scene_sequence
        self.slugline = slugline
        self.content = content
        self.description = description
        self.plot_section = plot_section

    def __repr__(self):
        return '<Scene {}>'.format(self.slugline)
