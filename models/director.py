from sqlalchemy.orm import Mapped, mapped_column

from . import db
from .association import MovieDirector


class Director(db.Model):
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(db.String(100), nullable=False)

    movies = db.relationship(
        'Movie',
        secondary=MovieDirector.__table__,
        back_populates='directors'
    )

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<Director {self.name}>"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }