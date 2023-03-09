from datetime import date
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from bootstrap_modal_forms.forms import BSModalForm, BSModalModelForm

from applications.variables import ESTADOS_CONFIRMACION
from applications.material.models import Material
from applications.usuario.models import DatosUsuario
from applications.sociedad.models import Sociedad
from .models import (
    ComisionFondoPensiones,
    DatosPlanilla,
    EsSalud,
    BoletaPago)


class ComisionFondoPensionesForm(BSModalModelForm):
    class Meta:
        model = ComisionFondoPensiones
        fields = (
            'fondo_pensiones',
            'fecha_vigencia',
            'aporte_obligatorio',
            'comision_flujo',
            'comision_flujo_mixta',
            'prima_seguro',
            )
        widgets = {
            'fecha_vigencia' : forms.DateInput(
                attrs ={
                    'type':'date',
                    },
                format = '%Y-%m-%d',
                ),
            }

    def __init__(self, *args, **kwargs):
        super(ComisionFondoPensionesForm, self).__init__(*args, **kwargs)
        if not self.fields['fecha_vigencia'].initial:
            self.fields['fecha_vigencia'].initial = date.today()
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class DatosPlanillaForm(BSModalModelForm):
    class Meta:
        model = DatosPlanilla
        fields = (
            'usuario',
            'sociedad',
            'fecha_inicio',
            'sueldo_bruto',
            'moneda',
            'movilidad',
            'planilla',
            'suspension_cuarta',
            'fondo_pensiones',
            'tipo_comision',
            'asignacion_familiar',
            'area',
            'cargo',
            )
        widgets = {
            'fecha_inicio' : forms.DateInput(
                attrs ={
                    'type':'date',
                    },
                format = '%Y-%m-%d',
                ),
            }

    def __init__(self, *args, **kwargs):
        super(DatosPlanillaForm, self).__init__(*args, **kwargs)
        self.fields['usuario'].queryset = get_user_model().objects.filter(is_active=1)      
        self.fields['sociedad'].queryset = Sociedad.objects.filter(estado_sunat=1)    

        if not self.fields['fecha_inicio'].initial:
            self.fields['fecha_inicio'].initial = date.today()
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        self.fields['planilla'].widget.attrs['class'] = 'form-check-input'
        self.fields['suspension_cuarta'].widget.attrs['class'] = 'form-check-input'
        self.fields['asignacion_familiar'].widget.attrs['class'] = 'form-check-input'

class DatosPlanillaDarBajaForm(BSModalModelForm):
    class Meta:
        model = DatosPlanilla
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

    
    def __init__(self, *args, **kwargs):
        super(DatosPlanillaDarBajaForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class EsSaludForm(BSModalModelForm):
    class Meta:
        model = EsSalud
        fields = (
            'fecha_inicio',
            'porcentaje',
            'ley30334',
            )
        widgets = {
            'fecha_inicio' : forms.DateInput(
                attrs ={
                    'type':'date',
                    },
                format = '%Y-%m-%d',
                ),
            }

    def __init__(self, *args, **kwargs):
        super(EsSaludForm, self).__init__(*args, **kwargs)
        if not self.fields['fecha_inicio'].initial:
            self.fields['fecha_inicio'].initial = date.today()
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        self.fields['ley30334'].widget.attrs['class'] = 'form-check-input'


class BoletaPagoForm(BSModalModelForm):
    class Meta:
        model = BoletaPago
        fields = (
            'datos_planilla',
            'year',
            'month',
            'tipo',
            'haber_mensual',
            'lic_con_goce_haber',
            'dominical',
            'movilidad',
            'asig_familiar',
            'vacaciones',
            'gratificacion',
            'ley29351',
            'bonif_1mayo',
            'essalud',
            'aporte_obligatorio',
            'comision_porcentaje',
            'prima_seguro',
            'impuesto_quinta',
            'neto_recibido',
            )

    def __init__(self, *args, **kwargs):
        super(BoletaPagoForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
