from django.contrib import admin
from .models import Transportista

@admin.register(Transportista)
class TransportistaAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'tipo_documento',
        'numero_documento',
        'razon_social',
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