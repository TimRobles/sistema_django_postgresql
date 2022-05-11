from datetime import date
from django import forms

from .models import DatosContratoPlanilla, DatosContratoHonorarios
from bootstrap_modal_forms.forms import BSModalForm, BSModalModelForm


class DatosContratoPlanillaForm(BSModalModelForm):
    class Meta:
        model = DatosContratoPlanilla
        fields=(
            'usuario',
            'sociedad',
            'fecha_alta',
            'sueldo_bruto',
            'cargo',
            'movilidad',
            'asignacion_familiar',
            'archivo_contrato',
            )

        widgets = {
            'fecha_alta' : forms.DateInput(
                attrs ={
                    'type':'date',
                    },
                format = '%Y-%m-%d',
                
                ),
        }

    def __init__(self, *args, **kwargs):
        super(DatosContratoPlanillaForm, self).__init__(*args, **kwargs)          
        for visible in self.visible_fields():
            if visible.field != self.fields['asignacion_familiar']:
                visible.field.widget.attrs['class'] = 'form-control'

                

class DatosContratoHonorariosForm(BSModalModelForm):
    class Meta:
        model = DatosContratoHonorarios
        fields=(
            'usuario',
            'sociedad',
            'fecha_alta',
            'sueldo',
            'suspension_cuarta',
            'archivo_suspension_cuarta',
            'archivo_contrato',
            'cargo',
            )

        widgets = {
            'fecha_alta' : forms.DateInput(
                attrs ={
                    'type':'date',
                    },
                format = '%Y-%m-%d',
                
                ),
        }

    def __init__(self, *args, **kwargs):
        super(DatosContratoHonorariosForm, self).__init__(*args, **kwargs)          
        for visible in self.visible_fields():
            if visible.field != self.fields['suspension_cuarta']:
                visible.field.widget.attrs['class'] = 'form-control'

