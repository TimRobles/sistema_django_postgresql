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

    def __init__(self, *args, **kwargs):
        super(GuiaDestinoForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class GuiaBultosForm(BSModalModelForm):
    class Meta:
        model = Guia
        fields=(
            'numero_bultos',
            )

    def __init__(self, *args, **kwargs):
        super(GuiaBultosForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
