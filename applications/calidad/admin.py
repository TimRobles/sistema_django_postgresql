from django.contrib import admin
from .models import(
    EstadoSerie,
    NotaControlCalidadStock,
    NotaControlCalidadStockDetalle,
    Serie,
    FallaMaterial,
    HistorialEstadoSerie,
    SerieCalidad,
    SerieConsulta,
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
class SerieAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'serie_base',
        'content_type',
        'id_registro',
        'sociedad',
        'created_at',
        'created_by',
        'updated_at',
        'updated_by',
    )
    search_fields = (
        'serie_base',
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

@admin.register(NotaControlCalidadStock)
class NotaControlCalidadStockAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'nro_nota_calidad',
        'nota_ingreso',
        'motivo_anulacion',
        'comentario',
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

@admin.register(NotaControlCalidadStockDetalle)
class NotaControlCalidadStockDetalleAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'item',
        'nota_ingreso_detalle',
        'cantidad_calidad',
        'inspeccion',
        'nota_control_calidad_stock',
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


@admin.register(SerieConsulta)
class SerieConsultaAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'serie_base',
        'content_type',
        'id_registro',
        'sociedad',
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
    

@admin.register(SerieCalidad)
class SerieCalidadAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'serie',
        'content_type',
        'id_registro',
        'nota_control_calidad_stock_detalle',
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