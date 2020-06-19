from .base import *

DEBUG = False

SECRET_KEY = os.environ['SECRET_KEY']

DATABASES = {
    'default':  {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'treedo',
        'USER': 'rational',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '',
    }
}
