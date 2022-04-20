from django.contrib import admin

from .models import *

class HistoricoUserAdmin(admin.ModelAdmin):
    list_display = (
        'usuario',
        'fecha_alta',
        'fecha_baja',
        'created_at', 
        'created_by', 
        'updated_at', 
        'updated_by', 
    )
    exclude = (
        'fecha_baja',
        'estado',
    )

    def save_model(self, request, obj, form, change):
        if obj.created_by == None:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)

class DatosUsuarioAdmin(admin.ModelAdmin):
    list_display = (
        'usuario',
        'tipo_documento',
        'numero_documento',
        'created_at',
        'created_by',
        'updated_at',
        'updated_by',
        )
        
    def save_model(self, request, obj, form, change):
        if obj.created_by == None:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)

admin.site.register(HistoricoUser, HistoricoUserAdmin)
admin.site.register(DatosUsuario, DatosUsuarioAdmin)