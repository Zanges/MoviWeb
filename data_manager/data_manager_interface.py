from abc import ABC


class DataManagerInterface(ABC):
    pass
# Since I'm using FlaskAlchemy, I don't see a good point in implementing an interface where I would lose all benefits of Alchemy.