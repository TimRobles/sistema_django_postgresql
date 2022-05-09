import os
import uuid
from django.conf import settings                                                                                                         

from .models import NivelUno

def contexto_menu(request):
    programa_nivel_uno = NivelUno.objects.all()
    data = {}
    data['programa_nivel_uno'] = programa_nivel_uno
    return data

def cache_bust(request):
    if settings.DEBUG:                                                                                                                   
        version = uuid.uuid1()
    else:                                                                                                                                
        version = os.environ.get('PROJECT_VERSION')
        if version is None:
            version = '1'
            
    texto = '__v__=%s' % (str(version))
    return {'cache_bust':texto}