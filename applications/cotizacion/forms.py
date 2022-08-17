from bootstrap_modal_forms.forms import BSModalForm, BSModalModelForm
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from applications.datos_globales.models import Moneda
from applications.cotizacion.models import PrecioListaMaterial
from applications.comprobante_compra.models import ComprobanteCompraPI

class PrecioListaMaterialForm (BSModalForm):
    class Meta:
        model = PrecioListaMaterial
        comprobante = forms.ModelChoiceField(queryset=ComprobanteCompraPI.objects.all())
        fields = (
            'comprobante',
            'precio_compra',
            'precio_lista',
            'precio_sin_igv',
            'moneda',
            'logistico',
            'margen_venta',
        )

    def __init__(self, *args, **kwargs):
        super(PrecioListaMaterialForm, self).__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
