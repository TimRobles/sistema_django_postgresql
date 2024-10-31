from django import forms 
from django.contrib.auth import authenticate
from applications.importaciones import *
from django.core.exceptions import ValidationError


from applications.usuario.models import HistoricoUser
from applications.usuario.models import DatosUsuario
from applications.usuario.models import Vacaciones, VacacionesDetalle

from bootstrap_modal_forms.forms import BSModalForm, BSModalModelForm

class HistoricoUserForm(forms.ModelForm):
    class Meta:
        model = HistoricoUser
        fields = (
            'fecha_alta',
            'fecha_baja',
            )

class DatosUsuarioForm(forms.ModelForm):
    nombres = forms.CharField(max_length=50)
    apellidos = forms.CharField(max_length=50)
    correo = forms.CharField(max_length=50)
    class Meta:
        model = DatosUsuario
        fields = (
            'nombres', 
            'apellidos', 
            'tipo_documento',
            'numero_documento', 
            'fecha_nacimiento', 
            'foto', 
            'direccion', 
            'telefono_personal',
            'correo',
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
        self.fields['nombres'].initial = usuario.first_name
        self.fields['apellidos'].initial = usuario.last_name
        self.fields['correo'].initial = usuario.email

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
            if fecha_alta == None:
                texto = 'Ingresar fecha de alta.'
                self.add_error('fecha_alta', texto)
            elif fecha_alta > date.today():
                texto = 'Fecha de alta no puede ser mayor a la fecha actual.'
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


class HistoricoUserCreateForm(BSModalModelForm):
    class Meta:
        model = HistoricoUser
        fields = (
            'usuario',
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
        if fecha_alta == None:
            texto = 'Ingresar fecha de alta.'
            self.add_error('fecha_alta', texto)
        elif fecha_alta > date.today():
                texto = 'Fecha de alta no puede ser mayor a la fecha actual.'
                self.add_error('fecha_alta', texto)            
        
        return fecha_alta

    def __init__(self, *args, **kwargs):
        super(HistoricoUserCreateForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        self.fields['usuario'].queryset = get_user_model().objects.exclude(HistoricoUser_usuario__estado=1).exclude(HistoricoUser_usuario__estado=2)


    ################################# V A C A C I O N E S ################################################

class VacacionesBuscarForm(forms.Form):
    usuario = forms.ModelChoiceField(queryset=get_user_model().objects, required=False)
    estado = forms.ChoiceField(choices=((None, '--------------------'),) + ESTADO_VACACIONES, required=False)

    def __init__(self, *args, **kwargs):
        filtro_estado = kwargs.pop('filtro_estado')
        filtro_usuario = kwargs.pop('filtro_usuario')

        super(VacacionesBuscarForm, self).__init__(*args, **kwargs)
        self.fields['estado'].initial = filtro_estado
        self.fields['usuario'].initial = filtro_usuario

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class VacacionesForm(BSModalModelForm):
    class Meta:
        model = Vacaciones
        fields = (
            'usuario',
            'dias_vacaciones',
            )

    def __init__(self, *args, **kwargs):
        super(VacacionesForm, self).__init__(*args, **kwargs)
        self.fields['usuario'].queryset = (get_user_model().objects.filter(is_active=1).order_by('username'))     
        self.fields['dias_vacaciones'].required = True
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class VacacionesDetalleForm(BSModalModelForm):
    class Meta:
        model = VacacionesDetalle
        fields = (
            'fecha_inicio',
            'fecha_fin',
            'motivo',
            )
        
        widgets = {
            'fecha_inicio': forms.DateInput(
                attrs ={
                    'type':'date',
                    },
                format = '%Y-%m-%d',
                ), 
            
            'fecha_fin': forms.DateInput(
                attrs ={
                    'type':'date',
                    },
                format = '%Y-%m-%d',
                ), 
        }

    def __init__(self, *args, **kwargs):
        self.usuario = kwargs.pop('usuario')
        self.dias_restantes = kwargs.pop('dias_restantes')
        super(VacacionesDetalleForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    def clean_fecha_fin(self):
        fecha_inicio = self.cleaned_data.get('fecha_inicio')
        fecha_fin = self.cleaned_data.get('fecha_fin')

        if fecha_fin < fecha_inicio:
            self.add_error('fecha_fin', 'La Fecha Fin debe ser igual o mayor a la Fecha Inicio')
        return fecha_fin

    def clean(self):
        cleaned_data = super().clean()
        fecha_inicio = cleaned_data.get('fecha_inicio')
        fecha_fin = cleaned_data.get('fecha_fin')

        if fecha_inicio and fecha_fin:
            existing_records = VacacionesDetalle.objects.filter(
                fecha_inicio__lte=fecha_fin,
                fecha_fin__gte=fecha_inicio,
                vacaciones__usuario = self.usuario,
            )
            if existing_records.exists():
                self.add_error('fecha_fin', 'Ya existe un registro de vacaciones que coincide con estas fechas.')

        if fecha_inicio and fecha_fin:
            duration = (fecha_fin - fecha_inicio).days + 1  # +1 para incluir el día de inicio
            if duration > self.dias_restantes:

                self.add_error('fecha_fin', f'El rango de fechas seleccionadas contiene {duration} días')
                self.add_error('fecha_fin', f'Solo se cuenta con {self.dias_restantes} días restantes de vacaciones')

        return cleaned_data

class VacacionesDetalleActualizarForm(BSModalModelForm):
    class Meta:
        model = VacacionesDetalle
        fields = (
            'fecha_inicio',
            'fecha_fin',
            'motivo',
            )
        
        widgets = {
            'fecha_inicio': forms.DateInput(
                attrs ={
                    'type':'date',
                    },
                format = '%Y-%m-%d',
                ), 
            
            'fecha_fin': forms.DateInput(
                attrs ={
                    'type':'date',
                    },
                format = '%Y-%m-%d',
                ), 
        }        

    def __init__(self, *args, **kwargs):
        super(VacacionesDetalleActualizarForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
