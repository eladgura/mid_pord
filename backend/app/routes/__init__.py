from flask import Blueprint
from . import auth, books, loans, users
auth_bp = Blueprint('auth', __name__)
books_bp = Blueprint('books', __name__)
loans_bp = Blueprint('loans', __name__)
users_bp = Blueprint('users', __name__)