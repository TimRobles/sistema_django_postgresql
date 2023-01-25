from django.shortcuts import render
from django.core.paginator import Paginator
from applications.importaciones import *
from django import forms
from applications.datos_globales.models import (
    NubefactRespuesta,
    Provincia, 
    Distrito, 
    Departamento, 
    TipoCambio,
    TipoCambioSunat,
    )
from applications.datos_globales.forms import TipoCambioForm

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
    provincia = forms.ModelChoiceField(queryset = Provincia.objects.all(), required=False)

def ProvinciaView(request, id_departamento):
    form = ProvinciaForm()
    form.fields['provincia'].queryset = Provincia.objects.filter(departamento = id_departamento)

    data = dict()
    if request.method == 'GET':
        template = 'includes/form.html'
        context = {'form':form}

        data['info'] = render_to_string(
            template,
            context,
            request=request
        ).replace('selected', 'selected=""')
        return JsonResponse(data)

class DistritoForm(forms.Form):
    distrito = forms.ModelChoiceField(queryset = Distrito.objects.all(), required=False)

def DistritoView(request, id_provincia):
    form = DistritoForm()
    form.fields['distrito'].queryset = Distrito.objects.filter(provincia = id_provincia)
    data = dict()
    if request.method == 'GET':
        template = 'includes/form.html'
        context = {'form':form}

        data['info'] = render_to_string(
            template,
            context,
            request=request
        ).replace('selected', 'selected=""')
        return JsonResponse(data)

def DistritoJsonView(request):
    if request.is_ajax():
        term = request.GET.get('term')
        buscar = Distrito.objects.all().filter(
            Q(nombre__icontains=term) | Q(codigo__icontains=term)
            )
        data = []
        for dato in buscar:
            data.append({
                'id' : dato.codigo,
                'nombre' : dato.__str__(),
                })
        return JsonResponse(data, safe=False)

class TipoCambioSunatView(PermissionRequiredMixin, TemplateView):
    permission_required = ('datos_globales.view_tipocambio')
    template_name = "datos_globales/tipo_cambio_sunat/inicio.html"
    
    def get_context_data(self, **kwargs):
        context = super(TipoCambioSunatView, self).get_context_data(**kwargs)
        tipo_cambio = TipoCambioSunat.objects.all()
        objectsxpage =  10 # Show 10 objects per page.

        if len(tipo_cambio) > objectsxpage:
            paginator = Paginator(tipo_cambio, objectsxpage)
            page_number = self.request.GET.get('page')
            tipo_cambio = paginator.get_page(page_number)

        context['contexto_tipo_cambio'] = tipo_cambio
        context['contexto_pagina'] = tipo_cambio
        return context

class TipoCambioListView(PermissionRequiredMixin, TemplateView):
    permission_required = ('datos_globales.view_tipocambio')
    template_name = "datos_globales/tipo_cambio/inicio.html"
    
    def get_context_data(self, **kwargs):
        context = super(TipoCambioListView, self).get_context_data(**kwargs)
        tipo_cambio = TipoCambio.objects.all()
        objectsxpage =  10 # Show 10 objects per page.

        if len(tipo_cambio) > objectsxpage:
            paginator = Paginator(tipo_cambio, objectsxpage)
            page_number = self.request.GET.get('page')
            tipo_cambio = paginator.get_page(page_number)

        context['contexto_tipo_cambio'] = tipo_cambio
        context['contexto_pagina'] = tipo_cambio
        return context
    

def TipoCambioTabla(request):
    data = dict()
    if request.method == 'GET':
        template = 'datos_globales/tipo_cambio/inicio_tabla.html'
        context = {}
        tipo_cambio = TipoCambio.objects.all()
        objectsxpage =  10 # Show 10 objects per page.

        if len(tipo_cambio) > objectsxpage:
            paginator = Paginator(tipo_cambio, objectsxpage)
            page_number = request.GET.get('page')
            tipo_cambio = paginator.get_page(page_number)

        context['contexto_tipo_cambio'] = tipo_cambio
        context['contexto_pagina'] = tipo_cambio

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)

class TipoCambioCreateView(PermissionRequiredMixin, BSModalCreateView):
    permission_required = ('datos_globales.add_tipocambio')
    model = TipoCambio
    template_name = "includes/formulario generico.html"
    form_class = TipoCambioForm
    success_url = reverse_lazy('datos_globales_app:tipo_cambio_inicio')

    def get_context_data(self, **kwargs):
        context = super(TipoCambioCreateView, self).get_context_data(**kwargs)
        context['accion']="Registrar"
        context['titulo']="Tipo de Cambio"
        return context

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

class TipoCambioUpdateView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('datos_globales.change_tipocambio')

    model = TipoCambio
    template_name = "includes/formulario generico.html"
    form_class = TipoCambioForm
    success_url = reverse_lazy('datos_globales_app:tipo_cambio_inicio')

    def get_context_data(self, **kwargs):
        context = super(TipoCambioUpdateView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        context['titulo'] = "Tipo de Cambio"
        return context

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

class TipoCambioDeleteView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('datos_globales.delete_tipocambio')

    model = TipoCambio
    template_name = "includes/eliminar generico.html"
    success_url = reverse_lazy('datos_globales_app:tipo_cambio_inicio')

    def get_context_data(self, **kwargs):
        context = super(TipoCambioDeleteView, self).get_context_data(**kwargs)
        context['accion'] = "Eliminar"
        context['titulo'] = "Tipo de Cambio"
        return context