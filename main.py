from flask import Flask, request, g
from flask_jwt_extended import JWTManager, jwt_required
from business_logic import register_user, login_user, create_book, get_books, delete_book
from models import db
from config import Config
import logging
from flask_request_id_header.middleware import RequestID
import uuid
from logger import setup_logger

app = Flask(__name__)
app.config.from_object(Config)
app.wsgi_app = RequestID(app)
db.init_app(app)
jwt = JWTManager(app)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@app.before_request
def before_request():
    g.request_id = str(uuid.uuid4())
    g.logger = setup_logger(request_id=g.request_id)
    g.logger.info(f"Starting request {g.request_id}: {request.method} {request.path}")

@app.after_request
def after_request(response):
    g.logger.info(f"Ending request {g.request_id}: {request.method} {request.path} - Status {response.status_code}")
    return response

@app.route('/register', methods=['POST'])
def register():
    return register_user()

@app.route('/login', methods=['POST'])
def login():
    return login_user()

@app.route('/create-book', methods=['POST'])
@jwt_required()
def create_book_route():
    return create_book()

@app.route('/get-book', methods=['GET'])
@jwt_required()
def get_books_route():
    return get_books()

@app.route('/delete-book/<int:book_id>', methods=['DELETE'])
@jwt_required()
def delete_book_route(book_id):
    return delete_book(book_id)

if __name__ == '__main__':
    app.run(debug=True)