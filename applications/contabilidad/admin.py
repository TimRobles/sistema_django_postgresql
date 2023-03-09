from django.contrib import admin
from .models import(
    FondoPensiones,
    ComisionFondoPensiones,
    DatosPlanilla,
    EsSalud,
    BoletaPago,
    ReciboBoletaPago
)


@admin.register(FondoPensiones)
class FondoPensionesAdmin(admin.ModelAdmin):
    list_display = (
        'nombre',
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


@admin.register(ComisionFondoPensiones)
class ComisionFondoPensionesAdmin(admin.ModelAdmin):
    list_display = (
        'fondo_pensiones',
        'fecha_vigencia',
        'aporte_obligatorio',
        'comision_flujo',
        'comision_flujo_mixta',
        'prima_seguro',
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


@admin.register(DatosPlanilla)
class DatosPlanillaAdmin(admin.ModelAdmin):
    list_display = (
        'fecha_inicio',
        'fecha_baja',
        'sueldo_bruto',
        'moneda',
        'movilidad',
        'usuario',
        'planilla',
        'suspension_cuarta',
        'fondo_pensiones',
        'tipo_comision',
        'asignacion_familiar',
        'area',
        'cargo',
        'sociedad',
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


@admin.register(EsSalud)
class EsSaludAdmin(admin.ModelAdmin):
    list_display = (
        'fecha_inicio',
        'porcentaje',
        'ley30334',
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


@admin.register(BoletaPago)
class BoletaPagoAdmin(admin.ModelAdmin):
    list_display = (
        'datos_planilla',
        'year',
        'month',
        'tipo',
        'haber_mensual',
        'lic_con_goce_haber',
        'dominical',
        'movilidad',
        'asig_familiar',
        'vacaciones',
        'gratificacion',
        'ley29351',
        'bonif_1mayo',
        'essalud',
        'aporte_obligatorio',
        'comision_porcentaje',
        'prima_seguro',
        'impuesto_quinta',
        'neto_recibido',
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


@admin.register(ReciboBoletaPago)
class ReciboBoletaPagoAdmin(admin.ModelAdmin):
    list_display = (
        'boleta_pago',
        'fecha_pagar',
        'tipo_pago',
        'monto',
        'redondeo',
        'monto_pagado',
        'voucher',
        'fecha_pago',
        'content_type',
        'id_registro',
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
      