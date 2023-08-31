from django.contrib import admin
from .models import (
    CambioSociedadStock,
    CambioSociedadStockDetalle,
)

@admin.register(CambioSociedadStock)
class CambioSociedadStockAdmin(admin.ModelAdmin):
    list_display = (
        'nro_cambio',
        'encargado',
        'sede',
        'observaciones',
        'estado',
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

@admin.register(CambioSociedadStockDetalle)
class CambioSociedadStockDetalleAdmin(admin.ModelAdmin):
    list_display = (
        'item',
        'cambio_sociedad_stock',
        'content_type',
        'id_registro',
        'almacen',
        'tipo_stock',
        'cantidad',
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
