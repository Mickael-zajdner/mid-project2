from flask import Blueprint, jsonify, request
from books.models import Book
from database import db

books_bp = Blueprint('books', __name__)


@books_bp.route('/books', methods=["GET"])
def display_all_books():
    try:
        # Query all books from the database
        all_books = Book.query.all()

        # Prepare a list of dictionaries containing book information
        books_data = []
        for book in all_books:
            book_info = {
                'id': book.id,
                'name': book.name,
                'author': book.author,
                'year_published': book.year_published,
                'book_type': book.book_type,
                'availability': book.availability
            }
            books_data.append(book_info)

        # Return the list of books as JSON
        return jsonify({'books': books_data})
    except Exception as e:
        # Handle any exceptions, e.g., log the error
        return jsonify({'error': f'Error: {str(e)}'}), 500


@books_bp.route('/books', methods=["POST"])
def add_book():
    try:
        # Get data from the request
        data = request.get_json()

        # Create a new Book instance
        new_book = Book(
            name=data['name'],
            author=data['author'],
            year_published=data['year_published'],
            book_type=data['book_type'],
            availability=data['availability']
        )

        # Add the new book to the database
        db.session.add(new_book)
        db.session.commit()

        return jsonify({'message': 'Book added successfully'}), 201
    except Exception as e:
        # Handle any exceptions, e.g., log the error
        return jsonify({'error': f'Error: {str(e)}'}), 500


@books_bp.route('/books/<int:book_id>', methods=["DELETE"])
def delete_book(book_id):
    try:
        # Get the book with the provided ID from the database
        book_to_delete = Book.query.get(book_id)

        # Check if the book exists
        if not book_to_delete:
            return jsonify({'error': 'Book not found'}), 404

        # Delete the book from the database
        db.session.delete(book_to_delete)
        db.session.commit()

        return jsonify({'message': 'Book deleted successfully'}), 200
    except Exception as e:
        # Handle any exceptions, e.g., log the error
        return jsonify({'error': f'Error: {str(e)}'}), 500

@books_bp.route('/books/<int:book_id>', methods=["PUT"])
def update_book(book_id):
    try:
        # Get the book with the provided ID from the database
        book_to_update = Book.query.get(book_id)

        # Check if the book exists
        if not book_to_update:
            return jsonify({'error': 'Book not found'}), 404

        # Get data from the request
        data = request.get_json()

        # Update book attributes if data is provided in the request
        if 'name' in data:
            book_to_update.name = data['name']
        if 'author' in data:
            book_to_update.author = data['author']
        if 'year_published' in data:
            book_to_update.year_published = data['year_published']
        if 'book_type' in data:
            book_to_update.type = data['book_type']
        if 'availability' in data:
            book_to_update.availability = data['availability']

        # Commit the changes to the database
        db.session.commit()

        return jsonify({'message': 'Book updated successfully'}), 200
    except Exception as e:
        # Handle any exceptions, e.g., log the error
        return jsonify({'error': f'Error: {str(e)}'}), 500

@books_bp.route('/books/<int:book_id>', methods=["GET"])
def display_book(book_id):
    try:
        # Query the book with the provided ID from the database
        book = Book.query.get(book_id)

        # Check if the book exists
        if not book:
            return jsonify({'error': 'Book not found'}), 404

        # Prepare a dictionary containing book information
        book_info = {
            'id': book.id,
            'name': book.name,
            'author': book.author,
            'year_published': book.year_published,
            'book_type': book.book_type,
            'availability': book.availability
        }

        # Return the book information as JSON
        return jsonify({'book': book_info})
    except Exception as e:
        # Handle any exceptions, e.g., log the error
        return jsonify({'error': f'Error: {str(e)}'}), 500
    
@books_bp.route('/books', methods=["GET"])
def get_books_filtered():
    search_query = request.args.get('name')
    
    # If there's a search query, filter the books
    if search_query:
        books = Book.query.filter(Book.name.ilike(f"%{search_query}%")).all()
    else:
        books = Book.query.all()

    # Convert the books to a list of dictionaries
    books_list = [{"id": book.id, "name": book.name, "author": book.author, "year_published": book.year_published, "book_type": book.book_type, "availability": book.availability} for book in books]

    return jsonify({"books": books_list})

@books_bp.route('/books/search', methods=["GET"])
def search_books_by_name():
    try:
        search_query = request.args.get('name')

        # If there's a search query, filter the books
        if search_query:
            books = Book.query.filter(Book.name.ilike(f"%{search_query}%")).all()
        else:
            books = Book.query.all()

        # Convert the books to a list of dictionaries
        books_list = [{"id": book.id, "name": book.name, "author": book.author, "year_published": book.year_published, "book_type": book.book_type, "availability": book.availability} for book in books]

        return jsonify({"books": books_list})
    except Exception as e:
        # Handle any exceptions, e.g., log the error
        return jsonify({'error': f'Error: {str(e)}'}), 500
