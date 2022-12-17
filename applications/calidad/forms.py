from django import forms
from applications.nota_ingreso.models import NotaIngreso
from bootstrap_modal_forms.forms import BSModalForm, BSModalModelForm
from .models import FallaMaterial, HistorialEstadoSerie, NotaControlCalidadStock, NotaControlCalidadStockDetalle, Serie


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

class SerieAgregarBuenoForm(BSModalModelForm):
    serie_base = forms.CharField(required=True)
    class Meta:
        model = HistorialEstadoSerie
        fields=(
            'serie_base',
            'observacion',
            )

    def clean(self):
        cleaned_data = super().clean()
        serie_base = cleaned_data.get('serie_base')
        filtro = Serie.objects.filter(serie_base__unaccent__iexact = serie_base, content_type = self.content_type, id_registro = self.id_registro)
        if serie_base != self.instance.serie_id:
            if len(filtro)>0:
                self.add_error('serie_base', 'Esta serie ya se encuentre registrada')

    def __init__(self, *args, **kwargs):
        self.content_type = kwargs.pop('content_type')
        self.id_registro = kwargs.pop('id_registro')
        super(SerieAgregarBuenoForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class SerieAgregarMaloForm(BSModalModelForm):
    serie_base = forms.CharField(required=True)
    falla_material = forms.ModelChoiceField(queryset=None)
    class Meta:
        model = HistorialEstadoSerie
        fields=(
            'serie_base',
            'falla_material',
            'observacion',
            )

    def clean(self):
        cleaned_data = super().clean()
        serie_base = cleaned_data.get('serie_base')
        filtro = Serie.objects.filter(serie_base__unaccent__iexact = serie_base, content_type = self.content_type, id_registro = self.id_registro)
        if serie_base != self.instance.serie_id:
            if len(filtro)>0:
                self.add_error('serie_base', 'Esta serie ya se encuentre registrada')

    def __init__(self, *args, **kwargs):
        self.content_type = kwargs.pop('content_type')
        self.id_registro = kwargs.pop('id_registro')
        lista_fallas = kwargs.pop('fallas')
        super(SerieAgregarMaloForm, self).__init__(*args, **kwargs)
        self.fields['falla_material'].queryset = lista_fallas
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class SerieAgregarMaloSinSerieForm(BSModalModelForm):
    serie_base = forms.CharField(required=True)
    falla_material = forms.ModelChoiceField(queryset=None)
    class Meta:
        model = HistorialEstadoSerie
        fields=(
            'serie_base',
            'falla_material',
            'observacion',
            )

    def clean(self):
        cleaned_data = super().clean()
        serie_base = cleaned_data.get('serie_base')
        filtro = Serie.objects.filter(serie_base__unaccent__iexact = serie_base, content_type = self.content_type, id_registro = self.id_registro)
        if serie_base != self.instance.serie_id:
            if len(filtro)>0:
                self.add_error('serie_base', 'Esta serie ya se encuentre registrada')

    def __init__(self, *args, **kwargs):
        self.content_type = kwargs.pop('content_type')
        self.id_registro = kwargs.pop('id_registro')
        lista_fallas = kwargs.pop('fallas')
        nro_serie = kwargs.pop('nro_serie')
        super(SerieAgregarMaloSinSerieForm, self).__init__(*args, **kwargs)
        self.fields['falla_material'].queryset = lista_fallas
        self.fields['serie_base'].initial = nro_serie
        self.fields['serie_base'].disabled = True
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class SerieActualizarBuenoForm(BSModalModelForm):
    serie_base = forms.CharField(required=True)
    class Meta:
        model = HistorialEstadoSerie
        fields=(
            'serie_base',
            'observacion',
            )

    def clean(self):
        cleaned_data = super().clean()
        serie_base = cleaned_data.get('serie_base')
        filtro = Serie.objects.filter(serie_base__unaccent__iexact = serie_base, content_type = self.content_type, id_registro = self.id_registro)
        if serie_base != self.instance.serie_base:
            if len(filtro)>0:
                self.add_error('serie_base', 'Esta serie ya se encuentre registrada')

    def __init__(self, *args, **kwargs):
        self.content_type = kwargs.pop('content_type')
        self.id_registro = kwargs.pop('id_registro')
        super(SerieActualizarBuenoForm, self).__init__(*args, **kwargs)
        self.fields['observacion'].initial = self.instance.observacion
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class SerieActualizarMaloForm(BSModalModelForm):
    serie_base = forms.CharField(required=True)
    falla_material = forms.ModelChoiceField(queryset=None)
    class Meta:
        model = HistorialEstadoSerie
        fields=(
            'serie_base',
            'falla_material',
            'observacion',
            )

    def clean(self):
        cleaned_data = super().clean()
        serie_base = cleaned_data.get('serie_base')
        filtro = Serie.objects.filter(serie_base__unaccent__iexact = serie_base, content_type = self.content_type, id_registro = self.id_registro)
        if serie_base != self.instance.serie_base:
            if len(filtro)>0:
                self.add_error('serie_base', 'Esta serie ya se encuentre registrada')

    def __init__(self, *args, **kwargs):
        self.content_type = kwargs.pop('content_type')
        self.id_registro = kwargs.pop('id_registro')
        lista_fallas = kwargs.pop('fallas')
        super(SerieActualizarMaloForm, self).__init__(*args, **kwargs)
        self.fields['falla_material'].queryset = lista_fallas
        self.fields['falla_material'].initial = self.instance.falla
        self.fields['observacion'].initial = self.instance.observacion
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class SerieActualizarMaloSinSerieForm(BSModalModelForm):
    serie_base = forms.CharField(required=True)
    falla_material = forms.ModelChoiceField(queryset=None)
    class Meta:
        model = HistorialEstadoSerie
        fields=(
            'serie_base',
            'falla_material',
            'observacion',
            )

    def clean(self):
        cleaned_data = super().clean()
        serie_base = cleaned_data.get('serie_base')
        filtro = Serie.objects.filter(serie_base__unaccent__iexact = serie_base, content_type = self.content_type, id_registro = self.id_registro)
        if serie_base != self.instance.serie_base:
            if len(filtro)>0:
                self.add_error('serie_base', 'Esta serie ya se encuentre registrada')

    def __init__(self, *args, **kwargs):
        self.content_type = kwargs.pop('content_type')
        self.id_registro = kwargs.pop('id_registro')
        lista_fallas = kwargs.pop('fallas')
        super(SerieActualizarMaloSinSerieForm, self).__init__(*args, **kwargs)
        self.fields['falla_material'].queryset = lista_fallas
        self.fields['falla_material'].initial = self.instance.falla
        self.fields['observacion'].initial = self.instance.observacion
        self.fields['serie_base'].disabled = True
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'