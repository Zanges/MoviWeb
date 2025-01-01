from sqlalchemy.orm import Mapped, mapped_column

from . import db


class Director(db.Model):
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(db.String(100), nullable=False)
    birth_date: Mapped[str] = mapped_column(db.Date, nullable=True)
    date_of_death: Mapped[str] = mapped_column(db.Date, nullable=True)

    movies = db.relationship("Movie", back_populates="director", lazy=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<Director {self.name}>"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "birth_date": self.birth_date,
            "date_of_death": self.date_of_death,
        }