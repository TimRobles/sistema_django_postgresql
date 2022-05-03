from datetime import date
from django import forms

from .models import Visita

from bootstrap_modal_forms.forms import BSModalForm, BSModalModelForm

class VisitaForm(BSModalModelForm):
    class Meta:
        model = Visita
        fields=(
            'nombre',
            'tipo_documento',
            'numero_documento',
            'usuario_atendio',
            'motivo_visita',
            'empresa_cliente',
            )
        widgets = {
            'fecha_registro' : forms.DateInput(
                attrs ={
                    'type':'date',
                    },
                format = '%Y-%m-%d',
                ),
        }

    def __init__(self, *args, **kwargs):
        super(VisitaForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class VisitaBuscarForm(forms.Form):
    nombre = forms.CharField(max_length=50, required=False)
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
        filtro_nombre = kwargs.pop('filtro_nombre')
        filtro_fecha = kwargs.pop('filtro_fecha')
        super(VisitaBuscarForm, self).__init__(*args, **kwargs)
        self.fields['nombre'].initial = filtro_nombre
        self.fields['fecha'].initial = filtro_fecha
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'