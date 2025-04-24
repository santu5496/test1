# dashboard.py
from flask import Blueprint, request, jsonify, redirect, url_for
from model import DisasterPredictor

dashboard_bp = Blueprint('dashboard', __name__)

# Load the trained model
predictor = DisasterPredictor()
predictor.load_model()

@dashboard_bp.route('/predict', methods=['POST'])
def predict_route():
    try:
        data = request.get_json(force=True)

        # Make a prediction using the loaded model
        disaster_type = predictor.predict(data)

        return jsonify({'disaster_type': disaster_type})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@dashboard_bp.route('/call_predict', methods=['POST'])
def call_predict():
    return redirect(url_for('predict_route'))
@dashboard_bp.route('/submit', methods=['POST'])
def submit():
    
    
    return redirect(url_for('static', filename='script.js'))


```
```python
# app.py
from flask import Flask, render_template
from dashboard import dashboard_bp

app = Flask(__name__)
app.register_blueprint(dashboard_bp)

@app.route('/')
def index():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)