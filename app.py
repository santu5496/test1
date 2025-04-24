from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from dashboard import dashboard_bp
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your_default_secret_key')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Updated User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    authenticated = db.Column(db.Boolean, default=False)  # Add authenticated attribute

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def is_active(self):
        return True

    def get_id(self):
        return str(self.id)

    def is_authenticated(self):
        return self.authenticated

    def is_anonymous(self):
        return False

# Create the database tables
with app.app_context():
    db.create_all()

# Register blueprints
app.register_blueprint(dashboard_bp)

# Registration route
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data:
      return jsonify({'message': 'No data provided'}), 400
    
    username = data.get('username',None)
    email = data.get('email',None)
    password = data.get('password',None)

    if not username or not email or not password:
        return jsonify({'message': 'Missing required fields'}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({'message': 'Username already exists'}), 400
    if User.query.filter_by(email=email).first():
       return jsonify({'message': 'email already exists'}), 400

    user = User()
    user.username = username
    user.email = email
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201

# Login route
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'message': 'Missing credentials'}), 400

    user = User.query.filter_by(username=username).first()

    if user and user.check_password(password):
        user.authenticated = True
        db.session.commit()
        session['user_id'] = user.id  # Store user ID in session
        return jsonify({'message': 'Logged in successfully'}), 200
    else:
        return jsonify({'message': 'Invalid username or password'}), 401


# Logout route
@app.route('/logout')
def logout():
    session.pop('user_id', None)  # Remove user ID from session
    return jsonify({'message': 'Logged out successfully'}), 200

# index route
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])  # Make sure you have methods=['POST']
def predict():
    if request.method == 'POST':
        data = request.get_json()
        # ... Your prediction logic using the data ...
        # ... Example: Let's just return some dummy data for now ...
        prediction = "Flood"  # Replace with your actual prediction
        probability = 0.85  # Replace with your actual probability
        return jsonify({'disaster_type': prediction, 'probability': probability})
    return "not"


if __name__ == '__main__':
    app.run(debug=True)

