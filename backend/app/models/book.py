import secrets
from app import db

class Book(db.Model):
    __tablename__ = 'book'

    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(100), unique=True, nullable=False, default=secrets.token_urlsafe)
    name = db.Column(db.String(100), nullable=False)
    picture = db.Column(db.String(100))
    genre = db.Column(db.String(100))
    author = db.Column(db.String(100))
    in_stock = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f"<Book {self.name}>"

    def to_dict(self):
        return {
            'id': self.id,
            'token': self.token,
            'name': self.name,
            'picture': self.picture,
            'genre': self.genre,
            'author': self.author,
            'in_stock': self.in_stock
        }
