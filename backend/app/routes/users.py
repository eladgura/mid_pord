# app/routes/users.py

import datetime
import bcrypt
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.user import User
from app.models.loan import Loan
from werkzeug.security import generate_password_hash
import os
from werkzeug.utils import secure_filename

users_bp = Blueprint('users', __name__)

@users_bp.route('/users/search', methods=['GET'])
@jwt_required()
def search_users():
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user['username']).first()

    if not user.is_admin:
        return jsonify({"message": "Admin access required"}), 403

    search_term = request.args.get('term')

    # Perform search based on username or email
    users = User.query.filter(
        (User.username.ilike(f'%{search_term}%')) |
        (User.email.ilike(f'%{search_term}%'))
    ).all()

    return jsonify([user.to_dict() for user in users])
@users_bp.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify(user.to_dict())

@users_bp.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()
    hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
    new_user = User(
        username=data['username'],
        email=data['email'],
        password=hashed_password.decode('utf-8')
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.to_dict()), 201

@users_bp.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    user = User.query.get_or_404(id)
    data = request.get_json()

    user.username = data.get('username', user.username)
    user.email = data.get('email', user.email)
    
    if 'password' in data:
        hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
        user.password = hashed_password.decode('utf-8')
    
    user.is_admin = data.get('is_admin', user.is_admin)

    db.session.commit()
    return jsonify(user.to_dict())

@users_bp.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return '', 204

@users_bp.route('/profile', methods=['GET', 'PUT'])
@jwt_required()
def profile():
    current_user_identity = get_jwt_identity()
    user = User.query.filter_by(username=current_user_identity['username']).first()
    
    if request.method == 'GET':
        loans = Loan.query.filter_by(user_id=user.id).all()
        return jsonify({
            'user': user.to_dict(),
            'loans': [loan.to_dict() for loan in loans]
        })
    
    if request.method == 'PUT':
        data = request.form
        if 'email' in data:
            user.email = data['email']
        if 'password' in data:
            hashed_password = generate_password_hash(data['password'])
            user.password = hashed_password
        
        if 'picture' in request.files:
            picture_file = request.files['picture']
            if picture_file:
                filename = secure_filename(picture_file.filename)
                #
        
        db.session.commit()
        return jsonify({'message': 'Profile updated successfully', 'user': user.to_dict()}), 200

@users_bp.route('/return_book/<int:loan_id>', methods=['PUT'])
@jwt_required()
def return_book(loan_id):
    current_user_identity = get_jwt_identity()
    user = User.query.filter_by(username=current_user_identity['username']).first()
    
    loan = Loan.query.get_or_404(loan_id)
    
    if loan.user_id != user.id:
        return jsonify({'message': 'Unauthorized access to this loan'}), 403

    loan.returned_date = datetime.utcnow()
    loan.check_overdue()
    db.session.commit()
    
    return jsonify({'message': 'Book returned successfully', 'loan': loan.to_dict()}), 200


@users_bp.route('/users/me', methods=['GET'])
@jwt_required()
def get_user_profile():
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user['username']).first()
    if user:
        return jsonify(user.to_dict())
    else:
        return jsonify({"message": "User not found"}), 404

@users_bp.route('/users/me', methods=['PUT'])
@jwt_required()
def update_user_profile():
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user['username']).first()
    if user:
        data = request.get_json()
        user.username = data.get('username', user.username)
        user.email = data.get('email', user.email)
        
        if 'password' in data:
            hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
            user.password = hashed_password.decode('utf-8')
        
        db.session.commit()
        return jsonify(user.to_dict())
    else:
        return jsonify({"message": "User not found"}), 404