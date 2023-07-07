from dataclasses import fields
from datetime import date
from django import forms
from django.contrib.auth import get_user_model

from applications.sede.models import Sede

from .models import ResponsableAsistencia, Visita, Asistencia

from bootstrap_modal_forms.forms import BSModalForm, BSModalModelForm

from applications.variables import MOTIVO_INASISTENCIA

class VisitaForm(BSModalModelForm):
    class Meta:
        model = Visita
        fields=(
            'tipo_documento',
            'numero_documento',
            'nombre',
            'sede',
            'usuario_atendio',
            'motivo_visita',
            'cliente',
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
        self.fields['usuario_atendio'].queryset = get_user_model().objects.filter(is_active=1)
        self.fields['sede'].queryset = Sede.objects.filter(estado=1)
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

class AsistenciaForm(BSModalModelForm):
    sede = forms.ModelChoiceField(queryset=Sede.objects.filter(estado=1))
    longitud = forms.FloatField(required=False, widget = forms.HiddenInput())
    latitud = forms.FloatField(required=False, widget = forms.HiddenInput())

    class Meta:
        model = Asistencia
        fields=(
            'usuario',
            'sede',
            'justificacion',
            )

    def __init__(self, *args, **kwargs):
        super(AsistenciaForm, self).__init__(*args, **kwargs)
        self.fields['usuario'].queryset = ResponsableAsistencia.objects.get(usuario_responsable = self.request.user).usuario_a_registrar
        self.fields['justificacion'].help_text = 'En caso de tardanza'
        
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class AsistenciaBuscarForm(forms.Form):
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
        super(AsistenciaBuscarForm, self).__init__(*args, **kwargs)
        self.fields['nombre'].initial = filtro_nombre
        self.fields['fecha'].initial = filtro_fecha
        
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class AsistenciaPersonalBuscarForm(forms.Form):
    nombre = forms.CharField(max_length=50, required=False)
    fecha_registro = forms.DateField(
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
        filtro_fecha_registro = kwargs.pop('filtro_fecha_registro')
        super(AsistenciaPersonalBuscarForm, self).__init__(*args, **kwargs)
        self.fields['nombre'].initial = filtro_nombre
        self.fields['fecha_registro'].initial = filtro_fecha_registro
        
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class AsistenciaSalidaForm(BSModalModelForm):
    longitud = forms.FloatField(required=False, widget = forms.HiddenInput())
    latitud = forms.FloatField(required=False, widget = forms.HiddenInput())

    class Meta:
        model = Asistencia
        fields = (
            'sede',
            'justificacion',
        )
    def __init__(self, *args, **kwargs):
        super(AsistenciaSalidaForm, self).__init__(*args, **kwargs)
        self.fields['sede'].queryset = Sede.objects.filter(estado=1)
        self.fields['justificacion'].help_text = 'En caso de salir temprano'
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class InasistenciaForm(BSModalModelForm):
    motivo_inasistencia = forms.ChoiceField(choices=((None, '--------------------'),) + MOTIVO_INASISTENCIA[1:] )
    fecha = forms.DateField(
        widget = forms.DateInput(
                attrs ={
                    'type':'date',
                    },
                format = '%Y-%m-%d',
                )
        )

    class Meta:
        model = Asistencia
        fields = (
            'usuario',
            'motivo_inasistencia',
            'fecha',
            'justificacion',
            'archivo',
        )


    def __init__(self, *args, **kwargs):
        super(InasistenciaForm, self).__init__(*args, **kwargs)
        self.fields['usuario'].queryset = ResponsableAsistencia.objects.get(usuario_responsable = self.request.user).usuario_a_registrar

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class InasistenciaAprobarForm(BSModalModelForm):
    comentario = forms.CharField(label='Comentario de aprobación',max_length=50,required=False)
    class Meta:
        model = Asistencia
        fields = (
            'comentario',
        )

    def __init__(self, *args, **kwargs):
        super(InasistenciaAprobarForm, self).__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class InasistenciaRechazarForm(BSModalModelForm):
    motivo_inasistencia = forms.ChoiceField(choices=((None, '--------------------'),) + MOTIVO_INASISTENCIA[1:] )
    comentario = forms.CharField(label='Comentario de rechazo',max_length=50,required=True)
    class Meta:
        model = Asistencia
        fields = (
            'motivo_inasistencia',
            'comentario',
            'editar_solicitud',
        )

    def __init__(self, *args, **kwargs):
        super(InasistenciaRechazarForm, self).__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        self.fields['editar_solicitud'].widget.attrs['class'] = 'form-check-input'

class InasistenciaActualizarForm(BSModalModelForm):
    class Meta:
        model = Asistencia
        fields = (
            'motivo_inasistencia',
            'fecha_registro',
            'justificacion',
            'archivo',
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
        super(InasistenciaActualizarForm, self).__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
