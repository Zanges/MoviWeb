from sqlalchemy.orm import Mapped, mapped_column

from . import db


class Movie(db.Model):
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(db.String(100), nullable=False)
    release_date: Mapped[str] = mapped_column(db.Date, nullable=True)
    director_id: Mapped[int] = mapped_column(
        db.Integer, db.ForeignKey("director.id"), nullable=False
    )

    director = db.relationship("Director", back_populates="movies")

    users = db.relationship('UserMovie', back_populates='movie')

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