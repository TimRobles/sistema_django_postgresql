from django.contrib import admin
from .models import(
    Guia,
    GuiaDetalle,
)

@admin.register(Guia)
class GuiaAdmin(admin.ModelAdmin):
    list_display = (
        'sociedad',
        'serie_comprobante',
        'cliente',
        'cliente_interlocutor',
        'fecha_emision',
        'fecha_traslado',
        'sede',
        'transportista',
        'observaciones',
        'numero_bultos',
        'direccion_partida',
        'direccion_destino',
        'ubigeo_partida',
        'ubigeo_destino',
        'url',
        'estado',
        'motivo_anulación',
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


@admin.register(GuiaDetalle)
class GuiaDetalleAdmin(admin.ModelAdmin):
    '''Admin View for GuiaDetalle'''

    list_display = (
        'item',
        'content_type',
        'id_registro',
        'cantidad',
        'peso',
        'guia',
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

