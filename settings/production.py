from .base import *
import dj_database_url

DEBUG = True

SECRET_KEY = os.environ['SECRET_KEY']

DATABASES['default'] = dj_database_url.config(conn_max_age=600, ssl_require=True)

ALLOWED_HOSTS = ['treedo-rational-labs.herokuapp.com', 'treedo.wtf']
