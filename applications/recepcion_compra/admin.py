from django.contrib import admin

from applications.recepcion_compra.models import ArchivoRecepcionCompra, DocumentoReclamo, DocumentoReclamoDetalle, FotoRecepcionCompra, RecepcionCompra

# Register your models here.
@admin.register(RecepcionCompra)
class RecepcionCompraAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'numero_comprobante_compra',
        'content_type',
        'id_registro',
        'fecha_recepcion',
        'usuario_recepcion',
        'nro_bultos',
        'observaciones',
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

        
@admin.register(ArchivoRecepcionCompra)
class ArchivoRecepcionCompraAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'archivo',
        'recepcion_compra',
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

        
@admin.register(FotoRecepcionCompra)
class FotoRecepcionCompraAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'foto',
        'recepcion_compra',
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


@admin.register(DocumentoReclamo)
class DocumentoReclamoAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'recepcion_compra',
        'fecha_documento',
        'usuario',
        'observaciones',
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


@admin.register(DocumentoReclamoDetalle)
class DocumentoReclamoDetalleAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'documento_reclamo',
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