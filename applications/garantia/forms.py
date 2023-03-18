from datetime import date
from django import forms
from django.contrib.contenttypes.models import ContentType
from applications.calidad.models import FallaMaterial, HistorialEstadoSerie, SolucionMaterial
from bootstrap_modal_forms.forms import BSModalForm, BSModalModelForm
from applications.sociedad.models import Sociedad
from applications.variables import ESTADOS_DOCUMENTO,ESTADOS_CONTROL_RECLAMO_GARANTIA,ESTADOS_SALIDA_RECLAMO_GARANTIA
from applications.garantia.models import IngresoReclamoGarantia, ControlCalidadReclamoGarantia, SalidaReclamoGarantia, SerieIngresoReclamoGarantiaDetalle, SerieReclamoHistorial
from applications.sede.models import Sede
from applications.material.models import Material
from applications.clientes.models import Cliente, ClienteInterlocutor, InterlocutorCliente
from applications.garantia.models import IngresoReclamoGarantia, IngresoReclamoGarantiaDetalle

class IngresoReclamoGarantiaBuscarForm(forms.Form):
    fecha_ingreso = forms.DateField(required=False, widget=forms.DateInput(attrs ={'type':'date',},format = '%Y-%m-%d',))
    nro_ingreso_reclamo_garantia = forms.IntegerField(required=False)
    cliente = forms.ModelChoiceField(queryset=Cliente.objects.all(), required=False)
    sociedad = forms.ModelChoiceField(queryset=Sociedad.objects.all(), required=False)
    
    def __init__(self, *args, **kwargs):
        filtro_fecha_ingreso = kwargs.pop('filtro_fecha_ingreso')
        filtro_nro_ingreso_reclamo_garantia = kwargs.pop('filtro_nro_ingreso_reclamo_garantia')
        filtro_cliente = kwargs.pop('filtro_cliente')
        filtro_sociedad = kwargs.pop('filtro_sociedad')

        super(IngresoReclamoGarantiaBuscarForm, self).__init__(*args, **kwargs)

        self.fields['fecha_ingreso'].initial = filtro_fecha_ingreso
        self.fields['nro_ingreso_reclamo_garantia'].initial = filtro_nro_ingreso_reclamo_garantia
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

class IngresoReclamoGarantiaAlmacenForm(BSModalModelForm):
    class Meta:
        model = IngresoReclamoGarantia
        fields = (
            'almacen',
            )

    def __init__(self, *args, **kwargs):
        super(IngresoReclamoGarantiaAlmacenForm, self).__init__(*args, **kwargs)
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
    class Meta:
        model = IngresoReclamoGarantiaDetalle
        fields=(
            'material',
            'cantidad',
            )

    def __init__(self, *args, **kwargs):
        super(IngresoReclamoGarantiaMaterialForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        self.fields['cantidad'].widget.attrs['min'] = 0
        self.fields['cantidad'].widget.attrs['step'] = 0.001


class  IngresoReclamoGarantiaMaterialUpdateForm(BSModalModelForm):
    class Meta:
        model = IngresoReclamoGarantiaDetalle
        fields=(
            'cantidad',
            )

    def __init__(self, *args, **kwargs):
        super(IngresoReclamoGarantiaMaterialUpdateForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        self.fields['cantidad'].widget.attrs['min'] = 0
        self.fields['cantidad'].widget.attrs['step'] = 0.001


class SerieIngresoReclamoGarantiaDetalleForm(forms.Form):
    serie_base = forms.CharField(label='Nro. Serie', max_length=200, required=False)
    class Meta:
        fields=(
            'serie_base',
            )

    def __init__(self, *args, **kwargs):
        filtro_serie_base = kwargs.pop('filtro_serie_base')
        super(SerieIngresoReclamoGarantiaDetalleForm, self).__init__(*args, **kwargs)
        self.fields['serie_base'].initial = filtro_serie_base
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class SerieIngresoReclamoGarantiaComentarioForm(BSModalModelForm):
    class Meta:
        model = SerieIngresoReclamoGarantiaDetalle
        fields=(
            'comentario',
            )

    def __init__(self, *args, **kwargs):
        super(SerieIngresoReclamoGarantiaComentarioForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


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


class ControlCalidadReclamoGarantiaObservacionForm(BSModalModelForm):
    class Meta:
        model = ControlCalidadReclamoGarantia
        fields = (
            'observacion',
        )

    def __init__(self, *args, **kwargs):
        super(ControlCalidadReclamoGarantiaObservacionForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class RegistrarFallaCreateForm(BSModalForm):
    falla_material = forms.ModelChoiceField(queryset=FallaMaterial.objects.all())
    observacion = forms.CharField(widget=forms.Textarea(), required=False)
    class Meta:
        model = SerieReclamoHistorial
        fields = (
            'falla_material',
            'observacion',
        )

    def __init__(self, *args, **kwargs):
        fallas = kwargs.pop('fallas')
        super(RegistrarFallaCreateForm, self).__init__(*args, **kwargs)
        self.fields['falla_material'].queryset = fallas
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class RegistrarFallaUpdateForm(BSModalModelForm):
    class Meta:
        model = HistorialEstadoSerie
        fields = (
            'falla_material',
            'observacion',
        )

    def __init__(self, *args, **kwargs):
        fallas = kwargs.pop('fallas')
        super(RegistrarFallaUpdateForm, self).__init__(*args, **kwargs)
        self.fields['falla_material'].queryset = fallas
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class RegistrarSolucionCreateForm(BSModalForm):
    solucion = forms.ModelChoiceField(queryset=SolucionMaterial.objects.all())
    observacion = forms.CharField(widget=forms.Textarea(), required=False)
    comentario = forms.CharField(widget=forms.Textarea(), required=False)
    class Meta:
        model = SerieReclamoHistorial
        fields = (
            'solucion',
            'observacion',
            'comentario',
        )

    def __init__(self, *args, **kwargs):
        soluciones = kwargs.pop('soluciones')
        super(RegistrarSolucionCreateForm, self).__init__(*args, **kwargs)
        self.fields['solucion'].queryset = soluciones
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class RegistrarSolucionUpdateForm(BSModalModelForm):
    comentario = forms.CharField(widget=forms.Textarea(), required=False)
    class Meta:
        model = HistorialEstadoSerie
        fields = (
            'solucion',
            'observacion',
            'comentario',
        )

    def __init__(self, *args, **kwargs):
        soluciones = kwargs.pop('soluciones')
        comentario = kwargs.pop('comentario')
        super(RegistrarSolucionUpdateForm, self).__init__(*args, **kwargs)
        self.fields['solucion'].queryset = soluciones
        self.fields['comentario'].initial = comentario
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
            'observacion',
            )

    def __init__(self, *args, **kwargs):
        super(SalidaReclamoGarantiaEncargadoForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'



class SalidaReclamoGarantiaObservacionForm(BSModalModelForm):
    class Meta:
        model = SalidaReclamoGarantia
        fields = (
            'observacion',
        )

    def __init__(self, *args, **kwargs):
        super(SalidaReclamoGarantiaObservacionForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'