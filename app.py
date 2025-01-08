import os

from flask import Flask, jsonify, request

from data_manager.sqlite_data_manager import SQLiteDataManager
from models import db
from models.director import Director
from models.movie import Movie
from models.user import User
from models.association import UserMovie


def create_app():
    """ Create a Flask app and initialize the data manager """
    app = Flask(__name__)

    # Ensure 'data' directory exists
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, 'data')
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    data_manager = SQLiteDataManager(os.path.join(data_dir, 'movie_database.db'), app)

    with app.app_context():
        db.create_all()  # Create tables if they don't exist

    return app, data_manager

app, data_manager = create_app()

@app.route('/')
def home():
    """ Home page """
    return "Welcome to MovieWeb App!"


@app.route('/users', methods=['GET'])
def users_list():
    """ display a list of all users """
    pass


@app.route('/user/<int:user_id>', methods=['GET'])
def user_page(user_id):
    """ display a user's page with their movies """
    pass


@app.route('/user/<int:user_id>/add_movie', methods=['GET'])
def add_movie_page(user_id):
    """ display a page to add a movie to a user's list """
    pass


@app.route('/add_movie', methods=['GET'])
def add_new_movie_page():
    """ display a page to add a new movie """
    pass


@app.route('/user/<int:user_id>/modify_movie/<int:movie_id>', methods=['GET'])
def modify_movie_page(user_id, movie_id):
    """ display a page to modify a movie in a user's list """
    pass


if __name__ == '__main__':
    app.run(debug=True)
