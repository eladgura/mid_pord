import os
from app import create_app, db
from flask_cors import CORS
app = create_app()
CORS(app)
def init_db():
    data_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data')
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    with app.app_context():
        db.create_all()
        print("Database initialized successfully.")


if __name__ == "__main__":
    init_db()
    app.run(debug=True)  # You can set debug=False in production
