from flask import Flask, request, render_template, abort, jsonify
import shortuuid
import os
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from pygments import highlight
from pygments.lexers import get_lexer_by_name, get_all_lexers
from pygments.formatters import HtmlFormatter
import jwt
import datetime

app = Flask(__name__)

# small change
# Get the API key from the environment variable
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('API_KEY')

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
SECRET_KEY = app.config['SECRET_KEY']

# Directory to store paste files
PASTE_DIR = 'pastes'
if not os.path.exists(PASTE_DIR):
    os.makedirs(PASTE_DIR)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    pastes = db.relationship('Paste', backref='owner', lazy=True)

# Paste model
class Paste(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    public = db.Column(db.Boolean, default=True)  # True for public, False for private
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# Function to generate a JWT token for a user
def generate_token(user_id):
    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1),  # Token expiration time
        'iat': datetime.datetime.utcnow(),  # Token issued time
        'sub': user_id  # The subject of the token (e.g., user ID)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

# Function to verify the provided JWT token
def verify_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload['sub']  # Return user ID or any other relevant information
    except jwt.ExpiredSignatureError:
        abort(401, description="Token has expired")
    except jwt.InvalidTokenError:
        abort(401, description="Invalid token")

# Route to create a new paste
@app.route('/create_paste', methods=['POST'])
def create_paste():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        abort(401, description="Authorization header is missing")

    try:
        token = auth_header.split(" ")[1]
        user_id = verify_token(token)
    except IndexError:
        abort(401, description="Bearer token malformed")

    data = request.json
    content = data.get('content')
    is_public = data.get('public', True)  # Default is public if not provided

    if not content:
        return jsonify({'error': 'Content is required'}), 400

    user = User.query.get(user_id)
    if not user:
        return abort(404, description="User not found")

    # Create a new paste
    new_paste = Paste(content=content, public=is_public, owner=user)
    db.session.add(new_paste)
    db.session.commit()

    return jsonify({'message': 'Paste created successfully', 'paste_id': new_paste.id}), 201

# Route to register a new user
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    user = User.query.filter_by(username=username).first()
    if user:
        return jsonify({'error': 'User already exists'}), 400

    password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(username=username, password_hash=password_hash)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201

# Route to list user's own pastes (public and private) and all other users' public pastes
@app.route('/my_pastes', methods=['GET'])
def my_pastes():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        abort(401, description="Authorization header is missing")

    try:
        token = auth_header.split(" ")[1]
        user_id = verify_token(token)
    except IndexError:
        abort(401, description="Bearer token malformed")

    # Get the logged-in user's pastes (both public and private)
    user_pastes = Paste.query.filter_by(user_id=user_id).all()

    # Get all public pastes from other users
    public_pastes = Paste.query.filter(Paste.public == True, Paste.user_id != user_id).all()

    # Serialize the pastes
    user_pastes_data = [{'id': paste.id, 'content': paste.content, 'public': paste.public} for paste in user_pastes]
    public_pastes_data = [{'id': paste.id, 'content': paste.content, 'owner': paste.owner.username} for paste in public_pastes]

    return jsonify({
        'user_pastes': user_pastes_data,
        'public_pastes': public_pastes_data
    })

# Route to edit a paste
@app.route('/edit_paste/<int:paste_id>', methods=['PUT'])
def edit_paste(paste_id):
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        abort(401, description="Authorization header is missing")

    try:
        token = auth_header.split(" ")[1]
        user_id = verify_token(token)
    except IndexError:
        abort(401, description="Bearer token malformed")

    # Fetch the paste by its ID
    paste = Paste.query.get(paste_id)
    if not paste:
        return abort(404, description="Paste not found")

    # Check if the logged-in user is the owner of the paste
    if paste.user_id != user_id:
        return abort(403, description="You are not authorized to edit this paste")

    # Get new data from the request body
    data = request.json
    new_content = data.get('content')
    is_public = data.get('public', True)  # Default to public if not specified

    if not new_content:
        return jsonify({'error': 'Content is required'}), 400

    # Update the paste content and public/private status
    paste.content = new_content
    paste.public = is_public

    # Commit the changes to the database
    db.session.commit()

    return jsonify({'message': 'Paste updated successfully', 'paste_id': paste.id}), 200

# Route to login a user and get a token
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    if not user or not bcrypt.check_password_hash(user.password_hash, password):
        return abort(401, description="Invalid username or password")

    token = generate_token(user_id=user.id)
    return jsonify({'token': token})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    app.run(debug=True)