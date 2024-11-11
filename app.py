from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from functools import wraps

app = Flask(__name__)

# Allow CORS with specific settings
CORS(app, resources={r"/*": {"origins": "http://localhost:4200"}})

# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'  # encode and decode JWT
db = SQLAlchemy(app)

# Define User table
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(150), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


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

@app.route('/signup', methods=['POST'])
def signup():
    try:
        data = request.get_json()
        print('Received signup request:', data)

        # Check if the username or email already exists
        existing_user = User.query.filter(
            (User.username == data['username']) | (User.email == data['email'])
        ).first()

        if existing_user:
            print('User with this username or email already exists')
            return jsonify({'message': 'User with this username or email already exists'}), 409

        # Create a new user
        hashed_password = generate_password_hash(data['password'], method='sha256')
        new_user = User(username=data['username'], email=data['email'], password_hash=hashed_password)

        db.session.add(new_user)
        db.session.commit()

        print('User created successfully')
        return jsonify({'message': 'User created successfully'}), 201
    except Exception as e:
        print('Error during signup:', str(e))
        return jsonify({'message': 'Sign Up failed due to an internal error'}), 500

# Endpoint for Sign In
@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        print('Received login request:', data)

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
        return jsonify({'message': 'Login failed due to an internal error'}), 500


@app.route('/protected', methods=['GET'])
@token_required
def protected(current_user):
    return jsonify({'message': f'Hello {current_user.username}, you have access to this protected route!'})

# Route to test if everything is working
@app.route('/')
def hello():
    return "Your Flask app is running."

if __name__ == '__main__':
    # Run the application
    app.run(debug=True)
