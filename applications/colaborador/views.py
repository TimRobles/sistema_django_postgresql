from datetime import datetime, time

from requests import request
from applications.importaciones import *

from .forms import (
    DatosContratoPlanillaForm,
    )

from .models import (
    DatosContratoPlanilla,
    )

class DatosContratoPlanillaListView(ListView):
    model = DatosContratoPlanilla
    template_name = "colaborador/datos_contrato/planilla/inicio.html"
    context_object_name = 'contexto_datoscontratoplanilla'

    def get_queryset(self):
        queryset = super(DatosContratoPlanillaListView, self).get_queryset()
        return queryset

def DatosContratoPlanillaTabla(request):
    data = dict()
    if request.method == 'GET':
        template = 'colaborador/datos_contrato/planilla/inicio_tabla.html'
        context = {}
        datoscontratoplanilla = DatosContratoPlanilla.objects.all()
        context['contexto_datoscontratoplanilla'] = datoscontratoplanilla

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)

class DatosContratoPlanillaCreateView(BSModalCreateView):
    model = DatosContratoPlanilla
    template_name = "colaborador/datos_contrato/planilla/registrar.html"
    form_class = DatosContratoPlanillaForm
    success_url = reverse_lazy('colaborador_app:datos_contrato_planilla_inicio')

    def get_context_data(self, **kwargs):
        context = super(DatosContratoPlanillaCreateView, self).get_context_data(**kwargs)
        context['accion']="Registrar"
        context['titulo']="datos del contrato de planilla"
        return context

    def form_valid(self, form):
        registro_guardar(form.instance, self.request)

        return super().form_valid(form)

