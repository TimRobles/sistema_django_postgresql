from django import forms
from applications.datos_globales.models import Area, Cargo, Moneda, TipoInterlocutor, Pais

class MonedaForm(forms.ModelForm):
    class Meta:
        model = Moneda
        fields = (
            'nombre',
            'abreviatura',
            'simbolo',
            'estado',
            )

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        filtro = Moneda.objects.filter(nombre__unaccent__iexact = nombre)
        if nombre != self.instance.nombre:
            if len(filtro)>0:
                self.add_error('nombre', 'Ya existe una Moneda con este nombre')

        return nombre


class AreaForm(forms.ModelForm):
    class Meta:
        model = Area
        fields = (
            'nombre',
            'estado',
            )

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        filtro = Area.objects.filter(nombre__unaccent__iexact = nombre)
        if nombre != self.instance.nombre:
            if len(filtro)>0:
                self.add_error('nombre', 'Ya existe un Área con este nombre')

        return nombre


class CargoForm(forms.ModelForm):
    class Meta:
        model = Cargo
        fields = (
            'area',
            'nombre',
            )

    def clean(self):
        cleaned_data = super().clean()
        nombre = cleaned_data.get('nombre')
        area = cleaned_data.get('area')
        filtro = Cargo.objects.filter(nombre__unaccent__iexact = nombre, area = area)
        if nombre != self.instance.nombre:
            if len(filtro)>0:
                self.add_error('nombre', 'Ya existe un Cargo con este nombre')
                

class TipoInterlocutorForm(forms.ModelForm):
    class Meta:
        model = TipoInterlocutor
        fields = (
            'nombre',
            )

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        filtro = TipoInterlocutor.objects.filter(nombre__unaccent__iexact = nombre)
        if nombre != self.instance.nombre:
            if len(filtro)>0:
                self.add_error('nombre', 'Ya existe un Tipo de Interlocutor con este nombre')

        return nombre

class PaisForm(forms.ModelForm):
    class Meta:
        model = Pais
        fields = (
            'nombre',
            )

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        filtro = Pais.objects.filter(nombre__unaccent__iexact = nombre)
        if nombre != self.instance.nombre:
            if len(filtro)>0:
                self.add_error('nombre', 'Ya existe un País con este nombre')

        return nombre