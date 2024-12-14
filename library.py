from flask import Flask, jsonify, request, send_from_directory
from flasgger import Swagger
import os

app = Flask(__name__)

swagger = Swagger(app, template_file=os.path.join('api-docs', 'swagger.yaml'))




class Book:
    def __init__(self, title, author, published_year, isbn, genre="Unknown"):
        self.title = title
        self.author = author
        self.published_year = published_year
        self.isbn = isbn
        self.genre = genre

books = [
    Book("The Hobbit", "J.R.R. Tolkien", "1937", "9780547928227", "Fantasy"),
    Book("A Game of Thrones", "George R.R. Martin", "1996", "9780553103540", "Fantasy"),
    Book("1984", "George Orwell","1949", "9780451524935", "Dystopian"),
    Book("The Way of Kings", "Brandon Sanderson", "2010", "9780765326355", "Fantasy")
]

@app.route("/books", methods=["GET"])
def get_books():
    if not books:
        return jsonify({"message": "No books found"}), 404
    
    book_list = [
        {
            "title": book.title,
            "author": book.author,
            "published_year": book.published_year,
            "isbn": book.isbn,
            "genre": book.genre
        } for book in books
    ]
    return jsonify(book_list), 200

@app.route("/books/search", methods=["GET"])
def search_books():

    author_filter = request.args.get('author', '').strip().lower()
    year_filter = request.args.get('year')
    genre_filter = request.args.get('genre', '').strip().lower()

    filtered_books = books.copy()

    if author_filter:
        filtered_books = [
            book for book in filtered_books 
            if author_filter in book.author.lower()
        ]

    if year_filter:
        try:
          
            filtered_books = [
                book for book in filtered_books 
                if book.published_year == year_filter
            ]
        except ValueError:
            return jsonify({"message": "Invalid year format"}), 400

    if genre_filter:
        filtered_books = [
            book for book in filtered_books 
            if genre_filter in book.genre.lower()
        ]

    if not filtered_books:
        return jsonify({"message": "No books found matching the search criteria"}), 404

    book_list = [
        {
            "title": book.title,
            "author": book.author,
            "published_year": book.published_year,
            "isbn": book.isbn,
            "genre": book.genre
        } for book in filtered_books
    ]
    
    return jsonify(book_list), 200

@app.route("/books", methods=["POST"])
def add_book():
    book_data = request.json
    
    required_fields = ['title', 'author', 'published_year', 'isbn']
    if not all(field in book_data for field in required_fields):
        return jsonify({"message": "Missing required book information"}), 400
    
    if any(book.isbn == book_data['isbn'] for book in books):
        return jsonify({"message": "Book with this ISBN already exists"}), 409
    
    new_book = Book(
        title=book_data['title'],
        author=book_data['author'],
        published_year=book_data['published_year'].split(),
        isbn=book_data['isbn'],
        genre=book_data.get('genre', "Unknown")
    )
    
    books.append(new_book)
    return jsonify({"message": "Book added successfully"}), 201

@app.route("/books/<string:isbn>", methods=["DELETE"])
def delete_book(isbn):
    for book in books:
        if book.isbn == isbn:
            books.remove(book)
            return jsonify({"message": "Book deleted successfully"}), 200
    
    return jsonify({"message": "Book not found"}), 404

@app.route("/books/<string:isbn>", methods=["PUT"])
def update_book(isbn):

    book_to_update = next((book for book in books if book.isbn == isbn), None)
    
    if not book_to_update:
        return jsonify({"message": "Book not found"}), 404
    
    update_data = request.json
    
    book_to_update.title = update_data.get('title', book_to_update.title)
    book_to_update.author = update_data.get('author', book_to_update.author)
    book_to_update.published_year = update_data.get('published_year', book_to_update.published_year)
    book_to_update.genre = update_data.get('genre', book_to_update.genre)
    
    return jsonify({"message": "Book updated successfully"}), 200

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors for unknown routes."""
    return jsonify({"error": "Resource not found"}), 404

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=3000)