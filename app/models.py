from datetime import datetime
from time import time
import jwt
from app import db, login, app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(128))
    projects = db.relationship('Projects', backref='author', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)  

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)


class Projects(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(140))
    company = db.Column(db.String(140))
    priority = db.Column(db.String(140))
    priority_dept = db.Column(db.String(140))
    requester = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    status = db.Column(db.String(140))
    department = db.Column(db.String(140))
    hours = db.Column(db.String(140))
    ticket = db.Column(db.String(140))
    Comments = db.relationship('Comments', backref='authcomment', lazy='dynamic')

    def __repr__(self):
        return '<Projects {}>'.format(self.description)


class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(1024))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    comment_id = db.Column(db.Integer, db.ForeignKey('projects.id'))

    def __repr__(self):
        return '<Comments {}>'.format(self.comment)



class CompleteProjects(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(140))
    company = db.Column(db.String(140))
    priority = db.Column(db.String(140))
    priority_dept = db.Column(db.String(140))
    requester = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    department = db.Column(db.String(140))
    hours = db.Column(db.String(140))
    ticket = db.Column(db.String(140))
    Comments = db.relationship('CompleteComments', backref='authcomment', lazy='dynamic')

    def __repr__(self):
        return '<CompleteProjects {}>'.format(self.description)


class CompleteComments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(1024))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    comment_id = db.Column(db.Integer, db.ForeignKey('complete_projects.id'))

    def __repr__(self):
        return '<CompleteComments {}>'.format(self.comment)



@login.user_loader
def load_user(id):
	return User.query.get(int(id))


