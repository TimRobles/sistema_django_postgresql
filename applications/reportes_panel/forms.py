from django import forms
from bootstrap_modal_forms.forms import BSModalModelForm
from applications.sociedad.models import Sociedad
from applications.material.models import Marca, Material
from applications.clientes.models import Cliente

class ReportesPanelFiltrosForm(forms.Form):
    marca = forms.ModelChoiceField(queryset=Marca.objects.all())
    fecha_inicio = forms.DateField(
        required=False,
        widget = forms.DateInput(
                attrs ={
                    'type':'date',
                    },
                format = '%Y-%m-%d',
                )
        )
    fecha_fin = forms.DateField(
        required=False,
        widget = forms.DateInput(
                attrs ={
                    'type':'date',
                    },
                format = '%Y-%m-%d',
                )
        )
    sociedad = forms.ModelChoiceField(queryset=Sociedad.objects.all())
    # cliente = forms.ModelChoiceField(queryset=Cliente.objects.filter(estado_sunat = 1))

    def __init__(self, *args, **kwargs):
        filtro_marca = kwargs.pop('filtro_marca')
        filtro_sociedad = kwargs.pop('filtro_sociedad')
        filtro_fecha_inicio = kwargs.pop('filtro_fecha_inicio')
        filtro_fecha_fin = kwargs.pop('filtro_fecha_fin')
        # filtro_cliente = kwargs.pop('filtro_cliente')
        super(ReportesPanelFiltrosForm, self).__init__(*args, **kwargs)
        self.fields['marca'].initial = filtro_marca
        self.fields['marca'].required = False
        self.fields['sociedad'].initial = filtro_sociedad
        self.fields['sociedad'].required = False
        self.fields['fecha_inicio'].initial = filtro_fecha_inicio
        self.fields['fecha_fin'].initial = filtro_fecha_fin
        # self.fields['cliente'].initial = filtro_cliente
        # self.fields['cliente'].required = False
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class ReporteProductoClienteVentasFiltrosForm(forms.Form):
    producto = forms.ModelChoiceField(queryset=Material.objects.all())
    sociedad = forms.ModelChoiceField(queryset=Sociedad.objects.all())
    cliente = forms.ModelChoiceField(queryset=Cliente.objects.all())

    def __init__(self, *args, **kwargs):
        filtro_sociedad = kwargs.pop('filtro_sociedad')
        filtro_producto = kwargs.pop('filtro_producto')
        filtro_cliente = kwargs.pop('filtro_cliente')
        super(ReporteProductoClienteVentasFiltrosForm, self).__init__(*args, **kwargs)
        self.fields['sociedad'].initial = filtro_sociedad
        self.fields['sociedad'].required = False
        self.fields['producto'].initial = filtro_producto
        self.fields['producto'].required = False
        self.fields['cliente'].initial = filtro_cliente
        self.fields['cliente'].required = False
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class ReporteUbigeoVentasFiltrosForm(forms.Form):
    sociedad = forms.ModelChoiceField(queryset=Sociedad.objects.all())
    # producto = forms.ModelChoiceField(queryset=Material.objects.all())

    def __init__(self, *args, **kwargs):
        filtro_sociedad = kwargs.pop('filtro_sociedad')
        # filtro_producto = kwargs.pop('filtro_producto')
        super(ReporteUbigeoVentasFiltrosForm, self).__init__(*args, **kwargs)
        self.fields['sociedad'].initial = filtro_sociedad
        self.fields['sociedad'].required = False
        # self.fields['producto'].initial = filtro_producto
        # self.fields['producto'].required = False
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'