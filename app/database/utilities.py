import pymysql
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base

from app.configuration import SQLALCHEMY_URL
from app.configuration import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE


metadata = MetaData()
Base = declarative_base(metadata=metadata)


def init_sqlalchemy_engine():
    engine = create_engine(SQLALCHEMY_URL)
    return engine


def init_mysql_db():
    con = pymysql.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DATABASE,
        use_unicode=True,
        charset='utf8'
    )
    return con
