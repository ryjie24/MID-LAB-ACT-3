from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import OperationalError
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

# Define the Author and Book models
class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    books = db.relationship('Book', backref='author', lazy=True)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)

# Routes
@app.route('/')
def index():
    try:
        authors = Author.query.all()
        return render_template('index.html', authors=authors)
    except OperationalError as e:
        return f"Database error: {str(e)}", 500

@app.route('/add_author', methods=['POST'])
def add_author():
    try:
        name = request.form.get('name')
        author = Author(name=name)
        db.session.add(author)
        db.session.commit()
        return redirect(url_for('index'))
    except OperationalError as e:
        return f"Database error: {str(e)}", 500

@app.route('/add_book', methods=['POST'])
def add_book():
    try:
        title = request.form.get('title')
        author_id = request.form.get('author_id')
        book = Book(title=title, author_id=author_id)
        db.session.add(book)
        db.session.commit()
        return redirect(url_for('index'))
    except OperationalError as e:
        return f"Database error: {str(e)}", 500

# Initialize the database using a CLI command
@app.cli.command('init-db')
def init_db():
    """Initialize the database."""
    try:
        db.create_all()
        print("Database initialized successfully.")
    except OperationalError as e:
        print(f"Failed to initialize database: {str(e)}")

# Initialize the database when the app starts
with app.app_context():
    try:
        db.create_all()
        print("Database initialized successfully.")
    except OperationalError as e:
        print(f"Failed to initialize database: {str(e)}")

if __name__ == '__main__':
    app.run(debug=True)