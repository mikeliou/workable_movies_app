from sqlalchemy import Column, Integer, DateTime, Boolean
from sqlalchemy.orm import Session, sessionmaker

from app.database.utilities import init_sqlalchemy_engine, Base


class Action(Base):
    __tablename__ = 'actions'

    id = Column(Integer, primary_key=True)
    action_type = Column(Boolean)
    movie_id = Column(Integer)
    user_id = Column(Integer)
    created = Column(DateTime)
    updated = Column(DateTime)

    def __init__(self, action_type, movie_id, user_id, created, updated):
        self.action_type = action_type
        self.movie_id = movie_id
        self.user_id = user_id
        self.created = created
        self.updated = updated
        self.engine = init_sqlalchemy_engine()

    def insert(self):
        """
        Inserts action record to Database
        """
        Session = sessionmaker(bind=self.engine)
        session = Session()
        session.add(self)
        session.commit()

    @staticmethod
    def select_user_preferences(user_id):
        """
        Selects the action records based on user id from Database
        :param user_id: int
        :return: results_action : list of dicts
        """
        Session = sessionmaker(bind=init_sqlalchemy_engine())
        session = Session()
        results = session.query(Action).filter(Action.user_id == user_id).all()
        results_actions = []
        for r in results:
            action = {
                'id': r.id,
                'action_type': r.action_type,
                'movie_id': r.movie_id,
                'user_id': r.user_id,
                'created': r.created,
                'updated': r.updated
            }
            results_actions.append(action)

        return results_actions

    @staticmethod
    def delete(action_id):
        """
        Deletes action record from Database
        :param action_id: int
        """
        Session = sessionmaker(bind=init_sqlalchemy_engine())
        session = Session()
        session.query(Action).filter(Action.id == action_id).delete()
        session.commit()
