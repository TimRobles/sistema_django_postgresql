from django.contrib import admin
from .models import(
    Cheque,
    ChequeFisico,
    ChequeVueltoExtra,
    FondoPensiones,
    ComisionFondoPensiones,
    DatosPlanilla,
    EsSalud,
    BoletaPago,
    ReciboBoletaPago,
    TipoServicio,
    Institucion,
    MedioPago,
    Servicio,
    ReciboServicio,
    Telecredito,
)


@admin.register(FondoPensiones)
class FondoPensionesAdmin(admin.ModelAdmin):
    list_display = (
        'id',
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
        'id',
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
        'id',
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
        'id',
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
        'id',
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
        'compra_vacaciones',
        'gratificacion',
        'ley29351',
        'cts',
        'bonif_1mayo',
        'essalud',
        'aporte_obligatorio',
        'comision',
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
        'id',
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


@admin.register(TipoServicio)
class TipoServicioAdmin(admin.ModelAdmin):
    list_display = (
        'id',
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


@admin.register(Institucion)
class InstitucionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'nombre',
        'url',
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


@admin.register(MedioPago)
class MedioPagoAdmin(admin.ModelAdmin):
    list_display = (
        'id',
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


@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'institucion',
        'tipo_servicio',
        'numero_referencia',
        'titular_servicio',
        'direccion',
        'alias',
        'estado',
        'sociedad',
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


@admin.register(ReciboServicio)
class ReciboServicioAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'servicio',
        'foto',
        'fecha_emision',
        'fecha_vencimiento',
        'monto',
        'moneda',
        'mora',
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

@admin.register(Telecredito)
class TelecreditoAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'concepto',
        'moneda',
        'banco',
        'numero',
        'monto',
        'fecha_emision',
        'fecha_cobro',
        'foto',
        'monto_usado',
        'usuario',
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

@admin.register(Cheque)
class ChequeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'concepto',
        'moneda',
        'monto_cheque',
        'monto_usado',
        'redondeo',
        'vuelto',
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

@admin.register(ChequeFisico)
class ChequeFisicoAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'banco',
        'numero',
        'responsable',
        'monto',
        'fecha_emision',
        'fecha_cobro',
        'foto',
        'sociedad',
        'estado',
        'cheque',
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
    
@admin.register(ChequeVueltoExtra)
class ChequeVueltoExtraAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'vuelto_original',
        'vuelto_extra',
        'moneda',
        'tipo_cambio',
        'cheque',
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