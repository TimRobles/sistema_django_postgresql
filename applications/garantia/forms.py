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
    
    class Meta:
        fields = (
            'fecha_ingreso',
            'nro_ingreso_garantia',
            'cliente',
            'sociedad',
            'estado',
            )

    def __init__(self, *args, **kwargs):
        super(IngresoGarantiaBuscarForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'