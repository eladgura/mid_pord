from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.user import User
from app.models.book import Book
from app.models.loan import Loan
from app import db

admin_bp = Blueprint('admin', __name__)

# Admin route to add a new book
@admin_bp.route('/books', methods=['POST'])
@jwt_required()
def add_book():
    if not get_jwt_identity().get('is_admin'):
        return jsonify({"message": "Unauthorized access"}), 403
    
    data = request.get_json()
    title = data.get('title')
    author = data.get('author')
    description = data.get('description')
    year = data.get('year')
    # Add more fields as per your Book model
    
    new_book = Book(title=title, author=author, description=description, year=year)
    db.session.add(new_book)
    db.session.commit()

    return jsonify({"message": "Book added successfully"}), 201

# Admin route to view all loans
@admin_bp.route('/loans', methods=['GET'])
@jwt_required()
def view_loans():
    if not get_jwt_identity().get('is_admin'):
        return jsonify({"message": "Unauthorized access"}), 403
    
    loans = Loan.query.all()
    loan_list = []
    for loan in loans:
        loan_list.append({
            'id': loan.id,
            'book_id': loan.book_id,
            'user_id': loan.user_id,
            # Add more fields as per your Loan model
        })

    return jsonify({"loans": loan_list}), 200

# Admin route to view all users
@admin_bp.route('/users', methods=['GET'])
@jwt_required()
def view_users():
    if not get_jwt_identity().get('is_admin'):
        return jsonify({"message": "Unauthorized access"}), 403
    
    users = User.query.all()
    user_list = []
    for user in users:
        user_list.append({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            # Add more fields as per your User model
        })

    return jsonify({"users": user_list}), 200
