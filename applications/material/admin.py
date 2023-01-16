from django.contrib import admin
from django import forms
from applications.material.forms import (
    ClaseForm,
    ComponenteForm,
    AtributoForm,
    FamiliaForm,
    SubFamiliaForm,
    IdiomaForm,      
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


class ModeloForm(forms.ModelForm):
    class Meta:
        model = Modelo
        fields=(
            'nombre',
            )

    def __init__(self, *args, **kwargs):
        super(ModeloForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        filtro = Modelo.objects.filter(nombre__unaccent__iexact = nombre)
        if nombre != self.instance.nombre:
            if len(filtro)>0:
                self.add_error('nombre', 'Ya existe un Modelo con este nombre')

        return nombre

class MarcaForm(forms.ModelForm):
    class Meta:
        model = Marca
        fields=(
            'nombre',
            'modelos',
            )

        widgets = {
            'modelos': forms.CheckboxSelectMultiple(),
        }

    def clean(self):
        cleaned_data = super().clean()
        nombre = cleaned_data.get('nombre')
        filtro = Marca.objects.filter(nombre__unaccent__iexact = nombre)
        if nombre != self.instance.nombre:
            if len(filtro)>0:
                self.add_error('nombre', 'Ya existe un Marca con este nombre')

    def __init__(self, *args, **kwargs):
        super(MarcaForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        self.fields['modelos'].widget.attrs['class'] = 'nobull'

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
        'id',
        'nombre',
        )
    
    form = MarcaForm

    def save_model(self, request, obj, form, change):
        if obj.created_by == None:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = (
            'descripcion_venta',
            'descripcion_corta',
            'unidad_base',
            'peso_unidad_base',
            'marca',
            'modelo',
            'subfamilia',
            'clase',
            'control_serie',
            'control_lote',
            'control_calidad',
            'estado_alta_baja',
            'mostrar',
            'traduccion',
            'partida',
            'uso_funcion',
            'compuesto_por',
            'es_componente',
            'atributo',
            'componente',
            'id_producto_temporal',
            'id_multiplay',
            )

class MaterialAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'descripcion_venta',
        'descripcion_corta',
        'unidad_base',
        'marca',
        'control_serie',
        'control_lote',
        'control_calidad',
        'estado_alta_baja',
        'id_multiplay',
        )
    form = MaterialForm

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
        'id',
        'content_type',
        'id_registro',
        'proveedor',
        'name',
        'brand',
        'description',
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