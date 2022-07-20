from django import forms
from bootstrap_modal_forms.forms import BSModalForm, BSModalModelForm
from .models import ComprobanteCompraPI, ArchivoComprobanteCompraPI

class ComprobanteCompraPILogisticoForm(BSModalModelForm):
    class Meta:
        model = ComprobanteCompraPI
        fields=(
            'logistico',
            )

    def __init__(self, *args, **kwargs):
        super(ComprobanteCompraPILogisticoForm, self).__init__(*args, **kwargs)
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