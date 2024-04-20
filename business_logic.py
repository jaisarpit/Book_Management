import logging
from flask import jsonify, request, g
from flask_jwt_extended import create_access_token
from datetime import timedelta
from models import Books, Users, db

def register_user():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if Users.query.filter_by(username=username).first():
        g.logger.warning('Username already exists: %s', username)
        return jsonify({'message': 'Username already exists'}), 400

    new_user = Users(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()

    user_id = new_user.id

    user_info = {
        'user_id': user_id,
        'username': username
    }
    return jsonify({'message': 'User registered successfully', 'user_info': user_info}), 201         # added the user_info with response

def login_user():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    user = Users.query.filter_by(username=username, password=password).first()

    if user:
        access_token = create_access_token(identity=username, expires_delta=timedelta(days=1))

        return jsonify(access_token=access_token, user_id=user.id), 200                              # added the user_id with response
    else:
        return jsonify({'message': 'Invalid username or password'}), 401

def create_book():
    data = request.json

    new_book = Books(
        name=data['name'],
        description=data['description'],
        num_pages=data['num_pages'],
        author_name=data['author_name'],
        publisher_name=data['publisher_name']
    )
    
    author_name = data['author_name']
    publisher_name = data['publisher_name']

    if Books.query.filter_by(name=data['name'], author_name=author_name, publisher_name=publisher_name).first():
        g.logger.warning('Book already exists: %s', data['name'])
        return jsonify({'message': 'Book already exists'}), 400
    
    db.session.add(new_book)
    db.session.commit()

    # Retrieve the ID of the newly created book
    book_id = new_book.id

    # Return the ID along with the success message and book information
    book_info = {
        'id': book_id,
        'name': new_book.name,
        'description': new_book.description,
        'num_pages': new_book.num_pages,
        'author_name': new_book.author_name,
        'publisher_name': new_book.publisher_name
    }
    g.logger.info('Book created successfully: %s', book_info)
    return jsonify({'message': ' Book created successfully', 'book_info': book_info}), 201

def get_books():
    query_params = request.args
    author_name = query_params.get('author_name')
    publisher_name = query_params.get('publisher_name')

    if author_name and publisher_name:
        books = Books.query.filter_by(author_name=author_name, publisher_name=publisher_name).all()
    elif publisher_name:
        books = Books.query.filter_by(publisher_name=publisher_name).all()
    elif author_name:
        books = Books.query.filter_by(author_name=author_name).all()
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
    
    g.logger.info(' Book details fetched successfully: %s', books_data)

    return jsonify(books_data), 200

def delete_book(book_id):
    book = Books.query.get(book_id)
    if book:
        db.session.delete(book)
        db.session.commit()

        g.logger.info('Book deleted successfully: %s', book.name)

        return jsonify({'message': 'Book deleted successfully'}), 200
    else:
        return jsonify({'message': 'Book not found'}), 404