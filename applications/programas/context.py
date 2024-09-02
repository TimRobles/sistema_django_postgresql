import os
import uuid
from django.conf import settings

from .models import NivelUno

git_version = os.popen('git describe --tags --always').read().strip()
def contexto_menu(request):
    programa_nivel_uno = NivelUno.objects.all()
    data = {}
    data['programa_nivel_uno'] = programa_nivel_uno
    return data

def cache_bust(request):
    if settings.DEBUG:                                                                                                                   
        version = git_version
    else:                                                                                                                                
        version = os.environ.get('PROJECT_VERSION')
        if version is None:
            version = '1'
            
    texto = '__v__=%s' % (str(version))
    return {'cache_bust':texto}