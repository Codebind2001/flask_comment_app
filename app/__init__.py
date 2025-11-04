from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS  # ✅ add this import

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    CORS(app)  # ✅ enable CORS for frontend access

    from app import routes
    app.register_blueprint(routes.bp)

    return app
