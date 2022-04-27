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
    template_name = "includes/formulario generico.html"
    form_class = VisitaForm
    success_url = reverse_lazy('visita_app:visita_inicio')

    def form_valid(self, form):

        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(VisitaCreateView, self).get_context_data(**kwargs)
        context['accion']="Registrar"
        context['titulo']="Visita"
        return context


