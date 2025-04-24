from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from dashboard import dashboard_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # Use SQLite for simplicity
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)



# Create the database tables
with app.app_context():
    db.create_all()

# Register the dashboard blueprint
app.register_blueprint(dashboard_bp)

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({'message': 'Missing required fields'}), 400
    
    if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
       return jsonify({'message': 'User already exists'}), 400

    user = User()
    user.username = username
    user.email = email
    user.set_password(password)

    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        data = request.get_json()
        temperature = data.get('temperature')
        rainfall = data.get('rainfall')
        wind_speed = data.get('wind-speed')
        humidity = data.get('humidity')
        location = data.get('location')

        # Perform prediction logic here (replace with your actual model or logic)
        prediction = "Flood"  # Example prediction
        probability = 0.85  # Example probability

        # Return the prediction and probability
        return jsonify({'disaster_type': prediction, 'probability': probability})

    return "Invalid method", 400



@app.route('/')
def index():
    return redirect(url_for('static', filename='dashboard.html'))



if __name__ == '__main__':
    app.run(debug=True)

