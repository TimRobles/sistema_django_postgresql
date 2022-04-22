from .models import NivelUno

def contexto_menu(request):
    programa_nivel_uno = NivelUno.objects.all()
    data = {}
    data['programa_nivel_uno'] = programa_nivel_uno
    return data