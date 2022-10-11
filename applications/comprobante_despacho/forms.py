from django import forms
from bootstrap_modal_forms.forms import BSModalForm, BSModalModelForm
from applications.envio_clientes.models import Transportista
from applications.comprobante_despacho.models import Guia
from applications.clientes.models import ClienteInterlocutor, InterlocutorCliente
from applications.datos_globales.models import Distrito
from applications.sede.models import Sede


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
    direcciones = forms.ModelChoiceField(queryset=Sede.objects.all(), required=False)
    ubigeo = forms.ModelChoiceField(queryset=Distrito.objects.none(), required=False)
    class Meta:
        model = Guia
        fields=(
            'direcciones',
            'direccion_partida',
            'ubigeo',
            )

    def __init__(self, *args, **kwargs):
        super(GuiaPartidaForm, self).__init__(*args, **kwargs)
        self.fields['ubigeo'].queryset = Distrito.objects.filter(codigo=self.instance.ubigeo_partida.codigo)
        self.fields['ubigeo'].initial = self.instance.ubigeo_partida
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        if 'ubigeo' in self.data:
            self.fields['ubigeo'].queryset=Distrito.objects.all()


class GuiaDestinoForm(BSModalModelForm):
    CHOICES = (
        ('0', '----------------'),
        ('1', 'Direccion 1 | 010105'),
        ('2', 'Direccion 2 | 021208'),
    )
    direcciones = forms.ChoiceField(choices=CHOICES, required=False)
    ubigeo = forms.ModelChoiceField(queryset=Distrito.objects.none(), required=False)
    class Meta:
        model = Guia
        fields=(
            'direcciones',
            'direccion_destino',
            'ubigeo',
            )

    def __init__(self, *args, **kwargs):
        super(GuiaDestinoForm, self).__init__(*args, **kwargs)
        self.fields['ubigeo'].queryset = Distrito.objects.filter(codigo=self.instance.ubigeo_destino.codigo)
        self.fields['ubigeo'].initial = self.instance.ubigeo_destino
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        if 'ubigeo' in self.data:
            self.fields['ubigeo'].queryset=Distrito.objects.all()


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
