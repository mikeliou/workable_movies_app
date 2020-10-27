from datetime import datetime
import math

import pymysql
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import Session, sessionmaker

from app.database.utilities import init_sqlalchemy_engine, init_mysql_db, Base
from app.database.mysql_queries import GET_MOVIE_DATA, GET_MOVIE_DATA_BY_ID


class Movie(Base):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    title = Column(String(50))
    description = Column(String(255))
    posted_by = Column(Integer)
    created = Column(DateTime)
    updated = Column(DateTime)

    def __init__(self, title, description, posted_by, created, updated, full_name=None, likes=None, dislikes=None):
        self.title = title
        self.description = description
        self.posted_by = posted_by
        self.created = created
        self.updated = updated
        self.full_name = full_name
        self.likes = likes
        self.dislikes = dislikes
        self.tdiff = []
        self.engine = init_sqlalchemy_engine()
        self.mysql_engine = init_mysql_db()

    def insert(self):
        """
        Inserts movie record to Database
        """
        Session = sessionmaker(bind=self.engine)
        session = Session()
        session.add(self)
        session.commit()

    @staticmethod
    def select_all():
        """
        Selects all movies records from Database
        :return: movies_list: list of dicts
        """
        mysql_engine = init_mysql_db()
        with mysql_engine.cursor(pymysql.cursors.DictCursor) as cur:
            cur.execute(GET_MOVIE_DATA)
            movies = cur.fetchall()

            movies_list = []
            for m in movies:
                tdiff = datetime.now() - m['created']
                tdiff_mins = math.floor(tdiff.seconds / 60)
                tdiff_hours = math.floor(tdiff.seconds / 3600)
                tdiff_months = math.floor(tdiff.days / 30)
                tdiff_years = math.floor(tdiff.days / 365)

                m['tdiff'] = [tdiff_years, tdiff_months, tdiff.days, tdiff_hours, tdiff_mins, tdiff.seconds]

                movies_list.append(m)

            return movies_list

    @staticmethod
    def select_by_userid(user_id):
        """
        Selects all movies records based on user id from Database
        :param user_id: int
        :return: movies_list: list of dicts
        """
        mysql_engine = init_mysql_db()
        with mysql_engine.cursor(pymysql.cursors.DictCursor) as cur:
            cur.execute(GET_MOVIE_DATA_BY_ID, (user_id, user_id))
            movies = cur.fetchall()

            movies_list = []
            for m in movies:
                tdiff = datetime.now() - m['created']
                tdiff_mins = math.floor(tdiff.seconds / 60)
                tdiff_hours = math.floor(tdiff.seconds / 3600)
                tdiff_months = math.floor(tdiff.days / 30)
                tdiff_years = math.floor(tdiff.days / 365)

                m['tdiff'] = [tdiff_years, tdiff_months, tdiff.days, tdiff_hours, tdiff_mins, tdiff.seconds]

                movies_list.append(m)

            return movies_list

    @staticmethod
    def check_movie_exists(title):
        """
        Checks if movie exists in Database based on title
        :param title: string
        :return: boolean
        """
        Session = sessionmaker(bind=init_sqlalchemy_engine())
        session = Session()
        results = session.query(Movie).filter(Movie.title == title.casefold()).count()

        return True if results == 0 else False
