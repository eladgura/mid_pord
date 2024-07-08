import secrets
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.book import Book
from app.models.user import User

# Define the Blueprint for books
books_bp = Blueprint('books', __name__)

# GET all books
@books_bp.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    return jsonify([book.to_dict() for book in books])

# GET a specific book by ID
@books_bp.route('/books/<int:id>', methods=['GET'])
def get_book(id):
    book = Book.query.get_or_404(id)
    return jsonify(book.to_dict())

@books_bp.route('/books', methods=['POST'])
@jwt_required()
def add_book():
    data = request.get_json()
    new_book = Book(
        name=data['name'],
        genre=data['genre'],
        author=data['author'],
        in_stock=data['in_stock'],
        token=secrets.token_urlsafe()  # Generate token here or assign as needed
    )
    db.session.add(new_book)
    db.session.commit()
    return jsonify(new_book.to_dict()), 201

# PUT update an existing book by ID
@books_bp.route('/books/<int:id>', methods=['PUT'])
@jwt_required()
def update_book(id):
    book = Book.query.get_or_404(id)
    data = request.get_json()

    book.name = data.get('name', book.name)
    book.genre = data.get('genre', book.genre)
    book.author = data.get('author', book.author)
    book.in_stock = data.get('in_stock', book.in_stock)

    db.session.commit()
    return jsonify(book.to_dict())

@books_bp.route('/books/<int:book_id>', methods=['DELETE'])
@jwt_required()
def delete_book(book_id):
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user['username']).first()

    if not user.is_admin:
        return jsonify({"message": "Admin access required"}), 403

    book = Book.query.get_or_404(book_id)
    book.in_stock = 0  # Mark as out of stock
    db.session.commit()
    
    return jsonify({"message": "Book marked as out of stock"}), 200

#WARNING!!!!!!!!!!!
# DELETE a book by ID (only admins can delete)(and it is permenent)
#@books_bp.route('/books/<int:id>', methods=['DELETE'])
#@jwt_required()
#def delete_book(id):
   # book = Book.query.get_or_404(id)
   # current_user = get_jwt_identity()
   # user = User.query.filter_by(username=current_user['username']).first()

   # if not user.is_admin:
     #   return jsonify({"message": "Admin privileges required"}), 403

   ## book.in_stock = 0
    ##db.session.commit()
    ##return '', 204