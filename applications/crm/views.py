from django.core.paginator import Paginator
from django.shortcuts import render
from applications.importaciones import *
from applications.crm.forms import ClienteCRMBuscarForm, ClienteCRMDetalleForm, ClienteCRMForm
from applications.crm.models import ClienteCRM, ClienteCRMDetalle
from applications.clientes.models import ClienteInterlocutor, InterlocutorCliente

class ClienteCRMListView(PermissionRequiredMixin, FormView):
    permission_required = ('crm.view_clientes_crm')
    template_name = "crm/clientes_crm/inicio.html"
    form_class = ClienteCRMBuscarForm
    success_url = '.'

    def get_form_kwargs(self):
        kwargs = super(ClienteCRMListView, self).get_form_kwargs()
        kwargs['filtro_razon_social'] = self.request.GET.get('razon_social')
        kwargs['filtro_medio'] = self.request.GET.get('medio')
        kwargs['filtro_estado'] = self.request.GET.get('estado')
        kwargs['filtro_pais'] = self.request.GET.get('pais')
        kwargs['filtro_fecha_registro'] = self.request.GET.get('fecha_registro')

        return kwargs

    def get_context_data(self, **kwargs):
        context = super(ClienteCRMListView,self).get_context_data(**kwargs)
        clientes_crm = ClienteCRM.objects.all()
        
        filtro_razon_social = self.request.GET.get('razon_social')
        filtro_medio = self.request.GET.get('medio')
        filtro_estado = self.request.GET.get('estado')
        filtro_pais = self.request.GET.get('pais')
        filtro_fecha_registro = self.request.GET.get('fecha_registro')
        
        contexto_filtro = []

        if filtro_razon_social:
            condicion = Q(cliente_crm__razon_social__unaccent__icontains = filtro_razon_social.split(" ")[0])
            for palabra in filtro_razon_social.split(" ")[1:]:
                condicion &= Q(cliente_crm__razon_social__unaccent__icontains = palabra)
            clientes_crm = clientes_crm.filter(condicion)
            contexto_filtro.append(f"razon_social={filtro_razon_social}")

        if filtro_medio:
            condicion = Q(medio__icontains = filtro_medio)
            clientes_crm = clientes_crm.filter(condicion)
            contexto_filtro.append(f"medio={filtro_medio}")

        if filtro_estado:
            condicion = Q(estado__icontains = filtro_estado)
            clientes_crm = clientes_crm.filter(condicion)
            contexto_filtro.append(f"estado={filtro_estado}")

        if filtro_pais:
            condicion = Q(pais = filtro_pais)
            clientes_crm = clientes_crm.filter(condicion)
            contexto_filtro.append(f"pais={filtro_pais}")        
        
        if filtro_fecha_registro:
            condicion = Q(fecha_registro = filtro_fecha_registro)
            clientes_crm = clientes_crm.filter(condicion)
            contexto_filtro.append(f"fecha_registro={filtro_fecha_registro}")

        context['contexto_filtro'] = "&".join(contexto_filtro)

        context['pagina_filtro'] = ""
        if self.request.GET.get('page'):
            if context['contexto_filtro']:
                context['pagina_filtro'] = f'&page={self.request.GET.get("page")}'
            else:
                context['pagina_filtro'] = f'page={self.request.GET.get("page")}'
        context['contexto_filtro'] = '?' + context['contexto_filtro']

        objectsxpage =  15 # Show 10 objects per page.

        if len(clientes_crm) > objectsxpage:
            paginator = Paginator(clientes_crm, objectsxpage)
            page_number = self.request.GET.get('page')
            clientes_crm = paginator.get_page(page_number)
   
        context['contexto_pagina'] = clientes_crm
        return context

def ClienteCRMTabla(request):
    data = dict()
    if request.method == 'GET':
        template = 'crm/clientes_crm/inicio_tabla.html'
        context = {}
        clientes_crm = ClienteCRM.objects.all()

        filtro_razon_social = request.GET.get('razon_social')
        filtro_medio = request.GET.get('medio')
        filtro_estado = request.GET.get('estado')
        filtro_pais = request.GET.get('pais')
        filtro_fecha_registro = request.GET.get('fecha_registro')

        contexto_filtro = []

        if filtro_razon_social:
            condicion = Q(cliente_crm__razon_social__unaccent__icontains = filtro_razon_social.split(" ")[0])
            for palabra in filtro_razon_social.split(" ")[1:]:
                condicion &= Q(cliente_crm__razon_social__unaccent__icontains = palabra)
            clientes_crm = clientes_crm.filter(condicion)
            contexto_filtro.append(f"razon_social={filtro_razon_social}")

        if filtro_medio:
            condicion = Q(medio__icontains = filtro_medio)
            clientes_crm = clientes_crm.filter(condicion)
            contexto_filtro.append(f"medio={filtro_medio}")

        if filtro_estado:
            condicion = Q(estado__icontains = filtro_estado)
            clientes_crm = clientes_crm.filter(condicion)
            contexto_filtro.append(f"estado={filtro_estado}")

        if filtro_pais:
            condicion = Q(pais = filtro_pais)
            clientes_crm = clientes_crm.filter(condicion)
            contexto_filtro.append(f"pais={filtro_pais}")

        if filtro_fecha_registro:
            condicion = Q(fecha_registro = filtro_fecha_registro)
            clientes_crm = clientes_crm.filter(condicion)
            contexto_filtro.append(f"fecha_registro={filtro_fecha_registro}")

        context['contexto_filtro'] = "&".join(contexto_filtro)

        context['pagina_filtro'] = ""
        if request.GET.get('page'):
            if context['contexto_filtro']:
                context['pagina_filtro'] = f'&page={request.GET.get("page")}'
            else:
                context['pagina_filtro'] = f'page={request.GET.get("page")}'
        context['contexto_filtro'] = '?' + context['contexto_filtro']

        objectsxpage =  15 # Show 10 objects per page.

        if len(clientes_crm) > objectsxpage:
            paginator = Paginator(clientes_crm, objectsxpage)
            page_number = request.GET.get('page')
            clientes_crm = paginator.get_page(page_number)
   
        context['contexto_pagina'] = clientes_crm

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)

class ClienteCRMCreateView(PermissionRequiredMixin, BSModalCreateView):
    permission_required = ('crm.add_clientes_crm')
    model = ClienteCRM
    template_name = "crm/clientes_crm/form_cliente.html"
    form_class = ClienteCRMForm
    success_url = reverse_lazy('crm_app:cliente_crm_inicio')
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ClienteCRMCreateView, self).get_context_data(**kwargs)
        context['accion']="Registrar"
        context['titulo']="Cliente CRM"
        return context


class ClienteCRMUpdateView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('crm.change_clientes_crm')
    model = ClienteCRM
    template_name = "crm/clientes_crm/form_cliente.html"
    form_class = ClienteCRMForm
    success_url = reverse_lazy('crm_app:cliente_crm_inicio')

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ClienteCRMUpdateView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        context['titulo'] = "Cliente CRM"
        return context


class ClienteCRMDetailView(PermissionRequiredMixin, DetailView):
    permission_required = ('crm.view_clientecrm')
    model = ClienteCRM
    template_name = "crm/clientes_crm/detalle.html"
    context_object_name = 'contexto_cliente_crm'

    def get_context_data(self, **kwargs):
        cliente_crm = ClienteCRM.objects.get(id = self.kwargs['pk'])
        context = super(ClienteCRMDetailView, self).get_context_data(**kwargs)
        context['cliente_crm_detalle'] = ClienteCRMDetalle.objects.filter(cliente_crm = cliente_crm)
        return context

def ClienteCRMDetailTabla(request, pk):
    data = dict()
    if request.method == 'GET':
        template = 'crm/clientes_crm/detalle_tabla.html'
        context = {}
        cliente_crm = ClienteCRM.objects.get(id = pk)
        context['contexto_cliente_crm'] = cliente_crm
        context['cliente_crm_detalle'] = ClienteCRMDetalle.objects.filter(cliente_crm = cliente_crm)
        
        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)

class ClienteCRMDetalleCreateView(PermissionRequiredMixin, BSModalCreateView):
    permission_required = ('crm.add_representantelegal')
    model = ClienteCRMDetalle
    template_name = "crm/clientes_crm/form_detalle.html"
    form_class = ClienteCRMDetalleForm
    
    def get_success_url(self, **kwargs):
        return reverse_lazy('crm_app:cliente_crm_detalle', kwargs={'pk':self.kwargs['cliente_crm_id']})
    
    # def get_form_kwargs(self):
    #     kwargs = super().get_form_kwargs()
    #     detalle = kwargs['instance']
    #     print('************************')
    #     print(detalle)
    #     print('************************')
    #     lista = []
    #     relaciones = ClienteInterlocutor.objects.filter(cliente = detalle.cliente_crm.cliente_crm)
    #     for relacion in relaciones:
    #         lista.append(relacion.interlocutor.id)

    #     kwargs['cliente'] = detalle.cliente_crm
    #     kwargs['interlocutor_queryset'] = InterlocutorCliente.objects.filter(id__in = lista)
    #     kwargs['interlocutor'] = detalle.interlocutor
    #     return kwargs

    def form_valid(self, form):
        form.instance.cliente_crm = ClienteCRM.objects.get(id = self.kwargs['cliente_crm_id'])
        registro_guardar(form.instance, self.request)

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ClienteCRMDetalleCreateView, self).get_context_data(**kwargs)
        context['accion']="Registrar"
        context['titulo']="Detalle Cliente CRM"
        return context