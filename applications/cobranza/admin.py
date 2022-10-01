from django.contrib import admin
from .models import(
    Cuota,
    Deuda,
    Egreso,
    Ingreso,
    LineaCredito,
    Pago,
    Redondeo,
    Retiro,
    SolicitudCredito,
    SolicitudCreditoCuota,
)

@admin.register(LineaCredito)
class LineaCreditoAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'cliente',
        'monto',
        'moneda',
        'condiciones_pago',
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


@admin.register(SolicitudCredito)
class SolicitudCreditoAdmin(admin.ModelAdmin):
    list_display = (
        'cotizacion_venta',
        'total_cotizado',
        'total_credito',
        'interlocutor_solicita',
        'estado',
        'aprobado_por',
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


@admin.register(SolicitudCreditoCuota)
class SolicitudCreditoCuotaAdmin(admin.ModelAdmin):
    list_display = (
        'solicitud_credito',
        'monto',
        'dias_pago',
        'fecha_pago',
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

    
# @admin.register(Nota)
# class NotaAdmin(admin.ModelAdmin):
#     list_display = (
#         'id',
#         'nota_credito',
#         'monto',
#         'moneda',
#         'fecha',
#         'sociedad',
#         'cliente',
#         'created_at',
#         'created_by',
#         'updated_at',
#         'updated_by',
#     )

#     def save_model(self, request, obj, form, change):
#         if obj.created_by == None:
#             obj.created_by = request.user
#         obj.updated_by = request.user
#         super().save_model(request, obj, form, change)


@admin.register(Ingreso)
class IngresoAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'monto',
        'cuenta_bancaria',
        'fecha',
        'numero_operacion',
        'cuenta_origen',
        'comentario',
        'comision',
        'tipo_cambio',
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


@admin.register(Egreso)
class EgresoAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'monto',
        'cuenta_bancaria',
        'fecha',
        'numero_operacion',
        'cuenta_destino',
        'comentario',
        'comision',
        'tipo_cambio',
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


@admin.register(Deuda)
class DeudaAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'content_type',
        'id_registro',
        'monto',
        'moneda',
        'tipo_cambio',
        'fecha_deuda',
        'fecha_vencimiento',
        'sociedad',
        'cliente',
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


@admin.register(Cuota)
class CuotaAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'deuda',
        'fecha',
        'monto',
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


@admin.register(Redondeo)
class RedondeoAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'deuda',
        'fecha',
        'monto',
        'moneda',
        'tipo_cambio',
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


@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'deuda',
        'content_type',
        'id_registro',
        'monto',
        'tipo_cambio',
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


@admin.register(Retiro)
class RetiroAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'egreso',
        'content_type',
        'id_registro',
        'monto',
        'tipo_cambio',
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