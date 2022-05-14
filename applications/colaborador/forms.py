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
            visible.field.widget.attrs['class'] = 'form-control'
        self.fields['asignacion_familiar'].widget.attrs['class'] = 'form-check-input'

class DatosContratoActualizarPlanillaForm(BSModalModelForm):
    class Meta:
        model = DatosContratoPlanilla
        fields=(
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
        super(DatosContratoActualizarPlanillaForm, self).__init__(*args, **kwargs)          
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        self.fields['asignacion_familiar'].widget.attrs['class'] = 'form-check-input'

class DatosContratoPlanillaDarBajaForm(BSModalModelForm):
    class Meta:
        model = DatosContratoPlanilla
        fields = (
            'fecha_baja',
            )
        widgets = {
            'fecha_baja': forms.DateInput(
                attrs ={
                    'type':'date',
                    },
                format = '%Y-%m-%d',
                ), 
        }


    def clean_fecha_baja(self):
        fecha_baja = self.cleaned_data.get('fecha_baja')
        fecha_alta = self.instance.fecha_alta

        
        if fecha_baja == None:
            texto = 'Ingresar fecha de baja.'
            self.add_error('fecha_baja', texto)

        try:
            if fecha_alta > fecha_baja:
                texto = 'Fecha de baja no puede ser menor a la fecha de alta del contrato por planilla.'
                self.add_error('fecha_baja', texto)
        except:
            pass
        
        return fecha_baja
    
    def __init__(self, *args, **kwargs):
        super(DatosContratoPlanillaDarBajaForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'



class DatosContratoHonorariosForm(BSModalModelForm):
    class Meta:
        model = DatosContratoHonorarios
        fields=(
            'usuario',
            'sociedad',
            'fecha_alta',
            'sueldo',
            'cargo',
            'suspension_cuarta',
            'year',
            'archivo_suspension_cuarta',
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
        super(DatosContratoHonorariosForm, self).__init__(*args, **kwargs)          
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        self.fields['suspension_cuarta'].widget.attrs['class'] = 'form-check-input'

class DatosContratoActualizarHonorariosForm(BSModalModelForm):
    class Meta:
        model = DatosContratoHonorarios
        fields=(
            'fecha_alta',
            'sueldo',
            'cargo',
            'suspension_cuarta',
            'year',
            'archivo_suspension_cuarta',
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
        super(DatosContratoActualizarHonorariosForm, self).__init__(*args, **kwargs)          
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        self.fields['suspension_cuarta'].widget.attrs['class'] = 'form-check-input'

class DatosContratoHonorariosDarBajaForm(BSModalModelForm):
    class Meta:
        model = DatosContratoHonorarios
        fields = (
            'fecha_baja',
            )
        widgets = {
            'fecha_baja': forms.DateInput(
                attrs ={
                    'type':'date',
                    },
                format = '%Y-%m-%d',
                ), 
        }


    def clean_fecha_baja(self):
        fecha_baja = self.cleaned_data.get('fecha_baja')
        fecha_alta = self.instance.fecha_alta

        
        if fecha_baja == None:
            texto = 'Ingresar fecha de baja.'
            self.add_error('fecha_baja', texto)

        try:
            if fecha_alta > fecha_baja:
                texto = 'Fecha de baja no puede ser menor a la fecha de alta del contrato.'
                self.add_error('fecha_baja', texto)
        except:
            pass
        
        return fecha_baja
    
    def __init__(self, *args, **kwargs):
        super(DatosContratoHonorariosDarBajaForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

