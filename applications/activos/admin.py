from django.contrib import admin
from .models import (
    Activo,
    ActivoBase,
    ActivoUbicacion,
    ActivoSociedad,
    ArchivoComprobanteCompraActivo,
    ComprobanteCompraActivo,
    ComprobanteCompraActivoDetalle,
    FamiliaActivo,
    MarcaActivo,
    ModeloActivo,
    SubFamiliaActivo
)

class ActivoBaseAdmin(admin.ModelAdmin):
    list_display = (
        'descripcion_venta',
        'descripcion_corta',
        'unidad',
        'peso',
        'sub_familia',
        'depreciacion',
        'producto_sunat',
        'estado',
        'traduccion',
        'partida',
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


class FamiliaAdmin(admin.ModelAdmin):
    list_display = (
        'nombre',
        )

    def save_model(self, request, obj, form, change):
        if obj.created_by == None:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


class SubFamiliaAdmin(admin.ModelAdmin):
    list_display = (
        'nombre',
        'familia',
        )
    list_filter = [
        'familia',
        ]

    def save_model(self, request, obj, form, change):
        if obj.created_by == None:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


class ModeloAdmin(admin.ModelAdmin):
    list_display = (
        'nombre',
        )

    def save_model(self, request, obj, form, change):
        if obj.created_by == None:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


class MarcaAdmin(admin.ModelAdmin):
    list_display = (
        'nombre',
        )
    
    def save_model(self, request, obj, form, change):
        if obj.created_by == None:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


class ActivoAdmin(admin.ModelAdmin):
    list_display = (
        'numero_serie',
        'descripcion',
        'content_type',
        'id_registro',
        'activo_base',
        'marca',
        'modelo',
        'fecha_compra',
        'tiempo_garantia',
        'color',
        'informacion_adicional',
        'declarable',
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

class ActivoSociedadAdmin(admin.ModelAdmin):
    list_display = (
        'sociedad',
        'activo',
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

class ActivoUbicacionAdmin(admin.ModelAdmin):
    list_display = (
        'sede',
        'piso',
        'activo',
        'comentario',
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


class ComprobanteCompraActivoAdmin(admin.ModelAdmin):

    list_display = (
        'numero_comprobante',
        'internacional_nacional',
        'incoterms',
        'tipo_comprobante',
        'orden_compra',
        'sociedad',
        'fecha_comprobante',
        'moneda',
        'descuento_global',
        'total_descuento',
        'total_anticipo',
        'total_gravada',
        'total_inafecta',
        'total_exonerada',
        'total_igv',
        'total_gratuita',
        'total_otros_cargos',
        'total_icbper',
        'total',
        'archivo',
        'condiciones',
        'logistico',
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

class ComprobanteCompraActivoDetalleAdmin(admin.ModelAdmin):

    list_display = (
        'item',
        'descripcion_comprobante',
        'orden_compra_detalle',
        'activo',
        'cantidad',
        'precio_unitario_sin_igv',
        'precio_unitario_con_igv',
        'precio_final_con_igv',
        'descuento',
        'sub_total',
        'igv',
        'total',
        'tipo_igv',
        'comprobante_compra_activo',
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

class ArchivoComprobanteCompraActivoAdmin(admin.ModelAdmin):

    list_display = (
        'archivo',
        'comprobante_compra_activo',
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

admin.site.register(ComprobanteCompraActivo, ComprobanteCompraActivoAdmin)
admin.site.register(ComprobanteCompraActivoDetalle, ComprobanteCompraActivoDetalleAdmin)
admin.site.register(ArchivoComprobanteCompraActivo, ArchivoComprobanteCompraActivoAdmin)
admin.site.register(ActivoUbicacion, ActivoUbicacionAdmin)
admin.site.register(ActivoSociedad, ActivoSociedadAdmin)
admin.site.register(Activo, ActivoAdmin)
admin.site.register(FamiliaActivo, FamiliaAdmin)
admin.site.register(SubFamiliaActivo, SubFamiliaAdmin)
admin.site.register(MarcaActivo, MarcaAdmin)
admin.site.register(ModeloActivo, ModeloAdmin)
admin.site.register(ActivoBase, ActivoBaseAdmin)

