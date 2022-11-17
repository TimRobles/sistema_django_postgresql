from django.contrib import admin
from applications.soporte_sistema.models import Excepcion

# Register your models here.
@admin.register(Excepcion)
class ExcepcionAdmin(admin.ModelAdmin):
    list_display = (
        'texto',
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
    