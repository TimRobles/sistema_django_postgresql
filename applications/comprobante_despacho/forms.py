from datetime import date
from django import forms
from bootstrap_modal_forms.forms import BSModalForm, BSModalModelForm
from applications.envio_clientes.models import Transportista
from applications.comprobante_despacho.models import Guia, GuiaDetalle
from applications.clientes.models import ClienteInterlocutor, InterlocutorCliente
from applications.datos_globales.models import Distrito, SeriesComprobante
from applications.sede.models import Sede
from django.contrib.contenttypes.models import ContentType


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


class GuiaDetallePesoForm(BSModalModelForm):
    class Meta:
        model = GuiaDetalle
        fields=(
            'peso',
            )

    def __init__(self, *args, **kwargs):
        super(GuiaDetallePesoForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class GuiaPartidaForm(BSModalModelForm):
    direcciones = forms.ChoiceField(choices=[None], required=False)
    ubigeo = forms.ModelChoiceField(queryset=Distrito.objects.none(), required=False)
    class Meta:
        model = Guia
        fields=(
            'direcciones',
            'direccion_partida',
            'ubigeo',
            )

    def __init__(self, *args, **kwargs):
        lista = kwargs.pop('lista')
        super(GuiaPartidaForm, self).__init__(*args, **kwargs)
        self.fields['direcciones'].choices = lista
        if self.instance.ubigeo_partida:
            self.fields['ubigeo'].queryset = Distrito.objects.filter(codigo=self.instance.ubigeo_partida.codigo)
            self.fields['ubigeo'].initial = self.instance.ubigeo_partida
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        if 'ubigeo' in self.data:
            self.fields['ubigeo'].queryset=Distrito.objects.all()


class GuiaDestinoForm(BSModalModelForm):
    direcciones = forms.ChoiceField(choices=[None], required=False)
    ubigeo = forms.ModelChoiceField(queryset=Distrito.objects.none(), required=False)
    class Meta:
        model = Guia
        fields=(
            'direcciones',
            'direccion_destino',
            'ubigeo',
            )

    def __init__(self, *args, **kwargs):
        lista = kwargs.pop('lista')
        super(GuiaDestinoForm, self).__init__(*args, **kwargs)
        self.fields['direcciones'].choices = lista
        if self.instance.ubigeo_destino:
            self.fields['ubigeo'].queryset = Distrito.objects.filter(codigo=self.instance.ubigeo_destino.codigo)
            self.fields['ubigeo'].initial = self.instance.ubigeo_destino
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        if 'ubigeo' in self.data:
            self.fields['ubigeo'].queryset=Distrito.objects.all()


class GuiaSerieForm(BSModalModelForm):
    class Meta:
        model = Guia
        fields = (
            'serie_comprobante',
            )

    def __init__(self, *args, **kwargs):
        super(GuiaSerieForm, self).__init__(*args, **kwargs)
        self.fields['serie_comprobante'].queryset = SeriesComprobante.objects.filter(tipo_comprobante=ContentType.objects.get_for_model(Guia), mostrar=True)
        self.fields['serie_comprobante'].required = True
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
            'conductor_nombre',
            'conductor_apellidos',
            'conductor_numero_licencia',
            'placa_numero',
            )

    def __init__(self, *args, **kwargs):
        super(GuiaConductorForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.required = False


class GuiaMotivoTrasladoForm(BSModalModelForm):
    class Meta:
        model = Guia
        fields=(
            'motivo_traslado',
            )

    def __init__(self, *args, **kwargs):
        super(GuiaMotivoTrasladoForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class GuiaFechaTrasladoForm(BSModalModelForm):
    class Meta:
        model = Guia
        fields = (
            'fecha_traslado',
            )

        widgets = {
            'fecha_traslado' : forms.DateInput(
                attrs ={
                    'type':'date',
                    },
                format = '%Y-%m-%d',
                ),
            }
    
    def clean_fecha_traslado(self):
        fecha_traslado = self.cleaned_data.get('fecha_traslado')
        if fecha_traslado < date.today():
            self.add_error('fecha_traslado', 'La fecha de baja no puede ser menor a la fecha de hoy.')
        return fecha_traslado

    def __init__(self, *args, **kwargs):
        super(GuiaFechaTrasladoForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.required = True


class GuiaClienteForm(BSModalModelForm):
    class Meta:
        model = Guia
        fields = (
            'cliente_interlocutor',
            )

    def __init__(self, *args, **kwargs):
        interlocutor_queryset = kwargs.pop('interlocutor_queryset')
        interlocutor = kwargs.pop('interlocutor')
        super(GuiaClienteForm, self).__init__(*args, **kwargs)
        self.fields['cliente_interlocutor'].queryset = interlocutor_queryset
        self.fields['cliente_interlocutor'].initial = interlocutor
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class GuiaAnularForm(BSModalModelForm):
    class Meta:
        model = Guia
        fields = (
            'motivo_anulacion',
            )

    def __init__(self, *args, **kwargs):
        super(GuiaAnularForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'