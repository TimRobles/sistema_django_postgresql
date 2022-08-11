from django import forms

from applications.sorteo_aptc.models import UsuarioAPTC

class RespuestaUsuarioForm(forms.ModelForm):
    class Meta:
        model = UsuarioAPTC
        fields = [
            'nombre',
            'tipo_documento',
            'numero_documento',
            'telefono',
            'correo',
            'empresa',
        ]
    
    def __init__(self, *args, **kwargs):
        super(RespuestaUsuarioForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


# class EncuestarForm(forms.Form):
#     tipo_encuesta = forms.ModelChoiceField(queryset=Encuesta.objects.all())


# class EncuestaClienteForm(forms.Form):
#     cliente = forms.ModelChoiceField(queryset=Cliente.objects.all())
#     tipo_encuesta = forms.ModelChoiceField(queryset=Encuesta.objects.all())
    