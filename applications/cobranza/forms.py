from django import forms
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
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


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
        print("***************************************")
        print(self.instance.id)
        print(type(self.instance.id))
        print("***************************************")
        if self.instance.id:
            print("//////////////////////")
            ingreso = Ingreso.objects.get(id=self.instance.id_registro)
            self.fields['ingresos'].initial = ingreso
            print("//////////////////////")
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'