from django.contrib import admin

from applications.comprobante_compra.models import ArchivoComprobanteCompraPI, ComprobanteCompraCI, ComprobanteCompraCIDetalle, ComprobanteCompraPI, ComprobanteCompraPIDetalle

# Register your models here.
@admin.register(ComprobanteCompraPI)
class ComprobanteCompraPIAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'internacional_nacional',
        'incoterms',
        'numero_comprobante_compra',
        'orden_compra',
        'sociedad',
        'fecha_comprobante',
        'moneda',
        'total',
        'slug',
        'condiciones',
        'estado',
        'motivo_anulacion',
        'logistico',
        'created_by',
        'created_at',
        'updated_by',
        'updated_at',
        )

    def save_model(self, request, obj, form, change):
        if obj.created_by == None:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)
        

@admin.register(ComprobanteCompraPIDetalle)
class ComprobanteCompraPIDetalleAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'item',
        'orden_compra_detalle',
        'cantidad',
        'precio_final_con_igv',
        'total',
        'tipo_igv',
        'comprobante_compra',
        'created_by',
        'created_at',
        'updated_by',
        'updated_at',
        )

    def save_model(self, request, obj, form, change):
        if obj.created_by == None:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(ArchivoComprobanteCompraPI)
class ArchivoComprobanteCompraPIAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'archivo',
        'comprobante_compra',
        'created_by',
        'created_at',
        'updated_by',
        'updated_at',
        )

    def save_model(self, request, obj, form, change):
        if obj.created_by == None:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(ComprobanteCompraCI)
class ComprobanteCompraCIAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'internacional_nacional',
        'incoterms',
        'numero_comprobante_compra',
        'comprobante_compra_PI',
        'sociedad',
        'fecha_comprobante',
        'moneda',
        'total',
        'slug',
        'archivo',
        'condiciones',
        'estado',
        'motivo_anulacion',
        'created_by',
        'created_at',
        'updated_by',
        'updated_at',
        )

    def save_model(self, request, obj, form, change):
        if obj.created_by == None:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(ComprobanteCompraCIDetalle)
class ComprobanteCompraCIDetalleAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'item',
        'content_type',
        'id_registro',
        'cantidad',
        'precio_final_con_igv',
        'total',
        'tipo_igv',
        'comprobante_compra',
        'created_by',
        'created_at',
        'updated_by',
        'updated_at',
        )

    def save_model(self, request, obj, form, change):
        if obj.created_by == None:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)