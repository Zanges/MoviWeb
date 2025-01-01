from data_manager.data_manager_interface import DataManagerInterface
from models import db
from models.association import UserMovie
from models.movie import Movie
from models.user import User


class SQLiteDataManager(DataManagerInterface):
    def __init__(self, db_path: str, app):
        super().__init__()
        app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
        db.init_app(app)

    def get_current_user_name(self) -> str:
        """ Get the current user's name """
        return self.get_user().name

    @staticmethod
    def get_user_list() -> list[User]:
        """ Get a list of all users """
        return User.query.all()

    def get_user(self) -> User:
        """ Get the current user """
        return User.query.get(self._current_user_id)

    @staticmethod
    def get_user_by_id(user_id: int) -> User:
        """ Get a user by their id """
        return User.query.get(user_id)

    def get_user_movies(self) -> list:
        """ Get a list of all movies for the current user """
        return self.get_user().movies

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

    def add_movie_to_user(self, movie: Movie) -> User:
        """ Add a movie to the current user """
        user_id = self._current_user_id
        movie_id = movie.id

        association = UserMovie.query.filter_by(user_id=user_id, movie_id=movie_id).first()

        if not association:
            # Create a new association
            association = UserMovie(user_id=user_id, movie_id=movie_id)
            db.session.add(association)
        db.session.commit()

        return self.get_user()

    def remove_movie_from_user(self, movie: Movie) -> User:
        """ Remove a movie from the current user """
        user_id = self._current_user_id
        movie_id = movie.id

        association = UserMovie.query.filter_by(user_id=user_id, movie_id=movie_id).first()

        if association:
            db.session.delete(association)
        db.session.commit()

        return self.get_user()

    @staticmethod
    def get_full_movie_list() -> list[Movie]:
        """ Get a list of all movies """
        return Movie.query.all()

    @staticmethod
    def get_movie_by_id(movie_id: int) -> Movie:
        """ Get a movie by its id """
        return Movie.query.get(movie_id)

    @staticmethod
    def get_movies_by_title(title: str) -> list[Movie]:
        """ Get a list of movies by their title """
        return Movie.query.filter_by(title=title).all()

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
    