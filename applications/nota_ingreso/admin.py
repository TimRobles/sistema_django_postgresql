from django.contrib import admin

from applications.nota_ingreso.models import NotaIngreso, NotaIngresoDetalle, NotaStockInicial, NotaStockInicialDetalle

# Register your models here.
@admin.register(NotaIngreso)
class NotaIngresoAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'nro_nota_ingreso',
        'recepcion_compra',
        'sociedad',
        'fecha_ingreso',
        'observaciones',
        'motivo_anulacion',
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


@admin.register(NotaIngresoDetalle)
class NotaIngresoDetalleAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'item',
        'content_type',
        'id_registro',
        'proveedor',
        'cantidad_conteo',
        'almacen',
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


@admin.register(NotaStockInicial)
class NotaStockInicialAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'nro_nota_stock_inicial',
        'sociedad',
        'fecha_ingreso',
        'observaciones',
        'motivo_anulacion',
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


@admin.register(NotaStockInicialDetalle)
class NotaStockInicialDetalleAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'item',
        'content_type',
        'id_registro',
        'cantidad_total',
        'nota_stock_inicial',
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
    