from applications.importaciones import *
from applications.sorteo_webinar.forms import CargarExcelForm
from applications.sorteo_webinar.funciones import llenar_datos
from applications.sorteo_webinar.models import Participante

class ParticipanteListView(ListView):
    model = Participante
    template_name = "sorteo webinar/lista.html"
    context_object_name = 'participantes'

class SorteoView(LoginRequiredMixin, TemplateView):
    template_name = "sorteo webinar/sortear.html"

def Sortear(request):
    elegidos = Participante.objects.filter(elegido=True).filter(premio=None)
    premios = Participante.objects.exclude(premio=None)
    ganador = Participante.objects.filter(elegido=False).order_by('?').first()
    texto = '<h4>Nombre: %s</h4>' % (ganador.nombre_completo)
    if len(elegidos) % 3 == 2:
        ganador.elegido = True
        ganador.premio = 'Premio N°%i' % (len(premios)+1)
        ganador.save()
        titulo = "<h2>¡Felicidades!</h2>"

        limpiar = Participante.objects.filter(elegido=True).filter(premio=None)
        for limpia in limpiar:
            limpia.elegido = False
            limpia.save()
    else:
        ganador.elegido = True
        ganador.save()
        titulo = "<h2>¡Gracias por participar!</h2>"

    return HttpResponse("%s | %s | %s" % (ganador.nombre_completo, titulo, texto))

def Datos(request):
    data = []
    participantes = Participante.objects.all()
    for participante in participantes:
        data.append({'nombre':participante.nombre_completo})
    return JsonResponse(data, safe=False)

def Limpiar(request):
    participantes = Participante.objects.all()
    for participante in participantes:
        participante.premio = None
        participante.elegido = False
        participante.save()
    return HttpResponseRedirect(reverse_lazy('sorteo_webinar_app:sorteo_webinar_lista'))

def Eliminar(request):
    participantes = Participante.objects.all()
    for participante in participantes:
        participante.delete()
    return HttpResponseRedirect(reverse_lazy('sorteo_webinar_app:sorteo_webinar_lista'))


class CargarExcelFormView(BSModalFormView):
    template_name = "includes/formulario generico.html"
    form_class = CargarExcelForm
    success_url = reverse_lazy('sorteo_webinar_app:sorteo_webinar_lista')

    def form_valid(self, form):
        excel = form.cleaned_data.get('excel')
        llenar_datos(excel)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(CargarExcelFormView, self).get_context_data(**kwargs)
        context['accion'] = 'Cargar'
        context['titulo'] = 'Participantes'
        return context
    