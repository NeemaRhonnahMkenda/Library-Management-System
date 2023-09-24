from curses import flash
from flask import Flask, Request, jsonify, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import render_template
from datetime import datetime

from sqlalchemy import desc, func


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
db = SQLAlchemy(app)

# Initialize Flask-Migrate with your Flask app and database
migrate = Migrate(app, db)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    isbn = db.Column(db.String(13), unique=True, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    
    
class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    
class Borrowed(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    isbn_number = db.Column(db.Integer, db.ForeignKey('book.isbn'), nullable=False)
    book_name = db.Column(db.Integer, db.ForeignKey('book.title'), nullable=False)
    author_name = db.Column(db.Integer, db.ForeignKey('book.author'), nullable=False)
    member_name = db.Column(db.Integer, db.ForeignKey('member.name'), nullable=False)
    borrowed_date = db.Column(db.Date, nullable=False)
    
    

# book html adjustments
@app.route('/add_book', methods=['POST'])
def add_book():
    if request.method == 'POST':
        isbn = request.form['isbn']
        title = request.form['title']
        author = request.form['author']

        # Check if a book with the same ISBN already exists
        existing_book = Book.query.filter_by(isbn=isbn).first()

        if existing_book:
            # If the book already exists, update its information
            existing_book.title = title
            existing_book.author = author
            db.session.commit()
            # flash('Book updated successfully', 'success')
        else:
            # If the book doesn't exist, create a new record
            new_book = Book(isbn=isbn, title=title, author=author)
            db.session.add(new_book)
            db.session.commit()
            # flash('Book added successfully', 'success')

        return redirect(url_for('books'))

@app.route('/delete_book', methods=['POST'])
def delete_book():
    if request.method == 'POST':
        book_id = request.form['book_id']

        # Get the book to be deleted from the database
        book_to_delete = Book.query.get(book_id)
        if book_to_delete:
            # Delete the book
            db.session.delete(book_to_delete)
            db.session.commit()
        #     flash('Book deleted successfully', 'success')  # Flash a success message
        # else:
        #     flash('Book not found', 'error')  # Flash an error message

        return redirect(url_for('books'))  # Redirect back to the books page
    
# member html adjustments
@app.route('/add_member', methods=['POST'])
def add_member():
    if request.method == 'POST':
        id = request.form['memberID']
        name = request.form['Membername']  # Changed field name to match HTML form
        email = request.form['email']  # Changed field name to match HTML form

        # Check if a member with the same email already exists
        existing_member = Member.query.filter_by(email=email).first()

        if existing_member:
            # If the member already exists, update their information
            existing_member.name = name
            db.session.commit()
            # flash('Member updated successfully', 'success')
        else:
            # If the member doesn't exist, create a new member record
            new_member = Member(id=id, name=name, email=email)
            db.session.add(new_member)
            db.session.commit()
            # flash('Member added successfully', 'success')
    return redirect(url_for('members'))

@app.route('/delete_member', methods=['POST'])
def delete_member():
    if request.method == 'POST':
        member_id = request.form['member_id']

        # Get the book to be deleted from the database
        member_to_delete = Member.query.get(member_id)
        if member_to_delete:
            # Delete the book
            db.session.delete(member_to_delete)
            db.session.commit()
        #     flash('Book deleted successfully', 'success')  # Flash a success message
        # else:
        #     flash('Book not found', 'error')  # Flash an error message

        return redirect(url_for('members'))  # Redirect back to the books page
    

# Add a route to handle lending books
@app.route('/lend_book', methods=['POST'])
def lend_book():
    if request.method == 'POST':
        isbn = request.form['isbn']
        title = request.form['bookTitle']
        author = request.form['author']
        member = request.form['memberName']
        due_date_str = request.form['dueDate']
        
        # Convert the due_date_str to a Python date object
        due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
        
        # Create a new Borrowed record in the database
        new_borrowed = Borrowed(
            isbn_number=isbn,
            book_name=title,
            author_name=author,
            member_name=member,
            borrowed_date=due_date  
        )
        db.session.add(new_borrowed)
        db.session.commit()

        # Redirect to the checkout page
        return redirect(url_for('checkout'))

# Add a route to handle returning books
@app.route('/return_book', methods=['GET', 'POST'])
def return_book(book_id):
    if request.method == 'POST':
        # Get the borrowed book record by ID and delete it from the database
        borrowed_book = Borrowed.query.get(book_id)
        if borrowed_book:
            db.session.delete(borrowed_book)
            db.session.commit()

    # Redirect to the checkout page
    return redirect(url_for('checkout'))



@app.route('/search')
def search():
    search_query = request.args.get('q')
    # Perform the search in your database (e.g., books)
    search_results = Book.query.filter(Book.title.ilike(f"%{search_query}%")).all()
    return render_template('search_results.html', search_query=search_query, results=search_results)

def highlight_keywords(text, keywords):
    for keyword in keywords:
        text = text.replace(keyword, f'<span class="highlight">{keyword}</span>')
    return text


@app.route('/')
def index():
    return render_template('Dashboard.html')

@app.route('/Books.html')
def books():
    # Fetch all books from the database
    books = Book.query.all()
    book_count = Book.query.count()
    return render_template('Books.html', books=books, book_count=book_count)

@app.route('/Members.html')
def members():
    # Fetch all members from the database
    members = Member.query.all()
    member_count = Member.query.count()
    return render_template('Members.html', members=members, member_count=member_count)

@app.route('/checkout.html')
def checkout():
    books = Book.query.all()
    members = Member.query.all()
    borrowed_books = Borrowed.query.all()
    borrowed_count = len(borrowed_books)  # Calculate the count of borrowed books
    return render_template('checkout.html', books=books, members=members, borrowed_books=borrowed_books, borrowed_count=borrowed_count)


@app.route('/Dashboard.html')
def dashboard():
    # Fetch the top 5 latest books based on their creation date
    latest_books = Book.query.limit(5).all()
    book_count = Book.query.count()
    top_borrowers = db.session.query(Member, func.count(Borrowed.id).label('total_borrowed'))\
        .join(Borrowed, Member.name == Borrowed.member_name)\
        .group_by(Member.id)\
        .order_by(desc('total_borrowed'))\
        .limit(3)\
        .all()
        
    return render_template('Dashboard.html', books=latest_books, book_count=book_count, top_borrowers=top_borrowers)

if __name__ == '__main__':
    app.run()
    
