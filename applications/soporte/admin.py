from django.contrib import admin
from django import forms

from applications.soporte.forms import(
    ProblemaForm,
)

from . models import(
    Problema,
    ProblemaDetalle,
)

@admin.register(Problema)
class ProblemaAdmin(admin.ModelAdmin):
    list_display = (
        'titulo',
        'descripcion',
        'estado',
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
        'imagen',
        'url',
        'problema',        
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
