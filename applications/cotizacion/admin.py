from django.contrib import admin
from .models import (
    PrecioListaMaterial,
    CotizacionVenta,
    CotizacionVentaDetalle,
    CotizacionOrdenCompra,
    CotizacionTerminosCondiciones,
    ReservaVenta,
    ReservaVentaDetalle,
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
        'sociedad',
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


@admin.register(CotizacionOrdenCompra)
class CotizacionOrdenCompraAdmin(admin.ModelAdmin):
    list_display = (
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


@admin.register(ReservaVenta)
class ReservaVentaAdmin(admin.ModelAdmin):
    list_display = (
        'cotizacion_venta',
        'sociedad',
        'numero_cotizacion',
        'cliente',
        'cliente_interlocutor',
        'fecha_cotizacion',
        'fecha_confirmacion',
        'tipo_cambio',
        'observaciones_adicionales',
        'condiciones_pago',
        'tipo_venta',
        'descuento_global',
        'total',
        'estado',
        'motivo_anualacion',
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


@admin.register(ReservaVentaDetalle)
class ReservaVentaDetalleAdmin(admin.ModelAdmin):
    list_display = (
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
        'tipo_igv',
        'reserva_venta',
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


        'created_at',
        'created_by',
        'updated_at',
        'updated_by',


@admin.register(ConfirmacionVenta)
class ConfirmacionVentaAdmin(admin.ModelAdmin):
    list_display = (
        'cotizacion_venta',
        'reserva_venta',
        'sociedad',
        'numero_cotizacion',
        'cliente',
        'fecha_cotizacion',
        'fecha_validez',
        'tipo_cambio',
        'observaciones_adicionales',
        'condiciones_pago',
        'tipo_venta',
        'descuento_global',
        'total',
        'estado',
        'motivo_anualacion',
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




