from app import db
from datetime import datetime

class Loan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    borrowed_date = db.Column(db.DateTime, default=datetime.utcnow)
    due_date = db.Column(db.DateTime)
    returned_date = db.Column(db.DateTime)
    overdue = db.Column(db.Boolean, default=False)

    def check_overdue(self):
        """Check if the loan is overdue."""
        if self.returned_date is None and datetime.utcnow() > self.due_date:
            self.overdue = True
        else:
            self.overdue = False
        return self.overdue

    @staticmethod
    def update_all_overdue_status():
        """Update the overdue status for all loans."""
        loans = Loan.query.all()
        for loan in loans:
            loan.check_overdue()
        db.session.commit()

    def to_dict(self):
        """Return a dictionary representation of the loan."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'book_id': self.book_id,
            'borrowed_date': self.borrowed_date.isoformat(),
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'returned_date': self.returned_date.isoformat() if self.returned_date else None,
            'overdue': self.overdue
        }
    def __repr__(self):
        return f'<Loan {self.id}>'
