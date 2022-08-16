from dataclasses import fields
from django import forms
from .models import Activo, ActivoBase, ActivoUbicacion, ActivoSociedad, ComprobanteCompraActivo, MarcaActivo, ModeloActivo
from bootstrap_modal_forms.forms import BSModalModelForm


class ActivoBaseForm(BSModalModelForm):
    class Meta:
        model = ActivoBase
        fields = (
            'descripcion_venta',
            'descripcion_corta',
            'unidad',
            'peso',
            'sub_familia',
            'depreciacion',
            'vida_util',
            'producto_sunat',
            'traduccion',
            'partida',
            )

    def __init__(self, *args, **kwargs):
        super(ActivoBaseForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class ModeloActivoForm(BSModalModelForm):
    class Meta:
        model = ModeloActivo
        fields=(
            'nombre',
            )

    def __init__(self, *args, **kwargs):
        super(ModeloActivoForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        filtro = ModeloActivo.objects.filter(nombre__unaccent__iexact = nombre)
        if nombre != self.instance.nombre:
            if len(filtro)>0:
                self.add_error('nombre', 'Ya existe un Modelo con este nombre')

        return nombre

class MarcaActivoForm(BSModalModelForm):
    class Meta:
        model = MarcaActivo
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
        filtro = MarcaActivo.objects.filter(nombre__unaccent__iexact = nombre)
        if nombre != self.instance.nombre:
            if len(filtro)>0:
                self.add_error('nombre', 'Ya existe un Marca con este nombre')

    def __init__(self, *args, **kwargs):
        super(MarcaActivoForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        self.fields['modelos'].widget.attrs['class'] = 'nobull'

class ActivoForm(BSModalModelForm):
    class Meta:
        model = Activo
        fields = (
            'numero_serie',
            'descripcion',
            'activo_base',
            'marca',
            'modelo',
            'fecha_compra',
            'tiempo_garantia',
            'color',
            'informacion_adicional',
            'declarable',
            )

        widgets = {
            'fecha_compra' : forms.DateInput(
                attrs ={
                    'type':'date',
                    },
                format = '%Y-%m-%d',
                ),
            }

    def __init__(self, *args, **kwargs):
        super(ActivoForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        self.fields['declarable'].widget.attrs['class'] = 'form-check-input'

class ActivoSociedadForm(BSModalModelForm):
    class Meta:
        model = ActivoSociedad
        fields=(
            'sociedad',
            )

    def __init__(self, *args, **kwargs):
        super(ActivoSociedadForm, self).__init__(*args, **kwargs)   
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class ActivoUbicacionForm(BSModalModelForm):
    class Meta:
        model = ActivoUbicacion
        fields=(
            'sede',
            'piso',
            'comentario',
            )

    def __init__(self, *args, **kwargs):
        super(ActivoUbicacionForm, self).__init__(*args, **kwargs)   
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class ComprobanteCompraActivoForm(BSModalModelForm):
    class Meta:
        model = ComprobanteCompraActivo
        fields = (
            'numero_comprobante',
            'tipo_comprobante',
            'fecha_comprobante',
            'internacional_nacional',
            'sociedad',
            'incoterms',
            'orden_compra',
            'moneda',
            'condiciones',
            'logistico',
            )

        widgets = {
            'fecha_comprobante' : forms.DateInput(
                attrs ={
                    'type':'date',
                    },
                format = '%Y-%m-%d',
                ),
            }

    def __init__(self, *args, **kwargs):
        super(ComprobanteCompraActivoForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'