from django.core.paginator import Paginator
from django import forms
from django.shortcuts import render
from applications.importaciones import *
from applications.funciones import numeroXn, registrar_excepcion
from applications.material.funciones import stock, ver_tipo_stock
from applications.movimiento_almacen.models import MovimientosAlmacen, TipoMovimiento
from applications.datos_globales.models import SeriesComprobante, Unidad
from applications.comprobante_despacho.models import Guia, GuiaDetalle
from applications.crm.forms import (
    ClienteCRMBuscarForm, 
    ClienteCRMDetalleForm, 
    ClienteCRMForm,
    EventoCRMActualizarForm,
    EventoCRMDetalleActualizarForm,
    EventoCRMDetalleForm,
    EventoCRMDetalleInformacionAdicionalForm, 
    ProveedorCRMForm, 
    EventoCRMForm, 
    EventoCRMBuscarForm, 
    EventoCRMDetalleDescripcionForm,
    )
from applications.crm.models import ClienteCRM, ClienteCRMDetalle, EventoCRMDetalle, EventoCRMDetalleInformacionAdicional, ProveedorCRM, EventoCRM

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

# class EventoCRMGuardarView(PermissionRequiredMixin, BSModalDeleteView):
#     permission_required = ('crm.change_eventocrm')
#     model = EventoCRM
#     template_name = "includes/eliminar generico.html"
    
#     def dispatch(self, request, *args, **kwargs):        
#         if not self.has_permission():
#             return render(request, 'includes/modal sin permiso.html')

#     def get_success_url(self, **kwargs):
#         return reverse_lazy('crm_app:evento_crm_detalle', kwargs={'pk':self.object.id})

#     @transaction.atomic
#     def delete(self, request, *args, **kwargs):
#         sid = transaction.savepoint()
#         try:
#             self.object = self.get_object()
#             movimiento_final = TipoMovimiento.objects.get(codigo=139)  # Salida por traslado
#             for detalle in self.object.EnvioTrasladoProductoDetalle_envio_traslado_producto.all():
#                 movimiento_uno = MovimientosAlmacen.objects.create(
#                     content_type_producto=detalle.content_type,
#                     id_registro_producto=detalle.id_registro,
#                     cantidad=detalle.cantidad_envio,
#                     tipo_movimiento=movimiento_final,
#                     tipo_stock=detalle.tipo_stock,
#                     signo_factor_multiplicador=-1,
#                     content_type_documento_proceso=ContentType.objects.get_for_model(self.object),
#                     id_registro_documento_proceso=self.object.id,
#                     almacen=detalle.almacen_origen,
#                     sociedad=self.object.sociedad,
#                     movimiento_anterior=None,
#                     movimiento_reversion=False,
#                     created_by=self.request.user,
#                     updated_by=self.request.user,
#                 )
#                 movimiento_dos = MovimientosAlmacen.objects.create(
#                     content_type_producto=detalle.content_type,
#                     id_registro_producto=detalle.id_registro,
#                     cantidad=detalle.cantidad_envio,
#                     tipo_movimiento=movimiento_final,
#                     tipo_stock=movimiento_final.tipo_stock_final,
#                     signo_factor_multiplicador=+1,
#                     content_type_documento_proceso=ContentType.objects.get_for_model(self.object),
#                     id_registro_documento_proceso=self.object.id,
#                     sociedad=self.object.sociedad,
#                     movimiento_anterior=movimiento_uno,
#                     movimiento_reversion=False,
#                     created_by=self.request.user,
#                     updated_by=self.request.user,
#                 )

#                 for validar in detalle.ValidarSerieEnvioTrasladoProductoDetalle_envio_traslado_producto_detalle.all():
#                     validar.serie.serie_movimiento_almacen.add(movimiento_uno)
#                     validar.serie.serie_movimiento_almacen.add(movimiento_dos)

#             numero_envio_traslado = EnvioTrasladoProducto.objects.all().aggregate(Count('numero_envio_traslado'))['numero_envio_traslado__count'] + 1
#             self.object.numero_envio_traslado = numero_envio_traslado
#             self.object.estado = 2
#             self.object.fecha_traslado = datetime.now()

#             registro_guardar(self.object, self.request)
#             self.object.save()
#             messages.success(request, MENSAJE_GUARDAR_ENVIO)
#         except Exception as ex:
#             transaction.savepoint_rollback(sid)
#             registrar_excepcion(self, ex, __file__)
#         return HttpResponseRedirect(self.get_success_url())

#     def get_context_data(self, **kwargs):
#         context = super(EnvioTrasladoProductoGuardarView, self).get_context_data(**kwargs)
#         context['accion'] = "Guardar"
#         context['titulo'] = "Envio"
#         context['dar_baja'] = True
#         return context

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