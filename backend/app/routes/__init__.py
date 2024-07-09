from flask import Blueprint
auth_bp = Blueprint('auth', __name__)
books_bp = Blueprint('books', __name__)
loans_bp = Blueprint('loans', __name__)
users_bp = Blueprint('users', __name__)
from app.routes.admin import admin_bp
