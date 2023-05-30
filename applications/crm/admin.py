from django.contrib import admin

from .models import ClienteCRM, ClienteCRMDetalle

@admin.register(ClienteCRM)
class ClienteCRMAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'cliente_crm',
        'medio',
        'estado',
        'created_by',
        'created_at',
        'updated_by',
        'updated_at',        
        )
        
    def save_model(self, request, obj, form, change):
        if obj.created_by == None:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(ClienteCRMDetalle)
class ClienteCRMDetalleAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'interlocutor',
        'correo',
        'telefono',
        'cliente_crm',
        'created_by',
        'created_at',
        'updated_by',
        'updated_at',        
        )
        
    def save_model(self, request, obj, form, change):
        if obj.created_by == None:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)