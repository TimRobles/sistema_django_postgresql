from django import forms
from applications.clientes.models import Cliente
from applications.datos_globales.models import CuentaBancariaSociedad, Moneda
from applications.funciones import tipo_de_cambio
from applications.sociedad.models import Sociedad
from bootstrap_modal_forms.forms import BSModalForm, BSModalModelForm
from applications.cobranza.models import Deuda, Ingreso, LineaCredito, Nota, Pago

class LineaCreditoForm(BSModalModelForm):
    class Meta:
        model = LineaCredito
        fields=(
            'cliente',
            'monto',
            'moneda',
            'condiciones_pago',
            'condiciones_pago',
            )

    def __init__(self, *args, **kwargs):
        super(LineaCreditoForm, self).__init__(*args, **kwargs)   
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class CuentaBancariaIngresoCambiarForm(BSModalModelForm):
    class Meta:
        model = Ingreso
        fields=(
            'cuenta_bancaria',
            'numero_operacion',
            'cuenta_origen',
            'comentario',
            'comision',
            'voucher',
            'tipo_cambio',
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
        super(CuentaBancariaIngresoCambiarForm, self).__init__(*args, **kwargs)   
        if not self.fields['tipo_cambio'].initial:
            self.fields['tipo_cambio'].initial = tipo_de_cambio()
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class CuentaBancariaIngresoForm(BSModalModelForm):
    class Meta:
        model = Ingreso
        fields=(
            'fecha',
            'monto',
            'numero_operacion',
            'cuenta_origen',
            'comentario',
            'comision',
            'voucher',
            'es_pago',
            'tipo_cambio',
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
        super(CuentaBancariaIngresoForm, self).__init__(*args, **kwargs)   
        if not self.fields['tipo_cambio'].initial:
            self.fields['tipo_cambio'].initial = tipo_de_cambio()
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        self.fields['es_pago'].widget.attrs['class'] = 'form-check-input'


class CuentaBancariaEfectivoIngresoForm(BSModalModelForm):
    class Meta:
        model = Ingreso
        fields=(
            'fecha',
            'monto',
            'comentario',
            'es_pago',
            'tipo_cambio',
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
        super(CuentaBancariaEfectivoIngresoForm, self).__init__(*args, **kwargs)   
        if not self.fields['tipo_cambio'].initial:
            self.fields['tipo_cambio'].initial = tipo_de_cambio()
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        self.fields['es_pago'].widget.attrs['class'] = 'form-check-input'


class CuentaBancariaIngresoPagarForm(BSModalModelForm):
    class Meta:
        model = Pago
        fields = (
            'monto',
            'deuda',
            'tipo_cambio',
            )
    def clean_monto(self):
        monto = self.cleaned_data.get('monto')
        self.fields['deuda'].queryset = Deuda.objects.all()
    
        return monto

    def __init__(self, *args, **kwargs):
        tipo_cambio = kwargs.pop('tipo_cambio')
        super(CuentaBancariaIngresoPagarForm, self).__init__(*args, **kwargs)   
        try:
            deuda = self.instance.deuda
            self.fields['deuda'].queryset = Deuda.objects.filter(id=deuda.id)
            self.fields['deuda'].initial = deuda
        except:
            self.fields['tipo_cambio'].initial = tipo_cambio
            self.fields['deuda'].queryset = Deuda.objects.none()

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class DeudaNotaForm(BSModalModelForm):
    nota = forms.ModelChoiceField(queryset=Nota.objects.none())
    class Meta:
        model = Pago
        fields = (
            'monto',
            'nota',
            'tipo_cambio',
            )

    def clean_monto(self):
        monto = self.cleaned_data.get('monto')
        self.fields['nota'].queryset = Nota.objects.all()
    
        return monto

    def __init__(self, *args, **kwargs):
        tipo_cambio = kwargs.pop('tipo_cambio')
        super(DeudaNotaForm, self).__init__(*args, **kwargs)   
        try:
            nota = Nota.objects.get(id=self.instance.id_registro)
            self.fields['nota'].queryset = Nota.objects.filter(id=nota.id)
            self.fields['nota'].initial = nota
            self.fields['nota'].help_text = 'Ingresa el monto de la Nota de Cŕedito'
        except:
            self.fields['tipo_cambio'].initial = tipo_cambio

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class DeudaPagarForm(BSModalModelForm):
    ingresos = forms.ModelChoiceField(queryset=Ingreso.objects.none())
    class Meta:
        model = Pago
        fields = (
            'monto',
            'ingresos',
            'tipo_cambio',
            )

    def clean_monto(self):
        monto = self.cleaned_data.get('monto')
        self.fields['ingresos'].queryset = Ingreso.objects.all()
    
        return monto

    def __init__(self, *args, **kwargs):
        tipo_cambio = kwargs.pop('tipo_cambio')
        super(DeudaPagarForm, self).__init__(*args, **kwargs)   
        try:
            # ingreso = self.instance.content_type.get_object_for_this_type(id=self.instance.id_registro)
            ingreso = Ingreso.objects.get(id=self.instance.id_registro)
            self.fields['ingresos'].queryset = Ingreso.objects.filter(id=ingreso.id)
            self.fields['ingresos'].initial = ingreso
            self.fields['ingresos'].help_text = 'Ingresa el Monto o Razon Social del Banco'
        except:
            self.fields['tipo_cambio'].initial = tipo_cambio

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class ClienteBuscarForm(forms.Form):
    razon_social = forms.CharField(label = 'Cliente', max_length=100, required=False)
    estado_cancelado = forms.ChoiceField(choices=[(1, 'TODOS'), (2, 'CON DEUDA'), (3, 'SIN DEUDA')], required=False)

    def __init__(self, *args, **kwargs):
        filtro_razon_social = kwargs.pop('filtro_razon_social')
        filtro_estado_cancelado = kwargs.pop('filtro_estado_cancelado')
        super(ClienteBuscarForm, self).__init__(*args, **kwargs)
        self.fields['razon_social'].initial = filtro_razon_social
        self.fields['estado_cancelado'].initial = filtro_estado_cancelado
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class DepositosBuscarForm(forms.Form):
    fecha = forms.DateField(required=False, widget=forms.DateInput(attrs ={'type':'date',},format = '%Y-%m-%d',))
    monto = forms.DecimalField(required=False)
    moneda = forms.ModelChoiceField(queryset=Moneda.objects.all(), required=False)
    cuenta_bancaria = forms.ModelChoiceField(queryset=CuentaBancariaSociedad.objects.all(), required=False)
    numero_operacion = forms.CharField(label = 'Número de Operación', max_length=100, required=False)
    comentario = forms.CharField(label = 'Comentario', max_length=100, required=False)
    pendiente_usar = forms.ChoiceField(choices=[(1, 'TODOS'),(2, 'PENDIENTE'),(3, 'USADO'),], required=False)
    foto = forms.ChoiceField(choices=[(1, 'TODOS'),(2, 'CON FOTO'),(3, 'SIN FOTO'),], required=False)

    def __init__(self, *args, **kwargs):
        filtro_fecha = kwargs.pop('filtro_fecha')
        filtro_monto = kwargs.pop('filtro_monto')
        filtro_moneda = kwargs.pop('filtro_moneda')
        filtro_cuenta_bancaria = kwargs.pop('filtro_cuenta_bancaria')
        filtro_numero_operacion = kwargs.pop('filtro_numero_operacion')
        filtro_comentario = kwargs.pop('filtro_comentario')
        filtro_pendiente_usar = kwargs.pop('filtro_pendiente_usar')
        filtro_foto = kwargs.pop('filtro_foto')
        super(DepositosBuscarForm, self).__init__(*args, **kwargs)
        self.fields['fecha'].initial = filtro_fecha
        self.fields['monto'].initial = filtro_monto
        self.fields['moneda'].initial = filtro_moneda
        self.fields['cuenta_bancaria'].initial = filtro_cuenta_bancaria
        self.fields['numero_operacion'].initial = filtro_numero_operacion
        self.fields['comentario'].initial = filtro_comentario
        self.fields['pendiente_usar'].initial = filtro_pendiente_usar
        self.fields['foto'].initial = filtro_foto
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control field-lineal'


class CuentaBancariaDetalleBuscarForm(forms.Form):
    fecha = forms.DateField(required=False, widget=forms.DateInput(attrs ={'type':'date',},format = '%Y-%m-%d',))
    monto = forms.DecimalField(required=False)
    numero_operacion = forms.CharField(label = 'Número de Operación', max_length=100, required=False)
    comentario = forms.CharField(label = 'Comentario', max_length=100, required=False)
    es_pago = forms.ChoiceField(choices=[(1, 'TODOS'),(2, 'ES PAGO'),(3, 'NO ES PAGO'),], required=False)
    foto = forms.ChoiceField(choices=[(1, 'TODOS'),(2, 'CON FOTO'),(3, 'SIN FOTO'),], required=False)

    def __init__(self, *args, **kwargs):
        filtro_fecha = kwargs.pop('filtro_fecha')
        filtro_monto = kwargs.pop('filtro_monto')
        filtro_numero_operacion = kwargs.pop('filtro_numero_operacion')
        filtro_comentario = kwargs.pop('filtro_comentario')
        filtro_es_pago = kwargs.pop('filtro_es_pago')
        filtro_foto = kwargs.pop('filtro_foto')
        super(CuentaBancariaDetalleBuscarForm, self).__init__(*args, **kwargs)
        self.fields['fecha'].initial = filtro_fecha
        self.fields['monto'].initial = filtro_monto
        self.fields['numero_operacion'].initial = filtro_numero_operacion
        self.fields['comentario'].initial = filtro_comentario
        self.fields['es_pago'].initial = filtro_es_pago
        self.fields['foto'].initial = filtro_foto
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control field-lineal'


class DeudaBuscarForm(forms.Form):
    fecha_deuda = forms.DateField(required=False, widget=forms.DateInput(attrs ={'type':'date',},format = '%Y-%m-%d',))
    monto = forms.DecimalField(required=False)
    moneda = forms.ModelChoiceField(queryset=Moneda.objects.all(), required=False)
    sociedad = forms.ModelChoiceField(queryset=Sociedad.objects.all(), required=False)
    numero_documento = forms.IntegerField(required=False)
    
    def __init__(self, *args, **kwargs):
        filtro_fecha_deuda = kwargs.pop('filtro_fecha_deuda')
        filtro_monto = kwargs.pop('filtro_monto')
        filtro_moneda = kwargs.pop('filtro_moneda')
        filtro_sociedad = kwargs.pop('filtro_sociedad')
        filtro_numero_documento = kwargs.pop('filtro_numero_documento')
        super(DeudaBuscarForm, self).__init__(*args, **kwargs)
        self.fields['fecha_deuda'].initial = filtro_fecha_deuda
        self.fields['monto'].initial = filtro_monto
        self.fields['moneda'].initial = filtro_moneda
        self.fields['sociedad'].initial = filtro_sociedad
        self.fields['numero_documento'].initial = filtro_numero_documento
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control field-lineal'


