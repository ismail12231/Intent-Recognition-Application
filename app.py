from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from functools import wraps
import joblib
import os

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "http://localhost:4200"}})

# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'  # Key for JWT encoding and decoding
db = SQLAlchemy(app)

# Define User table
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Define Requests table
class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    request_text = db.Column(db.Text, nullable=False)
    intent = db.Column(db.String(150))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship('User', backref=db.backref('requests', lazy=True))

# Function to create the database tables
def create_database():
    with app.app_context():
        try:
            print("Attempting to create database tables...")
            db.create_all()
            print("Database tables created successfully.")
        except Exception as e:
            print(f"Error creating database tables: {e}")

# Load model and vectorizer
try:
    model_path = os.path.join(os.getcwd(), 'insurance_intent_classifier.pkl')
    vectorizer_path = os.path.join(os.getcwd(), 'vectorizer.pkl')

    model = joblib.load(model_path)
    vectorizer = joblib.load(vectorizer_path)
    print("Model and vectorizer loaded successfully.")
except FileNotFoundError as e:
    print(f"Error loading model or vectorizer: {e}")
    model = None
    vectorizer = None

# JWT Token required decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('x-access-token')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = User.query.filter_by(id=data['user_id']).first()
        except Exception as e:
            print(f"Token decoding failed: {e}")
            return jsonify({'message': 'Token is invalid!'}), 401
        return f(current_user, *args, **kwargs)
    return decorated

# Endpoint for Sign Up
@app.route('/signup', methods=['POST'])
def signup():
    try:
        data = request.get_json()
        print('Received signup request:', data)

        if not all([data.get('username'), data.get('email'), data.get('password')]):
            return jsonify({'message': 'All fields are required'}), 400

        # Check if the username or email already exists
        existing_user = User.query.filter(
            (User.username == data['username']) | (User.email == data['email'])
        ).first()

        if existing_user:
            print('User with this username or email already exists')
            return jsonify({'message': 'User with this username or email already exists'}), 409

        # Create a new user
        hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256', salt_length=8)
        new_user = User(username=data['username'], email=data['email'], password_hash=hashed_password)

        db.session.add(new_user)
        db.session.commit()

        print('User created successfully')
        return jsonify({'message': 'User created successfully'}), 201
    except Exception as e:
        print('Error during signup:', str(e))
        return jsonify({'message': f'Sign Up failed due to an internal error: {str(e)}'}), 500

# Endpoint for Sign In
@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        print('Received login request:', data)

        if not all([data.get('username'), data.get('password')]):
            return jsonify({'message': 'Username and password are required'}), 400

        # Find the user by username
        user = User.query.filter_by(username=data['username']).first()

        if user and check_password_hash(user.password_hash, data['password']):
            # Generate a JWT token that will expire in 1 hour
            token = jwt.encode({
                'user_id': user.id,
                'exp': datetime.utcnow() + timedelta(hours=1)
            }, app.config['SECRET_KEY'], algorithm="HS256")

            print('Login successful')
            return jsonify({'message': 'Login successful', 'token': token}), 200

        print('Invalid username or password')
        return jsonify({'message': 'Invalid username or password'}), 401
    except Exception as e:
        print('Error during login:', str(e))
        return jsonify({'message': f'Login failed due to an internal error: {str(e)}'}), 500

# Endpoint to submit a request
@app.route('/api/request', methods=['POST'])
@token_required
def submit_request(current_user):
    try:
        data = request.get_json()
        request_text = data.get('request_text')

        if not request_text:
            return jsonify({'message': 'Request text is required'}), 400

        # Assuming model and vectorizer are loaded and ready to use
        if model is None or vectorizer is None:
            return jsonify({'message': 'Model not loaded, cannot classify the request'}), 500

        # Classify the intent
        request_vector = vectorizer.transform([request_text])
        predicted_intent = model.predict(request_vector)[0]

        # Save the request to the database
        new_request = Request(user_id=current_user.id, request_text=request_text, intent=predicted_intent)
        db.session.add(new_request)
        db.session.commit()

        return jsonify({'message': 'Request submitted successfully', 'intent': predicted_intent}), 201

    except Exception as e:
        print('Error during request submission:', str(e))
        return jsonify({'message': f'Request submission failed due to an internal error: {str(e)}'}), 500

# Endpoint to get request history
@app.route('/api/history', methods=['GET'])
@token_required
def get_history(current_user):
    try:
        # Retrieve all requests by the current user
        user_requests = Request.query.filter_by(user_id=current_user.id).all()

        # Format the response
        request_history = [{
            'id': req.id,
            'request_text': req.request_text,
            'intent': req.intent,
            'created_at': req.created_at.strftime("%Y-%m-%d %H:%M:%S")  # Format date to avoid serialization issues
        } for req in user_requests]

        return jsonify({'history': request_history}), 200
    except Exception as e:
        print('Error during history retrieval:', str(e))
        return jsonify({'message': f'History retrieval failed due to an internal error: {str(e)}'}), 500

# Route to test if everything is running
@app.route('/')
def hello():
    return "Your Flask app is running."

if __name__ == '__main__':
    # Call the function to create tables before running the server
    create_database()
    app.run(debug=True)
