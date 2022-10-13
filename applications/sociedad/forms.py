from datetime import date
from django import forms
from django.contrib.auth import get_user_model

from .models import Documento, Sociedad, RepresentanteLegal, TipoRepresentanteLegal

from bootstrap_modal_forms.forms import BSModalForm, BSModalModelForm

class SociedadForm(BSModalModelForm):
    class Meta:
        model = Sociedad
        fields=(
            'ruc',
            'razon_social',
            'nombre_comercial',
            'abreviatura',
            'alias',
            'direccion_legal',
            'ubigeo',
            'estado_sunat',
            'condicion_sunat',
            'logo',
            'color',
            )

    def __init__(self, *args, **kwargs):
        super(SociedadForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class DocumentoForm(BSModalModelForm):
    class Meta:
        model = Documento
        fields = (
            'nombre_documento',
            'descripcion_documento',
            'documento',
            )

    def __init__(self, *args, **kwargs):
        super(DocumentoForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.required = True

class TipoRepresentanteLegalForm(forms.ModelForm):
    class Meta:
        model = TipoRepresentanteLegal
        fields = (
            'nombre',
            )

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        filtro = TipoRepresentanteLegal.objects.filter(nombre__unaccent__iexact = nombre)
        if nombre != self.instance.nombre:
            if len(filtro)>0:
                self.add_error('nombre', 'Ya existe un Tipo de representante legal con este nombre')

        return nombre

class RepresentanteLegalForm(BSModalModelForm):
    class Meta:
        model = RepresentanteLegal
        fields = (
            'usuario',
            'tipo_representante_legal',
            'fecha_registro',
            )

        widgets = {
            'fecha_registro' : forms.DateInput(
                attrs ={
                    'type':'date',
                    },
                format = '%Y-%m-%d',
                ),
        }

    def clean_fecha_registro(self):
        fecha_registro = self.cleaned_data.get('fecha_registro')
        if fecha_registro > date.today():
            self.add_error('fecha_registro', 'La fecha de registro no puede ser mayor a la fecha de hoy.')

        return fecha_registro

    def __init__(self, *args, **kwargs):
        super(RepresentanteLegalForm, self).__init__(*args, **kwargs)
        self.fields['usuario'].queryset = get_user_model().objects.exclude(first_name = "")
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.required = True

class RepresentanteLegalDarBajaForm(BSModalModelForm):
    class Meta:
        model = RepresentanteLegal
        fields = (
            'fecha_baja',
            )

        widgets = {
            'fecha_baja' : forms.DateInput(
                attrs ={
                    'type':'date',
                    },
                format = '%Y-%m-%d',
                ),
        }

    def clean_fecha_baja(self):
        fecha_baja = self.cleaned_data.get('fecha_baja')
        if fecha_baja < self.instance.fecha_registro:
            self.add_error('fecha_baja', 'La fecha de baja no puede ser menor a la fecha de registro.')

        return fecha_baja

    def __init__(self, *args, **kwargs):
        super(RepresentanteLegalDarBajaForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.required = True
