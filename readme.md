# Mid-Term Project

## Overview

This project is a library management system consisting of a backend and a frontend. The backend is built with Flask and uses SQLAlchemy for database management. The frontend consists of HTML and CSS files for user interaction.

## Project Structure

mid_term_project/
├── backend/
│ ├── app/
│ │ ├── init.py
│ │ ├── config.py
│ │ ├── models/
│ │ │ ├── init.py
│ │ │ ├── book.py
│ │ │ ├── loan.py
│ │ │ ├── user.py
│ │ ├── routes/
│ │ │ ├── init.py
│ │ │ ├── auth.py
│ │ │ ├── books.py
│ │ │ ├── loans.py
│ │ │ ├── users.py
│ │ ├── utils/
│ │ │ ├── init.py
│ │ │ ├── enums.py
│ ├── data/
│ │ ├── library.db
│ ├── myenv/
│ ├── README.md
│ ├── requirements.txt
│ ├── run.py
├── frontend/
│ ├── home.html
│ ├── login.html
│ ├── profile.html
│ ├── register.html
│ ├── style.css

markdown
Copy code

## Setup

### Prerequisites

- Python 3.x
- Flask
- SQLAlchemy
- Flask-Migrate
- Flask-JWT-Extended
- Bcrypt

### Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/yourusername/mid_term_project.git
    cd mid_term_project/backend
    ```

2. Set up a virtual environment:

    ```sh
    python -m venv myenv
    source myenv/bin/activate  # On Windows, use `myenv\Scripts\activate`
    ```

3. Install the dependencies:

    ```sh
    pip install -r requirements.txt
    ```

4. Initialize the database:

    ```sh
    python run.py
    ```

### Running the Application

To start the Flask application, run:

```sh
python run.py
The backend will be available at http://127.0.0.1:5000.

API Endpoints
Authentication
POST /api/register: Register a new user.
POST /api/login: Log in an existing user.
Books
GET /api/books: Get all books.
GET /api/books/<int:id>: Get a specific book by ID.
POST /api/books: Add a new book (requires authentication).
PUT /api/books/<int:id>: Update an existing book by ID (requires authentication).
DELETE /api/books/<int:id>: Delete a book by ID (requires admin access and authentication).
Loans
POST /api/loans: Create a new loan (requires authentication).
PUT /api/loans/<int:id>: Update a loan (requires authentication).
Users
GET /api/users: Get all users.
GET /api/users/<int:id>: Get a specific user by ID.
POST /api/users: Add a new user.
PUT /api/users/<int:id>: Update a user by ID.
DELETE /api/users/<int:id>: Delete a user by ID.
Frontend
The frontend HTML files are located in the frontend/ directory. You can open these files directly in a web browser to view the user interface.

License
This project is licensed under the MIT License. See the LICENSE file for details.