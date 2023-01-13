from django.contrib import admin
from .models import (
    MotivoTraslado,
    EnvioTrasladoProducto,
    EnvioTrasladoProductoDetalle,
    RecepcionTrasladoProducto,
    RecepcionTrasladoProductoDetalle,
    TraspasoStock,
    TraspasoStockDetalle,
    ValidarSerieEnvioTrasladoProductoDetalle,
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
        'envio_traslado_producto',
        'content_type',
        'id_registro',
        'producto',
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


@admin.register(RecepcionTrasladoProducto)
class RecepcionTrasladoProductoAdmin(admin.ModelAdmin):
    list_display = (
        'envio_traslado_producto',
        'numero_recepcion_traslado',
        'sede_destino',
        'fecha_recepcion',
        'responsable',
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


@admin.register(RecepcionTrasladoProductoDetalle)
class RecepcionTrasladoProductoDetalleAdmin(admin.ModelAdmin):
    list_display = (
        'item',
        'envio_traslado_producto_detalle',
        'content_type',
        'id_registro',
        'producto',
        'almacen_destino',
        'cantidad_recepcion',
        'unidad',
        'estado',
        'recepcion_traslado_producto',
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

@admin.register(TraspasoStock)
class TraspasoStockAdmin(admin.ModelAdmin):
    list_display = (
        'nro_traspaso',
        'encargado',
        'sede',
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

@admin.register(TraspasoStockDetalle)
class TraspasoStockDetalleAdmin(admin.ModelAdmin):
    list_display = (
        'item',
        'traspaso_stock',
        'content_type',
        'id_registro',
        'almacen',
        'tipo_stock_inicial',
        'cantidad',
        'tipo_stock_final',
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


@admin.register(ValidarSerieEnvioTrasladoProductoDetalle)
class ValidarSerieEnvioTrasladoProductoDetalleAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'envio_traslado_producto_detalle',
        'serie',
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
    