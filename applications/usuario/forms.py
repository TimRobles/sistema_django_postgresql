from django import forms 
from django.contrib.auth import authenticate
from applications.importaciones import *

from applications.usuario.models import HistoricoUser
from applications.usuario.models import DatosUsuario

from bootstrap_modal_forms.forms import BSModalForm, BSModalModelForm

class HistoricoUserForm(forms.ModelForm):
    class Meta:
        model = HistoricoUser
        fields = (
            'fecha_alta',
            'fecha_baja',
            )

class DatosUsuarioForm(forms.ModelForm):
    Nombres = forms.CharField(max_length=50)
    Apellidos = forms.CharField(max_length=50)
    Correo = forms.CharField(max_length=50)
    class Meta:
        model = DatosUsuario
        fields = (
            'Nombres', 
            'Apellidos', 
            'tipo_documento',
            'numero_documento', 
            'fecha_nacimiento', 
            'foto', 
            'direccion', 
            'telefono_personal',
            'Correo',
            )
        widgets = {
            'fecha_nacimiento': forms.DateInput(
                format='%Y-%m-%d',
                attrs = {
                    'type': 'date',
                    'class': 'input-group-field',
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        usuario = kwargs.pop('usuario')
        super(DatosUsuarioForm, self).__init__(*args, **kwargs)
        self.fields['Nombres'].initial = usuario.first_name
        self.fields['Apellidos'].initial = usuario.last_name
        self.fields['Correo'].initial = usuario.email

        if self.fields['telefono_personal'].initial == None:   
            self.fields['telefono_personal'].initial = '+51'

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class UserPasswordForm(forms.Form):
    password1 = forms.CharField(
        label='Contraseña Actual',
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Contraseña Actual'
            }
        ))
    password2 = forms.CharField(
        label='Contraseña Nueva',
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Contraseña Nueva'
            }
        ))

    password3 = forms.CharField(
        label='Confirmar nueva contraseña',
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Confirmar nueva contraseña'
            }
        ))

    def clean(self):
        cleaned_data = super(UserPasswordForm , self).clean()
        password1 = self.cleaned_data["password1"]
        password2 = self.cleaned_data["password2"]
        password3 = self.cleaned_data["password3"]

        user = authenticate(username=self.request.user.username, password=password1)
        if not user:
            self.add_error('password1', 'Contraseña anterior incorrecta')

        else:
            if password2 != password3:
                self.add_error('password2', 'Las contraseñas no coinciden')
                
            else:
                messages.success(self.request, 'Se actualizo correctamente la contraseña')
                
        return cleaned_data


    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(UserPasswordForm , self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class HistoricoUserDarBajaForm(BSModalModelForm):
    class Meta:
        model = HistoricoUser
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
                texto = 'Fecha de baja no puede ser menor a la fecha de alta del usuario.'
                self.add_error('fecha_baja', texto)
        except:
            pass
        
        return fecha_baja
    
    def __init__(self, *args, **kwargs):
        super(HistoricoUserDarBajaForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class HistoricoUserDarAltaForm(BSModalModelForm):
    class Meta:
        model = HistoricoUser
        fields = (
            'fecha_alta',
            )
        widgets = {
            'fecha_alta': forms.DateInput(
                attrs ={
                    'type':'date',
                    },
                format = '%Y-%m-%d',
                ), 
        }
    
    def clean_fecha_alta(self):
        fecha_alta = self.cleaned_data.get('fecha_alta')
        if self.fecha_baja:
            if fecha_alta== None:
                texto = 'Ingresar fecha de alta.'
                self.add_error('fecha_alta', texto)

            try:
                if self.fecha_baja > fecha_alta:
                    texto = 'Fecha de alta no puede ser menor a la fecha de baja anterior del usuario.'
                    self.add_error('fecha_alta', texto)            
            except:
                pass

        return fecha_alta

    def __init__(self, *args, **kwargs):
        self.fecha_baja = kwargs.pop('fecha_baja')
        super(HistoricoUserDarAltaForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


