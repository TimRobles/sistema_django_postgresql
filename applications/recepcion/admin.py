from django.contrib import admin
from .models import (
    Visita,
)

class VisitaAdmin(admin.ModelAdmin):
    list_display = (
        'nombre',
        'tipo_documento',
        'numero_documento',
        'usuario_atendio',
        'motivo_visita',
        'hora_ingreso',
        'hora_salida',
        'empresa_cliente',
        )

    def save_model(self, request, obj, form, change):
        if obj.created_by == None:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)

admin.site.register(Visita, VisitaAdmin)
