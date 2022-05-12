from .base import *

DEBUG = True

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'dbprueba',
        'USER': 'multiplay',
        'PASSWORD': 'multiplay123',
        'HOST': 'localhost',
        'PORT': '5432',
    },
    'prod': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'sistema_django_prod',
        'USER': 'multiplay',
        'PASSWORD': 'multiplay123',
        'HOST': 'localhost',
        'PORT': '5432',
    },
}

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR.child('static'),
    ]
STATIC_ROOT = BASE_DIR

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR.ancestor(1).child('media_sistema_django_postgresql')

BUSCAR_IP = 'REMOTE_ADDR'