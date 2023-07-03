from django.contrib import admin
from django import forms
from applications.merchandising.forms import (
    ClaseMerchandisingForm,
    ComponenteMerchandisingForm,
    AtributoMerchandisingForm,
    FamiliaMerchandisingForm,
    SubFamiliaMerchandisingForm,
    IdiomaMerchandisingForm,      
    )

from .models import (
    AjusteInventarioMerchandising,
    AjusteInventarioMerchandisingDetalle,
    ClaseMerchandising,
    ComponenteMerchandising,
    AtributoMerchandising,
    FamiliaMerchandising,
    ImagenMerchandising,
    InventarioMerchandising,
    InventarioMerchandisingDetalle,
    RelacionMerchandisingComponente,
    SubFamiliaMerchandising,
    ModeloMerchandising,
    MarcaMerchandising,
    Merchandising,
    EspecificacionMerchandising,
    DatasheetMerchandising,
    VideoMerchandising,
    ProveedorMerchandising,
    EquivalenciaUnidadMerchandising,
    IdiomaMerchandising,
)

@admin.register(ClaseMerchandising)
class ClaseMerchandisingAdmin(admin.ModelAdmin):
    list_display = (
        'nombre',
        'imagen',
        'descripcion',
        )

    form = ClaseMerchandisingForm

    def save_model(self, request, obj, form, change):
        if obj.created_by == None:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(ComponenteMerchandising)
class ComponenteMerchandisingAdmin(admin.ModelAdmin):
    list_display = (
        'nombre',
        )

    form = ComponenteMerchandisingForm

    def save_model(self, request, obj, form, change):
        if obj.created_by == None:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(AtributoMerchandising)
class AtributoMerchandisingAdmin(admin.ModelAdmin):
    list_display = (
        'nombre',
        )

    form = AtributoMerchandisingForm

    def save_model(self, request, obj, form, change):
        if obj.created_by == None:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(FamiliaMerchandising)
class FamiliaMerchandisingAdmin(admin.ModelAdmin):
    list_display = (
        'nombre',
        )

    form = FamiliaMerchandisingForm

    def save_model(self, request, obj, form, change):
        if obj.created_by == None:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(SubFamiliaMerchandising)
class SubFamiliaMerchandisingAdmin(admin.ModelAdmin):
    list_display = (
        'nombre',
        'familia',
        )
    list_filter = [
        'familia',
        ]

    form = SubFamiliaMerchandisingForm

    def save_model(self, request, obj, form, change):
        if obj.created_by == None:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


class ModeloMerchandisingForm(forms.ModelForm):
    class Meta:
        model = ModeloMerchandising
        fields=(
            'nombre',
            )

    def __init__(self, *args, **kwargs):
        super(ModeloMerchandisingForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        filtro = ModeloMerchandising.objects.filter(nombre__unaccent__iexact = nombre)
        if nombre != self.instance.nombre:
            if len(filtro)>0:
                self.add_error('nombre', 'Ya existe un Modelo con este nombre')

        return nombre

class MarcaMerchandisingForm(forms.ModelForm):
    class Meta:
        model = MarcaMerchandising
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
        filtro = MarcaMerchandising.objects.filter(nombre__unaccent__iexact = nombre)
        if nombre != self.instance.nombre:
            if len(filtro)>0:
                self.add_error('nombre', 'Ya existe un Marca con este nombre')

    def __init__(self, *args, **kwargs):
        super(MarcaMerchandisingForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        self.fields['modelos'].widget.attrs['class'] = 'nobull'


@admin.register(ModeloMerchandising)
class ModeloMerchandisingAdmin(admin.ModelAdmin):
    list_display = (
        'nombre',
        )

    form = ModeloMerchandisingForm

    def save_model(self, request, obj, form, change):
        if obj.created_by == None:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(MarcaMerchandising)
class MarcaMerchandisingAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'nombre',
        )
    
    form = MarcaMerchandisingForm

    def save_model(self, request, obj, form, change):
        if obj.created_by == None:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


class MerchandisingForm(forms.ModelForm):
    class Meta:
        model = Merchandising
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


@admin.register(Merchandising)
class MerchandisingAdmin(admin.ModelAdmin):
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
        'created_at',
        'created_by',
        'updated_at',
        'updated_by',
        )
    form = MerchandisingForm

    def save_model(self, request, obj, form, change):
        if obj.created_by == None:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(RelacionMerchandisingComponente)
class RelacionMerchandisingComponenteAdmin(admin.ModelAdmin):
    list_display = (
        'merchandising',
        'componentemerchandising',
        'cantidad',
        )

    def save_model(self, request, obj, form, change):
        if obj.created_by == None:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(EspecificacionMerchandising)
class EspecificacionMerchandisingAdmin(admin.ModelAdmin):
    list_display = (
        'orden',
        'atributomerchandising',
        'valor',
        'merchandising',
        )

    def save_model(self, request, obj, form, change):
        if obj.created_by == None:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(DatasheetMerchandising)
class DatasheetMerchandisingAdmin(admin.ModelAdmin):
    list_display = (
        'descripcion',
        'merchandising',
        'archivo',
        )

    def save_model(self, request, obj, form, change):
        if obj.created_by == None:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(ImagenMerchandising)
class ImagenMerchandisingAdmin(admin.ModelAdmin):
    list_display = (
        'descripcion',
        'imagen',
        'merchandising',
        'estado_alta_baja',
        )

    def save_model(self, request, obj, form, change):
        if obj.created_by == None:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(VideoMerchandising)
class VideoMerchandisingAdmin(admin.ModelAdmin):
    list_display = (
        'descripcion',
        'url',
        'merchandising',
        )

    def save_model(self, request, obj, form, change):
        if obj.created_by == None:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(ProveedorMerchandising)
class ProveedorMerchandisingAdmin(admin.ModelAdmin):
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


@admin.register(EquivalenciaUnidadMerchandising)
class EquivalenciaUnidadMerchandisingAdmin(admin.ModelAdmin):
    list_display = (
        'merchandising',
        'cantidad_base',
        'nueva_unidad',
        'cantidad_nueva_unidad',
        )

    def save_model(self, request, obj, form, change):
        if obj.created_by == None:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(IdiomaMerchandising)
class IdiomaMerchandisingAdmin(admin.ModelAdmin):
    list_display = (
        'idioma',
        'merchandising',
        'traduccion',
        )

    def save_model(self, request, obj, form, change):
        if obj.created_by == None:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)
     
######################################################---INVENTARIO MERCHANDISING---######################################################

@admin.register(InventarioMerchandising)
class InventarioMerchandisingAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'sociedad',
        'sede',
        'fecha_inventario',
        'hora_inventario',
        'responsable',
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


@admin.register(InventarioMerchandisingDetalle)
class InventarioMerchandisingDetalleAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'item',
        'merchandising',
        'almacen',
        'tipo_stock',
        'cantidad',
        'inventario_merchandising',
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


@admin.register(AjusteInventarioMerchandising)
class AjusteInventarioMerchandisingAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'sociedad',
        'sede',
        'fecha_ajuste_inventario',
        'hora_ajuste_inventario',
        'responsable',
        'observacion',
        'estado',
        'inventario_merchandising',
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


@admin.register(AjusteInventarioMerchandisingDetalle)
class AjusteInventarioMerchandisingDetalleAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'item',
        'merchandising',
        'almacen',
        'tipo_stock',
        'cantidad_stock',
        'cantidad_contada',
        'ajuste_inventario_merchandising',
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


