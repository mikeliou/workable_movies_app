from passlib.hash import pbkdf2_sha256
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import Session, sessionmaker

from app.database.utilities import init_sqlalchemy_engine, Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    email = Column(String(50))
    password = Column(String(255))
    status = Column(String(50))
    created = Column(DateTime)
    updated = Column(DateTime)

    def __init__(self, first_name, last_name, email, password, created, updated):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.created = created
        self.updated = updated
        self.engine = init_sqlalchemy_engine()

    def insert(self):
        """
        Inserts user record to Database
        """
        Session = sessionmaker(bind=self.engine)
        session = Session()
        self.password = self.encrypt_password(self.password)
        session.add(self)
        session.commit()

    @staticmethod
    def select_by_email(email):
        """
        Selects user record based on email from Database
        :param email: string
        :return: user: dict
        """
        Session = sessionmaker(bind=init_sqlalchemy_engine())
        session = Session()
        results = session.query(User).filter(User.email == email).first()

        if not results:
            print('User not found')
            return

        user = {
            'id': results.id,
            'first_name': results.first_name,
            'last_name': results.last_name,
            'password': results.password
        }
        return user

    @staticmethod
    def select_by_user_id(user_id):
        """
        Selects user record based on user id from Database
        :param user_id: int
        :return: user: dict
        """
        Session = sessionmaker(bind=init_sqlalchemy_engine())
        session = Session()
        results = session.query(User).filter(User.id == user_id).first()

        if not results:
            print('User not found')
            return

        user = {
            'id': results.id,
            'first_name': results.first_name,
            'last_name': results.last_name
        }
        return user

    @staticmethod
    def check_email_exists(email):
        """
        Checks if email exists on Database
        :param email: string
        :return: boolean
        """
        Session = sessionmaker(bind=init_sqlalchemy_engine())
        session = Session()
        results = session.query(User).filter(User.email == email.casefold()).count()

        return True if results == 0 else False

    @staticmethod
    def encrypt_password(raw_password):
        """
        Encrypts raw password to hashed password
        :param raw_password: string
        :return: string
        """
        return pbkdf2_sha256.hash(raw_password)

    @staticmethod
    def check_password(raw_password, hashed_password):
        """
        Check if raw password verifies hashed password
        :param raw_password: string
        :return: boolean
        """
        return pbkdf2_sha256.verify(raw_password, hashed_password)

    @staticmethod
    def authenticate(email, raw_password):
        """
        Authenticates user from Database
        :param email: string
        :param raw_password: string
        :return: found_user: dict
        """
        found_user = User.select_by_email(email)
        if found_user and User.check_password(raw_password, found_user['password']):
            return found_user
        return
