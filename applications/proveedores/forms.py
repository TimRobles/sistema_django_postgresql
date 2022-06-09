from datetime import date
from django import forms
from .models import (
    CorreoInterlocutorProveedor, 
    Proveedor, 
    InterlocutorProveedor, 
    TelefonoInterlocutorProveedor,
    )
from bootstrap_modal_forms.forms import BSModalForm, BSModalModelForm

class ProveedorForm(BSModalModelForm):
    class Meta:
        model = Proveedor
        fields = (
            'nombre',
            'pais',
            'direccion',
            )

    def __init__(self, *args, **kwargs):
        super(ProveedorForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        filtro = Proveedor.objects.filter(nombre__unaccent__iexact = nombre)
        if nombre != self.instance.nombre:
            if len(filtro)>0:
                self.add_error('nombre', 'Ya existe un Proveedor con este nombre')

        return nombre

class InterlocutorProveedorForm(BSModalForm):
    nombres = forms.CharField(max_length=60, required=True)
    apellidos = forms.CharField(max_length=60, required=True)
    
    def __init__(self, *args, **kwargs):
        super(InterlocutorProveedorForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class InterlocutorProveedorUpdateForm(BSModalModelForm):
    class Meta:
        model = InterlocutorProveedor
        fields = (
            'nombres',
            'apellidos',
            )

    def __init__(self, *args, **kwargs):
        super(InterlocutorProveedorUpdateForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class TelefonoInterlocutorForm(BSModalModelForm):
    class Meta:
        model = TelefonoInterlocutorProveedor
        fields = (
            'numero',
            )
    
    def __init__(self, *args, **kwargs):
        super(TelefonoInterlocutorForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        self.fields['numero'].widget.attrs['placeholder'] = 'ej.: +12125552368'

    def clean(self):
        cleaned_data = super().clean()
        numero = cleaned_data.get('numero')
        filtro = TelefonoInterlocutorProveedor.objects.filter(numero__unaccent__iexact = numero)
        if numero != self.instance.numero:
            if len(filtro)>0:
                self.add_error('numero', 'Ya existe un Teléfono con este numero')

class TelefonoInterlocutorDarBajaForm(BSModalModelForm):
    class Meta:
        model = TelefonoInterlocutorProveedor
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
        model = CorreoInterlocutorProveedor
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
        filtro = CorreoInterlocutorProveedor.objects.filter(correo__unaccent__iexact = correo)
        if correo != self.instance.correo:
            if len(filtro)>0:
                self.add_error('correo', 'El correo ingresado ya se encuentra registrado')

class CorreoInterlocutorDarBajaForm(BSModalModelForm):
    class Meta:
        model = CorreoInterlocutorProveedor
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
