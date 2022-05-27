from django.contrib import admin
from applications.almacenes.forms import (
    AlmacenForm,
)
from .models import (
    Almacen,
)

class AlmacenAdmin(admin.ModelAdmin):
    list_display = (
        'nombre',
        'sede',
        'estado_alta_baja',
        )

    form = AlmacenForm

    def save_model(self, request, obj, form, change):
        if obj.created_by == None:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


admin.site.register(Almacen,AlmacenAdmin)