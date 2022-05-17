from dataclasses import fields
from django import forms

from .models import Modelo, Marca

from bootstrap_modal_forms.forms import BSModalForm, BSModalModelForm

class ModeloForm(BSModalModelForm):
    class Meta:
        model = Modelo
        fields=(
            'nombre',
            )

    def __init__(self, *args, **kwargs):
        super(ModeloForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class MarcaForm(BSModalModelForm):
    class Meta:
        model = Marca
        fields=(
            'nombre',
            'modelos',
            )

        widgets = {
            'modelos': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super(MarcaForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        self.fields['modelos'].widget.attrs['class'] = 'nobull'