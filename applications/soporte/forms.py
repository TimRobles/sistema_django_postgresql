from django import forms
from django.contrib.auth import get_user_model
from bootstrap_modal_forms.forms import BSModalModelForm
from applications.variables import ESTADO_PROBLEMAS
from .models import (
    Problema,
    ProblemaDetalle
)

class ProblemaBuscarForm(forms.Form): 
    titulo = forms.CharField(label = 'Titulo', max_length=100, required=False)
    estado = forms.ChoiceField(choices=((None, '--------------------'),) + ESTADO_PROBLEMAS, required=False)
    usuario = forms.ModelChoiceField(queryset=get_user_model().objects, required=False)

 
    def __init__(self, *args, **kwargs): 
        filtro_titulo = kwargs.pop('filtro_titulo')
        filtro_estado = kwargs.pop('filtro_estado')
        filtro_usuario = kwargs.pop('filtro_usuario')

        super(ProblemaBuscarForm, self).__init__(*args, **kwargs) 
        self.fields['titulo'].initial = filtro_titulo
        self.fields['estado'].initial = filtro_estado
        self.fields['usuario'].initial = filtro_usuario

        for visible in self.visible_fields(): 
            visible.field.widget.attrs['class'] = 'form-control' 



class ProblemaForm(BSModalModelForm):
    class Meta:
        model = Problema
        fields = (
            'titulo', 
            'descripcion'
            )

    def __init__(self, *args, **kwargs):
        super(ProblemaForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
