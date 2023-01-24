from django import forms
from applications.nota_ingreso.models import NotaIngreso
from applications.sociedad.models import Sociedad
from applications.variables import ESTADOS_NOTA_CALIDAD_STOCK
from django.contrib.auth import get_user_model
from bootstrap_modal_forms.forms import BSModalForm, BSModalModelForm
from .models import FallaMaterial, HistorialEstadoSerie, NotaControlCalidadStock, NotaControlCalidadStockDetalle, Serie, SerieCalidad

class NotaControlCalidadStockBuscarForm(forms.Form):
    sociedad = forms.ModelChoiceField(queryset=Sociedad.objects.filter(estado_sunat=1), required=False)
    estado = forms.ChoiceField(choices=((None, '-----------------'),) + ESTADOS_NOTA_CALIDAD_STOCK, required=False)
    usuario = forms.ModelChoiceField(queryset=get_user_model().objects, required=False)
    
    def __init__(self, *args, **kwargs):
        filtro_sociedad = kwargs.pop('filtro_sociedad')
        filtro_estado = kwargs.pop('filtro_estado')
        filtro_usuario = kwargs.pop('filtro_usuario')
        super(NotaControlCalidadStockBuscarForm, self).__init__(*args, **kwargs)
        self.fields['sociedad'].initial = filtro_sociedad
        self.fields['estado'].initial = filtro_estado
        self.fields['usuario'].initial = filtro_usuario
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class FallaMaterialForm(BSModalModelForm):
    class Meta:
        model = FallaMaterial
        fields=(
            'titulo',
            'comentario',
            'visible',
            )

    def __init__(self, *args, **kwargs):
        super(FallaMaterialForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        self.fields['visible'].widget.attrs['class'] = 'form-check-input'

class NotaControlCalidadStockForm(BSModalModelForm):
    class Meta:
        model = NotaControlCalidadStock
        fields=(
            'nota_ingreso',
            'comentario',
            )

    def __init__(self, *args, **kwargs):
        super(NotaControlCalidadStockForm, self).__init__(*args, **kwargs)
        self.fields['nota_ingreso'].queryset = NotaIngreso.objects.filter(estado=2)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class NotaControlCalidadStockAnularForm(BSModalModelForm):
    class Meta:
        model = NotaControlCalidadStock
        fields=(
            'motivo_anulacion',
            )

    def __init__(self, *args, **kwargs):
        super(NotaControlCalidadStockAnularForm, self).__init__(*args, **kwargs)          
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class NotaControlCalidadStockDetalleAgregarForm(BSModalModelForm):
    material = forms.ModelChoiceField(queryset=None)

    class Meta:
        model = NotaControlCalidadStockDetalle
        fields=(
            'material',
            'cantidad_calidad',
            'inspeccion',
            )
    
    def __init__(self, *args, **kwargs):
        lista_materiales = kwargs.pop('materiales')
        inspeccion = kwargs.pop('inspeccion')
        super(NotaControlCalidadStockDetalleAgregarForm, self).__init__(*args, **kwargs)
        self.fields['material'].queryset = lista_materiales
        if inspeccion:
            self.fields['inspeccion'].choices = inspeccion
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class NotaControlCalidadStockDetalleUpdateForm(BSModalModelForm):
    material = forms.CharField(required=False)
    class Meta:
        model = NotaControlCalidadStockDetalle
        fields=(
            'material',
            'cantidad_calidad',
            'inspeccion',
            )

    def __init__(self, *args, **kwargs):
        super(NotaControlCalidadStockDetalleUpdateForm, self).__init__(*args, **kwargs)
        self.fields['material'].initial = self.instance.material
        self.fields['material'].disabled = True
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        self.fields['material'].disabled = True

class NotaControlCalidadStockBuenoCreateForm(BSModalForm):
    serie_base = forms.CharField(max_length=200, required=True)
    observacion = forms.CharField(required=False, widget=forms.Textarea())

    class Meta:
        fields=(
            'serie_base',
            'observacion',
            )

    def __init__(self, *args, **kwargs):
        super(NotaControlCalidadStockBuenoCreateForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class NotaControlCalidadStockAgregarMaloCreateForm(BSModalForm):
    serie_base = forms.CharField(max_length=200, required=True)
    falla_material = forms.ModelChoiceField(queryset=None, required=True)
    observacion = forms.CharField(required=False, widget=forms.Textarea())
    class Meta:
        fields=(
            'serie_base',
            'falla_material',
            'observacion',
            )

    def __init__(self, *args, **kwargs):
        falla_material = kwargs.pop('falla_material')
        super(NotaControlCalidadStockAgregarMaloCreateForm, self).__init__(*args, **kwargs)
        self.fields['falla_material'].queryset = falla_material
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class NotaControlCalidadStockAgregarMaloSinSerieCreateForm(BSModalModelForm):
    serie_base = forms.CharField(max_length=200, required=True)
    falla_material = forms.ModelChoiceField(queryset=None, required=True)
    observacion = forms.CharField(required=False, widget=forms.Textarea())
    class Meta:
        model = HistorialEstadoSerie
        fields=(
            'serie_base',
            'falla_material',
            'observacion',
            )

    def __init__(self, *args, **kwargs):
        falla_material = kwargs.pop('falla_material')
        super(NotaControlCalidadStockAgregarMaloSinSerieCreateForm, self).__init__(*args, **kwargs)
        self.fields['falla_material'].queryset = falla_material
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class NotaControlCalidadStockBuenoUpdateForm(BSModalModelForm):
    class Meta:
        model = SerieCalidad
        fields=(
            'serie',
            'observacion',
            )

    def __init__(self, *args, **kwargs):
        super(NotaControlCalidadStockBuenoUpdateForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class NotaControlCalidadStockMaloUpdateForm(BSModalModelForm):
    class Meta:
        model = SerieCalidad
        fields=(
            'serie',
            'falla_material',
            'observacion',
            )

    def __init__(self, *args, **kwargs):
        falla_material = kwargs.pop('falla_material')
        super(NotaControlCalidadStockMaloUpdateForm, self).__init__(*args, **kwargs)
        self.fields['falla_material'].queryset = falla_material
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class NotaControlCalidadStockMaloSinSerieUpdateForm(BSModalModelForm):
    class Meta:
        model = SerieCalidad
        fields=(
            'serie',
            'falla_material',
            'observacion',
            )

    def __init__(self, *args, **kwargs):
        falla_material = kwargs.pop('falla_material')
        super(NotaControlCalidadStockMaloSinSerieUpdateForm, self).__init__(*args, **kwargs)
        self.fields['falla_material'].queryset = falla_material
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class SerieBuscarForm(BSModalForm):
    serie = forms.CharField(max_length=200, required=True)
    class Meta:
        fields=(
            'serie',
            )

    def __init__(self, *args, **kwargs):
        serie = kwargs.pop('serie')
        super(SerieBuscarForm, self).__init__(*args, **kwargs)
        self.fields['serie'].initial = serie
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

