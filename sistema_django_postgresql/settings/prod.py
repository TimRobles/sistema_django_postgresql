from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'www.multiplay-group.com', 'multiplay-group.com', 'sistema.multiplay.com.pe']
# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'sistema_django_prod',
        'USER': 'multiplay',
        'PASSWORD': 'multiplay123',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR.child('static'),
    ]
STATIC_ROOT = BASE_DIR.child('staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR.ancestor(1).child('media')

BUSCAR_IP = 'HTTP_CF_CONNECTING_IP'

CRONJOBS = [
    #cron format: minute, hour, day of month, month, day of week
    ('00 10 * * 1-6', 'applications.reportes.pdf.reporte_cobranza', '--settings sistema_django_postgresql.settings.prod >> /webapps/sistema_django_prod/sistema_django_postgresql/cronjob.log 2>&1'),
    ('00 01 * * *', 'applications.crm.models.actualizar_estado_cliente_crm', '--settings sistema_django_postgresql.settings.prod >> /webapps/sistema_django_prod/sistema_django_postgresql/cronjob.log 2>&1'),
    ('00 14 * * *', 'applications.datos_globales.funciones.actualizarTotalTipoCambioSunat', '--settings sistema_django_postgresql.settings.prod >> /webapps/sistema_django_prod/sistema_django_postgresql/cronjob.log 2>&1'),
    ('45 11 19 6 *', 'applications.sunarp.funcion_sunarp', '--settings sistema_django_postgresql.settings.prod >> /webapps/sistema_django_prod/sistema_django_postgresql/cronjob.log 2>&1'),
]
