from django.contrib import admin
from .models import (
    RequerimientoMaterial,
    RequerimientoMaterialDetalle,
)


class RequerimientoMaterialAdmin(admin.ModelAdmin):
    list_display = (
        'titulo',
        'fecha',
        'proveedor',
        'interlocutor_proveedor',
        'estado',
        'created_at',
        'updated_at',
        )

    def save_model(self, request, obj, form, change):
        if obj.created_by == None:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)

class RequerimientoMaterialDetalleAdmin(admin.ModelAdmin):
    list_display = (
        'item',
        'content_type',
        'id_registro',
        'cantidad',
        'requerimiento_material',
        )

    def save_model(self, request, obj, form, change):
        if obj.created_by == None:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


admin.site.register(RequerimientoMaterial, RequerimientoMaterialAdmin)
admin.site.register(RequerimientoMaterialDetalle, RequerimientoMaterialDetalleAdmin)
