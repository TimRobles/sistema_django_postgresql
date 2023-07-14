from django.core.paginator import Paginator
from django.shortcuts import render
from applications.importaciones import *
from applications.funciones import slug_aleatorio
from django.urls import reverse
from applications.crm.forms import (ClienteCRMBuscarForm,ClienteCRMDetalleForm, ClienteCRMForm, 
                                    EventoCRMForm, EventoCRMBuscarForm,EventoCRMDetalleDescripcionForm,
                                    PreguntaCRMBuscarForm, PreguntaCRMForm,
                                    AlternativaCRMForm,
                                    EncuestaCRMBuscarForm, EncuestaCRMForm, EncuestaPreguntaCRMForm,
                                    RespuestaCRMBuscarForm, RespuestaCRMForm)

from applications.crm.models import (ClienteCRM, ClienteCRMDetalle,
                                    EventoCRM,
                                    PreguntaCRM,
                                    AlternativaCRM,
                                    EncuestaCRM,
                                    RespuestaCRM,
                                    RespuestaDetalleCRM,
                                    )

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

        objectsxpage =  15 # Show 15 objects per page.

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

        objectsxpage =  15 # Show 15 objects per page.

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



























































































































































































































































































































































































































































































































































































class PreguntaCRMListView(FormView):
    template_name = "crm/encuestas_crm/pregunta/inicio.html"
    form_class = PreguntaCRMBuscarForm
    success_url = '.'

    def get_form_kwargs(self):
        kwargs = super(PreguntaCRMListView, self).get_form_kwargs()
        kwargs['filtro_tipo_pregunta'] = self.request.GET.get('tipo_pregunta')

        return kwargs

    def get_context_data(self, **kwargs):
        context = super(PreguntaCRMListView,self).get_context_data(**kwargs)
        pregunta_crm = PreguntaCRM.objects.all()
        
        filtro_tipo_pregunta = self.request.GET.get('tipo_pregunta')
        
        contexto_filtro = []

        if filtro_tipo_pregunta:
            condicion = Q(tipo_pregunta = filtro_tipo_pregunta)
            pregunta_crm = pregunta_crm.filter(condicion)
            contexto_filtro.append(f"tipo_pregunta={filtro_tipo_pregunta}")

        context['contexto_filtro'] = "&".join(contexto_filtro)

        context['pagina_filtro'] = ""
        if self.request.GET.get('page'):
            if context['contexto_filtro']:
                context['pagina_filtro'] = f'&page={self.request.GET.get("page")}'
            else:
                context['pagina_filtro'] = f'page={self.request.GET.get("page")}'
        context['contexto_filtro'] = '?' + context['contexto_filtro']

        objectsxpage =  15 # Show 15 objects per page.

        if len(pregunta_crm) > objectsxpage:
            paginator = Paginator(pregunta_crm, objectsxpage)
            page_number = self.request.GET.get('page')
            pregunta_crm = paginator.get_page(page_number)
   
        context['contexto_pagina'] = pregunta_crm
        context['contexto_pregunta_crm'] = pregunta_crm

        return context

def PreguntaCRMTabla(request):
    data = dict()
    if request.method == 'GET':
        template = 'crm/encuestas_crm/pregunta/inicio_tabla.html'
        context = {}
        pregunta_crm = PreguntaCRM.objects.all()

        filtro_tipo_pregunta = request.GET.get('tipo_pregunta')

        contexto_filtro = []

        if filtro_tipo_pregunta:
            condicion = Q(tipo_pregunta = filtro_tipo_pregunta)
            pregunta_crm = pregunta_crm.filter(condicion)
            contexto_filtro.append(f"tipo_pregunta={filtro_tipo_pregunta}")

        context['contexto_filtro'] = "&".join(contexto_filtro)

        context['pagina_filtro'] = ""
        if request.GET.get('page'):
            if context['contexto_filtro']:
                context['pagina_filtro'] = f'&page={request.GET.get("page")}'
            else:
                context['pagina_filtro'] = f'page={request.GET.get("page")}'
        context['contexto_filtro'] = '?' + context['contexto_filtro']

        objectsxpage =  15 # Show 15 objects per page.

        if len(pregunta_crm) > objectsxpage:
            paginator = Paginator(pregunta_crm, objectsxpage)
            page_number = request.GET.get('page')
            pregunta_crm = paginator.get_page(page_number)
   
        context['contexto_pagina'] = pregunta_crm

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)

class PreguntaCRMCreateView(BSModalCreateView):
# class PreguntaCRMCreateView(PermissionRequiredMixin, BSModalCreateView):
    # permission_required = ('crm.add_preguntacrm')
    model = PreguntaCRM
    template_name = "includes/formulario generico.html"
    form_class = PreguntaCRMForm
    success_url = reverse_lazy('crm_app:pregunta_crm_inicio')

    # def dispatch(self, request, *args, **kwargs):
    #     if not self.has_permission():
    #         return render(request, 'includes/modal sin permiso.html')
    #     return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(PreguntaCRMCreateView, self).get_context_data(**kwargs)
        context['accion']="Registrar"
        context['titulo']="Pregunta CRM"
        return context

class PreguntaCRMUpdateView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('crm.change_preguntacrm')
    model = PreguntaCRM
    template_name = "includes/formulario generico.html"
    form_class = PreguntaCRMForm
    success_url = reverse_lazy('crm_app:pregunta_crm_inicio')

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(PreguntaCRMUpdateView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        context['titulo'] = "Pregunta CRM"
        return context

class PreguntaCRMDeleteView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('crm.delete_preguntacrm')
    model = PreguntaCRM
    template_name = "includes/eliminar generico.html"
    success_url = reverse_lazy('crm_app:pregunta_crm_inicio')

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PreguntaCRMDeleteView, self).get_context_data(**kwargs)
        context['accion'] = "Eliminar"
        context['titulo'] = "Pregunta"
        context['item'] = self.object.texto
        return context

class PreguntaCRMDetailView(PermissionRequiredMixin, DetailView):
    permission_required = ('crm.view_preguntacrm')
    model = PreguntaCRM
    template_name = "crm/encuestas_crm/pregunta/detalle.html"
    context_object_name = 'contexto_pregunta_crm'

    def get_context_data(self, **kwargs):
        pregunta_crm = PreguntaCRM.objects.get(id = self.kwargs['pk'])
        context = super(PreguntaCRMDetailView, self).get_context_data(**kwargs)
        context['contexto_pregunta_crm'] = pregunta_crm
        context['alternativas'] = AlternativaCRM.objects.filter(pregunta_crm = pregunta_crm)

        
        return context

def PreguntaCRMDetailTabla(request, pk):
    data = dict()
    if request.method == 'GET':
        template = 'crm/encuestas_crm/pregunta/detalle_tabla.html'
        context = {}
        pregunta_crm = PreguntaCRM.objects.get(id = pk)

        context['contexto_pregunta_crm'] = pregunta_crm
        context['alternativas'] = AlternativaCRM.objects.filter(pregunta_crm = pregunta_crm)


        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)


class AlternativaCRMCreateView(PermissionRequiredMixin, BSModalCreateView):
    permission_required = ('crm.add_preguntacrm')
    model = AlternativaCRM
    template_name = "includes/formulario generico.html"
    form_class = AlternativaCRMForm
    success_url = reverse_lazy('crm_app:pregunta_crm_inicio')

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.pregunta_crm = PreguntaCRM.objects.get(id = self.kwargs['pregunta_id'])
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(AlternativaCRMCreateView, self).get_context_data(**kwargs)
        context['accion']="Registrar"
        context['titulo']="Alternativa CRM"
        return context

class AlternativaCRMUpdateView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('crm.change_preguntacrm')
    model = AlternativaCRM
    template_name = "includes/formulario generico.html"
    form_class = AlternativaCRMForm

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('crm_app:pregunta_crm_detalle', kwargs={'pk':self.object.pregunta_crm.id})

    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(AlternativaCRMUpdateView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        context['titulo'] = "Alternativa"
        return context

class AlternativaCRMDeleteView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('crm.delete_preguntacrm')
    model = AlternativaCRM
    template_name = "includes/eliminar generico.html"

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('crm_app:pregunta_crm_detalle', kwargs={'pk':self.object.pregunta_crm.id})

    def get_context_data(self, **kwargs):
        context = super(AlternativaCRMDeleteView, self).get_context_data(**kwargs)
        context['accion'] = "Eliminar"
        context['titulo'] = "Alternativa"
        context['item'] = self.object.texto
        return context


class EncuestaCRMListView(PermissionRequiredMixin, FormView):
    permission_required = ('crm.view_encuestacrm')
    template_name = "crm/encuestas_crm/encuesta/inicio.html"
    form_class = EncuestaCRMBuscarForm
    success_url = '.'

    def get_form_kwargs(self):
        kwargs = super(EncuestaCRMListView, self).get_form_kwargs()
        kwargs['filtro_tipo_encuesta'] = self.request.GET.get('tipo_encuesta')
        kwargs['filtro_pais'] = self.request.GET.get('pais')
        kwargs['filtro_titulo'] = self.request.GET.get('titulo')

        return kwargs

    def get_context_data(self, **kwargs):
        context = super(EncuestaCRMListView,self).get_context_data(**kwargs)
        encuesta_crm = EncuestaCRM.objects.all()

        filtro_tipo_encuesta = self.request.GET.get('tipo_encuesta')
        filtro_pais = self.request.GET.get('pais')
        filtro_titulo = self.request.GET.get('titulo')
        
        contexto_filtro = []

        if filtro_tipo_encuesta:
            condicion = Q(tipo_encuesta = filtro_tipo_encuesta)
            encuesta_crm = encuesta_crm.filter(condicion)
            contexto_filtro.append(f"tipo_encuesta={filtro_tipo_encuesta}")

        if filtro_pais:
            condicion = Q(pais = filtro_pais)
            encuesta_crm = encuesta_crm.filter(condicion)
            contexto_filtro.append(f"pais={filtro_pais}")

        if filtro_titulo:
            condicion = Q(titulo__unaccent__icontains = filtro_titulo.split(" ")[0])
            for palabra in filtro_titulo.split(" ")[1:]:
                condicion &= Q(titulo__unaccent__icontains = palabra)
            encuesta_crm = encuesta_crm.filter(condicion)
            contexto_filtro.append(f"titulo={filtro_titulo}")


        context['contexto_filtro'] = "&".join(contexto_filtro)

        context['pagina_filtro'] = ""
        if self.request.GET.get('page'):
            if context['contexto_filtro']:
                context['pagina_filtro'] = f'&page={self.request.GET.get("page")}'
            else:
                context['pagina_filtro'] = f'page={self.request.GET.get("page")}'
        context['contexto_filtro'] = '?' + context['contexto_filtro']

        objectsxpage =  15 # Show 15 objects per page.

        if len(encuesta_crm) > objectsxpage:
            paginator = Paginator(encuesta_crm, objectsxpage)
            page_number = self.request.GET.get('page')
            encuesta_crm = paginator.get_page(page_number)
   
        context['contexto_pagina'] = encuesta_crm
        context['contexto_encuesta_crm'] = encuesta_crm
        return context

def EncuestaCRMTabla(request):
    data = dict()
    if request.method == 'GET':
        template = 'crm/encuestas_crm/encuesta/inicio_tabla.html'
        context = {}
        encuesta_crm = EncuestaCRM.objects.all()

        filtro_tipo_encuesta = request.GET.get('tipo_encuesta')
        filtro_pais = request.GET.get('pais')
        filtro_titulo = request.GET.get('titulo')

        contexto_filtro = []

        if filtro_tipo_encuesta:
            condicion = Q(tipo_encuesta = filtro_tipo_encuesta)
            encuesta_crm = encuesta_crm.filter(condicion)
            contexto_filtro.append(f"tipo_encuesta={filtro_tipo_encuesta}")

        if filtro_pais:
            condicion = Q(pais = filtro_pais)
            encuesta_crm = encuesta_crm.filter(condicion)
            contexto_filtro.append(f"pais={filtro_pais}")

        if filtro_titulo:
            condicion = Q(titulo__unaccent__icontains = filtro_titulo.split(" ")[0])
            for palabra in filtro_titulo.split(" ")[1:]:
                condicion &= Q(titulo__unaccent__icontains = palabra)
            encuesta_crm = encuesta_crm.filter(condicion)
            contexto_filtro.append(f"titulo={filtro_titulo}")

        context['contexto_filtro'] = "&".join(contexto_filtro)

        context['pagina_filtro'] = ""
        if request.GET.get('page'):
            if context['contexto_filtro']:
                context['pagina_filtro'] = f'&page={request.GET.get("page")}'
            else:
                context['pagina_filtro'] = f'page={request.GET.get("page")}'
        context['contexto_filtro'] = '?' + context['contexto_filtro']

        objectsxpage =  15 # Show 15 objects per page.

        if len(encuesta_crm) > objectsxpage:
            paginator = Paginator(encuesta_crm, objectsxpage)
            page_number = request.GET.get('page')
            encuesta_crm = paginator.get_page(page_number)
   
        context['contexto_pagina'] = encuesta_crm
        context['contexto_encuesta_crm'] = encuesta_crm

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)

class EncuestaCRMCreateView(PermissionRequiredMixin, BSModalCreateView):
    permission_required = ('crm.add_preguntacrm')
    model = EncuestaCRM
    template_name = "includes/formulario generico.html"
    form_class = EncuestaCRMForm
    success_url = reverse_lazy('crm_app:encuesta_crm_inicio')

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.slug = slug_aleatorio(EncuestaCRM)
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(EncuestaCRMCreateView, self).get_context_data(**kwargs)
        context['accion']="Registrar"
        context['titulo']="Encuesta CRM"
        return context

class EncuestaCRMUpdateView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('crm.change_preguntacrm')
    model = EncuestaCRM
    template_name = "includes/formulario generico.html"
    form_class = EncuestaCRMForm
    success_url = reverse_lazy('crm_app:encuesta_crm_inicio')

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(EncuestaCRMUpdateView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        context['titulo'] = "Encuesta CRM"
        return context

class EncuestaCRMDetailView(PermissionRequiredMixin, DetailView):
    permission_required = ('crm.add_preguntacrm')
    model = EncuestaCRM
    template_name = "crm/encuestas_crm/encuesta/detalle.html"
    context_object_name = 'contexto_encuesta_crm'

    def get_context_data(self, **kwargs):
        encuesta = EncuestaCRM.objects.get(slug = self.kwargs['slug'])
        preguntas = PreguntaCRM.objects.all()
        alternativas = AlternativaCRM.objects.all()
        content_type = ContentType.objects.get_for_model(encuesta)

        context = super(EncuestaCRMDetailView, self).get_context_data(**kwargs)
        context['contexto_encuesta_crm'] = encuesta
        context['alternativas'] = alternativas
       
        return context

class EncuestaCRMDeleteView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('crm.delete_encuestacrm')
    model = EncuestaCRM
    template_name = "includes/eliminar generico.html"
    success_url = reverse_lazy('crm_app:encuesta_crm_inicio')

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(EncuestaCRMDeleteView, self).get_context_data(**kwargs)
        context['accion'] = "Eliminar"
        context['titulo'] = "Encuesta"
        context['item'] = self.object.titulo
        return context

def EncuestaCRMDetailTabla(request, slug):
    data = dict()
    if request.method == 'GET':
        template = 'crm/encuestas_crm/encuesta/detalle_tabla.html'
        context = {}
        encuesta = EncuestaCRM.objects.get(slug=slug)
        preguntas = PreguntaCRM.objects.all()
        alternativas = AlternativaCRM.objects.all()

        content_type = ContentType.objects.get_for_model(encuesta)

        context['contexto_encuesta_crm'] = encuesta
        context['alternativas'] = alternativas

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)

class EncuestaPreguntaCRMUpdateView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('crm.change_encuestacrm')
    model = EncuestaCRM
    template_name = "crm/encuestas_crm/encuesta/form añadir pregunta.html"
    form_class = EncuestaPreguntaCRMForm

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('crm_app:encuesta_crm_detalle', kwargs={'slug':self.get_object().slug})

    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(EncuestaPreguntaCRMUpdateView, self).get_context_data(**kwargs)
        context['accion'] = "Añadir"
        context['titulo'] = "pregunta"
        return context
    

class RespuestaCRMListView(FormView):
    template_name = "crm/encuestas_crm/respuesta/inicio.html"
    form_class = RespuestaCRMBuscarForm
    success_url = '.'

    def get_form_kwargs(self):
        kwargs = super(RespuestaCRMListView, self).get_form_kwargs()
        kwargs['filtro_cliente'] = self.request.GET.get('cliente')
        kwargs['filtro_encuesta'] = self.request.GET.get('encuesta')

        return kwargs

    def get_context_data(self, **kwargs):
        context = super(RespuestaCRMListView,self).get_context_data(**kwargs)
        respuesta_crm = RespuestaCRM.objects.all()

        filtro_cliente = self.request.GET.get('cliente')
        filtro_encuesta = self.request.GET.get('encuesta')
        
        contexto_filtro = []

        if filtro_cliente:
            condicion = Q(cliente = filtro_cliente)
            respuesta_crm = respuesta_crm.filter(condicion)
            contexto_filtro.append("cliente=" + filtro_cliente)

        if filtro_encuesta:
            condicion = Q(cliente = filtro_cliente)
            respuesta_crm = respuesta_crm.filter(condicion)
            contexto_filtro.append("encuesta=" + filtro_encuesta)

        context['contexto_filtro'] = "&".join(contexto_filtro)

        context['pagina_filtro'] = ""
        if self.request.GET.get('page'):
            if context['contexto_filtro']:
                context['pagina_filtro'] = f'&page={self.request.GET.get("page")}'
            else:
                context['pagina_filtro'] = f'page={self.request.GET.get("page")}'
        context['contexto_filtro'] = '?' + context['contexto_filtro']

        objectsxpage =  15 # Show 15 objects per page.

        if len(respuesta_crm) > objectsxpage:
            paginator = Paginator(respuesta_crm, objectsxpage)
            page_number = self.request.GET.get('page')
            respuesta_crm = paginator.get_page(page_number)
   
        context['contexto_pagina'] = respuesta_crm
        context['contexto_respuesta_crm'] = respuesta_crm
        return context

def RespuestaCRMTabla(request):
    data = dict()
    if request.method == 'GET':
        template = 'crm/encuestas_crm/respuesta/inicio_tabla.html'
        context = {}
        respuesta_crm = RespuestaCRM.objects.all()

        filtro_cliente = request.GET.get('cliente')
        filtro_encuesta = request.GET.get('encuesta')

        contexto_filtro = []

        if filtro_cliente:
            condicion = Q(cliente = filtro_cliente)
            respuesta_crm = respuesta_crm.filter(condicion)
            contexto_filtro.append("cliente=" + filtro_cliente)

        if filtro_encuesta:
            condicion = Q(cliente = filtro_cliente)
            respuesta_crm = respuesta_crm.filter(condicion)
            contexto_filtro.append("encuesta=" + filtro_encuesta)

        context['contexto_filtro'] = "&".join(contexto_filtro)

        context['pagina_filtro'] = ""
        if request.GET.get('page'):
            if context['contexto_filtro']:
                context['pagina_filtro'] = f'&page={request.GET.get("page")}'
            else:
                context['pagina_filtro'] = f'page={request.GET.get("page")}'
        context['contexto_filtro'] = '?' + context['contexto_filtro']

        objectsxpage =  15 # Show 15 objects per page.

        if len(respuesta_crm) > objectsxpage:
            paginator = Paginator(respuesta_crm, objectsxpage)
            page_number = request.GET.get('page')
            respuesta_crm = paginator.get_page(page_number)
   
        context['contexto_pagina'] = respuesta_crm
        context['contexto_respuesta_crm'] = respuesta_crm

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)

class RespuestaCRMCreateView(PermissionRequiredMixin, BSModalCreateView):
    permission_required = ('crm.add_respuestacrm')
    model = RespuestaCRM
    template_name = "includes/formulario generico.html"
    form_class = RespuestaCRMForm
    success_url = reverse_lazy('crm_app:respuesta_crm_inicio')

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        form.instance.slug = slug_aleatorio(RespuestaCRM)
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(RespuestaCRMCreateView, self).get_context_data(**kwargs)
        context['accion']="Registrar"
        context['titulo']="Respuesta CRM"
        return context

class RespuestaCRMUpdateView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('crm.change_respuestacrm')
    model = RespuestaCRM
    template_name = "includes/formulario generico.html"
    form_class = RespuestaCRMForm
    success_url = reverse_lazy('crm_app:respuesta_crm_inicio')

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(RespuestaCRMUpdateView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        context['titulo'] = "Respuesta CRM"
        return context

class RespuestaCRMDeleteView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('crm.delete_respuestacrm')
    model = RespuestaCRM
    template_name = "includes/eliminar generico.html"
    success_url = reverse_lazy('crm_app:respuesta_crm_inicio')

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(RespuestaCRMDeleteView, self).get_context_data(**kwargs)
        context['accion'] = "Eliminar"
        context['titulo'] = "Respuesta"
        return context


class RespuestaCRMDetailView(PermissionRequiredMixin, DetailView):
    permission_required = ('crm.view_respuestadetallecrm')
    model = RespuestaCRM
    template_name = "crm/encuestas_crm/respuesta/detalle.html"
    context_object_name = 'contexto_encuesta_crm'

    def get_context_data(self, **kwargs):
        respuesta = RespuestaCRM.objects.get(slug = self.kwargs['slug'])
        respuesta_detalle = RespuestaDetalleCRM.objects.ver_respuestas(respuesta)

        context = super(RespuestaCRMDetailView, self).get_context_data(**kwargs)
        context['contexto_respuesta'] = respuesta       
        context['contexto_respuesta'] = respuesta       
        context['respuesta_detalle'] = respuesta_detalle       
        return context

def RespuestaCRMDetailTabla(request, slug):
    data = dict()
    if request.method == 'GET':
        template = 'crm/encuestas_crm/respuesta/detalle_tabla.html'
        context = {}
        respuesta = RespuestaCRM.objects.get(slug=slug)
        respuesta_detalle = RespuestaDetalleCRM.objects.ver_respuestas(respuesta)

        context['contexto_respuesta'] = respuesta
        context['respuesta_detalle'] = respuesta_detalle       

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)

class RespuestaVerView(TemplateView): #respuesta_del_cliente
    template_name = "crm/encuestas_crm/respuesta/respuesta_ver.html"

    def get_context_data(self, **kwargs):
        respuesta = RespuestaCRM.objects.get(slug = self.kwargs['slug'])
        encuesta = respuesta.encuesta_crm
        preguntas = encuesta.pregunta_crm.all()
        print(preguntas)

        context = super(RespuestaVerView, self).get_context_data(**kwargs)
        context['respuesta'] = respuesta
        context['encuesta'] = encuesta
        context['preguntas'] = preguntas

        return context

class EncuestaRespuesta(PermissionRequiredMixin, View): #encuesta
    permission_required = ('crm.view_encuestacrm')

    def post(self, request, *args, **kwargs):
        respuesta_id = int(request.POST.get('respuesta'))
        created_by = None
        updated_by = None
        respuesta_crm = RespuestaCRM.objects.get(id=respuesta_id)
        respuesta_crm.RespuestaDetalleCRM_respuesta_crm.update(borrador=False)
        for k,v in request.POST.items():
            respuesta = v.split(',')
            print(k, respuesta)
            if k != 'respuesta':
                if "texto" in k:
                    alternativa_crm = None
                    pregunta_crm = PreguntaCRM.objects.get(id=int(respuesta[0]))
                    texto = ",".join(respuesta[2:])
                    borrador = False
                    if respuesta[1] == "true":
                        borrador = True
                else:
                    alternativa_crm = AlternativaCRM.objects.get(id=int(respuesta[0]))
                    pregunta_crm = PreguntaCRM.objects.get(id=int(respuesta[1]))
                    texto = None
                    borrador = False
                    if respuesta[2] == "true":
                        borrador = True

                RespuestaDetalleCRM.objects.create(
                    alternativa_crm = alternativa_crm,
                    pregunta_crm = pregunta_crm,
                    respuesta_crm = respuesta_crm,
                    texto = texto,
                    borrador = borrador,
                    created_by = created_by,
                    updated_by = updated_by,
                )
        respuesta_crm.estado = 2
        respuesta_crm.save()
        return HttpResponse('Hola')
