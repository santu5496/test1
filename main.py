import os
import sqlite3
from flask import Flask, request, jsonify, render_template
from model import DisasterPredictor

app = Flask(__name__)

DATABASE = 'database/flood_management.db'
predictor = DisasterPredictor()
predictor.load_model()

# Database connection
def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row  # This allows row results to be accessed like a dictionary
    return db

# Initialize the database schema
def init_db():
    db = get_db()
    with open('schema.sql', 'r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()

# Create DB if it doesn't exist
@app.before_request
def before_request():
    if not os.path.exists(DATABASE):
        os.makedirs(os.path.dirname(DATABASE), exist_ok=True)
        init_db()

@app.route('/')
def index():
    return render_template('login.html')

# Register a new user
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400

    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        db.commit()
        return jsonify({'message': 'User registered successfully'}), 201
    except sqlite3.IntegrityError:
        return jsonify({'message': 'Username already exists'}), 409
    finally:
        db.close()

# Login route: Verify the user from the database
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400

    db = get_db()
    cursor = db.cursor()
    
    # Query to check if the user exists in the database
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()

    if user:
        # If user found, return a success message and user data
        return jsonify({
            'message': 'Login successful',
            'user': {
                'id': user['id'],
                'username': user['username']
            }
        }), 200
    else:
        return jsonify({'message': 'Invalid username or password'}), 401

# Disaster prediction route
@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        temperature = float(data.get('temperature'))
        rainfall = float(data.get('rainfall'))
        wind_speed = float(data.get('wind_speed'))
        humidity = float(data.get('humidity'))

        if not all([temperature, rainfall, wind_speed, humidity]):
            return jsonify({"error": "All fields are required"}), 400

        input_data = {
            'temperature': temperature,
            'rainfall': rainfall,
            'wind_speed': wind_speed,
            'humidity': humidity
        }

        # Using the DisasterPredictor model to predict
        prediction, probability, will_occur = predictor.predict(input_data)

        return jsonify({
            'disaster_type': prediction,
            'probability': round(probability, 4),
            'disaster_message': "Disaster will occur" if will_occur == "Yes" else "Disaster will not occur"
        })

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

# Dashboard page
@app.route('/dashboard')
def dashboard_page():
    return render_template('dashboard.html')

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 3000)))
