from datetime import datetime, time
from applications.importaciones import *

from .forms import (
    VisitaForm,VisitaBuscarForm,
    AsistenciaForm,
    )

from .models import (
    Visita,
    Asistencia,
    )

class VisitaListView(FormView):
    template_name = "recepcion/visita/inicio.html"
    form_class = VisitaBuscarForm
    success_url = '.'

    def get_form_kwargs(self):
        kwargs = super(VisitaListView, self).get_form_kwargs()
        kwargs['filtro_nombre'] = self.request.GET.get('nombre')
        kwargs['filtro_fecha'] = self.request.GET.get('fecha')
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(VisitaListView,self).get_context_data(**kwargs)
        visitas = Visita.objects.all()
        filtro_nombre = self.request.GET.get('nombre')
        filtro_fecha = self.request.GET.get('fecha')
        if filtro_nombre and filtro_fecha:
            condicion = Q(nombre__unaccent__icontains = filtro_nombre.upper()) & Q(fecha_registro = datetime.strptime(filtro_fecha, "%Y-%m-%d").date())
            visitas = visitas.filter(condicion)
            context['contexto_filtro'] = "?nombre=" + filtro_nombre + '&fecha=' + filtro_fecha   
        elif filtro_fecha:
            condicion = Q(fecha_registro = datetime.strptime(filtro_fecha, "%Y-%m-%d").date())
            visitas = visitas.filter(condicion)
            context['contexto_filtro'] = "?nombre=" + filtro_nombre + '&fecha=' + filtro_fecha
        elif filtro_nombre:
            condicion = Q(nombre__unaccent__icontains = filtro_nombre.upper())
            visitas = visitas.filter(condicion)
            context['contexto_filtro'] = "?nombre=" + filtro_nombre + '&fecha=' + filtro_fecha
   
        context['contexto_visita'] = visitas
        return context

def VisitaTabla(request):
    data = dict()
    if request.method == 'GET':
        template = 'recepcion/visita/inicio_tabla.html'
        context = {}
        visitas = Visita.objects.all()
        filtro_nombre = request.GET.get('nombre')
        filtro_fecha = request.GET.get('fecha')
        if filtro_nombre and filtro_fecha:
            condicion = Q(nombre__icontains = filtro_nombre.upper()) & Q(fecha_registro = datetime.strptime(filtro_fecha, "%Y-%m-%d").date())
            visitas = visitas.filter(condicion)
   
        elif filtro_fecha:
            condicion = Q(fecha_registro = datetime.strptime(filtro_fecha, "%Y-%m-%d").date())
            visitas = visitas.filter(condicion)

        elif filtro_nombre:
            condicion = Q(nombre__icontains = filtro_nombre.upper())
            visitas = visitas.filter(condicion)

        context['contexto_visita'] = visitas

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)

class VisitaCreateView(BSModalCreateView):
    model = Visita
    template_name = "recepcion/visita/registrar.html"
    form_class = VisitaForm
    success_url = reverse_lazy('recepcion_app:visita_inicio')

    def get_context_data(self, **kwargs):
        context = super(VisitaCreateView, self).get_context_data(**kwargs)
        context['accion']="Registrar"
        context['titulo']="Visita"
        return context

    def form_valid(self, form):

        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)

        return super().form_valid(form)

class VisitaRegistrarSalidaView(BSModalDeleteView):
    model = Visita
    template_name = "includes/eliminar generico.html"
    success_url = reverse_lazy('recepcion_app:visita_inicio')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        hour = datetime.now()
        self.object.hora_salida = hour.strftime("%H:%M")
        registro_guardar(self.object, self.request)
        self.object.save()
        messages.success(request, MENSAJE_REGISTRAR_SALIDA)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(VisitaRegistrarSalidaView, self).get_context_data(**kwargs)
        context['accion'] = "Registrar Salida"
        context['titulo'] = "Visita"
        context['dar_baja'] = "true"
        context['item'] = self.object.nombre
        return context


class AsistenciaListView(ListView):
    model = Asistencia
    template_name = "recepcion/asistencia/inicio.html"
    context_object_name = 'contexto_asistencia'

def AsistenciaTabla(request):
    data = dict()
    if request.method == 'GET':
        template = 'recepcion/asistencia/inicio_tabla.html'
        context = {}
        context['contexto_asistencia'] = Asistencia.objects.all()

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)

class AsistenciaCreateView(BSModalCreateView):
    model = Asistencia
    template_name = "recepcion/asistencia/registrar.html"
    form_class = AsistenciaForm
    success_url = reverse_lazy('recepcion_app:asistencia_inicio')

    def get_context_data(self, **kwargs):
        context = super(AsistenciaCreateView, self).get_context_data(**kwargs)
        context['accion']="Registrar"
        context['titulo']="Asistencia"
        return context

    def form_valid(self, form):
        registro_guardar(form.instance, self.request)

        return super().form_valid(form)

class AsistenciaRegistrarSalidaView(BSModalDeleteView):
    model = Asistencia
    template_name = "includes/eliminar generico.html"
    success_url = reverse_lazy('recepcion_app:asistencia_inicio')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        hour = datetime.now()
        self.object.hora_salida = hour.strftime("%H:%M")
        registro_guardar(self.object, self.request)
        self.object.save()
        messages.success(request, MENSAJE_REGISTRAR_SALIDA)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(AsistenciaRegistrarSalidaView, self).get_context_data(**kwargs)
        context['accion'] = "Registrar Salida"
        context['titulo'] = "Asistencia"
        context['dar_baja'] = "true"
        context['item'] = self.object.usuario
        return context
