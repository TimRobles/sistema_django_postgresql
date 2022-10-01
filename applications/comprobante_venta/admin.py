from django.contrib import admin
from .models import(
    FacturaVenta,
    FacturaVentaDetalle,
    BoletaVenta,
    BoletaVentaDetalle,
)

@admin.register(FacturaVenta)
class FacturaVentaAdmin(admin.ModelAdmin):
    list_display = (
        'sociedad',
        'serie_comprobante',
        'numero_factura',
        'cliente',
        'cliente_interlocutor',
        'fecha_emision',
        'fecha_vencimiento',
        'moneda',
        'tipo_cambio',
        'tipo_venta',
        'condiciones_pago',
        'descuento_global',
        'total_descuento',
        'total_anticipo',
        'total_gravada',
        'total_inafecta',
        'total_exonerada',
        'total_gratuita',
        'total_otros_cargos',
        'total',
        'percepcion_tipo',
        'percepcion_base_imponible',
        'total_percepcion',
        'total_incluido_percepcion',
        'retencion_tipo',
        'retencion_base_imponible',
        'total_retencion',
        'total_impuestos_bolsas',
        'detraccion',
        'url',
        'observaciones',
        'estado',
        'motivo_anulacion',
        'confirmacion',
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


@admin.register(FacturaVentaDetalle)
class FacturaVentaDetalleAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'item',
        'content_type',
        'id_registro',
        'unidad',
        'codigo_interno',
        'descripcion_documento',
        'cantidad',
        'precio_unitario_sin_igv',
        'precio_unitario_con_igv',
        'precio_final_con_igv',
        'descuento',
        'sub_total',
        'tipo_igv',
        'igv',
        'total',
        'anticipo_regularizacion',
        'anticipo_documento_serie',
        'anticipo_documento_numero',
        'codigo_producto_sunat',
        'tipo_de_isc',
        'isc',
        'factura_venta',
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


@admin.register(BoletaVenta)
class BoletaVentaAdmin(admin.ModelAdmin):
    list_display = (
        'sociedad',
        'serie_comprobante',
        'numero_boleta',
        'cliente',
        'tipo_documento',
        'numero_documento',
        'cliente_interlocutor',
        'fecha_emision',
        'fecha_vencimiento',
        'moneda',
        'tipo_cambio',
        'tipo_venta',
        'condiciones_pago',
        'descuento_global',
        'total_descuento',
        'total_anticipo',
        'total_gravada',
        'total_inafecta',
        'total_exonerada',
        'total_gratuita',
        'total_otros_cargos',
        'total',
        'percepcion_tipo',
        'percepcion_base_imponible',
        'total_percepcion',
        'total_incluido_percepcion',
        'retencion_tipo',
        'retencion_base_imponible',
        'total_retencion',
        'total_impuestos_bolsas',
        'detraccion',
        'url',
        'observaciones',
        'estado',
        'motivo_anulacion',
        'confirmacion',
        'slug',
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


@admin.register(BoletaVentaDetalle)
class BoletaVentaDetalleAdmin(admin.ModelAdmin):
    list_display = (
        'item',
        'content_type',
        'id_registro',
        'unidad',
        'codigo_interno',
        'descripcion_documento',
        'cantidad',
        'precio_unitario_sin_igv',
        'precio_unitario_con_igv',
        'precio_final_con_igv',
        'descuento',
        'sub_total',
        'tipo_igv',
        'igv',
        'total',
        'anticipo_regularizacion',
        'anticipo_documento_serie',
        'anticipo_documento_numero',
        'codigo_producto_sunat',
        'tipo_de_isc',
        'isc',
        'descuento_sin_igv',
        'descuento_con_igv',
        'boleta_venta',
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