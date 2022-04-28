from datetime import datetime, time
from applications.importaciones import *

from .forms import (
    VisitaForm,
    )

from .models import (
    Visita,
    )

class VisitaListView(ListView):
    model = Visita
    template_name = "recepcion/visita/inicio.html"
    context_object_name = 'contexto_visita'


def VisitaTabla(request):
    data = dict()
    if request.method == 'GET':
        template = 'recepcion/visita/inicio_tabla.html'
        context = {}
        context['contexto_visita'] = Visita.objects.all()

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
    success_url = reverse_lazy('visita_app:visita_inicio')

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
    success_url = reverse_lazy('visita_app:visita_inicio')

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