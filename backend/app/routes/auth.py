from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app import db
from app.models.user import User
from app.models.loan import Loan

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')

    if User.query.filter_by(email=email).first() or User.query.filter_by(username=username).first():
        return jsonify({"message": "User already exists"}), 409

    hashed_password = generate_password_hash(password)
    new_user = User(username=username, password=hashed_password, email=email)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()

    if user and check_password_hash(user.password, password):
        access_token = create_access_token(identity={'username': user.username, 'is_admin': user.is_admin})
        
        # Update overdue status for all loans of the user
        loans = Loan.query.filter_by(user_id=user.id).all()
        overdue_loans = []
        for loan in loans:
            if loan.check_overdue():
                overdue_loans.append(loan)

        db.session.commit()

        overdue_message = ""
        if overdue_loans:
            overdue_message = "You have overdue books that need to be returned."
        
        return jsonify(access_token=access_token, message=overdue_message), 200

    return jsonify({"message": "Invalid credentials"}), 401
