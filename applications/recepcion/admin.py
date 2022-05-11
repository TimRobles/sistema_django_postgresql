from django.contrib import admin
from .models import (
    Visita,
    Asistencia,
    ResponsableAsistencia,
    IpPublica,
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


class ResponsableAsistenciaAdmin(admin.ModelAdmin):
    list_display = (
        'usuario_responsable',
        'permiso_cambio_ip',
        )
    list_filter = ('usuario_a_registrar',)


    def save_model(self, request, obj, form, change):
        if obj.created_by == None:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


class IpPublicaAdmin(admin.ModelAdmin):
    list_display = (
        'ip',
        'created_at',
        )


    def save_model(self, request, obj, form, change):
        if obj.created_by == None:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)




admin.site.register(Visita, VisitaAdmin)
admin.site.register(Asistencia, AsistenciaAdmin)
admin.site.register(ResponsableAsistencia, ResponsableAsistenciaAdmin)
admin.site.register(IpPublica, IpPublicaAdmin)

