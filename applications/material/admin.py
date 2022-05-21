from django.contrib import admin
from .models import (
    Clase,
    Componente,
    Atributo,
    Familia,
    RelacionMaterialComponente,
    SubFamilia,
    Modelo,
    Marca,
    Material,
    Especificacion,
    Datasheet,
)

class ClaseAdmin(admin.ModelAdmin):
    list_display = (
        'nombre',
        'imagen',
        'descripcion',
        )

    def save_model(self, request, obj, form, change):
        if obj.created_by == None:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


class ComponenteAdmin(admin.ModelAdmin):
    list_display = (
        'nombre',
        )

    def save_model(self, request, obj, form, change):
        if obj.created_by == None:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


class AtributoAdmin(admin.ModelAdmin):
    list_display = (
        'nombre',
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


class MaterialAdmin(admin.ModelAdmin):
    list_display = (
        'descripcion_venta',
        'descripcion_corta',
        'unidad_base',
        'marca',
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
        'archivo',
        'material',
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