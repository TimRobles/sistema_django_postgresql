from django.contrib import admin

from .models import(
    CondicionesGarantia,
    IngresoReclamoGarantia,
    IngresoReclamoGarantiaDetalle,
    ControlCalidadReclamoGarantia,
    ControlCalidadReclamoGarantiaDetalle,
    SalidaReclamoGarantia,
    SerieIngresoReclamoGarantiaDetalle,
    SerieReclamoHistorial,
)

@admin.register(IngresoReclamoGarantia)
class IngresoReclamoGarantiaAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'nro_ingreso_reclamo_garantia',
        'cliente',
        'cliente_interlocutor',
        'sociedad',
        'fecha_ingreso',
        'observacion',
        'encargado',
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


@admin.register(IngresoReclamoGarantiaDetalle)
class IngresoReclamoGarantiaDetalleAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'item',
        'content_type',
        'id_registro',
        'cantidad',
        'ingreso_reclamo_garantia',
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


@admin.register(SerieIngresoReclamoGarantiaDetalle)
class SerieIngresoReclamoGarantiaDetalleAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'ingreso_reclamo_garantia_detalle',
        'serie',
        'content_type_documento',
        'id_registro_documento',
        'comentario',
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


@admin.register(ControlCalidadReclamoGarantia)
class ControlCalidadReclamoGarantiaAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'ingreso_reclamo_garantia',
        'observacion',
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


@admin.register(ControlCalidadReclamoGarantiaDetalle)
class ControlCalidadReclamoGarantiaDetalleAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'control_calidad_reclamo_garantia',
        'serie_ingreso_reclamo_garantia_detalle',
        'serie_cambio',
        'tipo_analisis',
        'comentario',
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


@admin.register(SerieReclamoHistorial)
class SerieReclamoHistorialAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'serie_ingreso_reclamo_garantia_detalle',
        'historia_estado_serie',
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


@admin.register(SalidaReclamoGarantia)
class SalidaReclamoGarantiaAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'control_calidad_reclamo_garantia',
        'fecha_salida',
        'observacion',
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


@admin.register(CondicionesGarantia)
class CondicionesGarantiaAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'condicion',
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