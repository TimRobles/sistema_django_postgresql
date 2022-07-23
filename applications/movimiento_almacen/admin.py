from django.contrib import admin
from .models import TipoMovimiento, MovimientosAlmacen

# Register your models here.
@admin.register(TipoMovimiento)
class TipoMovimientoAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'codigo',
        'descripcion',
        'created_by',
        'created_at',
        'updated_by',
        'updated_at',
        )

    def save_model(self, request, obj, form, change):
        if obj.created_by == None:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)
        

@admin.register(MovimientosAlmacen)
class MovimientosAlmacenAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'content_type_producto',
        'id_registro_producto',
        'cantidad',
        'tipo_movimiento',
        'signo_factor_multiplicador',
        'content_type_documento_proceso',
        'id_registro_documento_proceso',
        'almacen',
        'sociedad',
        'movimiento_anterior',
        'movimiento_reversion',
        'created_by',
        'created_at',
        'updated_by',
        'updated_at',
        )

    def save_model(self, request, obj, form, change):
        if obj.created_by == None:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)

