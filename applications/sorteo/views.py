from applications.importaciones import *
from applications.sorteo.forms import GanadorForm

from applications.sorteo.models import Ticket

# Create your views here.

class TicketListView(LoginRequiredMixin, ListView):
    model = Ticket
    template_name = "sorteo/lista.html"
    context_object_name = 'tickets'


class SorteoView(LoginRequiredMixin, TemplateView):
    template_name = "sorteo/sorteo.html"


def Perdedor(request):
    elegido = Ticket.objects.filter(elegido=False).order_by('?').first()
    elegido.elegido = True
    elegido.save()
    return HttpResponse(elegido)


def Ganador(request):
    elegido = Ticket.objects.filter(elegido=False).exclude(bloqueo=True).order_by('?').first()
    numero = Ticket.objects.exclude(premio=None)
    elegido.elegido = True
    elegido.premio = 'Premio N°%i' % (len(numero)+1)
    elegido.save()

    tickets = Ticket.objects.filter(elegido=True).filter(premio=None)
    for ticket in tickets:
        ticket.elegido = False
        ticket.save()
    return HttpResponse(elegido)


def Datos(request, ticket):
    obj = Ticket.objects.get(ticket=ticket)
    texto = 'Nombre: %s\nEmpresa: %s' % (obj.contacto, obj.razon_social)
    return HttpResponse(texto)


class GanadorFormView(FormView):
    template_name = "includes/formulario generico.html"
    form_class = GanadorForm
    success_url = reverse_lazy('sorteo_app:lista')

    def form_valid(self, form):
        obj = Ticket.objects.get(ticket=form.cleaned_data.get('ticket'))
        numero = Ticket.objects.exclude(premio=None)
        obj.premio = 'Premio N°%i' % (len(numero)+1)
        obj.save()
        return super().form_valid(form)


def Reiniciar(request):
    tickets = Ticket.objects.exclude(premio=None)
    for ticket in tickets:
        ticket.premio = None
        ticket.save()

    tickets = Ticket.objects.filter(elegido=True)
    for ticket in tickets:
        ticket.elegido = False
        ticket.save()

    return HttpResponse('Reiniciado')
