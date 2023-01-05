import re
from django import forms
from django.contrib.auth import get_user_model
from applications.clientes.models import Cliente
from applications.datos_globales.models import SeriesComprobante
from applications.sociedad.models import Sociedad
from applications.variables import ESTADOS_DOCUMENTO
from bootstrap_modal_forms.forms import BSModalForm, BSModalModelForm
from applications.comprobante_venta.models import BoletaVenta, FacturaVenta, FacturaVentaDetalle
from django.contrib.contenttypes.models import ContentType


class BoletaVentaBuscarForm(forms.Form):
    numero_boleta = forms.CharField(label='Nro. boleta',max_length=150, required=False)
    sociedad = forms.ModelChoiceField(queryset=Sociedad.objects.filter(estado_sunat=1), required=False)
    cliente = forms.ModelChoiceField(queryset=Cliente.objects.all(), required=False)
    fecha_emision = forms.DateField(
        required=False,
        widget = forms.DateInput(
                attrs ={
                    'type':'date',
                    },
                format = '%Y-%m-%d',
                )
        )
    estado = forms.ChoiceField(choices=((None, '--------------------'),) + ESTADOS_DOCUMENTO, required=False)

    def __init__(self, *args, **kwargs):
        filtro_numero_boleta = kwargs.pop('filtro_numero_boleta')
        filtro_sociedad = kwargs.pop('filtro_sociedad')
        filtro_cliente = kwargs.pop('filtro_cliente')
        filtro_fecha_emision = kwargs.pop('filtro_fecha_emision')
        filtro_estado = kwargs.pop('filtro_estado')
        super(BoletaVentaBuscarForm, self).__init__(*args, **kwargs)
        self.fields['numero_boleta'].initial = filtro_numero_boleta
        self.fields['sociedad'].initial = filtro_sociedad
        self.fields['cliente'].initial = filtro_cliente
        self.fields['fecha_emision'].initial = filtro_fecha_emision
        self.fields['estado'].initial = filtro_estado
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class BoletaVentaSerieForm(BSModalModelForm):
    class Meta:
        model = BoletaVenta
        fields = (
            'serie_comprobante',
            )

    def __init__(self, *args, **kwargs):
        super(BoletaVentaSerieForm, self).__init__(*args, **kwargs)
        self.fields['serie_comprobante'].queryset = SeriesComprobante.objects.filter(tipo_comprobante=ContentType.objects.get_for_model(BoletaVenta))
        self.fields['serie_comprobante'].required = True
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            

class BoletaVentaAnularForm(BSModalModelForm):
    class Meta:
        model = BoletaVenta
        fields = (
            'motivo_anulacion',
            )

    def __init__(self, *args, **kwargs):
        super(BoletaVentaAnularForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class FacturaVentaBuscarForm(forms.Form):
    numero_factura = forms.IntegerField(label='Nro. Factura', required=False)
    sociedad = forms.ModelChoiceField(queryset=Sociedad.objects.filter(estado_sunat=1), required=False)
    cliente = forms.ModelChoiceField(queryset=Cliente.objects.all(), required=False)
    fecha_emision = forms.DateField(
        required=False,
        widget = forms.DateInput(
                attrs ={
                    'type':'date',
                    },
                format = '%Y-%m-%d',
                )
        )
    estado = forms.ChoiceField(choices=((None, '--------------------'),) + ESTADOS_DOCUMENTO, required=False)

    def __init__(self, *args, **kwargs):
        filtro_numero_factura = kwargs.pop('filtro_numero_factura')
        filtro_sociedad = kwargs.pop('filtro_sociedad')
        filtro_cliente = kwargs.pop('filtro_cliente')
        filtro_fecha_emision = kwargs.pop('filtro_fecha_emision')
        filtro_estado = kwargs.pop('filtro_estado')
        super(FacturaVentaBuscarForm, self).__init__(*args, **kwargs)
        self.fields['numero_factura'].initial = filtro_numero_factura
        self.fields['sociedad'].initial = filtro_sociedad
        self.fields['cliente'].initial = filtro_cliente
        self.fields['fecha_emision'].initial = filtro_fecha_emision
        self.fields['estado'].initial = filtro_estado
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class FacturaVentaSerieForm(BSModalModelForm):
    class Meta:
        model = FacturaVenta
        fields = (
            'serie_comprobante',
            )

    def __init__(self, *args, **kwargs):
        super(FacturaVentaSerieForm, self).__init__(*args, **kwargs)
        self.fields['serie_comprobante'].queryset = SeriesComprobante.objects.filter(tipo_comprobante=ContentType.objects.get_for_model(FacturaVenta))
        self.fields['serie_comprobante'].required = True
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            

class FacturaVentaAnularForm(BSModalModelForm):
    class Meta:
        model = FacturaVenta
        fields = (
            'motivo_anulacion',
            )

    def __init__(self, *args, **kwargs):
        super(FacturaVentaAnularForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            

class FacturaVentaDetalleForm(BSModalModelForm):
    class Meta:
        model = FacturaVentaDetalle
        fields = (
            'descripcion_documento',
            'total',
            )

    def __init__(self, *args, **kwargs):
        super(FacturaVentaDetalleForm, self).__init__(*args, **kwargs)
        try:
            self.initial['descripcion_documento'] = re.sub(" \(Cotización.*", "", self.instance.descripcion_documento)
        except Exception as e:
            print(e)
            pass
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'