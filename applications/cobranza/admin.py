from django.contrib import admin
from .models import(
    LineaCredito,
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