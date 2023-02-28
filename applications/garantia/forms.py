from datetime import date
from django import forms
from django.contrib.contenttypes.models import ContentType
from bootstrap_modal_forms.forms import BSModalForm, BSModalModelForm
from applications.sociedad.models import Sociedad
from applications.variables import ESTADOS_DOCUMENTO,ESTADOS_CONTROL_RECLAMO_GARANTIA,ESTADOS_SALIDA_RECLAMO_GARANTIA
from applications.garantia.models import IngresoReclamoGarantia, ControlCalidadReclamoGarantia, SalidaReclamoGarantia
from applications.sede.models import Sede
from applications.material.models import Material
from applications.clientes.models import Cliente, ClienteInterlocutor, InterlocutorCliente
from applications.garantia.models import IngresoReclamoGarantia, IngresoReclamoGarantiaDetalle

class IngresoReclamoGarantiaBuscarForm(forms.Form):
    fecha_ingreso = forms.DateField(required=False, widget=forms.DateInput(attrs ={'type':'date',},format = '%Y-%m-%d',))
    nro_ingreso_garantia = forms.IntegerField(required=False)
    cliente = forms.ModelChoiceField(queryset=Cliente.objects.all(), required=False)
    sociedad = forms.ModelChoiceField(queryset=Sociedad.objects.all(), required=False)
    
    def __init__(self, *args, **kwargs):
        filtro_fecha_ingreso = kwargs.pop('filtro_fecha_ingreso')
        filtro_nro_ingreso_garantia = kwargs.pop('filtro_nro_ingreso_garantia')
        filtro_cliente = kwargs.pop('filtro_cliente')
        filtro_sociedad = kwargs.pop('filtro_sociedad')

        super(IngresoReclamoGarantiaBuscarForm, self).__init__(*args, **kwargs)

        self.fields['fecha_ingreso'].initial = filtro_fecha_ingreso
        self.fields['nro_ingreso_garantia'].initial = filtro_nro_ingreso_garantia
        self.fields['cliente'].initial = filtro_cliente
        self.fields['sociedad'].initial = filtro_sociedad

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class IngresoReclamoGarantiaClienteForm(BSModalModelForm):
    class Meta:
        model = IngresoReclamoGarantia
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
        interlocutor_queryset = kwargs.pop('interlocutor_queryset')
        interlocutor = kwargs.pop('interlocutor')
        super(IngresoReclamoGarantiaClienteForm, self).__init__(*args, **kwargs)
        self.fields['cliente_interlocutor'].queryset = interlocutor_queryset
        self.fields['cliente_interlocutor'].initial = interlocutor
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class IngresoReclamoGarantiaEncargadoForm(BSModalModelForm):
    class Meta:
        model = IngresoReclamoGarantia
        fields = (
            'encargado',
            )

    def __init__(self, *args, **kwargs):
        super(IngresoReclamoGarantiaEncargadoForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class IngresoReclamoGarantiaSociedadForm(BSModalModelForm):
    class Meta:
        model = IngresoReclamoGarantia
        fields = (
            'sociedad',
            )

    def __init__(self, *args, **kwargs):
        super(IngresoReclamoGarantiaSociedadForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class IngresoReclamoGarantiaObservacionForm(BSModalModelForm):
    class Meta:
        model = IngresoReclamoGarantia
        fields = (
            'observacion',
        )

    def __init__(self, *args, **kwargs):
        super(IngresoReclamoGarantiaObservacionForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class IngresoReclamoGarantiaMaterialForm(BSModalForm):
    material = forms.ModelChoiceField(queryset=Material.objects.filter(mostrar=True))
    cantidad = forms.DecimalField(max_digits=22, decimal_places=10)
    precio_venta = forms.DecimalField(max_digits=22, decimal_places=10, required=False)
    class Meta:
        model = IngresoReclamoGarantiaDetalle
        fields=(
            'material',
            'cantidad',
            'precio_venta',
            )

    def __init__(self, *args, **kwargs):
        super(IngresoReclamoGarantiaMaterialForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        self.fields['cantidad'].widget.attrs['min'] = 0
        self.fields['cantidad'].widget.attrs['step'] = 0.001


######################### CONTROL RECLAMO GARANTÍA ##############################################


class ControlCalidadReclamoGarantiaBuscarForm(forms.Form):
    estado = forms.ChoiceField(choices=((None,'------------'),) + ESTADOS_CONTROL_RECLAMO_GARANTIA, required=False)
    cliente = forms.ModelChoiceField(queryset=Cliente.objects.all(), required=False)

    def __init__(self, *args, **kwargs):
        filtro_estado = kwargs.pop('filtro_estado')
        filtro_cliente = kwargs.pop('filtro_cliente')
        super(ControlCalidadReclamoGarantiaBuscarForm, self).__init__(*args, **kwargs)
        self.fields['estado'].initial = filtro_estado
        self.fields['cliente'].initial = filtro_cliente
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control field-lineal'


class ControlCalidadReclamoGarantiaEncargadoForm(BSModalModelForm):
    class Meta:
        model = ControlCalidadReclamoGarantia
        fields = (
            'encargado',
            )

    def __init__(self, *args, **kwargs):
        super(ControlCalidadReclamoGarantiaEncargadoForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


######################### SALIDA RECLAMO GARANTÍA ##############################################


class SalidaReclamoGarantiaBuscarForm(forms.Form):
    estado = forms.ChoiceField(choices=((None,'------------'),) + ESTADOS_SALIDA_RECLAMO_GARANTIA, required=False)
    cliente = forms.ModelChoiceField(queryset=Cliente.objects.all(), required=False)

    def __init__(self, *args, **kwargs):
        filtro_estado = kwargs.pop('filtro_estado')
        filtro_cliente = kwargs.pop('filtro_cliente')
        super(SalidaReclamoGarantiaBuscarForm, self).__init__(*args, **kwargs)
        self.fields['estado'].initial = filtro_estado
        self.fields['cliente'].initial = filtro_cliente
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control field-lineal'


class SalidaReclamoGarantiaEncargadoForm(BSModalModelForm):
    class Meta:
        model = SalidaReclamoGarantia
        fields = (
            'encargado',
            )

    def __init__(self, *args, **kwargs):
        super(SalidaReclamoGarantiaEncargadoForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
