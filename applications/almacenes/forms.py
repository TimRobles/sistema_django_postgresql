from django import forms
from bootstrap_modal_forms.forms import BSModalForm, BSModalModelForm
from .models import Almacen

class AlmacenForm(forms.ModelForm):
    class Meta:
        model = Almacen
        fields = (
            'nombre',
            'sede',
            'estado_alta_baja',
            )
            
    def clean(self):
        cleaned_data = super().clean()
        nombre = cleaned_data.get('nombre')
        sede = cleaned_data.get('sede')
        filtro = Almacen.objects.filter(nombre__unaccent__iexact = nombre, sede = sede )
        if nombre != self.instance.nombre:
            if len(filtro)>0:
                self.add_error('nombre', 'Ya existe un Almacén con este nombre.')
