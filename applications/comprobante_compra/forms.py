from django import forms
from django.contrib.auth import get_user_model
from bootstrap_modal_forms.forms import BSModalForm, BSModalModelForm
from .models import ComprobanteCompraCIDetalle, ComprobanteCompraPI, ArchivoComprobanteCompraPI

class ComprobanteCompraPIForm(BSModalModelForm):
    class Meta:
        model = ComprobanteCompraPI
        fields=(
            'fecha_comprobante',
            'numero_comprobante_compra',
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
        super(ComprobanteCompraPIForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class ComprobanteCompraPILlegadaForm(BSModalModelForm):
    class Meta:
        model = ComprobanteCompraPI
        fields=(
            'fecha_estimada_llegada',
            )
        widgets = {
            'fecha_estimada_llegada' : forms.DateInput(
                attrs ={
                    'type':'date',
                    },
                format = '%Y-%m-%d',
                ),
            }

    def __init__(self, *args, **kwargs):
        super(ComprobanteCompraPILlegadaForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class ArchivoComprobanteCompraPIForm(BSModalModelForm):
    class Meta:
        model = ArchivoComprobanteCompraPI
        fields=(
            'archivo',
            )

    def __init__(self, *args, **kwargs):
        super(ArchivoComprobanteCompraPIForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    
class RecepcionComprobanteCompraPIForm(BSModalForm):
    fecha_recepcion = forms.DateField(
        widget = forms.DateInput(
                attrs ={
                    'type':'date',
                    },
                format = '%Y-%m-%d',
                )
    )
    usuario_recepcion = forms.ModelChoiceField(queryset=get_user_model().objects.all())
    nro_bultos = forms.IntegerField()
    observaciones = forms.CharField(
        widget=forms.Textarea(),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super(RecepcionComprobanteCompraPIForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    
class ComprobanteCompraCIForm(BSModalForm):
    fecha_comprobante = forms.DateField(
        widget = forms.DateInput(
                attrs ={
                    'type':'date',
                    },
                format = '%Y-%m-%d',
                )
    )
    numero_comprobante_compra = forms.CharField()
    archivo = forms.FileField()

    def __init__(self, *args, **kwargs):
        super(ComprobanteCompraCIForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class ComprobanteCompraCIDetalleUpdateForm(BSModalModelForm):

    class Meta:
        model = ComprobanteCompraCIDetalle
        fields=(
            'item',
            'descripcion',
            'tipo_igv',
            'cantidad',
            'precio_unitario_sin_igv',
            'precio_unitario_con_igv',
            'precio_final_con_igv',
            'descuento',
            'sub_total',
            'igv',
            'total',
            )

    def __init__(self, *args, **kwargs):
        super(ComprobanteCompraCIDetalleUpdateForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'