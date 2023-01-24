from django.contrib import admin

from applications.muestra.models import NotaIngresoMuestra, NotaIngresoMuestraDetalle

# Register your models here.
@admin.register(NotaIngresoMuestra)
class NotaIngresoMuestraAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'nro_nota_ingreso_muestra',
        'sociedad',
        'proveedor',
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


@admin.register(NotaIngresoMuestraDetalle)
class NotaIngresoMuestraDetalleAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'item',
        'content_type',
        'id_registro',
        'cantidad_total',
        'nota_ingreso_muestra',
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