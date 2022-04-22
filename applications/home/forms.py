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

