from django.contrib import admin
from applications.activos.models import ActivoBase, ArchivoAsignacionActivo, AsignacionActivo, AsignacionDetalleActivo, FamiliaActivo, MarcaActivo, ModeloActivo, SubFamiliaActivo


class ActivoBaseAdmin(admin.ModelAdmin):
    list_display = (
        'descripcion_venta',
        'descripcion_corta',
        'unidad',
        'peso',
        'sub_familia',
        'depreciacion',
        'producto_sunat',
        'estado',
        'traduccion',
        'partida',
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


class FamiliaAdmin(admin.ModelAdmin):
    list_display = (
        'nombre',
        )

    def save_model(self, request, obj, form, change):
        if obj.created_by == None:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


class SubFamiliaAdmin(admin.ModelAdmin):
    list_display = (
        'nombre',
        'familia',
        )
    list_filter = [
        'familia',
        ]

    def save_model(self, request, obj, form, change):
        if obj.created_by == None:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


class ModeloAdmin(admin.ModelAdmin):
    list_display = (
        'nombre',
        )

    def save_model(self, request, obj, form, change):
        if obj.created_by == None:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


class MarcaAdmin(admin.ModelAdmin):
    list_display = (
        'nombre',
        )
    
    def save_model(self, request, obj, form, change):
        if obj.created_by == None:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


class AsignacionActivoAdmin(admin.ModelAdmin):
    list_display = (
        'titulo',
        'colaborador',
        'fecha_asignacion',
        'observacion',
        'fecha_entrega',
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


class AsignacionDetalleActivoAdmin(admin.ModelAdmin):
    list_display = (
        'activo',
        'asignacion',
    )

    def save_model(self, request, obj, form, change):
        if obj.created_by == None:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


class ArchivoAsignacionActivoAdmin(admin.ModelAdmin):
    list_display = (
        'archivo',
        'asignacion',
        'comentario',
    )

    def save_model(self, request, obj, form, change):
        if obj.created_by == None:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)



admin.site.register(FamiliaActivo, FamiliaAdmin)
admin.site.register(SubFamiliaActivo, SubFamiliaAdmin)
admin.site.register(MarcaActivo, MarcaAdmin)
admin.site.register(ModeloActivo, ModeloAdmin)
admin.site.register(ActivoBase, ActivoBaseAdmin)
admin.site.register(AsignacionActivo, AsignacionActivoAdmin)
admin.site.register(AsignacionDetalleActivo, AsignacionDetalleActivoAdmin)
admin.site.register(ArchivoAsignacionActivo, ArchivoAsignacionActivoAdmin)
