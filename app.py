from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Create empty data structures to store books and customers
books = []
customers = []

class Book:
    def __init__(self, title, author, copies):
        self.title = title
        self.author = author
        self.copies = copies

class Customer:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.borrowed_books = []

# Home page
@app.route('/')
def index():
    return render_template('index.html', books=books, customers=customers)

# Add a new book
@app.route('/add_book', methods=['POST'])
def add_book():
    title = request.form['title']
    author = request.form['author']
    copies = int(request.form['copies'])
    new_book = Book(title, author, copies)
    books.append(new_book)
    return redirect(url_for('index'))

# Add a new customer
@app.route('/add_customer', methods=['POST'])
def add_customer():
    id = request.form['id']
    name = request.form['name']
    new_customer = Customer(id, name)
    customers.append(new_customer)
    return redirect(url_for('index'))

# Borrow a book
@app.route('/borrow_book', methods=['POST'])
def borrow_book():
    customer_id = request.form['customer_id']
    book_title = request.form['book_title']
    for customer in customers:
        if customer.id == customer_id:
            for book in books:
                if book.title == book_title and book.copies > 0:
                    customer.borrowed_books.append(book)
                    book.copies -= 1
                    return redirect(url_for('index'))
    return "Book not found or customer not registered."

# Return a book
@app.route('/return_book', methods=['POST'])
def return_book():
    customer_id = request.form['customer_id']
    book_title = request.form['book_title']
    for customer in customers:
        if customer.id == customer_id:
            for book in customer.borrowed_books:
                if book.title == book_title:
                    customer.borrowed_books.remove(book)
                    book.copies += 1
                    return redirect(url_for('index'))
    return "Book not found or customer not registered."

if __name__ == '__main__':
    app.run(debug=True)
