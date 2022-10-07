from django.contrib import admin

from applications.logistica.models import Despacho, DespachoDetalle, DocumentoPrestamoMateriales, NotaSalida, NotaSalidaDetalle, SolicitudPrestamoMateriales, SolicitudPrestamoMaterialesDetalle

class SolicitudPrestamoMaterialesAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'numero_prestamo',
        'sociedad',
        'cliente',
        'interlocutor_cliente',
        'fecha_prestamo',
        'comentario',
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


class SolicitudPrestamoMaterialesDetalleAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'item',
        'content_type',
        'id_registro',
        'cantidad_prestamo',
        'observacion',
        'solicitud_prestamo_materiales',
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

class DocumentoPrestamoMaterialesAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'comentario',
        'documento',
        'solicitud_prestamo_materiales',
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

class NotaSalidaAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'confirmacion_venta',
        'solicitud_prestamo_materiales',
        'numero_salida',
        'observacion_adicional',
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

class NotaSalidaDetalleAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'item',
        'confirmacion_venta_detalle',
        'solicitud_prestamo_materiales_detalle',
        'sede',
        'almacen',
        'cantidad_salida',
        'nota_salida',
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

class DespachoAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'sociedad',
        'confirmacion_venta',
        'numero_despacho',
        'cliente',
        'observacion',
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

class DespachoDetalleAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'item',
        'confirmacion_venta_detalle',
        'cantidad_despachada',
        'despacho',
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

admin.site.register(SolicitudPrestamoMateriales, SolicitudPrestamoMaterialesAdmin)
admin.site.register(SolicitudPrestamoMaterialesDetalle, SolicitudPrestamoMaterialesDetalleAdmin)
admin.site.register(DocumentoPrestamoMateriales, DocumentoPrestamoMaterialesAdmin)
admin.site.register(NotaSalida, NotaSalidaAdmin)
admin.site.register(NotaSalidaDetalle, NotaSalidaDetalleAdmin)
admin.site.register(Despacho, DespachoAdmin)
admin.site.register(DespachoDetalle, DespachoDetalleAdmin)