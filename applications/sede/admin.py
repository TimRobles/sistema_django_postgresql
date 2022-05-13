from django.contrib import admin
from .models import (
    Sede,
)

class SedeAdmin(admin.ModelAdmin):
    list_display = (
        'nombre',
        'usuario_responsable',
        'direccion',
        'ubigeo',
        'distrito',
        'estado',
        )
    exclude = (
        'ubigeo',
        'estado',
        'distrito',
        )

    def save_model(self, request, obj, form, change):
        if obj.created_by == None:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)

admin.site.register(Sede, SedeAdmin)