from database import db

class Book(db.Model):
    __tablename__ = 'books'  # Specify the table name
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    year_published = db.Column(db.Integer, nullable=False)
    book_type = db.Column(db.Integer, nullable=False)
    availability = db.Column(db.Boolean, default=True)

