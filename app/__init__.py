from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Initialize the database
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Configuration (using SQLite for simplicity)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize the database with the app
    db.init_app(app)

    # Import routes here to register them
    from app import routes
    app.register_blueprint(routes.bp)

    return app
