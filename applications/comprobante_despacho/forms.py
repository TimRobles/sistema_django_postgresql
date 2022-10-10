from django import forms
from bootstrap_modal_forms.forms import BSModalForm, BSModalModelForm
from applications.envio_clientes.models import Transportista
from applications.comprobante_despacho.models import Guia
from applications.clientes.models import ClienteInterlocutor, InterlocutorCliente


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


class GuiaConductorForm(BSModalModelForm):
    class Meta:
        model = Guia
        fields=(
            'conductor_tipo_documento',
            'conductor_numero_documento',
            'conductor_denominacion',
            'placa_numero',
            )

    def __init__(self, *args, **kwargs):
        super(GuiaConductorForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class GuiaClienteForm(BSModalModelForm):
    class Meta:
        model = Guia
        fields = (
            'cliente',
            'cliente_interlocutor',
            )

    def clean_cliente(self):
        cliente = self.cleaned_data.get('cliente')
        if cliente:
            cliente_interlocutor = self.fields['cliente_interlocutor']
            lista = []
            relaciones = ClienteInterlocutor.objects.filter(cliente = cliente.id)
            for relacion in relaciones:
                lista.append(relacion.interlocutor.id)

            cliente_interlocutor.queryset = InterlocutorCliente.objects.filter(id__in = lista)
    
        return cliente

    def __init__(self, *args, **kwargs):
        # interlocutor_queryset = kwargs.pop('interlocutor_queryset')
        # interlocutor = kwargs.pop('interlocutor')
        super(GuiaClienteForm, self).__init__(*args, **kwargs)
        # self.fields['cliente_interlocutor'].queryset = interlocutor_queryset
        # self.fields['cliente_interlocutor'].initial = interlocutor
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
