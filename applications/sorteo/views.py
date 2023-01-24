from slugify import slugify
from applications.importaciones import *
from applications.sorteo.forms import CargarExcelForm, SorteoForm, TicketForm
from applications.sorteo.funciones import llenar_datos

from applications.sorteo.models import Sorteo, Ticket

# Create your views here.

class SorteoListView(LoginRequiredMixin, ListView):
    model = Sorteo
    template_name = "sorteo/sorteo/lista.html"
    context_object_name = 'sorteos'


def SorteoTabla(request):
    data = dict()
    if request.method == 'GET':
        template = 'sorteo/sorteo/lista_tabla.html'
        context = {}
        context['sorteos'] = Sorteo.objects.all()

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)


class SorteoCreateView(BSModalCreateView):
    model = Sorteo
    template_name = "includes/formulario generico.html"
    form_class = SorteoForm
    success_url = '.'

    def form_valid(self, form):
        form.instance.slug = slugify(form.instance.nombre_sorteo)
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["accion"] = 'Agregar'
        context["titulo"] = 'Sorteo'
        return context


class SorteoUpdateView(BSModalUpdateView):
    model = Sorteo
    template_name = "includes/formulario generico.html"
    form_class = SorteoForm
    success_url = '.'

    def form_valid(self, form):
        form.instance.slug = slugify(form.instance.nombre_sorteo)
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["accion"] = 'Actualizar'
        context["titulo"] = 'Sorteo'
        return context


class SorteoDetailView(DetailView):
    model = Sorteo
    template_name = "sorteo/sorteo/detalle.html"
    context_object_name = 'sorteo'


def SorteoDetailTabla(request, slug):
    data = dict()
    if request.method == 'GET':
        template = 'sorteo/sorteo/detalle_tabla.html'
        context = {}
        context['sorteo'] = Sorteo.objects.get(slug=slug)

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)


class TicketCreateView(BSModalCreateView):
    model = Ticket
    template_name = "includes/formulario generico.html"
    form_class = TicketForm
    success_url = '.'

    def form_valid(self, form):
        form.instance.sorteo = Sorteo.objects.get(id=self.kwargs['id_sorteo'])
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['sorteo'] = Sorteo.objects.get(id=self.kwargs['id_sorteo'])
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["accion"] = 'Agregar'
        context["titulo"] = 'Ticket'
        return context


class SorteoIniciarView(LoginRequiredMixin, TemplateView):
    template_name = "sorteo/sorteo/iniciar.html"
    
    def get_context_data(self, **kwargs):
        context = super(SorteoIniciarView, self).get_context_data(**kwargs)
        context['sorteo'] = Sorteo.objects.get(slug=self.kwargs['slug'])
        context['url_datos'] = reverse_lazy('sorteo_app:datos', kwargs={'slug':self.kwargs['slug']})
        context['url_sortear'] = reverse_lazy('sorteo_app:sortear', kwargs={'slug':self.kwargs['slug']})
        return context
    

def Sortear(request, slug):
    sorteo = Sorteo.objects.get(slug=slug)
    elegidos = Ticket.objects.filter(sorteo=sorteo).filter(elegido=True).filter(premio=None)
    premios = Ticket.objects.filter(sorteo=sorteo).exclude(premio=None)
    ticket = Ticket.objects.filter(sorteo=sorteo).filter(elegido=False).exclude(bloqueo=True).order_by('?').first()
    textos = []
    textos.append(f"{sorteo.nombre_dato_uno}: {ticket.dato_uno}")
    textos.append(f"{sorteo.nombre_dato_dos}: {ticket.dato_dos}")
    # if sorteo.nombre_dato_tres:
    #     textos.append(f"{sorteo.nombre_dato_tres}: {ticket.dato_tres}")
    # if sorteo.nombre_dato_cuatro:
    #     textos.append(f"{sorteo.nombre_dato_cuatro}: {ticket.dato_cuatro}")
    texto = f'<h4>{"</br>".join(textos)}</h4>'
    if len(elegidos) % 3 == 2:
        ticket.elegido = True
        ticket.premio = 'Premio N°%i' % (len(premios)+1)
        ticket.save()
        titulo = "<h2>¡Felicidades!</h2>"

        limpiar = Ticket.objects.filter(sorteo=sorteo).filter(elegido=True).filter(premio=None)
        for limpia in limpiar:
            limpia.elegido = False
            limpia.save()
    else:
        ticket.elegido = True
        ticket.save()
        titulo = "<h2>¡Gracias por participar!</h2>"

    return HttpResponse("%s | %s | %s" % (ticket.__str__(), titulo, texto))


def Datos(request, slug):
    data = []
    sorteo = Sorteo.objects.get(slug=slug)
    tickets = Ticket.objects.filter(sorteo=sorteo)
    for ticket in tickets:
        data.append({'nombre':ticket.__str__()})
    return JsonResponse(data, safe=False)


def Reiniciar(request, slug):
    sorteo = Sorteo.objects.get(slug=slug)
    tickets = Ticket.objects.filter(sorteo=sorteo).exclude(premio=None)
    for ticket in tickets:
        ticket.premio = None
        ticket.save()

    tickets = Ticket.objects.filter(sorteo=sorteo).filter(elegido=True)
    for ticket in tickets:
        ticket.elegido = False
        ticket.save()

    return HttpResponse('Reiniciado')


def Eliminar(request, slug):
    sorteo = Sorteo.objects.get(slug=slug)
    tickets = Ticket.objects.filter(sorteo=sorteo)
    for ticket in tickets:
        ticket.delete()

    return HttpResponse('Eliminando')


class CargarExcelFormView(BSModalFormView):
    template_name = "includes/formulario generico.html"
    form_class = CargarExcelForm
    success_url = reverse_lazy('sorteo_webinar_app:sorteo_webinar_lista')

    def form_valid(self, form):
        if self.request.session['primero']:
            sorteo = Sorteo.objects.get(slug=self.kwargs['slug'])
            excel = form.cleaned_data.get('excel')
            llenar_datos(excel, sorteo)
            self.request.session['primero'] = False
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        self.request.session['primero'] = True
        context = super(CargarExcelFormView, self).get_context_data(**kwargs)
        context['accion'] = 'Cargar'
        context['titulo'] = 'Tickets'
        return context
    