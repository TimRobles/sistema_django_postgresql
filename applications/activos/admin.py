from django.contrib import admin
from applications.activos.models import ActivoBase


class ActivoBaseAdmin(admin.ModelAdmin):
    list_display = (
        'descripcion_venta',
        'descripcion_corta',
        'unidad',
        'peso',
        'sub_familia',
        'depreciacion',
        'producto_sunat',
        'estado',
        'traduccion',
        'partida',
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


admin.site.register(ActivoBase, ActivoBaseAdmin)
