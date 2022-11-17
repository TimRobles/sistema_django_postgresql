from django.contrib import admin
from .models import (
    MotivoTraslado,
    EnvioTrasladoProducto,
    EnvioTrasladoProductoDetalle,
)

@admin.register(MotivoTraslado)
class MotivoTrasladoAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'motivo_traslado',
        'visible',
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

@admin.register(EnvioTrasladoProducto)
class EnvioTrasladoProductoAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'numero_envio_traslado',
        'sociedad',
        'sede_origen',
        'direccion_destino',
        'fecha_traslado',
        'responsable',
        'motivo_traslado',
        'observaciones',
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


@admin.register(EnvioTrasladoProductoDetalle)
class EnvioTrasladoProductoDetalleAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'envio_traslado_almacen',
        'content_type',
        'id_registro',
        'almacen_origen',
        'cantidad_envio',
        'unidad',
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
