from django.contrib import admin
from django import forms

from applications.soporte.forms import(
    ProblemaForm,
    SolicitudForm,
)

from . models import(
    Problema,
    ProblemaDetalle,
    Solicitud,
    SolicitudDetalle,
)

@admin.register(Problema)
class ProblemaAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'titulo',
        'descripcion',
        'estado',
        'comentario',
        'created_at',
        'created_by',
        'updated_at',
        'updated_by',
    )
    form = ProblemaForm

    def save_model(self, request, obj, form, change):
        if obj.created_by == None:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(ProblemaDetalle)
class ProblemaDetalleAdmin(admin.ModelAdmin):
    list_display = (
        'id',        
        'problema',        
        'imagen',
        'url',
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


@admin.register(Solicitud)
class SolicitudAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'titulo',
        'descripcion',
        'estado',
        'motivo_rechazo',  
        'comentario',  
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

@admin.register(SolicitudDetalle)
class SolicitudDetalleAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'solicitud',
        'imagen',
        'url',
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
