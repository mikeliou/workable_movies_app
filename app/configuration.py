import os


SQLALCHEMY_URL = os.environ.get('DATABASE_URL', 'mysql://root:mikeliou@localhost/movies')
MYSQL_USER = os.environ.get('MYSQL_USER', 'root')
MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', 'mikeliou')
MYSQL_HOST = os.environ.get('MYSQL_HOST', 'localhost')
MYSQL_DATABASE = os.environ.get('MYSQL_DATABASE', 'movies')

SERVICE_HOSTNAME = os.environ.get('SERVICE_HOSTNAME', 'localhost')
SERVICE_PORT = os.environ.get('SERVICE_PORT', 8000)
SERVICE_DEBUG = os.environ.get('SERVICE_DEBUG', True)
