from .base import *

DEBUG = True

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR.child('db.sqlite3'),
    },
    'prod': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'dbprueba',
        'USER': 'multiplay',
        'PASSWORD': 'multiplay123',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}