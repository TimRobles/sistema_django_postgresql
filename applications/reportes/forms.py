from django import forms
from applications.datos_globales.models import Departamento
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
    CHOICES_TIPO = [
        (1, 'STOCK DISPONIBLE'),
        (2, 'STOCK MALOGRADO'),
    ]
    sociedad = forms.ModelChoiceField(queryset=Sociedad.objects.all(), required=True)
    tipo = forms.ChoiceField(choices=CHOICES_TIPO, required=True)

    def __init__(self, *args, **kwargs):
        super(ReporteStockSociedadPdfForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class ReporteVentasDepartamentoPdfForm(forms.Form):
    CHOICES_TIPO = [
        (1, 'VENTA POR DEPARTAMENTO'),
    ]
    fecha_inicio = forms.DateField(
        required=True,
        widget = forms.DateInput(
                attrs ={
                    'type':'date',
                    },
                format = '%Y-%m-%d',
                )
        )
    fecha_fin = forms.DateField(
        required=True,
        widget = forms.DateInput(
                attrs ={
                    'type':'date',
                    },
                format = '%Y-%m-%d',
                )
        )
    departamento = forms.ModelChoiceField(queryset=Departamento.objects.all(), required=False)
    tipo = forms.ChoiceField(choices=CHOICES_TIPO, required=True)

    def __init__(self, *args, **kwargs):
        super(ReporteVentasDepartamentoPdfForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'