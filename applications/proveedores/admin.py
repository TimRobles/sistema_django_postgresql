from django.contrib import admin

from .models import (
    Proveedor,
    InterlocutorProveedor,
    ProveedorInterlocutor,
    TelefonoInterlocutorProveedor,
    CorreoInterlocutorProveedor,
)

class ProveedorAdmin(admin.ModelAdmin):
    list_display = (
        'nombre',
        'ruc',
        'pais',
        'direccion',
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


class InterlocutorProveedorAdmin(admin.ModelAdmin):
    list_display = (
        'nombres',
        'apellidos',
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


class ProveedorInterlocutorAdmin(admin.ModelAdmin):
    list_display = (
        'proveedor',
        'interlocutor',
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


class TelefonoInterlocutorProveedorAdmin(admin.ModelAdmin):
    list_display = (
        'numero',
        'interlocutor',
        'fecha_baja',
        'estado',
        'created_by',
        'created_at',
        'updated_by',
        'updated_at',
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

class CorreoInterlocutorProveedorAdmin(admin.ModelAdmin):
    list_display = (
        'correo',
        'interlocutor',
        'fecha_baja',
        'estado',
        'created_by',
        'created_at',
        'updated_by',
        'updated_at',        
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

admin.site.register(Proveedor, ProveedorAdmin)
admin.site.register(InterlocutorProveedor, InterlocutorProveedorAdmin)
admin.site.register(ProveedorInterlocutor, ProveedorInterlocutorAdmin)
admin.site.register(TelefonoInterlocutorProveedor, TelefonoInterlocutorProveedorAdmin)
admin.site.register(CorreoInterlocutorProveedor, CorreoInterlocutorProveedorAdmin)