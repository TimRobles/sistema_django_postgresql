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


class GuiaPartidaForm(BSModalModelForm):
    class Meta:
        model = Guia
        fields=(
            'direccion_partida',
            'ubigeo_partida',
            )

    # def clean_direccion_partida(self):
    #     direccion_partida = self.cleaned_data.get('direccion_partida')
    #     return direccion_partida

    def __init__(self, *args, **kwargs):
        super(GuiaPartidaForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'



class GuiaDestinoForm(BSModalModelForm):
    class Meta:
        model = Guia
        fields=(
            'direccion_destino',
            'ubigeo_destino',
            )

    # def clean_direccion_destino(self):
    #     direccion_destino = self.cleaned_data.get('direccion_destino')
    #     return direccion_destino

    def __init__(self, *args, **kwargs):
        super(GuiaDestinoForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

