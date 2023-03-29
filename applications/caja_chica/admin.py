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


@admin.register(CajaChica)
class CajaChicaAdmin(admin.ModelAdmin):
    list_display = (
        'saldo_inicial',
        'moneda',
        'saldo_inicial_caja_chica',
        'year',
        'month',
        'ingresos',
        'egresos',
        'saldo_final',
        'usuario',
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

@admin.register(CajaChicaSalida)
class CajaChicaSalidaAdmin(admin.ModelAdmin):
    list_display = (
        'concepto',
        'fecha',
        'monto',
        'caja_chica',
        'usuario',
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

@admin.register(ReciboCajaChica)
class ReciboCajaChicaAdmin(admin.ModelAdmin):
    list_display = (
        'concepto',
        'fecha',
        'monto',
        'moneda',
        'redondeo',
        'monto_pagado',
        'fecha_pago',
        'caja_chica',
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

@admin.register(CajaChicaPrestamo)
class CajaChicaPrestamoAdmin(admin.ModelAdmin):
    list_display = (
        'fecha',
        'caja_origen',
        'caja_destino',
        'monto',
        'tipo',
        'devolucion',
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




admin.site.register(Requerimiento, RequerimientoAdmin)
admin.site.register(RequerimientoVueltoExtra, RequerimientoVueltoExtraAdmin)
admin.site.register(RequerimientoDocumento, RequerimientoDocumentoAdmin)
admin.site.register(RequerimientoDocumentoDetalle, RequerimientoDocumentoDetalleAdmin)