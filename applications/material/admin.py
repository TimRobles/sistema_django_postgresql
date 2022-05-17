from django.contrib import admin
from applications.material.forms import (
    ClaseForm,
    ComponenteForm,
    AtributoForm,
    FamiliaForm,    
    SubFamiliaForm,      
    )

from .models import (
    Clase,
    Componente,
    Atributo,
    Familia,
    SubFamilia,
    Modelo,
    Marca,
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

admin.site.register(Marca, MarcaAdmin)
admin.site.register(Modelo, ModeloAdmin)
admin.site.register(SubFamilia, SubFamiliaAdmin)
admin.site.register(Familia, FamiliaAdmin)
admin.site.register(Atributo, AtributoAdmin)
admin.site.register(Componente, ComponenteAdmin)
admin.site.register(Clase, ClaseAdmin)