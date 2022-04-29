from django import forms
from django.contrib.auth import authenticate

from applications.sociedad.models import Sociedad

class UserLoginForm(forms.Form):
    sociedad = forms.ModelChoiceField(queryset=Sociedad.objects.all())
    username = forms.CharField(
        label='Usuario',
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Nombre de usuario'
            }
        )
        )
    password = forms.CharField(
        label='Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Contraseña'
            }
        )
        )

    def clean(self):
        cleaned_data = super(UserLoginForm, self).clean()
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']

        user = authenticate(
            username = username,
            password = password
        )
        if not user:
            self.add_error('password', 'Contraseña incorrecta.')

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class UserUpdateForm(forms.Form):
    GENDER_CHOICES = (
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otros'),
    )

    nombres = forms.CharField(max_length=50, required=False)
    apellidos = forms.CharField(max_length=50, required=False)
    email = forms.EmailField(required=False)
    genero = forms.ChoiceField(choices=GENDER_CHOICES, required=False)

    password1 = forms.CharField(
        label='Contraseña Actual',
        required=False,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Contraseña Actual'
            }
        ))
    password2 = forms.CharField(
        label='Contraseña Nueva',
        required=False,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Contraseña Nueva'
            }
        ))
    avatar = forms.ImageField(
        required=False,
        allow_empty_file=True
    )

    def clean(self):
        cleaned_data = super(UserUpdateForm , self).clean()
        password1 = self.cleaned_data["password1"]

        if password1 != "":
            user = authenticate(username=self.request.user.username, password=password1)
            if not user:
                raise forms.ValidationError('Contraseña incorrecta')

        return cleaned_data

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        kwargs.update(initial={
            # 'field': 'value'
            'nombres': self.request.user.nombres,
            'apellidos': self.request.user.apellidos,
            'email': self.request.user.email,
            'genero': self.request.user.genero,
            'avatar': self.request.user.avatar,
        })
        super(UserUpdateForm , self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class OlvideContrasenaForm(forms.Form):
    correo = forms.EmailField()

    def __init__(self, *args, **kwargs):
        super(OlvideContrasenaForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class RecuperarContrasenaForm(forms.Form):
    correo = forms.EmailField()
    password = forms.CharField()

    def __init__(self, *args, **kwargs):
        super(RecuperarContrasenaForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
