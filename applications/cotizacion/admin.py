from django.contrib import admin
from .models import (
    PrecioListaMaterial,
)

@admin.register(PrecioListaMaterial)
class PrecioListaMaterialAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'content_type_producto',
        'id_registro_producto',
        'content_type_documento',
        'id_registro_documento',
        'precio_compra',
        'precio_lista',
        'precio_sin_igv',
        'moneda',
        'logistico',
        'margen_venta',
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