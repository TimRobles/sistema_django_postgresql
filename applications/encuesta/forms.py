from django import forms

from applications.clientes.models import Cliente
from applications.encuesta.models import Encuesta, Pregunta, Respuesta, RespuestaDetalle

class RespuestaClienteForm(forms.ModelForm):
    class Meta:
        model = Respuesta
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(RespuestaClienteForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class RespuestaDetalleForm(forms.ModelForm):
    class Meta:
        model = RespuestaDetalle
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(RespuestaDetalleForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class EncuestarForm(forms.Form):
    tipo_encuesta = forms.ModelChoiceField(queryset=Encuesta.objects.all())


    
    