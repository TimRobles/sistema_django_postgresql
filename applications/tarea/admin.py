from django.contrib import admin
from .models import(
    TipoTarea,
    Tarea,
)

@admin.register(TipoTarea)
class TipoTareaAdmin(admin.ModelAdmin):
    list_display = (
        'nombre',
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

@admin.register(Tarea)
class TareaAdmin(admin.ModelAdmin):
    list_display = (
        'fecha_inicio',
        'fecha_limite',
        'fecha_cierre',
        'tipo_tarea',
        'descripcion',
        'area',
        'prioridad',
        'content_type',
        'id_registro',
        'estado',
    )

    def save_model(self, request, obj, form, change):
        if obj.created_by == None:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)
