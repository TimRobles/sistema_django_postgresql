from django.shortcuts import render
from applications.importaciones import *
from django import forms
from applications.datos_globales.models import (
    NubefactRespuesta,
    Provincia, 
    Distrito, 
    Departamento, 
    TipoCambio,
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
    
    data = [{"itemName":"Lima","id":'010101'},
            {"itemName":"Test item no. 2","id":6},
            {"itemName":"Test item no. 3","id":7},
            {"itemName":"Test item no. 4","id":8},
            {"itemName":"Test item no. 5","id":9},
            {"itemName":"Test item no. 6","id":10},
            {"itemName":"Test item no. 7","id":11}]

    buscar = Departamento.objects.all()
    data = []
    for dato in buscar:
        item = {}
        item['id'] = dato.codigo
        item['itemName'] = dato.nombre
        data.append(item)
    return JsonResponse(data, safe=False)

class TipoCambioListView(PermissionRequiredMixin, ListView):
    permission_required = ('datos_globales.view_tipocambio')

    model = TipoCambio
    template_name = "datos_globales/tipo_cambio/inicio.html"
    context_object_name = 'contexto_tipo_cambio'

def TipoCambioTabla(request):
    data = dict()
    if request.method == 'GET':
        template = 'datos_globales/tipo_cambio/inicio_tabla.html'
        context = {}
        context['contexto_tipo_cambio'] = TipoCambio.objects.all()

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