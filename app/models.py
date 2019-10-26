from datetime import datetime
from hashlib import md5
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

groupadmins = db.Table('groupadmins',
    db.Column('group_id', db.Integer, db.ForeignKey('playing_group.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(320))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    group_id = db.Column(db.Integer, db.ForeignKey('playing_group.id'), nullable=True)
    matches = db.relationship(
        'Match',
        primaryjoin='or_(Match.black_player_id == User.id, Match.white_player_id == User.id)',
        lazy='dynamic')
    admin_of_groups = db.relationship(
        'PlayingGroup',
        secondary=groupadmins,
        primaryjoin=(groupadmins.c.user_id == id),
        backref=db.backref('groupadmins', lazy='dynamic'),
        lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(320))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)

class PlayingGroup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    level = db.Column(db.Integer)
    notes = db.Column(db.String(640))
    admins = db.relationship(
        'User',
        secondary=groupadmins,
        primaryjoin=(groupadmins.c.group_id == id),
        backref=db.backref('groupadmins', lazy='dynamic'),
        lazy='dynamic')
    players = db.relationship('User', backref='group', lazy='dynamic')

    def __repr__(self):
        return '<Playing group {}, level {}>'.format(self.name, self.level)

class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    black_player_id = db.Column(db.Integer, db.ForeignKey('user.id'), index=True, nullable=False)
    white_player_id = db.Column(db.Integer, db.ForeignKey('user.id'), index=True, nullable=False)
    black_player = db.relationship("User", foreign_keys=[black_player_id])
    white_player = db.relationship("User", foreign_keys=[white_player_id])
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    result = db.Column(db.String(16))
    sgf = db.Column(db.String(65536))

