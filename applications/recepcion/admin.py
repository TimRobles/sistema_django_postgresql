from django.contrib import admin
from .models import (
    Visita,
    Asistencia,
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
        'fecha_registro',
        )
    exclude = (
        'hora_ingreso',
        'hora_salida',
        'fecha_registro',
    )

    def save_model(self, request, obj, form, change):
        if obj.created_by == None:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


class AsistenciaAdmin(admin.ModelAdmin):
    list_display = (
        'usuario',
        'hora_ingreso',
        'hora_salida',
        'fecha_registro',
        'created_by',
        'updated_by',
        'updated_at',
        'created_at',
        )
    exclude = (
        'hora_ingreso',
        'hora_salida',
        )

    def save_model(self, request, obj, form, change):
        if obj.created_by == None:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


admin.site.register(Visita, VisitaAdmin)
admin.site.register(Asistencia, AsistenciaAdmin)

