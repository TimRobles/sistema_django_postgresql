from django.shortcuts import render
from django import forms
from applications.importaciones import *
from .models import(
    LineaCredito,
)

from .forms import(
    LineaCreditoForm,
)

class LineaCreditoView(ListView):
    model = LineaCredito
    template_name = 'cobranza/linea_credito/inicio.html'
    context_object_name = 'contexto_linea_credito'

def LineaCreditoTabla(request):
    data = dict()
    if request.method == 'GET':
        template = 'cobranza/linea_credito/inicio_tabla.html'
        context = {}
        context['contexto_linea_credito'] = LineaCredito.objects.all()

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)

class LineaCreditoCreateView(BSModalCreateView):
    model = LineaCredito
    template_name = "includes/formulario generico.html"
    form_class = LineaCreditoForm
    success_url = reverse_lazy('cobranza_app:linea_credito_inicio')

    def form_valid(self, form):

        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(LineaCreditoCreateView, self).get_context_data(**kwargs)
        context['accion']="Registrar"
        context['titulo']="Linea de Crédito"
        return context

class LineaCreditoUpdateView(BSModalUpdateView):
    model = LineaCredito
    template_name = "includes/formulario generico.html"
    form_class = LineaCreditoForm
    success_url = reverse_lazy('cobranza_app:linea_credito_inicio')

    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(LineaCreditoUpdateView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        context['titulo'] = "Linea de Crédito"
        return context
