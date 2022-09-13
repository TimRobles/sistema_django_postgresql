from django import forms
from bootstrap_modal_forms.forms import BSModalForm, BSModalModelForm
from applications.cobranza.models import LineaCredito

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
