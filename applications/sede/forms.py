from django import forms
from .models import Sede
from applications.datos_globales.models import Provincia, Distrito, Departamento

from bootstrap_modal_forms.forms import  BSModalModelForm

class SedeCreateForm(BSModalModelForm):
    departamento_buscar = forms.ModelChoiceField(queryset = Departamento.objects.all())
    provincia_buscar = forms.ModelChoiceField(queryset = Provincia.objects.all(), required=False)
    distrito_buscar = forms.ModelChoiceField(queryset = Distrito.objects.all(), required=False)
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
        widgets = {
            'sociedad': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super(SedeCreateForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        self.fields['sociedad'].widget.attrs['class'] = 'nobull'

class SedeUpdateForm(BSModalModelForm):
    departamento_buscar = forms.ModelChoiceField(queryset = Departamento.objects.all())
    provincia_buscar = forms.ModelChoiceField(queryset = Provincia.objects.all(), required=False)
    distrito_buscar = forms.ModelChoiceField(queryset = Distrito.objects.all(), required=False)
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
        ubigeo = self.instance.ubigeo
        self.fields['departamento_buscar'].initial = ubigeo[:2]
        self.fields['provincia_buscar'].initial = ubigeo[:4]
        self.fields['distrito_buscar'].initial = ubigeo
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
