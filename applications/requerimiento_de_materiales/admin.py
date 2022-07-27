from django.contrib import admin
from .models import (
    ListaRequerimientoMaterial,
    ListaRequerimientoMaterialDetalle,    
    RequerimientoMaterialProveedor,
    RequerimientoMaterialProveedorDetalle,
)

class ListaRequerimientoMaterialAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'titulo',
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

class ListaRequerimientoMaterialDetalleAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'lista_requerimiento_material',
        'item',
        'content_type',
        'id_registro',
        'cantidad',
        'lista_requerimiento_material',
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


class RequerimientoMaterialProveedorAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'lista_requerimiento',
        'titulo',
        'fecha',
        'proveedor',
        'interlocutor_proveedor',
        'slug',
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

class RequerimientoMaterialProveedorDetalleAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'item',
        'requerimiento_material',
        'id_requerimiento_material_detalle',
        'cantidad',
        'requerimiento_material',
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



admin.site.register(ListaRequerimientoMaterial, ListaRequerimientoMaterialAdmin)
admin.site.register(ListaRequerimientoMaterialDetalle, ListaRequerimientoMaterialDetalleAdmin)
admin.site.register(RequerimientoMaterialProveedor, RequerimientoMaterialProveedorAdmin)
admin.site.register(RequerimientoMaterialProveedorDetalle, RequerimientoMaterialProveedorDetalleAdmin)
