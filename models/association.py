from sqlalchemy.orm import Mapped, mapped_column

from . import db

class UserMovie(db.Model):
    __tablename__ = 'user_movie'
    user_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    movie_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey('movie.id'), primary_key=True)
    rating: Mapped[int] = mapped_column(db.Integer, nullable=False)

    user = db.relationship('User', back_populates='movies')
    movie = db.relationship('Movie', back_populates='users')


class MovieDirector(db.Model):
    __tablename__ = 'movie_director'
    movie_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey('movie.id'), primary_key=True)
    director_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey('director.id'), primary_key=True)
