from django.contrib import admin

from applications.nota.models import NotaCredito, NotaCreditoDetalle
# Register your models here.
@admin.register(NotaCredito)
class NotaCreditoAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'serie_comprobante',
        'numero_nota',
        'cliente',
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


@admin.register(NotaCreditoDetalle)
class NotaCreditoDetalleAdmin(admin.ModelAdmin):
    list_display = (
        'nota_credito',
        'item',
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