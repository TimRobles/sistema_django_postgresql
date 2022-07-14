from django import forms
from bootstrap_modal_forms.forms import BSModalForm, BSModalModelForm
from .models import OfertaProveedor, OfertaProveedorDetalle

class OfertaProveedorForm(BSModalModelForm):
    class Meta:
        model = OfertaProveedor
        fields=(
            'moneda',
            'descuento_global',
            'total_descuento',
            'total_anticipo',
            'total_gravada',
            'total_inafecta',
            'total_exonerada',
            'total_igv',
            'total_gratuita',
            'total_otros_cargos',
            'total_isc',
            'total',
            )

    def __init__(self, *args, **kwargs):
        super(OfertaProveedorForm, self).__init__(*args, **kwargs)   
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class OfertaProveedorDetalleUpdateForm(BSModalModelForm):
    material = forms.CharField(required=False)

    class Meta:
        model = OfertaProveedorDetalle
        fields=(
            'cantidad',
            'precio_unitario_sin_igv',
            'precio_unitario_con_igv',
            'precio_final_con_igv',
            'descuento',
            'sub_total',
            'tipo_igv',
            'igv',
            'total',
            )
        

    def __init__(self, *args, **kwargs):
        super(OfertaProveedorDetalleUpdateForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'