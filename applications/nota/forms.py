from django import forms
from applications.comprobante_venta.models import BoletaVenta, FacturaVenta
from applications.nota.models import NotaCredito

from applications.sociedad.models import Sociedad
from applications.variables import CHOICE_VACIO
from bootstrap_modal_forms.forms import BSModalForm, BSModalModelForm


class NotaCreditoBuscarForm(forms.Form):
    cliente = forms.CharField(max_length=150, required=False)
    numero_nota = forms.CharField(max_length=10, required=False)
    sociedad = forms.ModelChoiceField(queryset=Sociedad.objects.filter(estado_sunat=1), required=False)
    fecha = forms.DateField(
        required=False,
        widget = forms.DateInput(
                attrs ={
                    'type':'date',
                    },
                format = '%Y-%m-%d',
                )
        )

    def __init__(self, *args, **kwargs):
        filtro_cliente = kwargs.pop('filtro_cliente')
        filtro_numero_nota = kwargs.pop('filtro_numero_nota')
        filtro_sociedad = kwargs.pop('filtro_sociedad')
        filtro_fecha = kwargs.pop('filtro_fecha')
        super(NotaCreditoBuscarForm, self).__init__(*args, **kwargs)
        self.fields['cliente'].initial = filtro_cliente
        self.fields['numero_nota'].initial = filtro_numero_nota
        self.fields['sociedad'].initial = filtro_sociedad
        self.fields['fecha'].initial = filtro_fecha
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class NotaCreditoCrearForm(BSModalForm):
    vacio = forms.CharField(required=False)
    factura = forms.ChoiceField(choices=CHOICE_VACIO, required=False)
    boleta = forms.ChoiceField(choices=CHOICE_VACIO, required=False)
    class Meta:
        fields = (
            'vacio',
            'factura',
            'boleta',
        )

    def clean_vacio(self):
        vacio = self.cleaned_data.get('vacio')
        factura = self.fields['factura']
        factura.choices = FacturaVenta.objects.values_list('id', 'id')
        boleta = self.fields['boleta']
        boleta.choices = BoletaVenta.objects.values_list('id', 'id')
        return vacio

    def clean(self):
        cleaned_data = super().clean()
        factura = cleaned_data.get('factura')
        boleta = cleaned_data.get('boleta')
        print(factura)
        print(boleta)
        if factura and boleta:
            self.add_error('factura', 'Solo puedes escoger 1 solo documento.')
            self.add_error('boleta', 'Solo puedes escoger 1 solo documento.')
            factura = self.fields['factura']
            factura.choices = CHOICE_VACIO
            boleta = self.fields['boleta']
            boleta.choices = CHOICE_VACIO
        return cleaned_data
        
    def __init__(self, *args, **kwargs):
        super(NotaCreditoCrearForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        self.fields['vacio'].widget.attrs['class'] = 'form-control ocultar'