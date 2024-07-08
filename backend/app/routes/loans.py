from datetime import datetime  # Import datetime module correctly
from flask import Blueprint, request, jsonify
from app import db
from app.models.loan import Loan

loans_bp = Blueprint('loans', __name__)

@loans_bp.route('/loans', methods=['GET'])
def get_loans():
    loans = Loan.query.all()
    return jsonify([loan.to_dict() for loan in loans])

@loans_bp.route('/loans/<int:id>', methods=['GET'])
def get_loan(id):
    loan = Loan.query.get_or_404(id)
    return jsonify(loan.to_dict())

@loans_bp.route('/loans', methods=['POST'])
def add_loan():
    data = request.get_json()

    # Parse due_date from ISO format string to datetime object
    due_date = datetime.strptime(data['due_date'], '%Y-%m-%dT%H:%M:%SZ')

    new_loan = Loan(
        user_id=data['user_id'],
        book_id=data['book_id'],
        due_date=due_date
    )

    db.session.add(new_loan)
    db.session.commit()

    return jsonify(new_loan.to_dict()), 201

@loans_bp.route('/loans/<int:id>', methods=['PUT'])
def update_loan(id):
    loan = Loan.query.get_or_404(id)
    data = request.get_json()

    # Update loan attributes
    loan.due_date = datetime.strptime(data.get('due_date'), '%Y-%m-%dT%H:%M:%SZ') if data.get('due_date') else loan.due_date
    loan.returned_date = datetime.strptime(data.get('returned_date'), '%Y-%m-%dT%H:%M:%SZ') if data.get('returned_date') else loan.returned_date
    loan.overdue = data.get('overdue', loan.overdue)

    db.session.commit()
    return jsonify(loan.to_dict())

@loans_bp.route('/loans/<int:id>', methods=['DELETE'])
def delete_loan(id):
    loan = Loan.query.get_or_404(id)
    db.session.delete(loan)
    db.session.commit()
    return '', 204
