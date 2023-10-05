from flask import Flask, render_template, jsonify
from books.routes import books_bp
from customers.routes import customers_bp
from loans.routes import loans_bp
from books.models import *
from customers.models import *
from loans.models import *
from database import db
from sqlalchemy import inspect

from flask_cors import CORS  # Import CORS

app = Flask(__name__)

CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

app.register_blueprint(books_bp)
app.register_blueprint(customers_bp)
app.register_blueprint(loans_bp)

if __name__ == "__main__":
    with app.app_context():
        inspector = inspect(db.engine)
        existing_tables = inspector.get_table_names()
        print("Existing Tables:", existing_tables)

        if not existing_tables:
            print("No tables found. Attempting to create tables...")
            try:
                db.create_all()
                print("Tables created successfully.")
            except Exception as e:
                print(f"Error creating tables: {str(e)}")
        else:
            print("Tables already exist. No action taken.")

    app.run(debug=True)
