from django import forms
from django.contrib.auth import get_user_model
from applications.sociedad.models import Sociedad
from .models import Sede
from applications.datos_globales.models import Provincia, Distrito, Departamento
from bootstrap_modal_forms.forms import  BSModalModelForm

class SedeCreateForm(BSModalModelForm):
    departamento_buscar = forms.ModelChoiceField(label = 'Departamento', queryset = Departamento.objects.all())
    provincia_buscar = forms.ModelChoiceField(label = 'Provincia', queryset = Provincia.objects.none())
    distrito_buscar = forms.ModelChoiceField(label = 'Distrito', queryset = Distrito.objects.none())
    class Meta:
        model = Sede
        fields = (
            'nombre',
            'sociedad',
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

    def clean_departamento_buscar(self):
        departamento_buscar = self.cleaned_data.get('departamento_buscar')
        provincia_buscar = self.fields['provincia_buscar']
        provincia_buscar.queryset = Provincia.objects.filter(departamento = departamento_buscar.codigo)
    
        return departamento_buscar

    def clean_provincia_buscar(self):
        provincia_buscar = self.cleaned_data.get('provincia_buscar')
        distrito_buscar = self.fields['distrito_buscar']
        distrito_buscar.queryset = Distrito.objects.filter(provincia = provincia_buscar.codigo)
    
        return provincia_buscar

    def clean(self):
        cleaned_data = super().clean()
        nombre = cleaned_data.get('nombre')
        filtro = Sede.objects.filter(nombre__unaccent__iexact = nombre)
        if nombre != self.instance.nombre:
            if len(filtro)>0:
                self.add_error('nombre', 'Ya existe una Sede con este nombre')

    def __init__(self, *args, **kwargs):
        super(SedeCreateForm, self).__init__(*args, **kwargs)
        self.fields['usuario_responsable'].queryset = get_user_model().objects.filter(is_active=1)  
        self.fields['sociedad'].queryset = Sociedad.objects.filter(estado_sunat=1) 
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        self.fields['sociedad'].widget.attrs['class'] = 'nobull'

class SedeUpdateForm(BSModalModelForm):
    departamento_buscar = forms.ModelChoiceField(label = 'Departamento', queryset = Departamento.objects.all())
    provincia_buscar = forms.ModelChoiceField(label = 'Provincia', queryset = Provincia.objects.none())
    distrito_buscar = forms.ModelChoiceField(label = 'Distrito', queryset = Distrito.objects.none())
    class Meta:
        model = Sede
        fields = (
            'usuario_responsable',
            'sociedad',
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
        super(SedeUpdateForm, self).__init__(*args, **kwargs)
        self.fields['sociedad'].queryset = Sociedad.objects.filter(estado_sunat=1)
        self.fields['usuario_responsable'].queryset = get_user_model().objects.filter(is_active=1) 
        distrito = self.instance.distrito
        provincia = distrito.provincia
        departamento = provincia.departamento
        self.fields['departamento_buscar'].initial = departamento
        self.fields['provincia_buscar'].queryset = Provincia.objects.filter(departamento = departamento.codigo)
        self.fields['provincia_buscar'].initial = provincia
        self.fields['distrito_buscar'].queryset = Distrito.objects.filter(provincia = provincia.codigo)
        self.fields['distrito_buscar'].initial = distrito
        
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        self.fields['sociedad'].widget.attrs['class'] = 'nobull'
