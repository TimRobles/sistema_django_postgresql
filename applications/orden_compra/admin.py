from django.contrib import admin
from .models import (
    OrdenCompra,
    OrdenCompraDetalle,
)

@admin.register(OrdenCompra)
class OrdenCompraAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'oferta_proveedor',
        'internacional_nacional',
        'incoterms',
        'numero_orden_compra',
        'oferta_proveedor',
        'orden_compra_anterior',
        'sociedad_id',
        'fecha_orden',
        'moneda',
        'descuento_global',
        'total_descuento',
        'total_anticipo',
        'total_gravada',
        'total_inafacta',
        'total_exonerada',
        'total_igv',
        'total_gratuita',
        'total_otros_cargos',
        'total_isc',
        'total',
        'slug',
        'archivo',
        'condiciones',
        'motivo_anulacion',
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


@admin.register(OrdenCompraDetalle)
class OrdenCompraDetalleAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'item',
        'content_type',
        'id_registro',
        'cantidad',
        'precio_unitario_sin_igv',
        'precio_unitario_con_igv',
        'precio_final_con_igv',
        'descuento',
        'sub_total',
        'igv',
        'total',
        'tipo_igv',
        'orden_compra',
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