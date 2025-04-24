from flask import Flask
from dashboard import dashboard_bp

app = Flask(__name__)

# Register the dashboard blueprint
app.register_blueprint(dashboard_bp)

if __name__ == '__main__':
    app.run(debug=True)
