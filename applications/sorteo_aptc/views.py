
from applications.funciones import numeroXn
from applications.sorteo_aptc.forms import RespuestaUsuarioForm
from applications.sorteo_aptc.models import UsuarioAPTC
from applications.importaciones import *


# Create your views here.

class UsuarioAPTCListView(ListView):
    model = UsuarioAPTC
    template_name = "sorteoaptc/sorteo lista.html"
    context_object_name = 'usuarios'

def UsuarioAPTCTabla(request):
    data = dict()
    if request.method == 'GET':
        template = 'sorteoaptc/sorteo tabla.html'
        context = {}
        context['usuarios'] = UsuarioAPTC.objects.all()
        
        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)


class UsuarioAPTCCreateView(BSModalCreateView):
    template_name = "sorteoaptc/sorteo usuario.html"
    model = UsuarioAPTC
    form_class = RespuestaUsuarioForm
    success_url = reverse_lazy('sorteo_aptc_app:respuesta_lista')

    def form_valid(self, form):
        buscar = UsuarioAPTC.objects.filter(
            fecha = date.today(),
            tipo_documento = form.cleaned_data['tipo_documento'],
            numero_documento = form.cleaned_data['numero_documento'],
            )
        if len(buscar)>0:
            form.add_error('numero_documento', 'Ya se encuentra registrado.')
            return super().form_invalid(form)

        nuevo_ticket = numeroXn(len(UsuarioAPTC.objects.all()) + 1, 4)
        form.instance.ticket = nuevo_ticket
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(UsuarioAPTCCreateView, self).get_context_data(**kwargs)
        context['accion'] = "Registrar"
        context['titulo'] = "Participante"
        return context


class UsuarioAPTCUpdateView(BSModalUpdateView):
    template_name = "sorteoaptc/sorteo usuario.html"
    model = UsuarioAPTC
    form_class = RespuestaUsuarioForm
    success_url = reverse_lazy('sorteo_aptc_app:respuesta_lista')

    def get_context_data(self, **kwargs):
        context = super(UsuarioAPTCUpdateView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        context['titulo'] = "Participante"
        return context


class SorteoView(LoginRequiredMixin, TemplateView):
    template_name = "sorteoaptc/sorteo sortear.html"

def Sortear(request):

    premios = UsuarioAPTC.objects.exclude(premio=None)
    elegidos = UsuarioAPTC.objects.filter(elegido=True).filter(premio=None)
    ticket = UsuarioAPTC.objects.filter(fecha = date.today(), elegido=False).exclude(bloqueo=True).order_by('?').first()
    if ticket.empresa:
        empresa = '</br>Empresa: %s' % ticket.empresa
    else:
        empresa = ""
    texto = '<h4>Ticket N° %s</br>Nombre: %s%s</h4>' % (ticket.ticket, ticket.nombre, empresa)
    if len(elegidos) % 3 == 2:
        ticket.elegido = True
        ticket.premio = 'Premio N°%i' % (len(premios)+1)
        ticket.save()
        titulo = "<h2>¡Felicidades!</h2>"

        limpiar = UsuarioAPTC.objects.filter(elegido=True).filter(premio=None)
        for limpia in limpiar:
            limpia.elegido = False
            limpia.save()
    else:
        ticket.elegido = True
        ticket.save()
        titulo = "<h2>¡Gracias por participar!</h2>"

    return HttpResponse("%s | %s | %s" % (ticket.__str__(), titulo, texto))


def Datos(request, ticket):
    obj = UsuarioAPTC.objects.get(ticket=ticket)
    if obj.empresa:
        empresa = '</br>Empresa: %s' % obj.empresa
    else:
        empresa = ""
    texto = '<h4>Ticket N° %s</br>Nombre: %s%s</h4>' % (obj.ticket, obj.nombre, empresa)
    return HttpResponse(texto)


def Reiniciar(request):
    tickets = UsuarioAPTC.objects.exclude(premio=None)
    for ticket in tickets:
        ticket.premio = None
        ticket.save()

    tickets = UsuarioAPTC.objects.filter(elegido=True)
    for ticket in tickets:
        ticket.elegido = False
        ticket.save()

    return HttpResponse('Reiniciado')


