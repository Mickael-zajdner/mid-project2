import datetime
from flask import Blueprint, jsonify, request
from books.models import Book
from customers.models import Customer
from loans.models import Loan  # Import your Loan model
from database import db

loans_bp = Blueprint('loans', __name__)


@loans_bp.route('/loans', methods=["GET"])
def display_all_loans():
    try:
        # Query all loans from the database
        all_loans = Loan.query.all()

        # Prepare a list of dictionaries containing loan information
        loans_data = []
        for loan in all_loans:
            loan_info = {
                'loan_id': loan.loan_id,
                'custID': loan.custID,
                'bookID': loan.bookID,
                'loan_date': loan.loan_date,
                'return_date': loan.return_date
            }
            loans_data.append(loan_info)

        # Return the list of loans as JSON
        return jsonify({'loans': loans_data})
    except Exception as e:
        # Handle any exceptions, e.g., log the error
        return jsonify({'error': f'Error: {str(e)}'}), 500


# @loans_bp.route('/loans', methods=["POST"])
# def add_loan():
#     try:
#         # Get data from the request
#         data = request.get_json()

#         # Check if custID and bookID exist in the database
#         customer = Customer.query.get(data['custID'])
#         book = Book.query.get(data['bookID'])

#         if not customer or not book:
#             return jsonify({'error': 'Customer or book not found'}), 404

#         # Check if the book is available
#         if not book.availability:
#             return jsonify({'error': 'Book not available for loan'}), 400

#         # Create a new Loan instance
#         new_loan = Loan(
#             custID=data['custID'],
#             bookID=data['bookID'],
#             loan_date=data['loan_date'],
#             return_date=data['return_date']
#         )

#         # Add the new loan to the database
#         db.session.add(new_loan)
#         db.session.commit()

        return jsonify({'message': 'Loan added successfully'}), 201
    except Exception as e:
        # Print the exception details for debugging
        print(f"Exception: {str(e)}")
        return jsonify({'error': f'Error: {str(e)}'}), 500



@loans_bp.route('/loans/<int:loan_id>', methods=["DELETE"])
def delete_loan(loan_id):
    try:
        # Get the loan with the provided ID from the database
        loan_to_delete = Loan.query.get(loan_id)

        # Check if the loan exists
        if not loan_to_delete:
            return jsonify({'error': 'Loan not found'}), 404

        # Delete the loan from the database
        db.session.delete(loan_to_delete)
        db.session.commit()

        return jsonify({'message': 'Loan deleted successfully'}), 200
    except Exception as e:
        # Handle any exceptions, e.g., log the error
        return jsonify({'error': f'Error: {str(e)}'}), 500


@loans_bp.route('/loans/<int:loan_id>', methods=["PUT"])
def update_loan(loan_id):
    try:
        # Get the loan with the provided ID from the database
        loan_to_update = Loan.query.get(loan_id)

        # Check if the loan exists
        if not loan_to_update:
            return jsonify({'error': 'Loan not found'}), 404

        # Get data from the request
        data = request.get_json()

        # Update loan attributes if data is provided in the request
        if 'custID' in data:
            loan_to_update.custID = data['custID']
        if 'bookID' in data:
            loan_to_update.bookID = data['bookID']
        if 'loan_date' in data:
            loan_to_update.loan_date = data['loan_date']
        if 'return_date' in data:
            loan_to_update.return_date = data['return_date']

        # Commit the changes to the database
        db.session.commit()

        return jsonify({'message': 'Loan updated successfully'}), 200
    except Exception as e:
        # Handle any exceptions, e.g., log the error
        return jsonify({'error': f'Error: {str(e)}'}), 500
@loans_bp.route('/loans', methods=["POST"])
def loan_book():
    try:
        # Get data from the request
        data = request.get_json()

        # Extract loan information
        cust_id = data.get('custID')
        book_id = data.get('bookID')
        loan_date = datetime.strptime(data.get('loan_date'), '%Y-%m-%d')
        return_date = datetime.strptime(data.get('return_date'), '%Y-%m-%d')

        # Check if the book is available
        book = Book.query.get(book_id)
        if not book or not book.availability:
            return jsonify({'error': 'Book not available for loan'}), 400

        # Check if the customer exists
        customer = Customer.query.get(cust_id)
        if not customer:
            return jsonify({'error': 'Customer not found'}), 404

        # Check if the customer has any overdue loans
        overdue_loans = Loan.query.filter_by(customer_id=cust_id, return_date=None).all()
        if overdue_loans:
            return jsonify({'error': 'Customer has overdue loans'}), 400

        # Create a new Loan instance
        new_loan = Loan(
            customer_id=cust_id,
            book_id=book_id,
            loan_date=loan_date,
            return_date=return_date
        )

        # Update book availability
        book.availability = False

        # Add the new loan to the database
        db.session.add(new_loan)
        db.session.commit()

        return jsonify({'message': 'Book loaned successfully'}), 201

    except Exception as e:
        # Log the error
        print(f"Error loaning book: {str(e)}")
        return jsonify({'error': f'Error loaning book: {str(e)}'}), 500
    

@loans_bp.route('/loans/return', methods=["POST"])
def return_book():
    try:
        # Get data from the request
        data = request.get_json()

        # Check if custID, bookID, and return_date exist in the request
        if 'custID' not in data or 'bookID' not in data or 'return_date' not in data:
            return jsonify({'error': 'Missing required data'}), 400

        # Check if custID and bookID exist in the database
        customer = Customer.query.get(data['custID'])
        book = Book.query.get(data['bookID'])

        if not customer or not book:
            return jsonify({'error': 'Customer or book not found'}), 404

        # Check if the book is currently on loan to the customer
        loan = Loan.query.filter_by(customer_id=data['custID'], book_id=data['bookID'], return_date=None).first()

        if not loan:
            return jsonify({'error': 'Book not currently on loan to the customer'}), 400

        # Update the return_date for the loan
        loan.return_date = datetime.strptime(data['return_date'], '%Y-%m-%d')

        # Update book availability
        book.availability = True

        # Commit the changes to the database
        db.session.commit()

        return jsonify({'message': 'Book returned successfully'}), 200

    except Exception as e:
        # Log the error
        print(f"Error returning book: {str(e)}")
        return jsonify({'error': f'Error returning book: {str(e)}'}), 500
