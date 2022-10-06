from django.contrib import admin
from .models import (
    ConfirmacionVentaCuota,
    ConfirmacionVentaDetalle,
    CotizacionDescuentoGlobal,
    CotizacionOtrosCargos,
    CotizacionSociedad,
    PrecioListaMaterial,
    CotizacionVenta,
    CotizacionVentaDetalle,
    CotizacionObservacion,
    ConfirmacionOrdenCompra,
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
        'tiempo_entrega',
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


@admin.register(ConfirmacionOrdenCompra)
class ConfirmacionOrdenCompraAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'numero_orden',
        'fecha_orden',
        'documento',
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
        'tipo_cambio',
        'observacion',
        'condiciones_pago',
        'tipo_venta',
        'total',
        'estado',
        'motivo_anulacion',
        'sunat_transaction',
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
        'item',
        'content_type',
        'id_registro',
        'cantidad_confirmada',
        'precio_unitario_sin_igv',
        'precio_unitario_con_igv',
        'precio_final_con_igv',
        'descuento',
        'sub_total',
        'igv',
        'total',
        'tipo_igv',
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


@admin.register(ConfirmacionVentaCuota)
class ConfirmacionVentaCuotaAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'confirmacion_venta',
        'monto',
        'dias_pago',
        'fecha_pago',
        'dias_calculo',
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


@admin.register(CotizacionDescuentoGlobal)
class CotizacionDescuentoGlobal(admin.ModelAdmin):
    list_display = (
        'id',
        'cotizacion_venta',
        'sociedad',
        'descuento_global',
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


@admin.register(CotizacionObservacion)
class CotizacionObservacion(admin.ModelAdmin):
    list_display = (
        'id',
        'cotizacion_venta',
        'sociedad',
        'observacion',
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


@admin.register(CotizacionOtrosCargos)
class CotizacionOtrosCargos(admin.ModelAdmin):
    list_display = (
        'id',
        'cotizacion_venta',
        'sociedad',
        'otros_cargos',
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