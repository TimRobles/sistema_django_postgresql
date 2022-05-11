from django import forms
from .models import Sede

from bootstrap_modal_forms.forms import  BSModalModelForm

class SedeCreateForm(BSModalModelForm):
    departamento_buscar = forms.CharField(max_length=50)
    provincia_buscar = forms.CharField(max_length=50)
    distrito_buscar = forms.CharField(max_length=50)
    class Meta:
        model = Sede
        fields = (
            'sociedad',
            'nombre',
            'usuario_responsable',
            'direccion',
            'departamento_buscar',
            'provincia_buscar',
            'distrito_buscar',
            'ubigeo',
            )
        

    def __init__(self, *args, **kwargs):
        super(SedeCreateForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class SedeUpdateForm(BSModalModelForm):
    departamento_buscar = forms.CharField(max_length=50)
    provincia_buscar = forms.CharField(max_length=50)
    distrito_buscar = forms.CharField(max_length=50)
    class Meta:
        model = Sede
        fields = (
            'usuario_responsable',
            'direccion',
            'departamento_buscar',
            'provincia_buscar',
            'distrito_buscar',
            'ubigeo',
            )
        

    def __init__(self, *args, **kwargs):
        super(SedeUpdateForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'