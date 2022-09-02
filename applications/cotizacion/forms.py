from pyexpat import model
from bootstrap_modal_forms.forms import BSModalForm, BSModalModelForm
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from applications.datos_globales.models import Moneda
from applications.cotizacion.models import CotizacionVenta, PrecioListaMaterial
from applications.comprobante_compra.models import ComprobanteCompraPI
from applications.clientes.forms import Cliente

class CotizacionVentaForm (BSModalForm):
    class Meta:
        model = CotizacionVenta
        fields = (
            'numero_cotizacion',
            'fecha_cotizacion',
        )

    def __init__(self, *args, **kwargs):
        super(CotizacionVentaForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class ClienteForm(BSModalModelForm):
    class Meta:
        model = Cliente
        fields = (
            'tipo_documento',
            'numero_documento',
            'razon_social',
            'nombre_comercial',
            'direccion_fiscal',
            'ubigeo',
            'estado_sunat',
            'condicion_sunat',
            )

    def __init__(self, *args, **kwargs):
        super(ClienteForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


