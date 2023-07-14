from django import forms
from bootstrap_modal_forms.forms import BSModalForm, BSModalModelForm
from applications.datos_globales.models import Pais
from applications.crm.models import (
    ClienteCRM,
    ClienteCRMDetalle, 
    ProveedorCRM,
    EventoCRM,
    PreguntaCRM,
    AlternativaCRM,
    EncuestaCRM,
    RespuestaCRM)
from applications.clientes.models import Cliente
from bootstrap_modal_forms.forms import BSModalForm, BSModalModelForm
from applications.datos_globales.models import Pais
from applications.variables import ESTADOS_CLIENTE_CRM, MEDIO, ESTADOS_EVENTO_CRM, TIPO_PREGUNTA_CRM, TIPO_ENCUESTA_CRM
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
    estado = forms.ChoiceField(choices=((None, '--------------------'),) + ESTADOS_CLIENTE_CRM, required=False)

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
            'fecha',
            'comentario',
            'monto',
            'archivo_recibido',
            'archivo_enviado',
            )
        
        widgets = {
            'fecha' : forms.DateInput(
                attrs ={
                    'type':'date',
                    },
                format = '%Y-%m-%d',
                ),
        }

    def __init__(self, *args, **kwargs):
        super(ClienteCRMDetalleForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class ProveedorCRMForm(BSModalModelForm):
    class Meta:
        model = ProveedorCRM
        fields = (
            'proveedor_crm',
            )

    def __init__(self, *args, **kwargs):
        super(ProveedorCRMForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class EventoCRMForm(BSModalModelForm):
    class Meta:
        model = EventoCRM
        fields=(
            'titulo',
            'fecha_inicio',
            'fecha_cierre',
            'pais',
            )
        
        widgets = {
            'fecha_inicio' : forms.DateInput(
                attrs ={
                    'type':'date',
                    },
                format = '%Y-%m-%d',
                ),
            
            'fecha_cierre' : forms.DateInput(
                attrs ={
                    'type':'date',
                    },
                format = '%Y-%m-%d',
                ),   
            }

    def __init__(self, *args, **kwargs):
        super(EventoCRMForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.required = True


class EventoCRMBuscarForm(forms.Form):
    pais = forms.ModelChoiceField(queryset=Pais.objects.all(), required=False)
    estado = forms.ChoiceField(choices=((None, '--------------------'),) + ESTADOS_EVENTO_CRM, required=False)
    fecha_inicio = forms.DateField(
        required=False,
        widget = forms.DateInput(
                attrs ={
                    'type':'date',
                    },
                format = '%Y-%m-%d',
                )
        )

    def __init__(self, *args, **kwargs):
        filtro_pais = kwargs.pop('filtro_pais')
        filtro_estado = kwargs.pop('filtro_estado')
        filtro_fecha_inicio = kwargs.pop('filtro_fecha_inicio')
        super(EventoCRMBuscarForm, self).__init__(*args, **kwargs)
        self.fields['pais'].initial = filtro_pais
        self.fields['estado'].initial = filtro_estado
        self.fields['fecha_inicio'].initial = filtro_fecha_inicio
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class EventoCRMDetalleDescripcionForm(BSModalModelForm):
    class Meta:
        model = EventoCRM
        fields=(
            'descripcion',
            )

    def __init__(self, *args, **kwargs):
        super(EventoCRMDetalleDescripcionForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class PreguntaCRMBuscarForm(forms.Form):
    tipo_pregunta = forms.ChoiceField(choices=((None, '--------------------'),) + TIPO_PREGUNTA_CRM, required=False)

    def __init__(self, *args, **kwargs):
        filtro_tipo_pregunta = kwargs.pop('filtro_tipo_pregunta')

        super(PreguntaCRMBuscarForm, self).__init__(*args, **kwargs)
        self.fields['tipo_pregunta'].initial = filtro_tipo_pregunta
        
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class PreguntaCRMForm(BSModalModelForm):
    class Meta:
        model = PreguntaCRM
        fields=(
            'texto',
            'orden',
            'tipo_pregunta',
            'mostrar',
            )

    def __init__(self, *args, **kwargs):
        super(PreguntaCRMForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        self.fields['mostrar'].widget.attrs['class'] = 'form-check-input'

class AlternativaCRMForm(BSModalModelForm):
    class Meta:
        model = AlternativaCRM
        fields=(
            'texto',
            'orden',
            'valor',
            'mostrar',
            )

    def __init__(self, *args, **kwargs):
        super(AlternativaCRMForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.required = True
        self.fields['mostrar'].widget.attrs['class'] = 'form-check-input'

class EncuestaCRMBuscarForm(forms.Form):
    tipo_encuesta = forms.ChoiceField(choices=((None, '--------------------'),) + TIPO_ENCUESTA_CRM, required=False)
    pais = forms.ModelChoiceField(queryset=Pais.objects.all(), required=False)
    titulo = forms.CharField(label = 'Titulo', max_length=100, required=False)

    def __init__(self, *args, **kwargs):
        filtro_tipo_encuesta = kwargs.pop('filtro_tipo_encuesta')
        filtro_pais = kwargs.pop('filtro_pais')
        filtro_titulo = kwargs.pop('filtro_titulo')

        super(EncuestaCRMBuscarForm, self).__init__(*args, **kwargs)
        self.fields['tipo_encuesta'].initial = filtro_tipo_encuesta
        self.fields['pais'].initial = filtro_pais
        self.fields['titulo'].initial = filtro_titulo
        
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class EncuestaCRMForm(BSModalModelForm):
    class Meta:
        model = EncuestaCRM
        fields=(
            'tipo_encuesta',
            'titulo',
            'mostrar',
            'pais',
            )

    def __init__(self, *args, **kwargs):
        super(EncuestaCRMForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.required = True
        self.fields['mostrar'].widget.attrs['class'] = 'form-check-input'

class EncuestaPreguntaCRMForm(BSModalModelForm):
    pregunta_crm = forms.ModelMultipleChoiceField(queryset=PreguntaCRM.objects.filter(mostrar=True))
    class Meta:
        model = EncuestaCRM
        fields=(
            'pregunta_crm',
            )

    def __init__(self, *args, **kwargs):
        super(EncuestaPreguntaCRMForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        # self.fields['pregunta_crm'].widget.attrs['class'] = 'no-bull'


class RespuestaCRMBuscarForm(forms.Form):
    cliente = forms.ModelChoiceField(queryset=Cliente.objects.all(), required=False)
    encuesta = forms.ModelChoiceField(queryset=EncuestaCRM.objects.all(), required=False)

    def __init__(self, *args, **kwargs):
        filtro_cliente = kwargs.pop('filtro_cliente')
        filtro_encuesta = kwargs.pop('filtro_encuesta')

        super(RespuestaCRMBuscarForm, self).__init__(*args, **kwargs)
        self.fields['encuesta'].initial = filtro_encuesta
        self.fields['cliente'].initial = filtro_cliente
        
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class RespuestaCRMForm(BSModalModelForm):
    class Meta:
        model = RespuestaCRM
        fields=(
            'cliente_crm',
            'interlocutor',
            'nombre_interlocutor',
            'encuesta_crm',
            )

    def __init__(self, *args, **kwargs):
        super(RespuestaCRMForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
