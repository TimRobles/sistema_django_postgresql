from django.contrib import admin
from .models import ArchivoOfertaProveedor, OfertaProveedorDetalle, OfertaProveedor

class OfertaProveedorAdmin(admin.ModelAdmin):
    '''Admin View for OfertaProveedor'''

    list_display = (
        'fecha',
        'internacional_nacional',
        'requerimiento_material',
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
        'slug',
        'condiciones',
        'estado',
        )

    def save_model(self, request, obj, form, change):
        if obj.created_by == None:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)

class OfertaProveedorDetalleAdmin(admin.ModelAdmin):

    list_display = (
        'proveedor_material',
        'cantidad',
        'precio_unitario_sin_igv',
        'precio_unitario_con_igv',
        'precio_final_con_igv',
        'descuento',
        'sub_total',
        'igv',
        'total',
        'tipo_igv',
        'oferta_proveedor',
        )

    def save_model(self, request, obj, form, change):
        if obj.created_by == None:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)

class ArchivoOfertaProveedorAdmin(admin.ModelAdmin):

    list_display = (
        'archivo',
        'oferta_proveedor',
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

admin.site.register(OfertaProveedor, OfertaProveedorAdmin)
admin.site.register(OfertaProveedorDetalle, OfertaProveedorDetalleAdmin)
admin.site.register(ArchivoOfertaProveedor, ArchivoOfertaProveedorAdmin)