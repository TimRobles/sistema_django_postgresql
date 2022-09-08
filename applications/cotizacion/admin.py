from django.contrib import admin
from .models import (
    ConfirmacionVentaDetalle,
    CotizacionSociedad,
    PrecioListaMaterial,
    CotizacionVenta,
    CotizacionVentaDetalle,
    CotizacionOrdenCompra,
    CotizacionTerminosCondiciones,
    ConfirmacionVenta,
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


@admin.register(CotizacionVenta)
class CotizacionVentaAdmin(admin.ModelAdmin):
    list_display = ( 
        'id',
        'numero_cotizacion',
        'cliente',
        'cliente_interlocutor',
        'fecha_cotizacion',
        'fecha_validez',
        'tipo_cambio',
        'observaciones_adicionales',
        'condiciones_pago',
        'tipo_venta',
        'descuento_global',
        'total',
        'estado',
        'motivo_anulacion',
        'slug',
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


@admin.register(CotizacionVentaDetalle)
class CotizacionVentaDetalleAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'cotizacion_venta',
        'content_type',
        'id_registro',
        'item',
        'cantidad',
        'precio_unitario_sin_igv',
        'precio_unitario_con_igv',
        'precio_final_con_igv',
        'descuento',
        'sub_total',
        'igv',
        'total',
        'tipo_igv',
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


@admin.register(CotizacionOrdenCompra)
class CotizacionOrdenCompraAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'numero_orden',
        'fecha_orden',
        'documento',
        'cotizacion_venta',
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


@admin.register(CotizacionTerminosCondiciones)
class CotizacionTerminosCondicionesAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'condicion',
        'condicion_visible',
        'orden',
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


@admin.register(ConfirmacionVenta)
class ConfirmacionVentaAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'cotizacion_venta',
        'sociedad',
        'fecha_confirmacion',
        'tipo_cambio',
        'estado',
        'motivo_anulacion',
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


@admin.register(ConfirmacionVentaDetalle)
class ConfirmacionVentaDetalleAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'cantidad_confirmada',
        'item',
        'content_type',
        'id_registro',
        'confirmacion_venta',
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


@admin.register(CotizacionSociedad)
class CotizacionSociedadAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'cotizacion_venta_detalle',
        'sociedad',
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