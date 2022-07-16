from django import forms
from bootstrap_modal_forms.forms import BSModalForm, BSModalModelForm
from .models import OrdenCompra, OrdenCompraDetalle

class OrdenCompraForm(BSModalModelForm):
    class Meta:
        model = OrdenCompra
        fields=(
            'moneda',
            'descuento_global',
            'total_descuento',
            'total_anticipo',
            'total_gravada',
            'total_exonerada',
            'total_igv',
            'total_gratuita',
            'total_otros_cargos',
            'total_isc',
            'total',
            )

    def __init__(self, *args, **kwargs):
        super(OrdenCompraForm, self).__init__(*args, **kwargs)   
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class OrdenCompraDetalleForm(BSModalModelForm):
    class Meta:
        model = OrdenCompraDetalle
        fields=(
            'item',
            'content_type',
            'id_registro',
            'cantidad',
            'precio_unitario_sin_igv',
            'precio_unitario_con_igv',
            'precio_final_con_igv',
            'descuento',
            'sub_total',
            'igv',
            'total',
            'tipo_igv',
            'orden_compra',
            )

    def __init__(self, *args, **kwargs):
        super(OrdenCompraDetalleForm, self).__init__(*args, **kwargs)   
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'