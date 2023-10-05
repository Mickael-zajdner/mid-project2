from flask import Blueprint, jsonify, request
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


@loans_bp.route('/loans', methods=["POST"])
def add_loan():
    try:
        # Get data from the request
        data = request.get_json()

        # Create a new Loan instance
        new_loan = Loan(
            custID=data['custID'],
            bookID=data['bookID'],
            loan_date=data['loan_date'],
            return_date=data['return_date']
        )

        # Add the new loan to the database
        db.session.add(new_loan)
        db.session.commit()

        return jsonify({'message': 'Loan added successfully'}), 201
    except Exception as e:
        # Handle any exceptions, e.g., log the error
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
