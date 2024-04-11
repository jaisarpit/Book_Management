# Built in imports
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from datetime import timedelta

# Rule based imports
from models import db, Books, Users
from config import Config


app = Flask(__name__)                              # initialize the app

app.config.from_object(Config)                     # set the config

db.init_app(app)                                   # initialize the database object

jwt = JWTManager(app)                              # initialize the JWT manager


@app.route('/register', methods=['POST'])
def register():
    """
        API to register the user
        Parameters:
            username: string
            password: string
    """
    data = request.json
    username = data.get('username')                 # fetching the username from the payload
    password = data.get('password')                 # fetching the password from the payload

    # Check if the username already exists
    if Users.query.filter_by(username=username).first():
        return jsonify({'message': 'Username already exists'}), 400

    # Create a new user
    new_user = Users(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201


@app.route('/login', methods=['POST'])
def login():
    """
        API to login the user
        Parameters:
            username: string
            password: string
    """
    data = request.json
    username = data.get('username')                         # fetching the username from the payload
    password = data.get('password')                         # fetching the password from the payload

    # fetch the user
    user = Users.query.filter_by(username=username, password=password).first()

    # check if the user already exist
    if user:
        access_token = create_access_token(identity=username, expires_delta=timedelta(days=1))
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({'message': 'Invalid username or password'}), 401


@app.route('/create-book', methods=['POST'])
@jwt_required()
def create_book():
    """
        API for creating the book
        Parameters:
            name: string
            description: string
            num_pages: string
            author_name: string
            publisher_name: string
    """
    data = request.json
    new_book = Books(
        name=data['name'],
        description=data['description'],
        num_pages=data['num_pages'],
        author_name=data['author_name'],
        publisher_name=data['publisher_name']
    )
    db.session.add(new_book)
    db.session.commit()
    return jsonify({'message': 'Book created successfully'}), 201


@app.route('/get-book', methods=['GET'])
@jwt_required()
def get_books():
    """
        API for fetching the book details
        Query Parameters:
            author_name: string
            publisher_name: string
    """
    query_params = request.args
    author_name = query_params.get('author_name')
    publisher_name = query_params.get('publisher_name')

    # If both author_name and publisher_name provided
    if author_name and publisher_name:
        books = Books.query.filter_by(author_name=author_name, publisher_name=publisher_name).all()

    # If only publisher_name provided
    elif publisher_name:
        books = Books.query.filter_by(publisher_name=publisher_name).all()

    # If only author_name provided
    elif author_name:
        books = Books.query.filter_by(author_name=author_name).all()

    # If none of the above provided
    else:
        books = Books.query.all()

    books_data = []
    for book in books:
        book_data = {
            'id': book.id,
            'name': book.name,
            'description': book.description,
            'num_pages': book.num_pages,
            'author_name': book.author_name,
            'publisher_name': book.publisher_name
        }
        books_data.append(book_data)

    return jsonify(books_data), 200


@app.route('/delete-book/<int:book_id>', methods=['DELETE'])
@jwt_required()
def delete_book(book_id):
    """
        API to delete the book
        Query Parameters:
            id: integer
    """
    book = Books.query.get(book_id)                       #  fetch the book from the database
    if book:
        db.session.delete(book)
        db.session.commit()
        return jsonify({'message': 'Book deleted successfully'}), 200
    else:
        return jsonify({'message': 'Book not found'}), 404


if __name__ == '__main__':
    app.run(debug=True)
