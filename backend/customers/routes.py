from flask import Blueprint, jsonify, request
from customers.models import Customer  # Import your Customer model
from database import db

customers_bp = Blueprint('customers', __name__)

@customers_bp.route('/customers', methods=["GET"])
def display_all_customers():
    try:
        # Query all customers from the database
        all_customers = Customer.query.all()

        # Prepare a list of dictionaries containing customer information
        customers_data = []
        for customer in all_customers:
            customer_info = {
                'id': customer.id,
                'name': customer.name,
                'city': customer.city,
                'age': customer.age
            }
            customers_data.append(customer_info)

        # Return the list of customers as JSON
        return jsonify({'customers': customers_data})
    except Exception as e:
        # Handle any exceptions, e.g., log the error
        return jsonify({'error': f'Error: {str(e)}'}), 500

@customers_bp.route('/customers', methods=["POST"])
def add_customer():
    try:
        # Get data from the request
        data = request.get_json()

        # Create a new Customer instance
        new_customer = Customer(
            name=data['name'],
            city=data['city'],
            age=data['age']
        )

        # Add the new customer to the database
        db.session.add(new_customer)
        db.session.commit()

        return jsonify({'message': 'Customer added successfully'}), 201
    except Exception as e:
        # Handle any exceptions, e.g., log the error
        return jsonify({'error': f'Error: {str(e)}'}), 500
    

@customers_bp.route('/customers/<int:customer_id>', methods=["DELETE"])
def delete_customer(customer_id):
    try:
        # Get the customer with the provided ID from the database
        customer_to_delete = Customer.query.get(customer_id)

        # Check if the customer exists
        if not customer_to_delete:
            return jsonify({'error': 'Customer not found'}), 404

        # Delete the customer from the database
        db.session.delete(customer_to_delete)
        db.session.commit()

        return jsonify({'message': 'Customer deleted successfully'}), 200
    except Exception as e:
        # Handle any exceptions, e.g., log the error
        return jsonify({'error': f'Error: {str(e)}'}), 500
    
@customers_bp.route('/customers/<int:customer_id>', methods=["PUT"])
def update_customer(customer_id):
    try:
        # Get the customer with the provided ID from the database
        customer_to_update = Customer.query.get(customer_id)

        # Check if the customer exists
        if not customer_to_update:
            return jsonify({'error': 'Customer not found'}), 404

        # Get data from the request
        data = request.get_json()

        # Update customer attributes if data is provided in the request
        if 'name' in data:
            customer_to_update.name = data['name']
        if 'city' in data:
            customer_to_update.city = data['city']
        if 'age' in data:
            customer_to_update.age = data['age']

        # Commit the changes to the database
        db.session.commit()

        return jsonify({'message': 'Customer updated successfully'}), 200
    except Exception as e:
        # Handle any exceptions, e.g., log the error
        return jsonify({'error': f'Error: {str(e)}'}), 500

@customers_bp.route('/customers/<int:customer_id>', methods=["GET"])
def display_customer(customer_id):
    try:
        # Query the customer with the provided ID from the database
        customer = Customer.query.get(customer_id)

        # Check if the customer exists
        if not customer:
            return jsonify({'error': 'Customer not found'}), 404

        # Prepare a dictionary containing customer information
        customer_info = {
            'id': customer.id,
            'name': customer.name,
            'city': customer.city,
            'age': customer.age
        }

        # Return the customer information as JSON
        return jsonify({'customer': customer_info})
    except Exception as e:
        # Handle any exceptions, e.g., log the error
        return jsonify({'error': f'Error: {str(e)}'}), 500
@customers_bp.route('/customers/search', methods=["GET"])
def search_customers_by_name():
    try:
        search_query = request.args.get('name')

        # If there's a search query, filter the customers
        if search_query:
            customers = Customer.query.filter(Customer.name.ilike(f"%{search_query}%")).all()
        else:
            customers = Customer.query.all()

        # Convert the customers to a list of dictionaries
        customers_list = [{"id": customer.id, "name": customer.name, "city": customer.city, "age": customer.age} for customer in customers]

        return jsonify({"customers": customers_list})
    except Exception as e:
        # Handle any exceptions, e.g., log the error
        return jsonify({'error': f'Error: {str(e)}'}), 500