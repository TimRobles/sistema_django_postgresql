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
            
    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        filtro = Almacen.objects.filter(nombre__unaccent__iexact = nombre)
        if nombre != self.instance.nombre:
            if len(filtro)>0:
                self.add_error('nombre', 'Ya existe un Almacén con este nombre.')

        return nombre