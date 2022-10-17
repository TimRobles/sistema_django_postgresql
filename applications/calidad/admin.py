from django.contrib import admin
from .models import(
    EstadoSerie,
    Serie,
    FallaMaterial,
    HistorialEstadoSerie,
)

@admin.register(EstadoSerie)
class EstadoSerieAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'numero_estado',
        'descripcion',
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

@admin.register(Serie)
class Admin(admin.ModelAdmin):
    list_display = (
        'id',
        'serie_base',
        'content_type',
        'id_registro',
        'estado_serie',
        'sociedad',
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

@admin.register(FallaMaterial)
class FallaMaterialAdmin(admin.ModelAdmin):
    list_display = (
        'id',        
        'sub_familia',
        'titulo',
        'comentario',
        'visible',
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

@admin.register(HistorialEstadoSerie)
class HistorialEstadoSerieAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'serie',
        'estado_serie',
        'falla_material',
        'observacion',
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
