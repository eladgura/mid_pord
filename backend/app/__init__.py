import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from app.config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    JWTManager(app)  # Initialize JWTManager here
    
    with app.app_context():
        from app.routes import auth, books, loans, users, admin
        
        app.register_blueprint(auth.auth_bp, url_prefix='/api')
        app.register_blueprint(books.books_bp, url_prefix='/api')
        app.register_blueprint(loans.loans_bp, url_prefix='/api')
        app.register_blueprint(users.users_bp, url_prefix='/api')
        app.register_blueprint(admin.admin_bp, url_prefix='/api')
        
        # Ensure data directory exists
        data_folder = os.path.join(os.path.dirname(__file__), r'C:\Users\elad\Documents\mid_term_project\mid_pord\backend\data')
        os.makedirs(data_folder, exist_ok=True)
        
        return app
