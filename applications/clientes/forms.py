from datetime import date
from django import forms
from applications.variables import TIPO_DOCUMENTO_CHOICES
from .models import (
    Cliente, 
    InterlocutorCliente, 
    TelefonoInterlocutorCliente,
    CorreoInterlocutorCliente,
    TipoInterlocutorCliente, 
    )

from bootstrap_modal_forms.forms import BSModalForm, BSModalModelForm

class ClienteForm(BSModalModelForm):
    class Meta:
        model = Cliente
        fields = (
            'tipo_documento',
            'numero_documento',
            'razon_social',
            'nombre_comercial',
            'direccion_fiscal',
            'ubigeo',
            'estado_sunat',
            )

    def __init__(self, *args, **kwargs):
        super(ClienteForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    def clean(self):
        cleaned_data = super().clean()
        numero_documento = cleaned_data.get('numero_documento')
        filtro = Cliente.objects.filter(numero_documento__unaccent__iexact = numero_documento)
        if numero_documento != self.instance.numero_documento:
            if len(filtro)>0:
                self.add_error('numero_documento', 'Ya existe un Cliente con este Número de documento')


class TipoInterlocutorClienteForm(forms.ModelForm):
    class Meta:
        model = TipoInterlocutorCliente
        fields = (
            'nombre',
            )

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        filtro = TipoInterlocutorCliente.objects.filter(nombre__unaccent__iexact = nombre)
        if nombre != self.instance.nombre:
            if len(filtro)>0:
                self.add_error('nombre', 'Ya existe un Tipo de Interlocutor Cliente con este nombre')

        return nombre


class InterlocutorClienteForm(BSModalForm):
    tipo_documento = forms.ChoiceField(label = 'Tipo de Documento', choices = TIPO_DOCUMENTO_CHOICES)
    numero_documento = forms.CharField(label = 'Número de Documento', max_length=15)
    nombre_completo = forms.CharField(label = 'Nombre Completo', max_length=120, required=True)
    tipo_interlocutor = forms.ModelChoiceField(label = 'Tipo de Interlocutor', queryset = TipoInterlocutorCliente.objects.all(), required=False)
    
    def __init__(self, *args, **kwargs):
        super(InterlocutorClienteForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class InterlocutorClienteUpdateForm(BSModalModelForm):
    class Meta:
        model = InterlocutorCliente
        fields = (
            'tipo_documento',
            'numero_documento',
            'nombre_completo',
            'tipo_interlocutor',
            )

    def __init__(self, *args, **kwargs):
        super(InterlocutorClienteUpdateForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class TelefonoInterlocutorForm(BSModalModelForm):
    class Meta:
        model = TelefonoInterlocutorCliente
        fields = (
            'numero',
            )

        widgets = {
            'numero' : forms.PasswordInput(
                attrs ={
                    'placeholder':'ej.: +12125552368',
                    },
                ),
            }
    
    def __init__(self, *args, **kwargs):
        super(TelefonoInterlocutorForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    def clean(self):
        cleaned_data = super().clean()
        numero = cleaned_data.get('numero')
        filtro = TelefonoInterlocutorCliente.objects.filter(numero__unaccent__iexact = numero)
        if numero != self.instance.numero:
            if len(filtro)>0:
                self.add_error('numero', 'Ya existe un Teléfono con este numero')

class TelefonoInterlocutorDarBajaForm(BSModalModelForm):
    class Meta:
        model = TelefonoInterlocutorCliente
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
        if fecha_baja > date.today():
            self.add_error('fecha_baja', 'La fecha de baja no puede ser mayor a la fecha de hoy.')
        return fecha_baja

    def __init__(self, *args, **kwargs):
        super(TelefonoInterlocutorDarBajaForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.required = True

class CorreoInterlocutorForm(BSModalModelForm):
    class Meta:
        model = CorreoInterlocutorCliente
        fields = (
            'correo',
            )

    def __init__(self, *args, **kwargs):
        super(CorreoInterlocutorForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    def clean(self):
        cleaned_data = super().clean()
        correo = cleaned_data.get('correo')
        filtro = CorreoInterlocutorCliente.objects.filter(correo__unaccent__iexact = correo)
        if correo != self.instance.correo:
            if len(filtro)>0:
                self.add_error('correo', 'El correo ingresado ya se encuentra registrado')

class CorreoInterlocutorDarBajaForm(BSModalModelForm):
    class Meta:
        model = CorreoInterlocutorCliente
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
        if fecha_baja > date.today():
            self.add_error('fecha_baja', 'La fecha de baja no puede ser mayor a la fecha de hoy.')
        return fecha_baja

    def __init__(self, *args, **kwargs):
        super(CorreoInterlocutorDarBajaForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.required = True