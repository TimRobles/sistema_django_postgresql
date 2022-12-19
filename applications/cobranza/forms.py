from django import forms
from applications.funciones import tipo_de_cambio
from bootstrap_modal_forms.forms import BSModalForm, BSModalModelForm
from applications.cobranza.models import Deuda, Ingreso, LineaCredito, Pago

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
            'deuda',
            'monto',
            'tipo_cambio',
            )

    def __init__(self, *args, **kwargs):
        tipo_cambio = kwargs.pop('tipo_cambio')
        lista_deudas = kwargs.pop('lista_deudas')
        super(CuentaBancariaIngresoPagarForm, self).__init__(*args, **kwargs)   
        if not self.fields['tipo_cambio'].initial:
            self.fields['tipo_cambio'].initial = tipo_cambio
        self.fields['deuda'].queryset = Deuda.objects.filter(id__in=lista_deudas)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class DeudaPagarForm(BSModalModelForm):
    ingresos = forms.ModelChoiceField(queryset=Ingreso.objects.all())
    class Meta:
        model = Pago
        fields = (
            'ingresos',
            'monto',
            'tipo_cambio',
            )

    def __init__(self, *args, **kwargs):
        tipo_cambio = kwargs.pop('tipo_cambio')
        lista_ingresos = kwargs.pop('lista_ingresos')
        super(DeudaPagarForm, self).__init__(*args, **kwargs)   
        if not self.fields['tipo_cambio'].initial:
            self.fields['tipo_cambio'].initial = tipo_cambio
        self.fields['ingresos'].queryset = Ingreso.objects.filter(id__in=lista_ingresos)
        if self.instance.id:
            ingreso = Ingreso.objects.get(id=self.instance.id_registro)
            self.fields['ingresos'].initial = ingreso
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class ClienteBuscarForm(forms.Form):
    razon_social = forms.CharField(label = 'Cliente', max_length=100, required=False)

    def __init__(self, *args, **kwargs):
        filtro_razon_social = kwargs.pop('filtro_razon_social')
        super(ClienteBuscarForm, self).__init__(*args, **kwargs)
        self.fields['razon_social'].initial = filtro_razon_social
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class DepositosBuscarForm(forms.Form):
    numero_operacion = forms.CharField(label = 'Razón Social', max_length=100, required=False)

    def __init__(self, *args, **kwargs):
        filtro_numero_operacion = kwargs.pop('filtro_numero_operacion')
        super(DepositosBuscarForm, self).__init__(*args, **kwargs)
        self.fields['numero_operacion'].initial = filtro_numero_operacion
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'