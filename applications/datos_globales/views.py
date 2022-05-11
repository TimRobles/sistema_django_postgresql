from django.shortcuts import render
from applications.importaciones import *
from django import forms
from applications.datos_globales.models import Provincia, Distrito, Departamento

# Create your views here.

class DepartamentoForm(forms.Form):
    CHOICES=('1', '-------')
    departamento = forms.ModelChoiceField(queryset = Departamento.objects.all())
    provincia = forms.ChoiceField(choices=[CHOICES], required=False)
    distrito = forms.ChoiceField(choices=[CHOICES], required=False)
    ubigeo = forms.CharField(max_length=6, required=False)

def DepartamentoView(request):
    form = DepartamentoForm()
    
    return render(request, 'includes/prueba.html', context={'form':form})

class ProvinciaForm(forms.Form):
    provincia = forms.ModelChoiceField(queryset = Provincia.objects.all(), required=False, empty_label=None)

def ProvinciaView(request, id_departamento):
    form = ProvinciaForm()
    form.fields['provincia'].queryset = Provincia.objects.filter(departamento = id_departamento)
    return render(request, 'includes/form.html', context={'form':form})

class DistritoForm(forms.Form):
    distrito = forms.ModelChoiceField(queryset = Distrito.objects.all(), required=False, empty_label=None)

def DistritoView(request, id_provincia):
    form = DistritoForm()
    form.fields['distrito'].queryset = Distrito.objects.filter(provincia = id_provincia)
    return render(request, 'includes/form.html', context={'form':form})