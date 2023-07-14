from django import forms
from bootstrap_modal_forms.forms import BSModalModelForm
from applications.sociedad.models import Sociedad
from applications.clientes.models import Cliente

class ReportesFiltrosForm(forms.Form):
    sociedad = forms.ModelChoiceField(queryset=Sociedad.objects.all())
    fecha_inicio = forms.DateField(
        required=False,
        widget = forms.DateInput(
                attrs ={
                    'type':'date',
                    },
                format = '%Y-%m-%d',
                )
        )
    fecha_fin = forms.DateField(
        required=False,
        widget = forms.DateInput(
                attrs ={
                    'type':'date',
                    },
                format = '%Y-%m-%d',
                )
        )
    cliente = forms.ModelChoiceField(queryset=Cliente.objects.filter(estado_sunat = 1))

    def __init__(self, *args, **kwargs):
        filtro_sociedad = kwargs.pop('filtro_sociedad')
        filtro_fecha_inicio = kwargs.pop('filtro_fecha_inicio')
        filtro_fecha_fin = kwargs.pop('filtro_fecha_fin')
        filtro_cliente = kwargs.pop('filtro_cliente')
        super(ReportesFiltrosForm, self).__init__(*args, **kwargs)
        self.fields['sociedad'].initial = filtro_sociedad
        self.fields['sociedad'].required = False
        self.fields['fecha_inicio'].initial = filtro_fecha_inicio
        self.fields['fecha_fin'].initial = filtro_fecha_fin
        self.fields['cliente'].initial = filtro_cliente
        self.fields['cliente'].required = False
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class ReporteStockSociedadPdfForm(forms.Form):
    sociedad = forms.ModelChoiceField(queryset=Sociedad.objects.all())

    def __init__(self, *args, **kwargs):
        super(ReporteStockSociedadPdfForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'