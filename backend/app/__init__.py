import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config import Config
from flask_jwt_extended import JWTManager

# Initialize SQLAlchemy
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    jwt = JWTManager(app)  # Initialize JWTManager here
    
    with app.app_context():
        ##from app.models import User, Book, Loan  # Import models
        from app.routes import auth, books, loans, users, admin  # Import routes
        
        app.register_blueprint(auth.auth_bp, url_prefix='/api')
        app.register_blueprint(books.books_bp, url_prefix='/api')
        app.register_blueprint(loans.loans_bp, url_prefix='/api')
        app.register_blueprint(users.users_bp, url_prefix='/api')
        app.register_blueprint(admin.admin_bp, url_prefix='/api' ) 
        # Create the data folder if it doesn't exist
        data_folder = os.path.join(os.path.dirname(__file__), '../data')
        os.makedirs(data_folder, exist_ok=True)
        
        return app
