from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
from werkzeug.security import generate_password_hash

app = Flask(__name__)
CORS(app)

# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define User table
class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(150), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Define Request table
class Request(db.Model):
    request_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    request_text = db.Column(db.Text, nullable=False)
    intent = db.Column(db.String(150))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# A basic route to test if everything is working
@app.route('/')
def hello():
    return "Hello, World! Your Flask app is running."

if __name__ == '__main__':
    # Create the database tables within an application context
    with app.app_context():
        db.create_all()  # This will create the tables in your database
    # Run the application
    app.run(debug=True)
