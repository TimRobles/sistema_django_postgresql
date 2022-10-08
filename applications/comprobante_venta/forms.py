import re
from django import forms
from applications.datos_globales.models import SeriesComprobante
from bootstrap_modal_forms.forms import BSModalForm, BSModalModelForm
from applications.comprobante_venta.models import BoletaVenta, FacturaVenta, FacturaVentaDetalle
from django.contrib.contenttypes.models import ContentType

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