from django.contrib import admin
from .models import(
    EntradaTransformacionProductos,
    EstadoSerie,
    NotaControlCalidadStock,
    NotaControlCalidadStockDetalle,
    ReparacionMaterial,
    SalidaTransformacionProductos,
    Serie,
    FallaMaterial,
    HistorialEstadoSerie,
    SerieCalidad,
    SerieConsulta,
    TransformacionProductos,
    ValidarSerieEntradaTransformacionProductos,
    ValidarSerieSalidaTransformacionProductos,
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
        'producto',
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
    search_fields = (
        'serie__serie_base',
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
        'content_type',
        'id_registro',
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
        # 'nota_ingreso_detalle',
        'content_type',
        'id_registro',
        'cantidad_calidad',
        'inspeccion',
        'nota_control_calidad_stock',
        'created_at',
        'created_by',
        'updated_at',
        'updated_by',
    )
    search_fields = (
        'nota_control_calidad_stock',
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
    search_fields = (
        'serie_base',
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


@admin.register(TransformacionProductos)
class TransformacionProductosAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'sociedad',
        'fecha_transformacion',
        'responsable',
        'tipo_stock',
        'observacion',
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


@admin.register(EntradaTransformacionProductos)
class EntradaTransformacionProductosAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'item',
        'material',
        'sede',
        'almacen',
        'cantidad',
        'transformacion_productos',
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


@admin.register(SalidaTransformacionProductos)
class SalidaTransformacionProductosAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'item',
        'material',
        'sede',
        'almacen',
        'cantidad',
        'transformacion_productos',
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


@admin.register(ReparacionMaterial)
class ReparacionMaterialAdmin(admin.ModelAdmin):
    list_display = (
        'id',
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


# @admin.register(ValidarSerieEntradaTransformacionProductos)
# class ValidarSerieEntradaTransformacionProductosAdmin(admin.ModelAdmin):
#     list_display = (
#         'id',
#         'entrada_transformacion_productos',
#         'serie',
#         'created_at',
#         'created_by',
#         'updated_at',
#         'updated_by',
#     )

#     def save_model(self, request, obj, form, change):
#         if obj.created_by == None:
#             obj.created_by = request.user
#         obj.updated_by = request.user
#         super().save_model(request, obj, form, change)


# @admin.register(ValidarSerieSalidaTransformacionProductos)
# class ValidarSerieSalidaTransformacionProductosAdmin(admin.ModelAdmin):
#     list_display = (
#         'id',
#         'entrada_transformacion_productos',
#         'serie',
#         'created_at',
#         'created_by',
#         'updated_at',
#         'updated_by',
#     )

#     def save_model(self, request, obj, form, change):
#         if obj.created_by == None:
#             obj.created_by = request.user
#         obj.updated_by = request.user
#         super().save_model(request, obj, form, change)