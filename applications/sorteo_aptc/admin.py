from django.contrib import admin

from applications.sorteo_aptc.models import UsuarioAPTC

# Register your models here.

@admin.register(UsuarioAPTC)
class UsuarioAPTCAdmin(admin.ModelAdmin):
    list_display = (
        'nombre',
        'tipo_documento',
        'numero_documento',
        'telefono',
        'correo',
        'empresa',
        'ticket',
        'premio',
        'elegido',
        'bloqueo',
        'created_at',
        'created_by',
        'updated_at',
        'updated_by',
        )
    list_filter = (
        'nombre',
        )
    search_fields = (
        'nombre',
        )
        
    def save_model(self, request, obj, form, change):
        if obj.created_by == None:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)
