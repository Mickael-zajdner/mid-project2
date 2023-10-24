# mid-project
# Library Management System

This is a simple library management system built using Flask for the backend and JavaScript for the frontend.

## Project Background

Libraries play a crucial role in fostering education, knowledge sharing, and community development. The Library Management System is designed to streamline and automate various aspects of a basic library setup, making it easier for librarians to manage their inventory and for patrons to borrow and return books.

## running the project 
use live server for run and test the project

## installetion 
i dont know whay but thers a lot to instell plz istall all useing the pip install Requirements.txt command.
I've checked it several times and I still don't understand why there are so many I uninstalled and reinstalled to bring back the virtual environment and I still have a lot of downloads left I doubt it's supposed to be like this but just to be clear I left all the downloads as they are.

## Functionality Options

## Display All Books:
Endpoint: /books
Method: GET
Description: Retrieve a list of all books in the library.
## Add a Book:
Endpoint: /books
Method: POST
Description: Add a new book to the library. Requires book title, author, and quantity.
## Update a Book:
Endpoint: /books/<book_id>
Method: PUT
Description: Update information for a specific book using its ID.
## Delete a Book:
Endpoint: /books/<book_id>
Method: DELETE
Description: Remove a book from the library using its ID.
## Display All Customers:
Endpoint: /customers
Method: GET
Description: Retrieve a list of all customers in the library.
## Add a Customer:
Endpoint: /customers
Method: POST
Description: Add a new customer to the library. Requires customer name and contact information.
## Update a Customer:
Endpoint: /customers/<cust_id>
Method: PUT
Description: Update information for a specific customer using their ID.
## Delete a Customer:
Endpoint: /customers/<cust_id>
Method: DELETE
Description: Remove a customer from the library using their ID.
## Display All Loans:
Endpoint: /loans
Method: GET
Description: Retrieve a list of all book loans in the library.
## Loan a Book:
Endpoint: /loans
Method: POST
Description: Loan a book to a customer. Requires customer ID, book ID, loan date, and return date.
## Return a Book:
Endpoint: /loans/return
Method: POST
Description: Return a borrowed book. Requires customer ID, book ID, and return date.
## Display Overdue Loans:
Endpoint: /loans/overdue
Method: GET
Description: Retrieve a list of all overdue book loans in the library.


