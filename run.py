from app import create_app, db
from app.models import Task, Comment

# Create the Flask app
app = create_app()

# Create the database tables (Flask 3.1+ compatible)
with app.app_context():
    db.create_all()

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
