from database import db

class Loan(db.Model):
    __tablename__ = 'loans'  # Specify the table name
    loan_id = db.Column(db.Integer, primary_key=True)
    custID = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    bookID = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    loan_date = db.Column(db.Date, nullable=False)
    return_date = db.Column(db.Date, nullable=True)
