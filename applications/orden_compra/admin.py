from django.contrib import admin
from .models import (
    OrdenCompra,
    OrdenCompraDetalle,
)

@admin.register(OrdenCompra)
class OrdenCompraAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'internacional_nacional',
        'incoterms',
        'numero_orden_compra',
        )

    def save_model(self, request, obj, form, change):
        if obj.created_by == None:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(OrdenCompraDetalle)
class OrdenCompraDetalleAdmin(admin.ModelAdmin):
    list_display = (
        'item',
        )
        
    def save_model(self, request, obj, form, change):
        if obj.created_by == None:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)