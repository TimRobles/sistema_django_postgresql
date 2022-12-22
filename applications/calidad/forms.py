from django import forms
from applications.nota_ingreso.models import NotaIngreso
from bootstrap_modal_forms.forms import BSModalForm, BSModalModelForm
from .models import FallaMaterial, HistorialEstadoSerie, NotaControlCalidadStock, NotaControlCalidadStockDetalle, Serie, SerieCalidad


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
        super(NotaControlCalidadStockDetalleAgregarForm, self).__init__(*args, **kwargs)
        self.fields['material'].queryset = lista_materiales
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

class SerieAgregarBuenoForm(BSModalForm):
    serie_base = forms.CharField(max_length=200, required=True)
    observacion = forms.CharField(required=False, widget=forms.Textarea())

    class Meta:
        fields=(
            'serie_base',
            'observacion',
            )

    def __init__(self, *args, **kwargs):
        super(SerieAgregarBuenoForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class SerieAgregarMaloForm(BSModalForm):
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
        super(SerieAgregarMaloForm, self).__init__(*args, **kwargs)
        self.fields['falla_material'].queryset = falla_material
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class SerieAgregarMaloSinSerieForm(BSModalModelForm):
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
        super(SerieAgregarMaloSinSerieForm, self).__init__(*args, **kwargs)
        self.fields['falla_material'].queryset = falla_material
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class SerieActualizarBuenoForm(BSModalModelForm):
    class Meta:
        model = SerieCalidad
        fields=(
            'serie',
            'observacion',
            )

    def __init__(self, *args, **kwargs):
        super(SerieActualizarBuenoForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class SerieActualizarMaloForm(BSModalModelForm):
    class Meta:
        model = SerieCalidad
        fields=(
            'serie',
            'falla_material',
            'observacion',
            )

    def __init__(self, *args, **kwargs):
        falla_material = kwargs.pop('falla_material')
        super(SerieActualizarMaloForm, self).__init__(*args, **kwargs)
        self.fields['falla_material'].queryset = falla_material
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class SerieActualizarMaloSinSerieForm(BSModalModelForm):
    class Meta:
        model = SerieCalidad
        fields=(
            'serie',
            'falla_material',
            'observacion',
            )

    def __init__(self, *args, **kwargs):
        falla_material = kwargs.pop('falla_material')
        super(SerieActualizarMaloSinSerieForm, self).__init__(*args, **kwargs)
        self.fields['falla_material'].queryset = falla_material
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'