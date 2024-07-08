from enum import Enum

class UserRole(Enum):
    ADMIN = "admin"
    USER = "user"

class BookGenre(Enum):
    FICTION = "Fiction"
    NONFICTION = "Non-Fiction"
    SCIFI = "Sci-Fi"
    FANTASY = "Fantasy"
    MYSTERY = "Mystery"
    BIOGRAPHY = "Biography"
    HISTORY = "History"
    POETRY = "Poetry"
