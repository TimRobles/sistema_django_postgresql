from django.contrib import admin

from .models import *

# Register your models here.

class RequerimientoAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'fecha',
        'monto',
        'moneda',
        'tipo_cambio',
        'concepto',
        'motivo_rechazo',
        'dato_rechazado',
        'monto_final',
        'concepto_final',
        'fecha_entrega',
        'monto_usado',
        'redondeo',
        'vuelto',
        'rechazo_rendicion',
        'content_type',
        'id_registro',
        'usuario_pedido',
        'usuario',
        'estado',

        'created_at',
        'created_by',
        'updated_at',
        'updated_by',
        )


class RequerimientoVueltoExtraAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'vuelto_original',
        'vuelto_extra',
        'moneda',
        'tipo_cambio',
        'requerimiento',

        'created_at',
        'created_by',
        'updated_at',
        'updated_by',
        )


class RequerimientoDocumentoAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'fecha',
        'tipo',
        'numero',
        'establecimiento',
        'moneda',
        'total_documento',
        'tipo_cambio',
        'total_requerimiento',
        'voucher',
        'sociedad',
        'requerimiento',

        'created_at',
        'created_by',
        'updated_at',
        'updated_by',
        )


class RequerimientoDocumentoDetalleAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'item',
        'producto',
        'cantidad',
        'unidad',
        'precio_unitario',
        'foto',
        'documento_requerimiento',

        'created_at',
        'created_by',
        'updated_at',
        'updated_by',
        )
    
admin.site.register(Requerimiento, RequerimientoAdmin)
admin.site.register(RequerimientoVueltoExtra, RequerimientoVueltoExtraAdmin)
admin.site.register(RequerimientoDocumento, RequerimientoDocumentoAdmin)
admin.site.register(RequerimientoDocumentoDetalle, RequerimientoDocumentoDetalleAdmin)