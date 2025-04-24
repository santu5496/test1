import os, sqlite3

from flask import Flask, request, jsonify, render_template, send_from_directory
import os
app = Flask(__name__)

DATABASE = 'database/flood_management.db'

def get_db():
    """Connect to the database."""
    db = sqlite3.connect(DATABASE)
    return db

def init_db():
    """Initialize the database with tables."""
    db = get_db()
    with open('schema.sql', 'r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()

@app.before_request
def before_request():
    """Ensure the database is initialized before each request."""
    if not os.path.exists(DATABASE):
        os.makedirs(os.path.dirname(DATABASE), exist_ok=True)
        init_db()

@app.route('/')
def index():
    """Render the login page."""
    return render_template('login.html')

@app.route('/static/<path:filename>')
def serve_static(filename):
    """Serve static files from the 'static' directory."""
    root_dir = os.path.dirname(os.path.abspath(__file__))
    return send_from_directory(os.path.join(root_dir, 'static'), filename)

@app.route("/login")
def login_page():
    return render_template('login.html')

@app.route('/register', methods=['POST'])
def register():
    """User registration endpoint."""
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

@app.route('/api/login', methods=['POST'])
def login():
    """User login endpoint."""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # basic check, in real app, hash and salt passwords
    if username == 'admin' and password == 'password':
        return jsonify({'message': 'Login successful'}), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/dashboard')
def dashboard_page():
    """Render the dashboard page."""
    return render_template('dashboard.html')

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 3000)))