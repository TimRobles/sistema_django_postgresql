from django import forms
from bootstrap_modal_forms.forms import BSModalForm, BSModalModelForm
from applications.envio_clientes.models import Transportista
from applications.comprobante_despacho.models import Guia


class GuiaTransportistaForm(BSModalModelForm):
    class Meta:
        model = Guia
        fields=(
            'transportista',
            )

    def clean_transportista(self):
        transportista = self.cleaned_data.get('transportista')
        return transportista

    def __init__(self, *args, **kwargs):
        super(GuiaTransportistaForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
