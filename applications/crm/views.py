from django.core.paginator import Paginator
from django.shortcuts import render
from applications.importaciones import *
from applications.crm.forms import ClienteCRMBuscarForm, ClienteCRMDetalleForm, ClienteCRMForm, ProveedorCRMForm, EventoCRMForm, EventoCRMBuscarForm, EventoCRMDetalleDescripcionForm
from applications.crm.models import ClienteCRM, ClienteCRMDetalle, ProveedorCRM, EventoCRM

class ClienteCRMListView(PermissionRequiredMixin, FormView):
    permission_required = ('crm.view_clientecrm')
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
            condicion = Q(cliente_crm__pais = filtro_pais)
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
            condicion = Q(cliente_crm__pais = filtro_pais)
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
    permission_required = ('crm.add_clientecrm')
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
    permission_required = ('crm.change_clientecrm')
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
    permission_required = ('crm.view_clientecrmdetalle')
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
    permission_required = ('crm.add_clientecrmdetalle')
    model = ClienteCRMDetalle
    template_name = "includes/formulario generico.html"
    form_class = ClienteCRMDetalleForm
    
    def get_success_url(self, **kwargs):
        return reverse_lazy('crm_app:cliente_crm_detalle', kwargs={'pk':self.kwargs['cliente_crm_id']})

    def form_valid(self, form):
        form.instance.cliente_crm = ClienteCRM.objects.get(id = self.kwargs['cliente_crm_id'])
        registro_guardar(form.instance, self.request)

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ClienteCRMDetalleCreateView, self).get_context_data(**kwargs)
        context['accion']="Registrar"
        context['titulo']="Información Adicional"
        return context
    

class ClienteCRMDetalleUpdateView(PermissionRequiredMixin,BSModalUpdateView):
    permission_required = ('crm.change_clientecrmdetalle')
    model = ClienteCRMDetalle
    template_name = "includes/formulario generico.html"
    form_class = ClienteCRMDetalleForm

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('crm_app:cliente_crm_detalle', kwargs={'pk':self.object.cliente_crm.id})

    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ClienteCRMDetalleUpdateView, self).get_context_data(**kwargs)
        context['accion']="Actualizar"
        context['titulo']="Información Adicional"
        return context
    

class ClienteCRMDetalleDeleteView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('crm.delete_clientecrmdetalle')
    model = ClienteCRMDetalle
    template_name = "includes/eliminar generico.html"
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('crm_app:cliente_crm_detalle', kwargs={'pk':self.object.cliente_crm.id})

    def get_context_data(self, **kwargs):
        context = super(ClienteCRMDetalleDeleteView, self).get_context_data(**kwargs)
        context['accion'] = "Eliminar"
        context['titulo'] = "Información Adicional"
        context['item'] = self.get_object().comentario
        context['dar_baja'] = "true"
        return context
    

class ProveedorCRMListView(PermissionRequiredMixin, ListView):
    permission_required = ('crm.view_proveedorcrm')
    model = ProveedorCRM
    template_name = "crm/proveedor_crm/inicio.html"
    context_object_name = 'contexto_proveedor_crm'

def ProveedorCRMTabla(request):
    data = dict()
    if request.method == 'GET':
        template = 'crm/proveedor_crm/inicio_tabla.html'
        context = {}
        context['contexto_proveedor_crm'] = ProveedorCRM.objects.all()

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)
    

class ProveedorCRMCreateView(PermissionRequiredMixin, BSModalCreateView):
    permission_required = ('crm.add_proveedorcrm')
    model = ProveedorCRM
    template_name = "crm/proveedor_crm/form.html"
    form_class = ProveedorCRMForm
    success_url = reverse_lazy('crm_app:proveedor_crm_inicio')

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ProveedorCRMCreateView, self).get_context_data(**kwargs)
        context['accion']="Registrar"
        context['titulo']="Proveedor CRM"
        return context

    def form_valid(self, form):

        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)

        return super().form_valid(form)


class EventoCRMListView(FormView):
    template_name = "crm/eventos_crm/inicio.html"
    form_class = EventoCRMBuscarForm
    success_url = '.'

    def get_form_kwargs(self):
        kwargs = super(EventoCRMListView, self).get_form_kwargs()
        kwargs['filtro_pais'] = self.request.GET.get('pais')
        kwargs['filtro_estado'] = self.request.GET.get('estado')
        kwargs['filtro_fecha_inicio'] = self.request.GET.get('fecha_inicio')

        return kwargs

    def get_context_data(self, **kwargs):
        context = super(EventoCRMListView,self).get_context_data(**kwargs)
        eventos_crm = EventoCRM.objects.all()
        
        filtro_pais = self.request.GET.get('pais')
        filtro_estado = self.request.GET.get('estado')
        filtro_fecha_inicio = self.request.GET.get('fecha_inicio')
        
        contexto_filtro = []

        if filtro_pais:
            condicion = Q(pais = filtro_pais)
            eventos_crm = eventos_crm.filter(condicion)
            contexto_filtro.append(f"pais={filtro_pais}")        
        
        if filtro_estado:
            condicion = Q(estado__icontains = filtro_estado)
            eventos_crm = eventos_crm.filter(condicion)
            contexto_filtro.append(f"estado={filtro_estado}")

        if filtro_fecha_inicio:
            condicion = Q(fecha_inicio = filtro_fecha_inicio)
            eventos_crm = eventos_crm.filter(condicion)
            contexto_filtro.append(f"fecha_inicio={filtro_fecha_inicio}")

        context['contexto_filtro'] = "&".join(contexto_filtro)

        context['pagina_filtro'] = ""
        if self.request.GET.get('page'):
            if context['contexto_filtro']:
                context['pagina_filtro'] = f'&page={self.request.GET.get("page")}'
            else:
                context['pagina_filtro'] = f'page={self.request.GET.get("page")}'
        context['contexto_filtro'] = '?' + context['contexto_filtro']

        objectsxpage =  15 # Show 15 objects per page.

        if len(eventos_crm) > objectsxpage:
            paginator = Paginator(eventos_crm, objectsxpage)
            page_number = self.request.GET.get('page')
            eventos_crm = paginator.get_page(page_number)
   
        context['contexto_pagina'] = eventos_crm
        context['contexto_evento_crm'] = eventos_crm
        return context

def EventoCRMTabla(request):
    data = dict()
    if request.method == 'GET':
        template = 'crm/eventos_crm/inicio_tabla.html'
        context = {}
        eventos_crm = EventoCRM.objects.all()

        filtro_pais = request.GET.get('pais')
        filtro_estado = request.GET.get('estado')
        filtro_fecha_inicio = request.GET.get('fecha_inicio')

        contexto_filtro = []

        if filtro_pais:
            condicion = Q(pais = filtro_pais)
            eventos_crm = eventos_crm.filter(condicion)
            contexto_filtro.append(f"pais={filtro_pais}")

        if filtro_estado:
            condicion = Q(estado__icontains = filtro_estado)
            eventos_crm = eventos_crm.filter(condicion)
            contexto_filtro.append(f"estado={filtro_estado}")

        if filtro_fecha_inicio:
            condicion = Q(fecha_inicio = filtro_fecha_inicio)
            eventos_crm = eventos_crm.filter(condicion)
            contexto_filtro.append(f"fecha_inicio={filtro_fecha_inicio}")

        context['contexto_filtro'] = "&".join(contexto_filtro)

        context['pagina_filtro'] = ""
        if request.GET.get('page'):
            if context['contexto_filtro']:
                context['pagina_filtro'] = f'&page={request.GET.get("page")}'
            else:
                context['pagina_filtro'] = f'page={request.GET.get("page")}'
        context['contexto_filtro'] = '?' + context['contexto_filtro']

        objectsxpage =  15 # Show 15 objects per page.

        if len(eventos_crm) > objectsxpage:
            paginator = Paginator(eventos_crm, objectsxpage)
            page_number = request.GET.get('page')
            eventos_crm = paginator.get_page(page_number)
   
        context['contexto_pagina'] = eventos_crm
        context['contexto_evento_crm'] = eventos_crm

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)


class EventoCRMCreateView(BSModalCreateView):
    model = EventoCRM
    template_name = "includes/formulario generico.html"
    form_class = EventoCRMForm
    success_url = reverse_lazy('crm_app:evento_crm_inicio')

    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(EventoCRMCreateView, self).get_context_data(**kwargs)
        context['accion']="Registrar"
        context['titulo']="Evento CRM"
        return context

class EventoCRMUpdateView(BSModalUpdateView):
    model = EventoCRM
    template_name = "includes/formulario generico.html"
    form_class = EventoCRMForm
    success_url = reverse_lazy('crm_app:evento_crm_inicio')

    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(EventoCRMUpdateView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        context['titulo'] = "Evento CRM"
        return context



class EventoCRMDetailView(DetailView):
    model = EventoCRM
    template_name = "crm/eventos_crm/detalle.html"
    context_object_name = 'contexto_evento_crm'

    def get_context_data(self, **kwargs):
        evento_crm = EventoCRM.objects.get(id = self.kwargs['pk'])
        context = super(EventoCRMDetailView, self).get_context_data(**kwargs)
        context['contexto_evento_crm'] = evento_crm
        
        return context

def EventoCRMDetailTabla(request, pk):
    data = dict()
    if request.method == 'GET':
        template = 'crm/eventos_crm/detalle_tabla.html'
        context = {}
        evento_crm = EventoCRM.objects.get(id = pk)

        context['contexto_evento_crm'] = evento_crm

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)

class  EventoCRMDetalleDescripcionView(BSModalUpdateView):
    model = EventoCRM
    template_name = "includes/formulario generico.html"
    form_class = EventoCRMDetalleDescripcionForm

    def get_success_url(self, **kwargs):
        return reverse_lazy('crm_app:evento_crm_detalle', kwargs={'pk':self.object.id})

    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(EventoCRMDetalleDescripcionView, self).get_context_data(**kwargs)
        context['accion'] = "Descripción"
        return context
