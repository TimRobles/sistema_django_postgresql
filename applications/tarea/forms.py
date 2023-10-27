from typing import Any, Dict
from django import forms
from django.contrib.auth import get_user_model
from .models import TipoTarea, Tarea, HistorialComentarioTarea
from bootstrap_modal_forms.forms import BSModalForm, BSModalModelForm
from applications.crm.models import EventoCRM
from applications.datos_globales.models import Area
from applications.variables import ESTADO_TAREA, PRIORIDAD_TAREA
from applications.variables import CHOICE_VACIO
from django.conf import settings
from applications.clientes.models import Cliente

class TipoTareaForm(BSModalModelForm):
    class Meta:
        model = TipoTarea
        fields=(
            'nombre',
            )

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        nombre_minuscula = nombre.lower()
        if TipoTarea.objects.filter(nombre__iexact=nombre_minuscula).exists():
            raise forms.ValidationError('Tipo de tarea ya existe.')
        return nombre       

    def __init__(self, *args, **kwargs):
        super(TipoTareaForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.required = True
            

class TareaBuscarForm(forms.Form):
    fecha_inicio = forms.DateField(
        required=False,
        widget = forms.DateInput(
                attrs ={
                    'type':'date',
                    },
                format = '%Y-%m-%d',
                )
        )
    estado = forms.ChoiceField(choices=((None, '--------------------'),) + ESTADO_TAREA, required=False)
    encargado = forms.ModelChoiceField(queryset=get_user_model().objects, required=False)
    apoyo = forms.ModelChoiceField(queryset=get_user_model().objects, required=False)
    tipo_tarea = forms.ModelChoiceField(queryset=TipoTarea.objects.all(), required=False)
    fecha_inicio_real = forms.DateField(
        required=False,
        widget = forms.DateInput(
                attrs ={
                    'type':'date',
                    },
                format = '%Y-%m-%d',
                )
        )    
    
    fecha_cierre= forms.DateField(
        required=False,
        widget = forms.DateInput(
                attrs ={
                    'type':'date',
                    },
                format = '%Y-%m-%d',
                )
        )
    def __init__(self, *args, **kwargs):
        filtro_fecha_inicio = kwargs.pop('filtro_fecha_inicio')
        filtro_estado = kwargs.pop('filtro_estado')
        filtro_tipo_tarea = kwargs.pop('filtro_tipo_tarea')

        filtro_fecha_inicio_real = kwargs.pop('filtro_fecha_inicio_real')
        filtro_fecha_cierre= kwargs.pop('filtro_fecha_cierre')
        filtro_encargado= kwargs.pop('filtro_encargado')
        filtro_apoyo= kwargs.pop('filtro_apoyo')

        super(TareaBuscarForm, self).__init__(*args, **kwargs)
        self.fields['fecha_inicio'].initial = filtro_fecha_inicio
        self.fields['estado'].initial = filtro_estado
        self.fields['tipo_tarea'].initial = filtro_tipo_tarea

        self.fields['fecha_inicio_real'].initial = filtro_fecha_inicio_real
        self.fields['fecha_cierre'].initial = filtro_fecha_cierre
        self.fields['encargado'].initial = filtro_encargado
        self.fields['apoyo'].initial = filtro_apoyo
    
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class TareaForm(BSModalModelForm):
    cliente = forms.ModelChoiceField(queryset=Cliente.objects.filter(estado_sunat = 1))
    class Meta:
        model = Tarea
        fields = (
            'tipo_tarea',
            'fecha_inicio',
            'fecha_limite',
            'descripcion',
            'area',
            'prioridad',
            'encargado',
            'cliente',
            'apoyo',
            )
        
        widgets = {
            'fecha_inicio' : forms.DateInput(
                attrs ={
                    'type':'date',
                    },
                format = '%Y-%m-%d',
                ),
            
            'fecha_limite' : forms.DateInput(
                attrs ={
                    'type':'date',
                    },
                format = '%Y-%m-%d',
                ),
            'apoyo' : forms.CheckboxSelectMultiple(),
            }

    def clean_fecha_limite(self):
        fecha_inicio = self.cleaned_data.get('fecha_inicio')
        fecha_limite = self.cleaned_data.get('fecha_limite')

        if fecha_limite < fecha_inicio:
            self.add_error('fecha_limite', 'La Fecha Limite debe ser igual o mayor a la Fecha Inicio')
        return fecha_limite

    def __init__(self, *args, **kwargs):
        super(TareaForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.required = True
        self.fields['apoyo'].widget.attrs['class'] = 'nobull'
        self.fields['apoyo'].required = False
        self.fields['cliente'].required = False
        # self.fields['apoyo'].widget.attrs['class'] = 'form-check-input'


class TareaActualizarForm(BSModalModelForm):
    class Meta:
        model = Tarea
        fields=(
            'tipo_tarea',
            'fecha_inicio',
            'fecha_limite',
            'area',
            'prioridad',
            'encargado',
            'apoyo',
            )
        
        widgets = {
            'fecha_inicio' : forms.DateInput(
                attrs ={
                    'type':'date',
                    },
                format = '%Y-%m-%d',
                ),
            
            'fecha_limite' : forms.DateInput(
                attrs ={
                    'type':'date',
                    },
                format = '%Y-%m-%d',
                ),
            'apoyo' : forms.CheckboxSelectMultiple(),
            }

    def __init__(self, *args, **kwargs):
        super(TareaActualizarForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.required = True
        self.fields['apoyo'].widget.attrs['class'] = 'nobull'
        self.fields['apoyo'].required = False

class TareaDescripcionForm(BSModalModelForm):
    class Meta:
        model = Tarea
        fields=(
            'descripcion',
            )

    def __init__(self, *args, **kwargs):
        super(TareaDescripcionForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class HistorialComentarioTareaForm(BSModalModelForm):
    class Meta:
        model = HistorialComentarioTarea
        fields=(
            'comentario',
            )

    def __init__(self, *args, **kwargs):
        super(HistorialComentarioTareaForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class TareaAsignarEventoForm(BSModalModelForm):
    evento = forms.ModelChoiceField(queryset=EventoCRM.objects.all(), required=False)

    class Meta:
        model = Tarea
        fields = (
            'evento',
        )
        
    def __init__(self, *args, **kwargs):
        super(TareaAsignarEventoForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class TareaAsignarClienteForm(BSModalModelForm):
    cliente = forms.ModelChoiceField(queryset=Cliente.objects.all(), required=False)

    class Meta:
        model = Tarea
        fields = (
            'cliente',
        )

    def clean_cliente(self):
        cliente = self.cleaned_data.get('cliente')
        return cliente

    def __init__(self, *args, **kwargs):
        super(TareaAsignarClienteForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'



