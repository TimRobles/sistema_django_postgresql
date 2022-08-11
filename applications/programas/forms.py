from django import forms
from django.db.models import Max

from applications.programas.models import NivelUno, NivelDos, NivelTres, NivelCuatro

class NivelUnoForm(forms.ModelForm):
    class Meta:
        model = NivelUno
        fields = (
            'orden',
            'nombre',
            'icono',
            )
    
    def __init__(self, *args, **kwargs):
        max_orden = NivelUno.objects.aggregate(Max('orden'))['orden__max']
        if max_orden == None:
            max_orden = 0
        super(NivelUnoForm, self).__init__(*args, **kwargs)
        self.fields['orden'].initial = max_orden + 1
        
    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        filtro = NivelUno.objects.filter(nombre__unaccent__iexact = nombre)
        if nombre != self.instance.nombre:
            if len(filtro)>0:
                self.add_error('nombre', 'Ya existe un Nivel Uno con este nombre')

        return nombre

class NivelDosForm(forms.ModelForm):
    class Meta:
        model = NivelDos
        fields = (
            'orden',
            'nombre',
            'app_name',
            'url_name',
            'nivel_uno',
            'icono',
            )

    def clean(self):
        cleaned_data = super().clean()
        orden = cleaned_data.get('orden')
        nombre = cleaned_data.get('nombre')
        nivel_uno = cleaned_data.get('nivel_uno')
        filtro_orden = NivelDos.objects.filter(orden = orden, nivel_uno = nivel_uno)
        filtro = NivelDos.objects.filter(nombre__unaccent__iexact = nombre, nivel_uno = nivel_uno)

        if orden != self.instance.orden:
            if len(filtro_orden)>0:
                self.add_error('orden', 'Ya existe un Nivel Dos con este orden')

        if nombre != self.instance.nombre:
            if len(filtro)>0:
                self.add_error('nombre', 'Ya existe un Nivel Dos con este nombre')        
        

class NivelTresForm(forms.ModelForm):
    class Meta:
        model = NivelTres
        fields = (
            'orden',
            'nombre',
            'app_name',
            'url_name',
            'nivel_dos',
            'icono',
            )

    def clean(self):
        cleaned_data = super().clean()
        orden = cleaned_data.get('orden')
        nombre = cleaned_data.get('nombre')
        nivel_dos = cleaned_data.get('nivel_dos')
        filtro_orden = NivelTres.objects.filter(orden = orden, nivel_dos = nivel_dos)
        filtro = NivelTres.objects.filter(nombre__unaccent__iexact = nombre, nivel_dos = nivel_dos)
        if orden != self.instance.orden:
            if len(filtro_orden)>0:
                self.add_error('orden', 'Ya existe un Nivel Tres con este orden')
        if nombre != self.instance.nombre:
            if len(filtro)>0:
                self.add_error('nombre', 'Ya existe un Nivel Tres con este nombre')

class NivelCuatroForm(forms.ModelForm):
    class Meta:
        model = NivelCuatro
        fields = (
            'orden',
            'nombre',
            'app_name',
            'url_name',
            'nivel_tres',
            'icono',
            )

    def clean(self):
        cleaned_data = super().clean()
        orden = cleaned_data.get('orden')
        nombre = cleaned_data.get('nombre')
        nivel_tres = cleaned_data.get('nivel_tres')
        filtro_orden = NivelCuatro.objects.filter(orden = orden, nivel_tres = nivel_tres)
        filtro = NivelCuatro.objects.filter(nombre__unaccent__iexact = nombre, nivel_tres = nivel_tres)
        if orden != self.instance.orden:
            if len(filtro_orden)>0:
                self.add_error('orden', 'Ya existe un Nivel Cuatro con este orden')
        if nombre != self.instance.nombre:
            if len(filtro)>0:
                self.add_error('nombre', 'Ya existe un Nivel Cuatro con este nombre')

        return nombre