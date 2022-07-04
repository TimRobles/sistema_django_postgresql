from django.contrib import admin
from applications.material.forms import (
    ClaseForm,
    ComponenteForm,
    AtributoForm,
    FamiliaForm,
    IdiomaMaterialForm,    
    SubFamiliaForm,
    MarcaForm,
    ModeloForm,
    IdiomaForm,      
    IdiomaMaterialForm,      
    )

from .models import (
    Clase,
    Componente,
    Atributo,
    Familia,
    ImagenMaterial,
    RelacionMaterialComponente,
    SubFamilia,
    Modelo,
    Marca,
    Material,
    Especificacion,
    Datasheet,
    VideoMaterial,
    ProveedorMaterial,
    EquivalenciaUnidad,
    Idioma,
    IdiomaMaterial,
)

class ClaseAdmin(admin.ModelAdmin):
    list_display = (
        'nombre',
        'imagen',
        'descripcion',
        )

    form = ClaseForm

    def save_model(self, request, obj, form, change):
        if obj.created_by == None:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


class ComponenteAdmin(admin.ModelAdmin):
    list_display = (
        'nombre',
        )

    form = ComponenteForm

    def save_model(self, request, obj, form, change):
        if obj.created_by == None:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


class AtributoAdmin(admin.ModelAdmin):
    list_display = (
        'nombre',
        )

    form = AtributoForm

    def save_model(self, request, obj, form, change):
        if obj.created_by == None:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


class FamiliaAdmin(admin.ModelAdmin):
    list_display = (
        'nombre',
        )

    form = FamiliaForm

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

    form = SubFamiliaForm

    def save_model(self, request, obj, form, change):
        if obj.created_by == None:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


class ModeloAdmin(admin.ModelAdmin):
    list_display = (
        'nombre',
        )

    form = ModeloForm

    def save_model(self, request, obj, form, change):
        if obj.created_by == None:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


class MarcaAdmin(admin.ModelAdmin):
    list_display = (
        'nombre',
        )
    
    form = MarcaForm

    def save_model(self, request, obj, form, change):
        if obj.created_by == None:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


class MaterialAdmin(admin.ModelAdmin):
    list_display = (
        'descripcion_venta',
        'descripcion_corta',
        'unidad_base',
        'marca',
        'estado_alta_baja',
        )

    def save_model(self, request, obj, form, change):
        if obj.created_by == None:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


class RelacionMaterialComponenteAdmin(admin.ModelAdmin):
    list_display = (
        'material',
        'componentematerial',
        'cantidad',
        )

    def save_model(self, request, obj, form, change):
        if obj.created_by == None:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


class EspecificacionAdmin(admin.ModelAdmin):
    list_display = (
        'orden',
        'atributomaterial',
        'valor',
        'material',
        )

    def save_model(self, request, obj, form, change):
        if obj.created_by == None:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


class DatasheetAdmin(admin.ModelAdmin):
    list_display = (
        'descripcion',
        'material',
        'archivo',
        )

    def save_model(self, request, obj, form, change):
        if obj.created_by == None:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


class ImagenMaterialAdmin(admin.ModelAdmin):
    list_display = (
        'descripcion',
        'imagen',
        'material',
        'estado_alta_baja',
        )

    def save_model(self, request, obj, form, change):
        if obj.created_by == None:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


class VideoMaterialAdmin(admin.ModelAdmin):
    list_display = (
        'descripcion',
        'url',
        'material',
        )

    def save_model(self, request, obj, form, change):
        if obj.created_by == None:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


class ProveedorMaterialAdmin(admin.ModelAdmin):
    list_display = (
        'content_type',
        'id_registro',
        'proveedor',
        'name',
        'brand',
        'description',
        )

    def save_model(self, request, obj, form, change):
        if obj.created_by == None:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


class EquivalenciaUnidadAdmin(admin.ModelAdmin):
    list_display = (
        'material',
        'cantidad_base',
        'nueva_unidad',
        'cantidad_nueva_unidad',
        )

    def save_model(self, request, obj, form, change):
        if obj.created_by == None:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


class IdiomaAdmin(admin.ModelAdmin):
    list_display = (
        'nombre',
        'created_at',
        'created_by',
        )
    form = IdiomaForm

    def save_model(self, request, obj, form, change):
        if obj.created_by == None:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)

class IdiomaMaterialAdmin(admin.ModelAdmin):
    list_display = (
        'idioma',
        'material',
        'traduccion',
        )

    def save_model(self, request, obj, form, change):
        if obj.created_by == None:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)
     


admin.site.register(Marca, MarcaAdmin)
admin.site.register(Modelo, ModeloAdmin)
admin.site.register(SubFamilia, SubFamiliaAdmin)
admin.site.register(Familia, FamiliaAdmin)
admin.site.register(Atributo, AtributoAdmin)
admin.site.register(Componente, ComponenteAdmin)
admin.site.register(Clase, ClaseAdmin)

admin.site.register(Material, MaterialAdmin)
admin.site.register(RelacionMaterialComponente,RelacionMaterialComponenteAdmin)
admin.site.register(Especificacion,EspecificacionAdmin)
admin.site.register(Datasheet,DatasheetAdmin)
admin.site.register(ImagenMaterial,ImagenMaterialAdmin)
admin.site.register(VideoMaterial,VideoMaterialAdmin)
admin.site.register(ProveedorMaterial,ProveedorMaterialAdmin)
admin.site.register(EquivalenciaUnidad,EquivalenciaUnidadAdmin)
admin.site.register(Idioma,IdiomaAdmin)
admin.site.register(IdiomaMaterial,IdiomaMaterialAdmin)