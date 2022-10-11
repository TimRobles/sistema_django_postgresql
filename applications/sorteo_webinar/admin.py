from django.contrib import admin

from applications.sorteo_webinar.models import Participante

# Register your models here.
@admin.register(Participante)
class ParticipanteAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'nombre_completo',
        'documento',
        'telefono',
        'correo',
        'elegido',
        'premio',
        )