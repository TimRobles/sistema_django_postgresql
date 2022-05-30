from django.contrib import admin

from applications.clientes.forms import TipoInterlocutorClienteForm

from .models import (
    Cliente,
    TipoInterlocutorCliente,
    InterlocutorCliente,
    ClienteInterlocutor,
    TelefonoInterlocutorCliente,
    CorreoInterlocutorCliente,
    RepresentanteLegalCliente,
)

class ClienteAdmin(admin.ModelAdmin):
    list_display = (
        'razon_social',
        'tipo_documento',
        'numero_documento',
        'direccion_fiscal',
        'ubigeo',
        'distrito',
        'estado_sunat',
        )
    exclude = (
        'razon_social',
        'direccion_fiscal',
        'ubigeo',
        'distrito',
        'estado_sunat',
        )

    ordering = (
        'razon_social',
        )

    def save_model(self, request, obj, form, change):
        if obj.created_by == None:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


class TipoInterlocutorClienteAdmin(admin.ModelAdmin):
    list_display = (
        'nombre',
        'created_by',
        'created_at',
        'updated_by',
        'updated_at',
        )
    form = TipoInterlocutorClienteForm

    def save_model(self, request, obj, form, change):
        if obj.created_by == None:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


class InterlocutorClienteAdmin(admin.ModelAdmin):
    list_display = (
        'nombre_completo',
        'tipo_interlocutor',
        'tipo_documento',
        'numero_documento',
        )

    def save_model(self, request, obj, form, change):
        if obj.created_by == None:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


class ClienteInterlocutorAdmin(admin.ModelAdmin):
    list_display = (
        'cliente',
        'interlocutor',
        'tipo_interlocutor',
        'estado',
        )

    def save_model(self, request, obj, form, change):
        if obj.created_by == None:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


class TelefonoInterlocutorClienteAdmin(admin.ModelAdmin):
    list_display = (
        'numero',
        'interlocutor',
        'fecha_baja',
        'estado',
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

class CorreoInterlocutorClienteAdmin(admin.ModelAdmin):
    list_display = (
        'correo',
        'interlocutor',
        'fecha_baja',
        'estado',        
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


class RepresentanteLegalClienteAdmin(admin.ModelAdmin):
    list_display = (
        'cliente',
        'interlocutor',
        'tipo_representante_legal',
        'fecha_inicio',
        'fecha_baja',
        'estado',        
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

admin.site.register(Cliente, ClienteAdmin)
admin.site.register(TipoInterlocutorCliente, TipoInterlocutorClienteAdmin)
admin.site.register(InterlocutorCliente, InterlocutorClienteAdmin)
admin.site.register(ClienteInterlocutor, ClienteInterlocutorAdmin)
admin.site.register(TelefonoInterlocutorCliente, TelefonoInterlocutorClienteAdmin)
admin.site.register(CorreoInterlocutorCliente, CorreoInterlocutorClienteAdmin)
admin.site.register(RepresentanteLegalCliente, RepresentanteLegalClienteAdmin)
