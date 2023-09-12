from django.core.paginator import Paginator
from django import forms
from django.shortcuts import render
from applications.importaciones import *
from applications.clientes.models import HistorialEstadoCliente
from applications.funciones import numeroXn, registrar_excepcion
from applications.material.funciones import stock, ver_tipo_stock
from applications.movimiento_almacen.models import MovimientosAlmacen, TipoMovimiento
from applications.datos_globales.models import Pais, SeriesComprobante, Unidad
from applications.comprobante_despacho.models import Guia, GuiaDetalle
from applications.funciones import slug_aleatorio
from applications.home.templatetags.funciones_propias import nombre_usuario
from django.urls import reverse
from applications.crm.forms import (ClienteCRMBuscarForm,ClienteCRMDetalleForm, EventoCRMFinalizarForm, 
                                    EventoCRMForm, EventoCRMBuscarForm,EventoCRMDetalleDescripcionForm,
                                    EventoCRMActualizarForm, EventoCRMDetalleActualizarForm, EventoCRMDetalleForm,
                                    EventoCRMDetalleInformacionAdicionalForm, ProveedorCRMForm, 
                                    PreguntaCRMBuscarForm, PreguntaCRMForm,
                                    AlternativaCRMForm,
                                    EncuestaCRMBuscarForm, EncuestaCRMForm, EncuestaPreguntaCRMForm,
                                    RespuestaCRMBuscarForm, RespuestaCRMForm, RespuestaCrearCRMForm)

from applications.crm.models import (
    ClienteCRMDetalle,
    EventoCRM,
    EventoCRMDetalle,
    EventoCRMDetalleInformacionAdicional,
    ProveedorCRM,
    PreguntaCRM,
    AlternativaCRM,
    EncuestaCRM,
    RespuestaCRM,
    RespuestaDetalleCRM,
    )

from applications.clientes.models import Cliente, ClienteInterlocutor, InterlocutorCliente
from applications.clientes.forms import ClienteNacionalForm, ClienteExtranjeroForm
from applications.cotizacion.models import CotizacionVenta
from applications.comprobante_venta.models import FacturaVenta

class ClienteCRMListView(PermissionRequiredMixin, FormView):
    permission_required = ('crm.view_clientecrm')
    template_name = "crm/clientes_crm/inicio.html"
    form_class = ClienteCRMBuscarForm
    success_url = '.'

    def get_form_kwargs(self):
        kwargs = super(ClienteCRMListView, self).get_form_kwargs()
        kwargs['filtro_razon_social'] = self.request.GET.get('razon_social')
        kwargs['filtro_medio'] = self.request.GET.get('medio')
        kwargs['filtro_pais'] = self.request.GET.get('pais')
        kwargs['filtro_fecha_registro'] = self.request.GET.get('created_at')
        kwargs['filtro_estado'] = self.request.GET.get('estado')

        return kwargs

    def get_context_data(self, **kwargs):
        context = super(ClienteCRMListView,self).get_context_data(**kwargs)
        clientes_crm = Cliente.objects.all()
        
        filtro_razon_social = self.request.GET.get('razon_social')
        filtro_medio = self.request.GET.get('medio')
        filtro_pais = self.request.GET.get('pais')
        filtro_fecha_registro = self.request.GET.get('created_at')
        filtro_estado = self.request.GET.get('estado')
        
        contexto_filtro = []

        if filtro_razon_social:
            condicion = Q(razon_social__unaccent__icontains = filtro_razon_social.split(" ")[0])
            for palabra in filtro_razon_social.split(" ")[1:]:
                condicion &= Q(razon_social__unaccent__icontains = palabra)
            clientes_crm = clientes_crm.filter(condicion)
            contexto_filtro.append(f"razon_social={filtro_razon_social}")

        if filtro_medio:
            condicion = Q(medio__icontains = filtro_medio)
            clientes_crm = clientes_crm.filter(condicion)
            contexto_filtro.append(f"medio={filtro_medio}")

        if filtro_pais:
            condicion = Q(pais = filtro_pais)
            clientes_crm = clientes_crm.filter(condicion)
            contexto_filtro.append(f"pais={filtro_pais}")        
        
        if filtro_fecha_registro:
            condicion = Q(created_at = filtro_fecha_registro)
            clientes_crm = clientes_crm.filter(condicion)
            contexto_filtro.append(f"created_at={filtro_fecha_registro}")

        if filtro_estado:
            condicion = Q(estado_cliente__icontains = filtro_estado)
            clientes_crm = clientes_crm.filter(condicion)
            contexto_filtro.append(f"estado_cliente={filtro_estado}")

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
        clientes_crm = Cliente.objects.all()

        filtro_razon_social = request.GET.get('razon_social')
        filtro_medio = request.GET.get('medio')
        filtro_pais = request.GET.get('pais')
        filtro_fecha_registro = request.GET.get('created_at')
        filtro_estado = request.GET.get('estado')

        contexto_filtro = []

        if filtro_razon_social:
            condicion = Q(razon_social__unaccent__icontains = filtro_razon_social.split(" ")[0])
            for palabra in filtro_razon_social.split(" ")[1:]:
                condicion &= Q(razon_social__unaccent__icontains = palabra)
            clientes_crm = clientes_crm.filter(condicion)
            contexto_filtro.append(f"razon_social={filtro_razon_social}")

        if filtro_medio:
            condicion = Q(medio__icontains = filtro_medio)
            clientes_crm = clientes_crm.filter(condicion)
            contexto_filtro.append(f"medio={filtro_medio}")

        if filtro_pais:
            condicion = Q(pais = filtro_pais)
            clientes_crm = clientes_crm.filter(condicion)
            contexto_filtro.append(f"pais={filtro_pais}")

        if filtro_fecha_registro:
            condicion = Q(created_at = filtro_fecha_registro)
            clientes_crm = clientes_crm.filter(condicion)
            contexto_filtro.append(f"created_at={filtro_fecha_registro}")

        if filtro_estado:
            condicion = Q(estado_cliente__icontains = filtro_estado)
            clientes_crm = clientes_crm.filter(condicion)
            contexto_filtro.append(f"estado_cliente={filtro_estado}")

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


class ClienteCRMNacionalCreateView(PermissionRequiredMixin, BSModalCreateView):
    permission_required = ('crm.add_clientecrm')
    model = Cliente
    template_name = "crm/clientes_crm/form.html"
    form_class = ClienteNacionalForm
    success_url = reverse_lazy('crm_app:cliente_crm_inicio')
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.pais = Pais.objects.get(nombre='PERÚ')
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ClienteCRMNacionalCreateView, self).get_context_data(**kwargs)
        context['accion']="Registrar"
        context['titulo']="Cliente Nacional"
        return context


class ClienteCRMExtranjeroCreateView(PermissionRequiredMixin, BSModalCreateView):
    permission_required = ('crm.add_clientecrm')
    model = Cliente
    template_name = "crm/clientes_crm/form.html"
    form_class = ClienteExtranjeroForm
    success_url = reverse_lazy('crm_app:cliente_crm_inicio')
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ClienteCRMExtranjeroCreateView, self).get_context_data(**kwargs)
        context['accion']="Registrar"
        context['titulo']="Cliente Extranjero"
        return context


class ClienteCRMNacionalUpdateView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('crm.change_clientecrm')
    model = Cliente
    template_name = "crm/clientes_crm/form.html"
    form_class = ClienteNacionalForm
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
        context = super(ClienteCRMNacionalUpdateView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        context['titulo'] = "Cliente Nacional"
        return context


class ClienteCRMExtranjeroUpdateView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('crm.change_clientecrm')
    model = Cliente
    template_name = "crm/clientes_crm/form.html"
    form_class = ClienteExtranjeroForm
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
        context = super(ClienteCRMExtranjeroUpdateView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        context['titulo'] = "Cliente Extranjero"
        return context
    

class ClienteCRMDetailView(PermissionRequiredMixin, DetailView):
    permission_required = ('crm.view_clientecrmdetalle')
    model = Cliente
    template_name = "crm/clientes_crm/detalle.html"
    context_object_name = 'contexto_cliente_crm'

    def get_context_data(self, **kwargs):
        cliente_crm = Cliente.objects.get(id = self.kwargs['pk'])
        context = super(ClienteCRMDetailView, self).get_context_data(**kwargs)
        context['cliente_crm_detalle'] = ClienteCRMDetalle.objects.filter(cliente_crm = cliente_crm)

        return context


def ClienteCRMDetailTabla(request, pk):
    data = dict()
    if request.method == 'GET':
        template = 'crm/clientes_crm/detalle_tabla.html'
        context = {}
        cliente_crm = Cliente.objects.get(id = pk)
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

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        cliente_crm = Cliente.objects.get(id = self.kwargs['cliente_crm_id'])
        lista = []
        relaciones = ClienteInterlocutor.objects.filter(cliente = cliente_crm)
        for relacion in relaciones:
            lista.append(relacion.interlocutor.id)

        kwargs['interlocutor_queryset'] = InterlocutorCliente.objects.filter(id__in = lista)
        return kwargs

    def form_valid(self, form):
        form.instance.cliente_crm = Cliente.objects.get(id = self.kwargs['cliente_crm_id'])
        registro_guardar(form.instance, self.request)

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ClienteCRMDetalleCreateView, self).get_context_data(**kwargs)
        context['accion']="Registrar"
        context['titulo']="Información de Actividad"
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

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        cliente_crm = Cliente.objects.get(id = self.object.cliente_crm.id)
        lista = []
        relaciones = ClienteInterlocutor.objects.filter(cliente = cliente_crm)
        for relacion in relaciones:
            lista.append(relacion.interlocutor.id)

        kwargs['interlocutor_queryset'] = InterlocutorCliente.objects.filter(id__in = lista)

        return kwargs
    
    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ClienteCRMDetalleUpdateView, self).get_context_data(**kwargs)
        context['accion']="Actualizar"
        context['titulo']="Información de Actividad"
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
        context['titulo'] = "Información de Actividad"
        context['item'] = self.get_object().get_tipo_actividad_display() + ' ' + str(self.get_object().fecha.strftime('%d/%m/%Y'))
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
    

class ClienteCRMCotizacionesView(DetailView):
    model = Cliente
    template_name = "crm/clientes_crm/cotizaciones.html"
    context_object_name = 'contexto_cliente_crm'

    def get_context_data(self, **kwargs):
        cliente_crm = Cliente.objects.get(id = self.kwargs['pk'])
        context = super(ClienteCRMCotizacionesView, self).get_context_data(**kwargs)
        cotizaciones = CotizacionVenta.objects.filter(cliente = cliente_crm)
        # context['cotizaciones'] = CotizacionVenta.objects.filter(cliente = cliente_crm)

        objectsxpage =  15 # Show 15 objects per page.

        if len(cotizaciones) > objectsxpage:
            paginator = Paginator(cotizaciones, objectsxpage)
            page_number = self.request.GET.get('page')
            cotizaciones = paginator.get_page(page_number)
   
        context['contexto_cotizaciones'] = cotizaciones
        context['contexto_pagina'] = cotizaciones
        context['contexto_filtro'] = '?' 

        return context
    

class ClienteCRMFacturasView(DetailView):
    model = Cliente
    template_name = "crm/clientes_crm/facturas.html"
    context_object_name = 'contexto_cliente_crm'

    def get_context_data(self, **kwargs):
        cliente_crm = Cliente.objects.get(id = self.kwargs['pk'])
        context = super(ClienteCRMFacturasView, self).get_context_data(**kwargs)
        facturas = FacturaVenta.objects.filter(cliente = cliente_crm)
        # context['facturas'] = FacturaVenta.objects.filter(cliente = cliente_crm)

        objectsxpage =  15 # Show 15 objects per page.

        if len(facturas) > objectsxpage:
            paginator = Paginator(facturas, objectsxpage)
            page_number = self.request.GET.get('page')
            facturas = paginator.get_page(page_number)
   
        context['contexto_facturas'] = facturas
        context['contexto_pagina'] = facturas
        context['contexto_filtro'] = '?'  

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


class EventoCRMGuardarView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('crm.change_eventocrm')
    model = EventoCRM
    template_name = "includes/eliminar generico.html"
    
    def dispatch(self, request, *args, **kwargs):        
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')

    def get_success_url(self, **kwargs):
        return reverse_lazy('crm_app:evento_crm_detalle', kwargs={'pk':self.object.id})

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            self.object = self.get_object()
            movimiento_final = TipoMovimiento.objects.get(codigo=139)  # Salida por traslado
            for detalle in self.object.EventoCRMDetalle_evento_crm.all():
                movimiento_uno = MovimientosAlmacen.objects.create(
                    content_type_producto=detalle.content_type,
                    id_registro_producto=detalle.id_registro,
                    cantidad=detalle.cantidad_asignada,
                    tipo_movimiento=movimiento_final,
                    tipo_stock=detalle.tipo_stock,
                    signo_factor_multiplicador=-1,
                    content_type_documento_proceso=ContentType.objects.get_for_model(self.object),
                    id_registro_documento_proceso=self.object.id,
                    almacen=detalle.almacen_origen,
                    sociedad=self.object.sociedad,
                    movimiento_anterior=None,
                    movimiento_reversion=False,
                    created_by=self.request.user,
                    updated_by=self.request.user,
                )
                movimiento_dos = MovimientosAlmacen.objects.create(
                    content_type_producto=detalle.content_type,
                    id_registro_producto=detalle.id_registro,
                    cantidad=detalle.cantidad_asignada,
                    tipo_movimiento=movimiento_final,
                    tipo_stock=movimiento_final.tipo_stock_final,
                    signo_factor_multiplicador=+1,
                    content_type_documento_proceso=ContentType.objects.get_for_model(self.object),
                    id_registro_documento_proceso=self.object.id,
                    sociedad=self.object.sociedad,
                    movimiento_anterior=movimiento_uno,
                    movimiento_reversion=False,
                    created_by=self.request.user,
                    updated_by=self.request.user,
                )

            self.object.estado = 2

            registro_guardar(self.object, self.request)
            self.object.save()
            messages.success(request, MENSAJE_GUARDAR_EVENTO_DETALLE)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(EventoCRMGuardarView, self).get_context_data(**kwargs)
        context['accion'] = "Guardar"
        context['titulo'] = "Detalle Evento"
        context['dar_baja'] = True
        return context


class EventoCRMFinalizarView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('crm.change_eventocrm')
    model = EventoCRM
    template_name = "includes/formulario generico.html"
    form_class = EventoCRMFinalizarForm

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('crm_app:evento_crm_inicio')

    def form_valid(self, form):
        form.instance.estado = 3
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(EventoCRMFinalizarView, self).get_context_data(**kwargs)
        context['accion']="Finalizar"
        context['titulo']="Evento CRM"
        return context

class EventoCRMDetailView(DetailView):
    model = EventoCRM
    template_name = "crm/eventos_crm/detalle.html"
    context_object_name = 'contexto_evento_crm'

    def get_context_data(self, **kwargs):
        evento_crm = EventoCRM.objects.get(id = self.kwargs['pk'])

        merchandisings = None
        try:
            merchandisings = evento_crm.EventoCRMDetalle_evento_crm.all()

            for merchandising in merchandisings:
                merchandising.merchandising = merchandising.content_type.get_object_for_this_type(id = merchandising.id_registro)
        except:
            pass

        context = super(EventoCRMDetailView, self).get_context_data(**kwargs)
        context['evento_crm_detalle_informacion_adicional'] = EventoCRMDetalleInformacionAdicional.objects.filter(evento_crm = evento_crm)
        context['evento_crm_detalle'] = EventoCRMDetalle.objects.filter(evento_crm = evento_crm)
        context['merchandisings'] = merchandisings
        
        return context


def EventoCRMDetailTabla(request, pk):
    data = dict()
    if request.method == 'GET':
        template = 'crm/eventos_crm/detalle_tabla.html'
        evento_crm = EventoCRM.objects.get(id = pk)

        merchandisings = None
        try:
            merchandisings = evento_crm.EventoCRMDetalle_evento_crm.all()

            for merchandising in merchandisings:
                merchandising.merchandising = merchandising.content_type.get_object_for_this_type(id = merchandising.id_registro)
        except:
            pass

        context = {}
        context['contexto_evento_crm'] = evento_crm
        context['evento_crm_detalle_informacion_adicional'] = EventoCRMDetalleInformacionAdicional.objects.filter(evento_crm = evento_crm)
        context['evento_crm_detalle'] = EventoCRMDetalle.objects.filter(evento_crm = evento_crm)
        context['merchandisings'] = merchandisings

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
    

class  EventoCRMActualizarView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('crm.change_eventocrm')
    model = EventoCRM
    template_name = "crm/eventos_crm/form_actualizar.html"
    form_class = EventoCRMActualizarForm
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('crm_app:evento_crm_detalle', kwargs={'pk':self.object.id})

    def form_valid(self, form):
        evento_crm = EventoCRM.objects.get(id=form.instance.id)
        if form.instance.sede_origen != evento_crm.sede_origen or form.instance.sociedad != evento_crm.sociedad:
            for detalle in form.instance.EventoCRMDetalle_evento_crm.all():
                detalle.almacen_origen = None
                registro_guardar(detalle, self.request)
                detalle.save()
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(EventoCRMActualizarView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        context['titulo'] = "Evento CRM"
        context['url_sede'] = reverse_lazy('sociedad_app:sociedad_sede', kwargs={'id_sociedad':1})[:-2]
        return context


class EventoCRMEliminarDeleteView(BSModalDeleteView):
    model = EventoCRM
    template_name = "includes/eliminar generico.html"
    success_url = reverse_lazy('crm_app:evento_crm_inicio')

    def get_context_data(self, **kwargs):
        context = super(EventoCRMEliminarDeleteView, self).get_context_data(**kwargs)
        context['accion']="Eliminar"
        context['titulo']="Evento"
        context['item']= self.object.titulo
        return context

class EventoCRMDetalleMerchandisingCreateView(PermissionRequiredMixin, BSModalFormView):
    permission_required = ('crm.change_eventocrmdetalle')
    template_name = "crm/eventos_crm/form_merchandising.html"
    form_class = EventoCRMDetalleForm

    def dispatch(self, request, *args, **kwargs):
        context = {}
        error_sede = False
        context['titulo'] = 'Error de guardar'
        evento_crm = EventoCRM.objects.get(id = self.kwargs['evento_crm_id'])
        if not evento_crm.sede_origen:
            error_sede = True

        if error_sede:
            context['texto'] = 'Ingrese una sede de origen.'
            return render(request, 'includes/modal sin permiso.html', context)
        
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('crm_app:evento_crm_detalle', kwargs={'pk':self.kwargs['evento_crm_id']})

    @transaction.atomic
    def form_valid(self, form):
        sid = transaction.savepoint()
        evento_crm = EventoCRM.objects.get(id = self.kwargs['evento_crm_id'])
        almacen_origen = form.cleaned_data.get('almacen_origen')
        tipo_stock = form.cleaned_data.get('tipo_stock')
        merchandising = form.cleaned_data.get('merchandising')
        cantidad_asignada = form.cleaned_data.get('cantidad_asignada')
        stock_disponible = ver_tipo_stock(ContentType.objects.get_for_model(merchandising), merchandising.id, evento_crm.sociedad.id, almacen_origen.id, tipo_stock.id)

        buscar = EventoCRMDetalle.objects.filter(
            content_type=ContentType.objects.get_for_model(merchandising),
            id_registro=merchandising.id,
            almacen_origen=almacen_origen,
            tipo_stock=tipo_stock,
            evento_crm=evento_crm,
        )

        print(buscar)

        if buscar:
            contar = buscar.aggregate(Sum('cantidad_asignada'))['cantidad_asignada__sum']
        else:
            contar = 0
        
        print(stock_disponible)
        print(contar)
        print(cantidad_asignada)

        if stock_disponible < contar + cantidad_asignada:
            form.add_error('cantidad_asignada', 'Se superó la cantidad contada. Máximo: %s. Contado: %s.' % (stock_disponible, contar + cantidad_asignada))
            return super().form_invalid(form)

        try:
            if self.request.session['primero']:
                item = len(EventoCRMDetalle.objects.filter(evento_crm = evento_crm))

                obj, created = EventoCRMDetalle.objects.get_or_create(
                    content_type = ContentType.objects.get_for_model(merchandising),
                    id_registro = merchandising.id,
                    evento_crm = evento_crm,
                    almacen_origen = almacen_origen,
                    tipo_stock = tipo_stock,
                    unidad = form.cleaned_data.get('unidad')
                )
                if created:
                    obj.item = item + 1
                    obj.cantidad_asignada = cantidad_asignada

                else:
                    obj.cantidad_asignada = obj.cantidad_asignada + cantidad_asignada

                registro_guardar(obj, self.request)
                obj.save()
                self.request.session['primero']=False
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        evento_crm = EventoCRM.objects.get(id = self.kwargs['evento_crm_id'])
        kwargs['evento_crm'] = evento_crm
        return kwargs

    def get_context_data(self, **kwargs):
        self.request.session['primero'] = True
        evento_crm = EventoCRM.objects.get(id = self.kwargs['evento_crm_id'])
        context = super(EventoCRMDetalleMerchandisingCreateView, self).get_context_data(**kwargs)
        context['accion'] = 'Agregar'
        context['titulo'] = 'Merchandising'
        context['sociedad'] = evento_crm.sociedad.id
        context['url_stock'] = reverse_lazy('merchandising_app:stock', kwargs={'id_merchandising':1})[:-2]
        context['url_unidad'] = reverse_lazy('merchandising_app:unidad_merchandising', kwargs={'id_merchandising':1})[:-2]
        return context


class  EventoCRMDetalleMerchandisingUpdateView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('crm.change_eventocrmdetalle')
    model = EventoCRMDetalle
    template_name = "crm/eventos_crm/form_actualizar_merchandising.html"
    form_class = EventoCRMDetalleActualizarForm

    def dispatch(self, request, *args, **kwargs):
        context = {}
        error_sede = False
        context['titulo'] = 'Error de guardar'
        detalle = EventoCRMDetalle.objects.get(id=self.kwargs['pk'])
        evento_crm = detalle.evento_crm
        if not evento_crm.sede_origen:
            error_sede = True

        if error_sede:
            context['texto'] = 'Ingrese una sede de origen.'
            return render(request, 'includes/modal sin permiso.html', context)
        
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('crm_app:evento_crm_detalle', kwargs={'pk':self.get_object().evento_crm.id})

    def get_form_kwargs(self, *args, **kwargs):
        print(self.kwargs)
        detalle = EventoCRMDetalle.objects.get(id=self.kwargs['pk'])
        evento_crm = detalle.evento_crm
        kwargs = super().get_form_kwargs()
        kwargs['evento_crm'] = evento_crm
        return kwargs

    def form_valid(self, form):
        detalle = EventoCRMDetalle.objects.get(id=self.kwargs['pk'])
        evento_crm = detalle.evento_crm
        almacen_origen = form.cleaned_data.get('almacen_origen')
        tipo_stock = form.cleaned_data.get('tipo_stock')
        cantidad_asignada = form.cleaned_data.get('cantidad_asignada')
        merchandising = detalle.producto
        stock_disponible = ver_tipo_stock(ContentType.objects.get_for_model(merchandising), merchandising.id, evento_crm.sociedad.id, almacen_origen.id, tipo_stock.id)

        buscar = EventoCRMDetalle.objects.filter(
            content_type=ContentType.objects.get_for_model(merchandising),
            id_registro=merchandising.id,
            tipo_stock=tipo_stock,
            evento_crm=evento_crm,
        ).exclude(id=detalle.id)

        if buscar:
            contar = buscar.aggregate(Sum('cantidad_asignada'))['cantidad_asignada__sum']
        else:
            contar = 0

        if stock_disponible < contar + cantidad_asignada:
            form.add_error('cantidad_asignada', 'Se superó la cantidad contada. Máximo: %s. Contado: %s.' % (stock_disponible, contar + cantidad_asignada))
            return super().form_invalid(form)

        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        detalle = EventoCRMDetalle.objects.get(id=self.kwargs['pk'])
        evento_crm = detalle.evento_crm
        context = super(EventoCRMDetalleMerchandisingUpdateView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        context['titulo'] = "Item"
        context['merchandising'] = self.get_object().content_type.get_object_for_this_type(id = self.get_object().id_registro)
        context['sociedad'] = evento_crm.sociedad.id
        context['url_stock'] = reverse_lazy('merchandising_app:stock', kwargs={'id_merchandising':1})[:-2]
        context['url_unidad'] = reverse_lazy('merchandising_app:unidad_merchandising', kwargs={'id_merchandising':1})[:-2]
        return context


class EventoCRMDetalleMerchandisingDeleteView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('crm.change_eventocrmdetalle')
    model = EventoCRMDetalle
    template_name = "includes/eliminar generico.html"

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('crm_app:evento_crm_detalle', kwargs={'pk':self.get_object().evento_crm.id})

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            merchandisings = EventoCRMDetalle.objects.filter(evento_crm=self.get_object().evento_crm)
            contador = 1
            for merchandising in merchandisings:
                if merchandising == self.get_object(): continue
                merchandising.item = contador
                merchandising.save()
                contador += 1
            return super().delete(request, *args, **kwargs)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(EventoCRMDetalleMerchandisingDeleteView, self).get_context_data(**kwargs)
        context['accion'] = "Eliminar"
        context['titulo'] = "Merchandising"
        context['item'] = self.get_object().content_type.get_object_for_this_type(id = self.get_object().id_registro)
        return context


class EventoCRMDetalleInformacionAdicionalCreateView(PermissionRequiredMixin, BSModalCreateView):
    permission_required = ('crm.add_eventocrmdetalle')
    model = EventoCRMDetalleInformacionAdicional
    template_name = "includes/formulario generico.html"
    form_class = EventoCRMDetalleInformacionAdicionalForm
    
    def get_success_url(self, **kwargs):
        return reverse_lazy('crm_app:evento_crm_detalle', kwargs={'pk':self.kwargs['evento_crm_id']})

    def form_valid(self, form):
        form.instance.evento_crm = EventoCRM.objects.get(id = self.kwargs['evento_crm_id'])
        registro_guardar(form.instance, self.request)

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(EventoCRMDetalleInformacionAdicionalCreateView, self).get_context_data(**kwargs)
        context['accion']="Registrar"
        context['titulo']="Información Adicional"
        return context
    

class EventoCRMDetalleInformacionAdicionalUpdateView(PermissionRequiredMixin,BSModalUpdateView):
    permission_required = ('crm.change_eventocrmdetalle')
    model = EventoCRMDetalleInformacionAdicional
    template_name = "includes/formulario generico.html"
    form_class = EventoCRMDetalleInformacionAdicionalForm

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('crm_app:evento_crm_detalle', kwargs={'pk':self.object.evento_crm.id})

    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(EventoCRMDetalleInformacionAdicionalUpdateView, self).get_context_data(**kwargs)
        context['accion']="Actualizar"
        context['titulo']="Información Adicional"
        return context
    

class EventoCRMDetalleInformacionAdicionalDeleteView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('crm.delete_eventocrmdetalle')
    model = EventoCRMDetalleInformacionAdicional
    template_name = "includes/eliminar generico.html"

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('crm_app:evento_crm_detalle', kwargs={'pk':self.object.evento_crm.id})

    def get_context_data(self, **kwargs):
        context = super(EventoCRMDetalleInformacionAdicionalDeleteView, self).get_context_data(**kwargs)
        context['accion'] = "Eliminar"
        context['titulo'] = "Información Adicional"
        context['item'] = self.get_object().comentario
        context['dar_baja'] = "true"
        return context
    

class EventoCRMGenerarGuiaView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('logistica.change_despachodetalle')
    model = EventoCRM
    template_name = "includes/eliminar generico.html"

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('comprobante_despacho_app:guia_detalle', kwargs={'id_guia':self.kwargs['guia'].id})

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            self.object = self.get_object()
            detalles = self.object.EventoCRMDetalle_evento_crm.all()
            serie_comprobante = SeriesComprobante.objects.por_defecto(ContentType.objects.get_for_model(Guia))
            observaciones = []
            observaciones.append('PRESENTACIÓN DE PRODUCTOS')
            # if self.object.observaciones:
            #     observaciones.append(self.object.observaciones)

            guia = Guia.objects.create(
                sociedad=self.object.sociedad,
                serie_comprobante=serie_comprobante,
                motivo_traslado='13',
                observaciones=" | ".join(observaciones),
                created_by=self.request.user,
                updated_by=self.request.user,
            )

            for detalle in detalles:
                guia_detalle = GuiaDetalle.objects.create(
                    item=detalle.item,
                    content_type=detalle.content_type,
                    id_registro=detalle.id_registro,
                    guia=guia,
                    cantidad=detalle.cantidad_asignada,
                    unidad=detalle.producto.unidad_base,
                    descripcion_documento=detalle.producto.descripcion_venta,
                    peso=detalle.producto.peso_unidad_base,
                    created_by=self.request.user,
                    updated_by=self.request.user,
                )
            self.kwargs['guia'] = guia
            self.request.session['primero'] = False
            messages.success(request, MENSAJE_GENERAR_GUIA)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        self.request.session['primero'] = True
        context = super(EventoCRMGenerarGuiaView, self).get_context_data(**kwargs)
        context['accion'] = "Generar"
        context['titulo'] = "Guía"
        context['dar_baja'] = "true"
        context['item'] = self.get_object()
        return context
    

class PreguntaCRMListView(PermissionRequiredMixin, FormView):
    permission_required = ('crm.view_preguntacrm')
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
        context['lista_preguntas'] = EncuestaCRM.objects.values_list('pregunta_crm', flat=True)
        context['lista_alternativas'] = AlternativaCRM.objects.values_list('pregunta_crm', flat=True)

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
        context['contexto_pregunta_crm'] = pregunta_crm
        context['lista_preguntas'] = EncuestaCRM.objects.values_list('pregunta_crm', flat=True)
        context['lista_alternativas'] = AlternativaCRM.objects.values_list('pregunta_crm', flat=True)

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)


class PreguntaCRMCreateView(PermissionRequiredMixin, BSModalCreateView):
    permission_required = ('crm.add_preguntacrm')
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
        context['lista_preguntas'] = EncuestaCRM.objects.values_list('pregunta_crm', flat=True)
        context['lista_alternativas'] = AlternativaCRM.objects.values_list('pregunta_crm', flat=True)

        return context


def PreguntaCRMDetailTabla(request, pk):
    data = dict()
    if request.method == 'GET':
        template = 'crm/encuestas_crm/pregunta/detalle_tabla.html'
        context = {}
        pregunta_crm = PreguntaCRM.objects.get(id = pk)

        context['contexto_pregunta_crm'] = pregunta_crm
        context['alternativas'] = AlternativaCRM.objects.filter(pregunta_crm = pregunta_crm)
        context['lista_preguntas'] = EncuestaCRM.objects.values_list('pregunta_crm', flat=True)
        context['lista_alternativas'] = AlternativaCRM.objects.values_list('pregunta_crm', flat=True)

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
        context['lista_encuestas'] = RespuestaCRM.objects.values_list('encuesta_crm', flat=True)

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
        context['lista_encuestas'] = RespuestaCRM.objects.values_list('encuesta_crm', flat=True)

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
        context['lista_encuestas'] = RespuestaCRM.objects.values_list('encuesta_crm', flat=True)

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
        context['lista_encuestas'] = RespuestaCRM.objects.values_list('encuesta_crm', flat=True)

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
    

class RespuestaCRMListView(PermissionRequiredMixin, FormView):
    permission_required = ('crm.view_respuestacrm')

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
            condicion = Q(cliente_crm = filtro_cliente)
            respuesta_crm = respuesta_crm.filter(condicion)
            contexto_filtro.append("cliente=" + filtro_cliente)

        if filtro_encuesta:
            condicion = Q(encuesta_crm = filtro_encuesta)
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
   
        context['contexto_respuesta_crm'] = respuesta_crm
        context['contexto_pagina'] = respuesta_crm
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
            condicion = Q(encuesta = filtro_encuesta)
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
    # form_class = RespuestaCRMForm
    form_class = RespuestaCrearCRMForm
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
    # template_name = "includes/formulario generico.html"
    template_name = "crm/clientes_crm/form_cliente.html"
    form_class = RespuestaCRMForm
    success_url = reverse_lazy('crm_app:respuesta_crm_inicio')

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        respuesta = kwargs['instance']
        lista = []
        relaciones = ClienteInterlocutor.objects.filter(cliente = respuesta.cliente_crm)
        for relacion in relaciones:
            lista.append(relacion.interlocutor.id)

        kwargs['interlocutor_queryset'] = InterlocutorCliente.objects.filter(id__in = lista)
        kwargs['interlocutor'] = respuesta.interlocutor
        return kwargs

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


class RespuestaVerView(TemplateView): #respuesta_del_cliente | encuesta para el cliente
    template_name = "crm/encuestas_crm/respuesta/respuesta_ver.html"

    def get_context_data(self, **kwargs):
        respuesta = RespuestaCRM.objects.get(slug = self.kwargs['slug'])
        encuesta = respuesta.encuesta_crm
        preguntas = encuesta.pregunta_crm.all()

        context = super(RespuestaVerView, self).get_context_data(**kwargs)
        context['respuesta'] = respuesta
        context['encuesta'] = encuesta
        context['preguntas'] = preguntas
        return context


class EncuestaRespuesta(View): #encuesta
    # permission_required = ('crm.view_encuestacrm')

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

    
class ClienteCRMDetalleVerView(PermissionRequiredMixin, BSModalReadView):
    permission_required = ('crm.view_clientecrmdetalle')
    model = ClienteCRMDetalle
    template_name = "crm/clientes_crm/detalle_reporte_actividad.html"

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('crm_app:cliente_crm_detalle', kwargs={'pk':self.object.cliente_crm.id})

    def get_context_data(self, **kwargs):
        context = super(ClienteCRMDetalleVerView, self).get_context_data(**kwargs)
        detalle_reporte = ClienteCRMDetalle.objects.get(id = self.kwargs['pk'])
        context['contexto_detalle_reporte'] = detalle_reporte
        context['titulo']=detalle_reporte.get_tipo_actividad_display()
        return context
    

