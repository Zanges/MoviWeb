from data_manager.data_manager_interface import DataManagerInterface
from models import db
from models.association import UserMovie
from models.director import Director
from models.movie import Movie
from models.user import User


INSTANCE = None


class SQLiteDataManager(DataManagerInterface):
    def __init__(self, db_path: str, app):
        app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
        db.init_app(app)

        global INSTANCE
        if INSTANCE is not None:
            raise Exception("Only one instance of SQLiteDataManager is allowed")
        INSTANCE = self

    @staticmethod
    def get_user_list() -> list[User]:
        """ Get a list of all users """
        return User.query.all()

    @staticmethod
    def get_user_by_id(user_id: int) -> User:
        """ Get a user by their id """
        return User.query.get(user_id)

    @staticmethod
    def add_new_user(user: User) -> User:
        """ Add a new user to the database """
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def delete_user(user: User) -> None:
        """ Delete a user from the database """
        db.session.delete(user)
        db.session.commit()

    @staticmethod
    def update_user(user: User) -> User:
        """ Update a user in the database """
        db.session.commit()
        return user

    @staticmethod
    def get_full_movie_list() -> list[Movie]:
        """ Get a list of all movies """
        return Movie.query.all()

    @staticmethod
    def get_user_movie_list(user: User) -> list[Movie]:
        """ Get a list of all movies a user has """
        return [user_movie.movie for user_movie in user.movies]

    @staticmethod
    def get_movie_by_id(movie_id: int) -> Movie:
        """ Get a movie by its id """
        return Movie.query.get(movie_id)

    @staticmethod
    def get_movies_by_title(title: str) -> list[Movie]:
        """ Get a list of movies by their title """
        return Movie.query.filter_by(title=title).all()

    @staticmethod
    def add_movie_to_user(user: User, movie: Movie) -> UserMovie:
        """ Add a movie to a user's list """
        user_movie = UserMovie(user=user, movie=movie)
        db.session.add(user_movie)
        db.session.commit()
        return user_movie

    @staticmethod
    def remove_movie_from_user(user: User, movie: Movie) -> None:
        """ Remove a movie from a user's list """
        user_movie = UserMovie.query.filter_by(user=user, movie=movie).first()
        db.session.delete(user_movie)
        db.session.commit()

    @staticmethod
    def add_new_movie(movie: Movie) -> Movie:
        """ Add a new movie to the database """
        db.session.add(movie)
        db.session.commit()
        return movie

    @staticmethod
    def delete_movie(movie: Movie) -> None:
        """ Delete a movie from the database """
        db.session.delete(movie)
        db.session.commit()

    @staticmethod
    def update_movie(movie: Movie) -> Movie:
        """ Update a movie in the database """
        db.session.commit()
        return movie

    @staticmethod
    def get_director_by_name(name: str) -> Director:
        """ Get a director by their name """
        return Director.query.filter_by(name=name).first()
    