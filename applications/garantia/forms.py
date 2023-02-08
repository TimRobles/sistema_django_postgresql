from datetime import date
from django import forms
from applications.sociedad.models import Sociedad
from applications.variables import ESTADOS_DOCUMENTO
from bootstrap_modal_forms.forms import BSModalForm, BSModalModelForm
from applications.garantia.models import IngresoReclamoGarantia, ControlCalidadReclamoGarantia, SalidaReclamoGarantia
from applications.sede.models import Sede
from django.contrib.contenttypes.models import ContentType
from applications.clientes.models import Cliente


class IngresoGarantiaBuscarForm(forms.Form):
    fecha_ingreso = forms.DateField(required=False, widget=forms.DateInput(attrs ={'type':'date',},format = '%Y-%m-%d',))
    nro_ingreso_garantia = forms.IntegerField(required=False)
    cliente = forms.ModelChoiceField(queryset=Cliente.objects.all(), required=False)
    sociedad = forms.ModelChoiceField(queryset=Sociedad.objects.all(), required=False)
    estado = forms.ChoiceField(choices=((None, '-------------------'),) + ESTADOS_DOCUMENTO, required=False)

    def __init__(self, *args, **kwargs):
        filtro_fecha_ingreso = kwargs.pop('filtro_fecha_ingreso')
        filtro_nro_ingreso_garantia = kwargs.pop('filtro_nro_ingreso_garantia')
        filtro_cliente = kwargs.pop('filtro_cliente')
        filtro_sociedad = kwargs.pop('filtro_sociedad')
        filtro_estado = kwargs.pop('filtro_estado')
        super(IngresoGarantiaBuscarForm, self).__init__(*args, **kwargs)
        self.fields['fecha_ingreso'].initial = filtro_fecha_ingreso
        self.fields['numero_ingreso_garantia'].initial = filtro_nro_ingreso_garantia
        self.fields['cliente'].initial = filtro_cliente
        self.fields['sociedad'].initial = filtro_sociedad
        self.fields['estado'].initial = filtro_estado
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control field-lineal'