from django.core.paginator import Paginator
from applications.envio_clientes.forms import TransportistaBuscarForm, TransportistaForm
from applications.envio_clientes.models import Transportista
from applications.importaciones import *

# Create your views here.

class TransportistaListView(PermissionRequiredMixin, FormView):
    permission_required = ('envio_clientes.view_transportista')
    template_name = "transportistas/transportista/inicio.html"
    form_class = TransportistaBuscarForm
    success_url = '.'

    def get_form_kwargs(self):
        kwargs = super(TransportistaListView, self).get_form_kwargs()
        kwargs['filtro_razon_social'] = self.request.GET.get('razon_social')
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(TransportistaListView,self).get_context_data(**kwargs)
        transportistas = Transportista.objects.all()
        filtro_razon_social = self.request.GET.get('razon_social')

        contexto_filtro = []

        if filtro_razon_social:
            condicion = Q(razon_social__unaccent__icontains = filtro_razon_social.split(" ")[0])
            for palabra in filtro_razon_social.split(" ")[1:]:
                condicion &= Q(razon_social__unaccent__icontains = palabra)
            transportistas = transportistas.filter(condicion)
            contexto_filtro.append("razon_social=" + filtro_razon_social)
        
        context['contexto_filtro'] = "&".join(contexto_filtro)

        context['pagina_filtro'] = ""
        if self.request.GET.get('page'):
            if context['contexto_filtro']:
                context['pagina_filtro'] = f'&page={self.request.GET.get("page")}'
            else:
                context['pagina_filtro'] = f'page={self.request.GET.get("page")}'
        context['contexto_filtro'] = '?' + context['contexto_filtro']

        objectsxpage =  20 # Show 20 objects per page.

        if len(transportistas) > objectsxpage:
            paginator = Paginator(transportistas, objectsxpage)
            page_number = self.request.GET.get('page')
            transportistas = paginator.get_page(page_number)
   
        context['contexto_pagina'] = transportistas
        return context

def TransportistaTabla(request):
    data = dict()
    if request.method == 'GET':
        template = 'transportistas/transportista/inicio_tabla.html'
        context = {}
        transportistas = Transportista.objects.all()
        filtro_razon_social = request.GET.get('razon_social')

        contexto_filtro = []
        
        if filtro_razon_social:
            condicion = Q(razon_social__unaccent__icontains = filtro_razon_social.split(" ")[0])
            for palabra in filtro_razon_social.split(" ")[1:]:
                condicion &= Q(razon_social__unaccent__icontains = palabra)
            transportistas = transportistas.filter(condicion)
            contexto_filtro.append("razon_social=" + filtro_razon_social)
        
        context['contexto_filtro'] = "&".join(contexto_filtro)

        context['pagina_filtro'] = ""
        if request.GET.get('page'):
            if context['contexto_filtro']:
                context['pagina_filtro'] = f'&page={request.GET.get("page")}'
            else:
                context['pagina_filtro'] = f'page={request.GET.get("page")}'
        context['contexto_filtro'] = '?' + context['contexto_filtro']

        objectsxpage =  20 # Show 20 objects per page.

        if len(transportistas) > objectsxpage:
            paginator = Paginator(transportistas, objectsxpage)
            page_number = request.GET.get('page')
            transportistas = paginator.get_page(page_number)
   
        context['contexto_pagina'] = transportistas

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)

class TransportistaCreateView(PermissionRequiredMixin, BSModalCreateView):
    permission_required = ('envio_clientes.add_transportista')
    model = Transportista
    template_name = "transportistas/transportista/form.html"
    form_class = TransportistaForm
    success_url = reverse_lazy('transportistas_app:transportista_inicio')

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(TransportistaCreateView, self).get_context_data(**kwargs)
        context['accion']="Registrar"
        context['titulo']="Transportista"
        return context

    def form_valid(self, form):

        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)

        return super().form_valid(form)

class TransportistaUpdateView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('envio_clientes.change_transportista')

    model = Transportista
    template_name = "transportistas/transportista/form.html"
    form_class = TransportistaForm
    success_url = reverse_lazy('transportistas_app:transportista_inicio')

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(TransportistaUpdateView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        context['titulo'] = "Transportista"
        return context

    def form_valid(self, form):

        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)
        
        return super().form_valid(form)