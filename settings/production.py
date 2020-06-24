from .base import *
import dj_database_url

DEBUG = True

SECRET_KEY = os.environ['SECRET_KEY']

DATABASES['default'] = dj_database_url.config(conn_max_age=600, ssl_require=True)

ALLOWED_HOSTS = ['treedo-rational-labs.herokuapp.com', 'treedo.wtf']

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                'treedo.context_processors.use_ga'
            ],
        },
    },
]
