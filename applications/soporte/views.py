from django.shortcuts import render
from applications.importaciones import *
from django.core.paginator import Paginator


from django import forms

from .forms import (
    ProblemaBuscarForm,
    ProblemaForm,
)

from .models import (
    Problema,
    ProblemaDetalle
)

class ProblemaListView(FormView):
    template_name = "soporte/problema/inicio.html"
    form_class = ProblemaBuscarForm

    def get_form_kwargs(self):
        kwargs = super(ProblemaListView, self).get_form_kwargs()
        kwargs['filtro_titulo'] = self.request.GET.get('titulo')
        kwargs['filtro_estado'] = self.request.GET.get('estado')
        kwargs['filtro_usuario'] = self.request.GET.get('usuario')
        return kwargs

    
    def get_context_data(self, **kwargs):
        context = super(ProblemaListView,self).get_context_data(**kwargs)
        problemas = Problema.objects.all().order_by('created_at')

        filtro_titulo = self.request.GET.get('titulo')
        filtro_estado = self.request.GET.get('estado')
        filtro_usuario = self.request.GET.get('usuario')

        contexto_filtro = []

        if filtro_titulo:
            condicion = Q(titulo__unaccent__icontains = filtro_titulo.split(" ")[0])
            for palabra in filtro_titulo.split(" ")[1:]:
                condicion &= Q(titulo__unaccent__icontains = palabra)
            encuesta_crm = encuesta_crm.filter(condicion)
            contexto_filtro.append(f"titulo={filtro_titulo}")

        if filtro_estado:
            condicion = Q(estado = filtro_estado)
            nota_control_calidad_stock = nota_control_calidad_stock.filter(condicion)
            contexto_filtro.append(f"estado={filtro_estado}")
        
        if filtro_usuario:
            condicion = Q(created_by = filtro_usuario)
            nota_control_calidad_stock = nota_control_calidad_stock.filter(condicion)
            contexto_filtro.append(f"usuario={filtro_usuario}")        

        context['contexto_filtro'] = "&".join(contexto_filtro)

        context['pagina_filtro'] = ""
        if self.request.GET.get('page'):
            if context['contexto_filtro']:
                context['pagina_filtro'] = f'&page={self.request.GET.get("page")}'
            else:
                context['pagina_filtro'] = f'page={self.request.GET.get("page")}'
        context['contexto_filtro'] = '?' + context['contexto_filtro']

        objectsxpage = 10 # Show 10 objects per page.

        if len(problemas) > objectsxpage:
            paginator = Paginator(problemas, objectsxpage)
            page_number = self.request.GET.get('page')
            problemas = paginator.get_page(page_number)

        context['contexto_problemas'] = problemas
        context['contexto_pagina'] = problemas

        return context


def ProblemaTabla(request):
    data = dict()
    if request.method == 'GET':
        template = 'soporte/problema/inicio_tabla.html'
        context = {}
        problemas = Problema.objects.all()

        filtro_titulo = request.GET.get('titulo')
        filtro_estado = request.GET.get('estado')
        filtro_usuario = request.GET.get('usuario')
        
        contexto_filtro = []

        if filtro_titulo:
            condicion = Q(titulo__unaccent__icontains = filtro_titulo.split(" ")[0])
            for palabra in filtro_titulo.split(" ")[1:]:
                condicion &= Q(titulo__unaccent__icontains = palabra)
            encuesta_crm = encuesta_crm.filter(condicion)
            contexto_filtro.append(f"titulo={filtro_titulo}")

        if filtro_estado:
            condicion = Q(estado = filtro_estado)
            nota_control_calidad_stock = nota_control_calidad_stock.filter(condicion)
            contexto_filtro.append(f"estado={filtro_estado}")

        if filtro_usuario:
            condicion = Q(created_by = filtro_usuario)
            nota_control_calidad_stock = nota_control_calidad_stock.filter(condicion)
            contexto_filtro.append(f"usuario={filtro_usuario}")

        context['contexto_filtro'] = "&".join(contexto_filtro)

        context['pagina_filtro'] = ""
        if request.GET.get('page'):
            if context['contexto_filtro']:
                context['pagina_filtro'] = f'&page={request.GET.get("page")}'
            else:
                context['pagina_filtro'] = f'page={request.GET.get("page")}'
        context['contexto_filtro'] = '?' + context['contexto_filtro']

        objectsxpage = 10 # Show 10 objects per page.

        if len(problemas) > objectsxpage:
            paginator = Paginator(problemas, objectsxpage)
            page_number = request.GET.get('page')
            problemas = paginator.get_page(page_number)
   
        context['contexto_problemas'] = problemas
        context['contexto_pagina'] = problemas

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)


class ProblemaCreateView(BSModalCreateView):
    model = Problema
    template_name = "includes/formulario generico.html"
    form_class = ProblemaForm
    success_url = reverse_lazy('soporte_app:problema_inicio')

    def get_context_data(self, **kwargs):
        context = super(ProblemaCreateView, self).get_context_data(**kwargs)
        context['accion']="Registrar"
        context['titulo']="Problema"
        return context

    def form_valid(self, form):
        form.instance.estado = 1
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)