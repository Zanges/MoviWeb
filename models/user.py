from sqlalchemy.orm import Mapped, mapped_column

from . import db


class User(db.Model):
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(db.String(100), nullable=False)

    movies = db.relationship('UserMovie', back_populates='user')

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<User {self.name}>"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
        }