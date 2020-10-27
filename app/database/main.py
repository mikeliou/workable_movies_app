from app.database.action import Action
from app.database.movie import Movie
from app.database.user import User

from app.database.utilities import init_sqlalchemy_engine, Base

if __name__ == "__main__":
    engine = init_sqlalchemy_engine()
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)