import re
from django import forms
from django.contrib.auth import get_user_model
from applications.datos_globales.models import SeriesComprobante
from bootstrap_modal_forms.forms import BSModalForm, BSModalModelForm
from applications.comprobante_venta.models import BoletaVenta, FacturaVenta, FacturaVentaDetalle
from django.contrib.contenttypes.models import ContentType


class BoletaVentaBuscarForm(forms.Form):
    # nro_boleta = forms.CharField(label='Nro. boleta',max_length=150, required=False)
    cliente = forms.CharField(max_length=150, required=False)
    fecha_emision = forms.DateField(
        required=False,
        widget = forms.DateInput(
                attrs ={
                    'type':'date',
                    },
                format = '%Y-%m-%d',
                )
        )
    # estado = forms.ModelChoiceField(queryset=get_user_model().objects)

    def __init__(self, *args, **kwargs):
        # filtro_nro_boleta = kwargs.pop('filtro_nro_boleta')
        filtro_cliente = kwargs.pop('filtro_cliente')
        filtro_fecha_emision = kwargs.pop('filtro_fecha_emision')
        # filtro_estado = kwargs.pop('filtro_estado')
        # estado = kwargs.pop('estados')
        super(BoletaVentaBuscarForm, self).__init__(*args, **kwargs)
        # self.fields['nro_boleta'].initial = filtro_nro_boleta
        self.fields['cliente'].initial = filtro_cliente
        self.fields['fecha_emision'].initial = filtro_fecha_emision
        # self.fields['estado'].initial = filtro_estado
        # self.fields['estado'].required = False
        # self.fields['estado'].queryset = estados
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
    # nro_factura = forms.CharField(label='Nro. Factura',max_length=150, required=False)
    cliente = forms.CharField(max_length=150, required=False)
    fecha_emision = forms.DateField(
        required=False,
        widget = forms.DateInput(
                attrs ={
                    'type':'date',
                    },
                format = '%Y-%m-%d',
                )
        )
    # estado = forms.ModelChoiceField(queryset=get_user_model().objects)

    def __init__(self, *args, **kwargs):
        # filtro_nro_factura = kwargs.pop('filtro_nro_factura')
        filtro_cliente = kwargs.pop('filtro_cliente')
        filtro_fecha_emision = kwargs.pop('filtro_fecha_emision')
        # filtro_estado = kwargs.pop('filtro_estado')
        # estado = kwargs.pop('estados')
        super(FacturaVentaBuscarForm, self).__init__(*args, **kwargs)
        # self.fields['nro_factura'].initial = filtro_nro_factura
        self.fields['cliente'].initial = filtro_cliente
        self.fields['fecha_emision'].initial = filtro_fecha_emision
        # self.fields['estado'].initial = filtro_estado
        # self.fields['estado'].required = False
        # self.fields['estado'].queryset = estados
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