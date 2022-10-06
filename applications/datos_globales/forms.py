from datetime import date
from django import forms
from applications.datos_globales.models import Area, Cargo, Moneda, TipoCambio, TipoCambioSunat, TipoInterlocutor, Pais
from bootstrap_modal_forms.forms import BSModalForm, BSModalModelForm

class MonedaForm(forms.ModelForm):
    class Meta:
        model = Moneda
        fields = (
            'nombre',
            'abreviatura',
            'simbolo',
            'principal',
            'secundario',
            'moneda_pais',
            'nubefact',
            'estado',
            )

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        filtro = Moneda.objects.filter(nombre__unaccent__iexact = nombre)
        if nombre != self.instance.nombre:
            if len(filtro)>0:
                self.add_error('nombre', 'Ya existe una Moneda con este nombre')

        return nombre


class AreaForm(forms.ModelForm):
    class Meta:
        model = Area
        fields = (
            'nombre',
            'estado',
            )

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        filtro = Area.objects.filter(nombre__unaccent__iexact = nombre)
        if nombre != self.instance.nombre:
            if len(filtro)>0:
                self.add_error('nombre', 'Ya existe un Área con este nombre')

        return nombre


class CargoForm(forms.ModelForm):
    class Meta:
        model = Cargo
        fields = (
            'nombre',
            'area',
            )

    def clean(self):
        cleaned_data = super().clean()
        nombre = cleaned_data.get('nombre')
        area = cleaned_data.get('area')
        filtro = Cargo.objects.filter(nombre__unaccent__iexact = nombre, area = area)
        if nombre != self.instance.nombre:
            if len(filtro)>0:
                self.add_error('nombre', 'Ya existe un Cargo con este nombre')
                

class TipoInterlocutorForm(forms.ModelForm):
    class Meta:
        model = TipoInterlocutor
        fields = (
            'nombre',
            )

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        filtro = TipoInterlocutor.objects.filter(nombre__unaccent__iexact = nombre)
        if nombre != self.instance.nombre:
            if len(filtro)>0:
                self.add_error('nombre', 'Ya existe un Tipo de Interlocutor con este nombre')

        return nombre

class PaisForm(forms.ModelForm):
    class Meta:
        model = Pais
        fields = (
            'nombre',
            )

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        filtro = Pais.objects.filter(nombre__unaccent__iexact = nombre)
        if nombre != self.instance.nombre:
            if len(filtro)>0:
                self.add_error('nombre', 'Ya existe un País con este nombre')

        return nombre

class TipoCambioForm(BSModalModelForm):
    class Meta:
        model = TipoCambio
        fields = (
            'fecha',
            'tipo_cambio_venta',
            'tipo_cambio_compra',
            'moneda_origen',
            'moneda_destino',
            )
        widgets = {
            'fecha' : forms.DateInput(
                attrs ={
                    'type':'date',
                    },
                format = '%Y-%m-%d',
                ),
            }

    def __init__(self, *args, **kwargs):
        super(TipoCambioForm, self).__init__(*args, **kwargs)
        if not self.fields['fecha'].initial:
            self.fields['fecha'].initial = date.today()
        self.fields['moneda_origen'].initial = Moneda.objects.get(principal=True)
        self.fields['moneda_destino'].initial = Moneda.objects.get(secundario=True)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class TipoCambioSunatForm(BSModalModelForm):
    class Meta:
        model = TipoCambioSunat
        fields = (
            'fecha',
            'tipo_cambio_venta',
            'tipo_cambio_compra',
            )
        widgets = {
            'fecha' : forms.DateInput(
                attrs ={
                    'type':'date',
                    },
                format = '%Y-%m-%d',
                ),
            }

    def __init__(self, *args, **kwargs):
        super(TipoCambioSunatForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'