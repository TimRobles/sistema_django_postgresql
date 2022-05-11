from django.contrib import admin

from .models import (
    DatosContratoPlanilla,
    DatosContratoHonorarios,
)

class DatosContratoPlanillaAdmin(admin.ModelAdmin):
    list_display = (
        'usuario',
        'fecha_alta',
        'sueldo_bruto',
        'movilidad',
        'asignacion_familiar',
        'archivo_contrato',
        'cargo',
        'estado_alta_baja',
        )
    exclude = (
        'hora_ingreso',
        'hora_salida',
        )

    def save_model(self, request, obj, form, change):
        if obj.created_by == None:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


class DatosContratoHonorariosAdmin(admin.ModelAdmin):
    list_display = (
        'usuario',
        'fecha_alta',
        'sueldo',
        'suspension_cuarta',
        'archivo_suspension_cuarta',
        'archivo_contrato',
        'cargo',
        'estado_alta_baja',
        )

    def save_model(self, request, obj, form, change):
        if obj.created_by == None:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


admin.site.register(DatosContratoPlanilla, DatosContratoPlanillaAdmin)
admin.site.register(DatosContratoHonorarios, DatosContratoHonorariosAdmin)

