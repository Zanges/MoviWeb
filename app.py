import os

from flask import Flask

from data_manager.sqlite_data_manager import SQLiteDataManager
from models import db

def create_app():
    app = Flask(__name__)

    # Ensure 'data' directory exists
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, 'data')
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    data_manager = SQLiteDataManager(os.path.join(data_dir, 'movie_database.db'), app)

    with app.app_context():
        db.create_all()  # Create tables if they don't exist

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
