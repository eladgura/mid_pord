import secrets
from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(100), unique=True, nullable=False, default=secrets.token_urlsafe)  # JWT hash
    username = db.Column(db.String(100), unique=False, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    picture = db.Column(db.String(100))
    is_admin = db.Column(db.Boolean, default=True)
    password = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

    def to_dict(self):
        return {
            'id': self.id,
            'token': self.token,
            'username': self.username,
            'email': self.email,
            'picture': self.picture,
            'is_admin': self.is_admin
        }

