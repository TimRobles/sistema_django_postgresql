from django.contrib import admin

from .models import(
    IngresoReclamoGarantia,
    IngresoReclamoGarantiaDetalle,
    ControlCalidadReclamoGarantia,
    ControlCalidadReclamoGarantiaDetalle,
    SalidaReclamoGarantia,
    SalidaReclamoGarantiaDetalle,
)

@admin.register(IngresoReclamoGarantia)
class IngresoReclamoGarantiaAdmin(admin.ModelAdmin):
    
    list_display = (
        'nro_ingreso_garantia',
        'cliente',
        'cliente_interlocutor',
        'sociedad',
        'fecha_ingreso',
        'observacion',
        'encargado',
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
        'item',
        'content_type',
        'id_registro',
        'serie',
        'cantidad',
        'precio_venta',
        'ingreso_garantia',
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
        'nro_calidad_garantia',
        'ingreso_garantia',
        'cliente',
        'cliente_interlocutor',
        'sociedad',
        'fecha_control',
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

@admin.register(ControlCalidadReclamoGarantiaDetalle)
class ControlCalidadReclamoGarantiaDetalleAdmin(admin.ModelAdmin):
    list_display = (
        'item',
        'content_type',
        'id_registro',
        'serie',
        'cantidad',
        'precio_venta',
        'calidad_garantia',
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
    '''Admin View for SalidaReclamoGarantia'''

    list_display = (
        'nro_salida_garantia',
        'control_garantia',
        'cliente',
        'cliente_interlocutor',
        'sociedad',
        'fecha_salida',
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


@admin.register(SalidaReclamoGarantiaDetalle)
class SalidaReclamoGarantiaDetalleAdmin(admin.ModelAdmin):

    list_display = (
        'item',
        'content_type',
        'id_registro',
        'serie',
        'cantidad',
        'precio_venta',
        'salida_garantia',
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
