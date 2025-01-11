import os

from flask import Flask, jsonify, request, render_template, redirect, url_for

from data_manager.sqlite_data_manager import SQLiteDataManager
from models import db
from models.director import Director
from models.movie import Movie
from models.user import User
from models.association import UserMovie
from omdbapi import get_movie_by_title


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
    return render_template('home.html'), 200


@app.route('/users', methods=['GET'])
def users_list():
    """ display a list of all users """
    users = data_manager.get_user_list()
    return render_template('users.html', users=users), 200


@app.route('/add_user', methods=['GET'])
def add_user_page():
    """ display a page to add a new user """
    return render_template('add_user.html'), 200


@app.route('/user/<int:user_id>', methods=['GET'])
def user_page(user_id):
    """ display a user's page with their movies """
    user = data_manager.get_user_by_id(user_id)
    if not user:
        return render_template('404.html'), 404
    return render_template('user_page.html', user=user), 200


@app.route('/user/<int:user_id>/add_movie', methods=['GET'])
def add_movie_page(user_id):
    """ display a page to add a movie to a user's list """
    user = data_manager.get_user_by_id(user_id)
    if not user:
        return render_template('404.html'), 404
    movies = data_manager.get_full_movie_list()
    return render_template(
        'user_add_movie.html',
        user=user,
        movies=movies
    ), 200


@app.route('/add_movie', methods=['GET'])
def add_new_movie_page():
    """ display a page to add a new movie """
    return render_template('add_movie.html'), 200


@app.route('/user/<int:user_id>/modify_movie/<int:movie_id>', methods=['GET'])
def modify_movie_page(user_id, movie_id):
    """ display a page to modify a movie in a user's list """
    user = data_manager.get_user_by_id(user_id)
    movie = data_manager.get_movie_by_id(movie_id)
    if not user or not movie:
        return render_template('404.html'), 404
    old_rating = data_manager.get_user_movie_rating(user_id, movie_id)
    return render_template(
        'user_update_movie.html',
        user=user,
        movie=movie,
        old_rating=old_rating
    ), 200


@app.route('/add_user', methods=['POST'])
def add_user():
    """ add a new user """
    name = request.form['name']
    user = User(name=name)
    data_manager.add_new_user(user)
    return redirect(url_for('users_list')), 201



@app.route('/delete_user', methods=['POST'])
def delete_user():
    """ delete a user """
    user_id = int(request.form['user_id'])
    user = data_manager.get_user_by_id(user_id)
    data_manager.delete_user(user)
    return redirect(url_for('users_list')), 204


@app.route('/add_user_movie', methods=['POST'])
def add_user_movie():
    """ add a movie to a user's list """
    user_id = int(request.form['user_id'])
    movie_id = int(request.form['movie'])
    rating = int(request.form['rating'])
    user = data_manager.get_user_by_id(user_id)
    movie = data_manager.get_movie_by_id(movie_id)
    data_manager.add_movie_to_user(user, movie, rating)
    return redirect(url_for('user_page', user_id=user_id)), 201


@app.route('/add_movie', methods=['POST'])
def add_movie():
    """ add a new movie """
    title = request.form['title']
    omdb_data = get_movie_by_title(title)
    if not omdb_data:
        return redirect(url_for('add_new_movie_page')), 500

    directors = []
    for director in omdb_data['directors']:
        # Check if the director already exists else create a new one
        director_obj = data_manager.get_director_by_name(director)
        if not director_obj:
            director_obj = Director(name=director)
            data_manager.add_director(director_obj)
        directors.append(director_obj)

    movie = Movie(
        title=omdb_data['title'],
        year=omdb_data['year'],
        poster=omdb_data['poster'],
        directors=directors
    )

    data_manager.add_new_movie(movie)
    return redirect(url_for('users_list')), 201


@app.route('/delete_user_movie', methods=['POST'])
def delete_user_movie():
    """ delete a movie from a user's list """
    user_id = int(request.form['user_id'])
    movie_id = int(request.form['movie_id'])
    user = data_manager.get_user_by_id(user_id)
    movie = data_manager.get_movie_by_id(movie_id)
    data_manager.remove_movie_from_user(user, movie)
    return redirect(url_for('user_page', user_id=user_id)), 204


@app.route('/update_user_movie', methods=['POST'])
def update_user_movie():
    """ update a movie in a user's list """
    user_id = int(request.form['user_id'])
    movie_id = int(request.form['movie_id'])
    rating = int(request.form['rating'])
    data_manager.update_user_movie(user_id, movie_id, rating)
    return redirect(url_for('user_page', user_id=user_id)), 201


if __name__ == '__main__':
    app.run(debug=True)
