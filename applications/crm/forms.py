from django import forms
from applications.crm.models import ClienteCRM, ClienteCRMDetalle
from bootstrap_modal_forms.forms import BSModalForm, BSModalModelForm
from applications.datos_globales.models import Pais
from applications.variables import ESTADOS_CLIENTE_CRM, MEDIO
from applications.clientes.models import ClienteInterlocutor, InterlocutorCliente


class ClienteCRMForm(BSModalModelForm):
    class Meta:
        model = ClienteCRM
        fields = (
            'cliente_crm',
            'medio',
            )

    def __init__(self, *args, **kwargs):
        super(ClienteCRMForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class ClienteCRMBuscarForm(forms.Form):
    razon_social = forms.CharField(label = 'Razón Social', max_length=100, required=False)
    medio = forms.ChoiceField(choices=((None, '--------------------'),) + MEDIO, required=False)
    estado = forms.ChoiceField(choices=((None, '--------------------'),) + ESTADOS_CLIENTE_CRM, required=False)
    pais = forms.ModelChoiceField(queryset=Pais.objects.all(), required=False)
    fecha_registro = forms.DateField(
        required=False,
        widget = forms.DateInput(
                attrs ={
                    'type':'date',
                    },
                format = '%Y-%m-%d',
                )
        )

    def __init__(self, *args, **kwargs):
        filtro_razon_social = kwargs.pop('filtro_razon_social')
        filtro_medio = kwargs.pop('filtro_medio')
        filtro_estado = kwargs.pop('filtro_estado')
        filtro_pais = kwargs.pop('filtro_pais')
        filtro_fecha_registro = kwargs.pop('filtro_fecha_registro')
        super(ClienteCRMBuscarForm, self).__init__(*args, **kwargs)
        self.fields['razon_social'].initial = filtro_razon_social
        self.fields['medio'].initial = filtro_medio
        self.fields['estado'].initial = filtro_estado
        self.fields['fecha_registro'].initial = filtro_fecha_registro
        self.fields['pais'].initial = filtro_pais
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class ClienteCRMDetalleForm(BSModalModelForm):
    class Meta:
        model = ClienteCRMDetalle
        fields = (
            'interlocutor',
            'correo',
            'telefono',
            )
    
    # def clean_cliente(self):
    #     cliente = self.cliente
    #     if cliente:
    #         interlocutor = self.fields['interlocutor']
    #         lista = []
    #         relaciones = ClienteInterlocutor.objects.filter(cliente = cliente.id)
    #         for relacion in relaciones:
    #             lista.append(relacion.interlocutor.id)

    #         interlocutor.queryset = InterlocutorCliente.objects.filter(id__in = lista)

    #     return cliente

    def __init__(self, *args, **kwargs):
        # self.cliente = kwargs.pop('cliente')
        # interlocutor_queryset = kwargs.pop('interlocutor_queryset')
        # interlocutor = kwargs.pop('interlocutor')
        super(ClienteCRMDetalleForm, self).__init__(*args, **kwargs)
        # self.fields['interlocutor'].queryset = interlocutor_queryset
        # self.fields['interlocutor'].initial = interlocutor
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'