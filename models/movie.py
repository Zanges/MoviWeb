from sqlalchemy.orm import Mapped, mapped_column

from . import db
from .association import MovieDirector, UserMovie


class Movie(db.Model):
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(db.String(100), nullable=False)
    release_date: Mapped[str] = mapped_column(db.Date, nullable=True)

    directors = db.relationship(
        'Movie',
        secondary=MovieDirector.__table__,
        back_populates='movie'
    )

    users = db.relationship(
        'UserMovie',
        secondary=UserMovie.__table__,
        back_populates='movie'
    )

    def __str__(self):
        return self.title

    def __repr__(self):
        return f"<Movie {self.title}>"

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "release_date": self.release_date,
            "director_id": self.director_id,
        }