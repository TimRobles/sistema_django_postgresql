from django import forms
from django.contrib.auth import get_user_model
from bootstrap_modal_forms.forms import BSModalForm, BSModalModelForm
from applications.sociedad.models import Sociedad
from applications.proveedores.models import Proveedor
from applications.material.models import Material

from .models import ComprobanteCompraCIDetalle, ComprobanteCompraPI, ArchivoComprobanteCompraPI

class ComprobanteCompraPICorregirForm(BSModalForm):
    fecha_comprobante = forms.DateField(widget=forms.DateInput(attrs ={'type':'date',},format = '%Y-%m-%d',), required=True)
    numero_comprobante_compra = forms.CharField(max_length=50, required=True)
    logistico = forms.DecimalField(required=True)
    sociedad = forms.ModelChoiceField(queryset=Sociedad.objects.filter(estado_sunat=1), required=True)
    
    def __init__(self, *args, **kwargs):
        fecha_comprobante = kwargs.pop('fecha_comprobante')
        numero_comprobante_compra = kwargs.pop('numero_comprobante_compra')
        logistico = kwargs.pop('logistico')
        sociedad = kwargs.pop('sociedad')
        super(ComprobanteCompraPICorregirForm, self).__init__(*args, **kwargs)
        self.fields['fecha_comprobante'].initial = fecha_comprobante
        self.fields['numero_comprobante_compra'].initial = numero_comprobante_compra
        self.fields['logistico'].initial = logistico
        self.fields['sociedad'].initial = sociedad
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

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



#_______________________
class ComprobanteCompraPIBuscarForm(forms.Form):
    sociedad = forms.ModelChoiceField(queryset=Sociedad.objects.filter(estado_sunat=1), required=False)
    proveedor = forms.ModelChoiceField(queryset= Proveedor.objects.all(), required=False)
    material = forms.ModelChoiceField(queryset= Material.objects.all(), required=False)

    def __init__(self, *args, **kwargs):
        filtro_sociedad = kwargs.pop('filtro_sociedad')
        filtro_proveedor = kwargs.pop('filtro_proveedor')
        filtro_material = kwargs.pop('filtro_material')

        super(ComprobanteCompraPIBuscarForm, self).__init__(*args, **kwargs)
        self.fields['sociedad'].initial = filtro_sociedad
        self.fields['proveedor'].initial = filtro_proveedor
        self.fields['material'].initial = filtro_material

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
#_______________________
