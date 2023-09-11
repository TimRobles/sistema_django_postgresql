from django import forms
from django.contrib.auth import get_user_model
from applications.sede.models import Sede
from bootstrap_modal_forms.forms import BSModalForm, BSModalModelForm
from applications.datos_globales.models import Moneda
from applications.variables import INCOTERMS, INTERNACIONAL_NACIONAL
from .models import CambioSociedadStock, CambioSociedadStockDetalle 
from applications.material.models import Material


class CambioSociedadStockForm(BSModalModelForm):
    class Meta:
        model = CambioSociedadStock
        fields = (
            'encargado',
            'sociedad_inicial',
            'sociedad_final',
            'sede',
            'observaciones',
            )
    
    def clean_sociedad_inicial(self):
        sociedad_inicial = self.cleaned_data.get('sociedad_inicial')
        sede = self.fields['sede']
        sede.queryset = sociedad_inicial.Sede_sociedad.filter(estado=1)
        
        return sociedad_inicial
        
    def __init__(self, *args, **kwargs):
        super(CambioSociedadStockForm, self).__init__(*args, **kwargs)   
        try:
            self.fields['sede'].queryset = kwargs['instance'].sociedad_inicial.Sede_sociedad.filter(estado=1)
        except:
            self.fields['sede'].queryset = Sede.objects.none()
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class CambioSociedadStockDetalleForm(BSModalModelForm):
    material = forms.ModelChoiceField(queryset=Material.objects.all())
    stock_disponible = forms.CharField(required=False)
    class Meta:
        model = CambioSociedadStockDetalle
        fields = (
            'material',
            'almacen',
            'tipo_stock',
            'stock_disponible',
            'cantidad',
            )
        
    def __init__(self, *args, **kwargs):
        cambio_sociedad_stock = kwargs.pop('cambio_sociedad_stock')
        super(CambioSociedadStockDetalleForm, self).__init__(*args, **kwargs)   
        self.fields['almacen'].queryset = cambio_sociedad_stock.sede.Almacen_sede.filter(estado_alta_baja=1)
        self.fields['stock_disponible'].disabled = True
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class CambioSociedadStockDetalleActualizarForm(BSModalModelForm):
    stock_disponible = forms.CharField(required=False)
    class Meta:
        model = CambioSociedadStockDetalle
        fields = (
            'almacen',
            'tipo_stock',
            'stock_disponible',
            'cantidad',
            )
        
    def __init__(self, *args, **kwargs):
        cambio_sociedad_stock = kwargs.pop('cambio_sociedad_stock')
        super(CambioSociedadStockDetalleActualizarForm, self).__init__(*args, **kwargs)   
        self.fields['almacen'].queryset = cambio_sociedad_stock.sede.Almacen_sede.filter(estado_alta_baja=1)
        self.fields['stock_disponible'].disabled = True
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class CambioSociedadStockDetalleSeriesForm(BSModalModelForm):
    cantidad_registrada = forms.DecimalField(label='Cantidad Registrada', max_digits=22, decimal_places=10, required=False)
    serie = forms.CharField(required=False)
    class Meta:
        model = CambioSociedadStockDetalle
        fields=(
            'serie',
            'cantidad',
            'cantidad_registrada',
            )

    def __init__(self, *args, **kwargs):
        cantidad = kwargs.pop('cantidad')
        cantidad_registrada = kwargs.pop('cantidad_registrada')
        super(CambioSociedadStockDetalleSeriesForm, self).__init__(*args, **kwargs)
        self.fields['cantidad'].initial = cantidad
        self.fields['cantidad_registrada'].initial = cantidad_registrada
        if cantidad_registrada == cantidad:
            self.fields['serie'].disabled = True
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            self.fields['cantidad'].disabled = True
            self.fields['cantidad_registrada'].disabled = True


class CambioSociedadForm(BSModalForm):
    internacional_nacional = forms.ChoiceField(choices=((None, '-----------------'),) + INTERNACIONAL_NACIONAL, required=False)
    incoterms = forms.ChoiceField(choices=((None, '-----------------'),) + INCOTERMS, required=False)
    moneda = forms.ModelChoiceField(queryset=Moneda.objects.filter(estado=1))
    class Meta:
        fields=(
            'internacional_nacional',
            'incoterms',
            'moneda',
            )

    def __init__(self, *args, **kwargs):
        super(CambioSociedadForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'