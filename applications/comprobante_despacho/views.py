import requests
from django.core.paginator import Paginator
from django import forms
from applications.comprobante_venta.funciones import anular_nubefact, consultar_guia, guia_nubefact
from applications.funciones import registrar_excepcion
from applications.importaciones import*
from applications.logistica.models import Despacho
from applications.envio_clientes.models import Transportista
from applications.datos_globales.models import NubefactRespuesta, SeriesComprobante
from applications.clientes.models import ClienteInterlocutor, InterlocutorCliente

from .models import(
    Guia,
    GuiaDetalle,
)

from .forms import(
    GuiaAnularForm,
    GuiaBultosForm,
    GuiaBuscarForm,
    GuiaClienteForm,
    GuiaConductorForm,
    GuiaDestinoForm,
    GuiaDetallePesoForm,
    GuiaFechaTrasladoForm,
    GuiaMotivoTrasladoForm,
    GuiaObservacionForm,
    GuiaPartidaForm,
    GuiaSerieForm,
    GuiaTransportistaForm,
)


class GuiaListView(PermissionRequiredMixin, FormView):
    permission_required = ('comprobante_despacho.view_guia')
    template_name = 'comprobante_despacho/guia/inicio.html'
    form_class = GuiaBuscarForm
    success_url = '.'

    def get_form_kwargs(self):
        kwargs = super(GuiaListView, self).get_form_kwargs()
        kwargs['filtro_fecha_emision'] = self.request.GET.get('fecha_emision')
        kwargs['filtro_numero_guia'] = self.request.GET.get('numero_guia')
        kwargs['filtro_cliente'] = self.request.GET.get('cliente')
        kwargs['filtro_sociedad'] = self.request.GET.get('sociedad')
        kwargs['filtro_estado'] = self.request.GET.get('estado')
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super(GuiaListView, self).get_context_data(**kwargs)
        guias = Guia.objects.all()
        filtro_fecha_emision = self.request.GET.get('fecha_emision')
        filtro_numero_guia = self.request.GET.get('numero_guia')
        filtro_cliente = self.request.GET.get('cliente')
        filtro_sociedad = self.request.GET.get('sociedad')
        filtro_estado = self.request.GET.get('estado')
        contexto_filtro = []
        if filtro_fecha_emision:
            condicion = Q(fecha_emision = filtro_fecha_emision)
            guias = guias.filter(condicion)
            contexto_filtro.append("fecha_emision=" + filtro_fecha_emision)
        if filtro_numero_guia:
            condicion = Q(numero_guia = filtro_numero_guia)
            guias = guias.filter(condicion)
            contexto_filtro.append("numero_guia=" + filtro_numero_guia)
        if filtro_cliente:
            condicion = Q(cliente = filtro_cliente)
            guias = guias.filter(condicion)
            contexto_filtro.append("cliente=" + filtro_cliente)
        if filtro_sociedad:
            condicion = Q(sociedad = filtro_sociedad)
            guias = guias.filter(condicion)
            contexto_filtro.append("sociedad=" + filtro_sociedad)
        if filtro_estado:
            condicion = Q(estado = filtro_estado)
            guias = guias.filter(condicion)
            contexto_filtro.append("estado=" + filtro_estado)
        
        context['contexto_filtro'] = "&".join(contexto_filtro)

        context['pagina_filtro'] = ""
        if self.request.GET.get('page'):
            if context['contexto_filtro']:
                context['pagina_filtro'] = f'&page={self.request.GET.get("page")}'
            else:
                context['pagina_filtro'] = f'page={self.request.GET.get("page")}'
        context['contexto_filtro'] = '?' + context['contexto_filtro']

        objectsxpage =  10 # Show 10 objects per page.

        if len(guias) > objectsxpage:
            paginator = Paginator(guias, objectsxpage)
            page_number = self.request.GET.get('page')
            guias = paginator.get_page(page_number)

        context['contexto_guia'] = guias
        context['contexto_pagina'] = guias
        return context

def GuiaTabla(request):
    data = dict()
    if request.method == 'GET':
        template = 'comprobante_despacho/guia/inicio_tabla.html'
        context = {}
        
        guias = Guia.objects.all()
        filtro_fecha_emision = request.GET.get('fecha_emision')
        filtro_numero_guia = request.GET.get('numero_guia')
        filtro_cliente = request.GET.get('cliente')
        filtro_sociedad = request.GET.get('sociedad')
        filtro_estado = request.GET.get('estado')
        contexto_filtro = []
        if filtro_fecha_emision:
            condicion = Q(fecha_emision = filtro_fecha_emision)
            guias = guias.filter(condicion)
            contexto_filtro.append("fecha_emision=" + filtro_fecha_emision)
        if filtro_numero_guia:
            condicion = Q(numero_guia = filtro_numero_guia)
            guias = guias.filter(condicion)
            contexto_filtro.append("numero_guia=" + filtro_numero_guia)
        if filtro_cliente:
            condicion = Q(cliente = filtro_cliente)
            guias = guias.filter(condicion)
            contexto_filtro.append("cliente=" + filtro_cliente)
        if filtro_sociedad:
            condicion = Q(sociedad = filtro_sociedad)
            guias = guias.filter(condicion)
            contexto_filtro.append("sociedad=" + filtro_sociedad)
        if filtro_estado:
            condicion = Q(estado = filtro_estado)
            guias = guias.filter(condicion)
            contexto_filtro.append("estado=" + filtro_estado)
        
        context['contexto_filtro'] = "&".join(contexto_filtro)

        context['pagina_filtro'] = ""
        if request.GET.get('page'):
            if context['contexto_filtro']:
                context['pagina_filtro'] = f'&page={request.GET.get("page")}'
            else:
                context['pagina_filtro'] = f'page={request.GET.get("page")}'
        context['contexto_filtro'] = '?' + context['contexto_filtro']

        objectsxpage =  10 # Show 10 objects per page.

        if len(guias) > objectsxpage:
            paginator = Paginator(guias, objectsxpage)
            page_number = request.GET.get('page')
            guias = paginator.get_page(page_number)

        context['contexto_guia'] = guias
        context['contexto_pagina'] = guias

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)


class GuiaDetalleView(PermissionRequiredMixin, TemplateView):
    permission_required = ('comprobante_despacho.view_guia')
    template_name = "comprobante_despacho/guia/detalle.html"

    def get_context_data(self, **kwargs):
        obj = Guia.objects.get(id = kwargs['id_guia'])

        materiales = None
        try:
            materiales = obj.GuiaDetalle_guia_venta.all()
        except:
            pass
        
        context = super(GuiaDetalleView, self).get_context_data(**kwargs)
        context['guia'] = obj
        context['materiales'] = materiales
        if obj.serie_comprobante:
            context['nubefact_acceso'] = obj.serie_comprobante.NubefactSerieAcceso_serie_comprobante.acceder(obj.sociedad, ContentType.objects.get_for_model(obj))
        url_nubefact = NubefactRespuesta.objects.respuesta(obj)
        if url_nubefact:
            context['url_nubefact'] = url_nubefact
        if obj.nubefact:
            context['url_nubefact'] = obj.nubefact
        context['respuestas_nubefact'] = NubefactRespuesta.objects.respuestas(obj)

        return context

def GuiaDetalleVerTabla(request, id_guia):
    data = dict()
    if request.method == 'GET':
        template = 'comprobante_despacho/guia/detalle_tabla.html'
        obj = Guia.objects.get(id=id_guia)

        materiales = None
        try:
            materiales = obj.GuiaDetalle_guia_venta.all()
        except:
            pass

        context = {}
        context['guia'] = obj
        context['materiales'] = materiales
        if obj.serie_comprobante:
            context['nubefact_acceso'] = obj.serie_comprobante.NubefactSerieAcceso_serie_comprobante.acceder(obj.sociedad, ContentType.objects.get_for_model(obj))
        url_nubefact = NubefactRespuesta.objects.respuesta(obj)
        if url_nubefact:
            context['url_nubefact'] = url_nubefact
        if obj.nubefact:
            context['url_nubefact'] = obj.nubefact
        context['respuestas_nubefact'] = NubefactRespuesta.objects.respuestas(obj)

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)


class GuiaCrearView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('comprobante_despacho.add_guia')
    model = Despacho
    template_name = "includes/form generico.html"

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('comprobante_despacho_app:guia_detalle', kwargs={'id_guia':self.object.id})
   
    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            self.object = self.get_object()

            detalles = self.object.DespachoDetalle_despacho.all()

            serie_comprobante = SeriesComprobante.objects.por_defecto(ContentType.objects.get_for_model(Guia))

            guia = Guia.objects.create(
                sociedad = self.object.sociedad,
                serie_comprobante = serie_comprobante,
                cliente = self.object.cliente,
                created_by = self.request.user,
                updated_by = self.request.user,
            )

            for detalle in detalles:
                guia_detalle = GuiaDetalle.objects.create(
                    item = detalle.item,
                    content_type = detalle.content_type,
                    id_registro = detalle.id_registro,
                    guia=guia,
                    cantidad=detalle.cantidad_despachada,
                    unidad=detalle.producto.unidad_base,
                    descripcion_documento=detalle.producto.descripcion_venta,
                    peso=detalle.producto.peso_unidad_base,
                    created_by=self.request.user,
                    updated_by=self.request.user,                
                )

            registro_guardar(self.object, self.request)
            self.object.save()

            messages.success(request, MENSAJE_GENERAR_GUIA)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(GuiaCrearView, self).get_context_data(**kwargs)
        context['accion'] = 'Generar'
        context['titulo'] = 'Guía'
        context['texto'] = '¿Seguro que desea generar Guía?'
        context['item'] = str(self.object.cliente) 
        return context

class GuiaTransportistaView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('comprobante_despacho.change_guia')
    model = Guia
    template_name = "comprobante_despacho/guia/form.html"
    form_class = GuiaTransportistaForm

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)
    
    def get_success_url(self):
        return reverse_lazy('comprobante_despacho_app:guia_detalle', kwargs={'id_guia':self.kwargs['pk']})

    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(GuiaTransportistaView, self).get_context_data(**kwargs)
        context['accion'] = "Elegir"
        context['titulo'] = "Transportista"
        return context


class GuiaTransportistaLimpiarView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('comprobante_despacho.change_guia')
    model = Guia
    template_name = "includes/eliminar generico.html"

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)
    
    def get_success_url(self):
        return reverse_lazy('comprobante_despacho_app:guia_detalle', kwargs={'id_guia':self.kwargs['pk']})

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.transportista = None
        registro_guardar(self.object, self.request)
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(GuiaTransportistaLimpiarView, self).get_context_data(**kwargs)
        context['accion'] = "Limpiar"
        context['titulo'] = "datos del Transportista"
        context['dar_baja'] = True
        return context
        

class GuiaDetallePesoView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('comprobante_despacho.change_guiadetalle')
    model = GuiaDetalle
    template_name = "includes/formulario generico.html"
    form_class = GuiaDetallePesoForm

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)
    
    def get_success_url(self):
        return reverse_lazy('comprobante_despacho_app:guia_detalle', kwargs={'id_guia':self.object.guia.id})

    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(GuiaDetallePesoView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        context['titulo'] = "Peso"
        return context
        

class GuiaSerieUpdateView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('comprobante_despacho.change_guia')
    model = Guia
    template_name = "includes/formulario generico.html"
    form_class = GuiaSerieForm
    success_url = '.'

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super(GuiaSerieUpdateView, self).get_context_data(**kwargs)
        context['accion'] = 'Seleccionar'
        context['titulo'] = 'Serie'
        return context


class GuiaPartidaView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('comprobante_despacho.change_guia')
    model = Guia
    template_name = "comprobante_despacho/guia/form direccion.html"
    form_class = GuiaPartidaForm

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)
    
    def get_success_url(self):
        return reverse_lazy('comprobante_despacho_app:guia_detalle', kwargs={'id_guia':self.kwargs['pk']})

    def form_valid(self, form):
        ubigeo = form.cleaned_data['ubigeo']
        form.instance.ubigeo_partida = ubigeo
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        lista = []
        lista.append((0, "--------------------"))
        
        for anexo in self.object.sociedad.Sede_sociedad.filter(estado=1):
            lista.append((anexo.id, "%s | %s" % (anexo.direccion, anexo.distrito.codigo)))
        kwargs['lista'] = lista
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(GuiaPartidaView, self).get_context_data(**kwargs)
        context['accion'] = "Elegir"
        context['titulo'] = "Dirección de Partida"
        return context

class GuiaDestinoView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('comprobante_despacho.change_guia')
    model = Guia
    template_name = "comprobante_despacho/guia/form direccion.html"
    form_class = GuiaDestinoForm

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)
    
    def get_success_url(self):
        return reverse_lazy('comprobante_despacho_app:guia_detalle', kwargs={'id_guia':self.kwargs['pk']})

    def form_valid(self, form):
        ubigeo = form.cleaned_data['ubigeo']
        form.instance.ubigeo_destino = ubigeo
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        lista = []
        lista.append((0, "--------------------"))
        lista.append((self.object.cliente.id, "%s | %s" % (self.object.cliente.direccion_fiscal, self.object.cliente.ubigeo)))
        
        for anexo in self.object.cliente.ClienteAnexo_cliente.filter(estado=1):
            lista.append((anexo.id, "%s | %s" % (anexo.direccion, anexo.distrito.codigo)))
        kwargs['lista'] = lista
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(GuiaDestinoView, self).get_context_data(**kwargs)
        context['accion'] = "Elegir"
        context['titulo'] = "Dirección de Destino"
        return context

class GuiaBultosView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('comprobante_despacho.change_guia')
    model = Guia
    template_name = "includes/formulario generico.html"
    form_class = GuiaBultosForm

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)
    
    def get_success_url(self):
        return reverse_lazy('comprobante_despacho_app:guia_detalle', kwargs={'id_guia':self.kwargs['pk']})

    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(GuiaBultosView, self).get_context_data(**kwargs)
        context['accion'] = "Asignar"
        context['titulo'] = "Número de Bultos"
        return context

class GuiaObservacionView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('comprobante_despacho.change_guia')
    model = Guia
    template_name = "includes/formulario generico.html"
    form_class = GuiaObservacionForm

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)
    
    def get_success_url(self):
        return reverse_lazy('comprobante_despacho_app:guia_detalle', kwargs={'id_guia':self.kwargs['pk']})

    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(GuiaObservacionView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        context['titulo'] = "Observaciones"
        return context

class GuiaConductorView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('comprobante_despacho.change_guia')
    model = Guia
    template_name = "comprobante_despacho/guia/form conductor.html"
    form_class = GuiaConductorForm

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)
    
    def get_success_url(self):
        return reverse_lazy('comprobante_despacho_app:guia_detalle', kwargs={'id_guia':self.kwargs['pk']})

    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(GuiaConductorView, self).get_context_data(**kwargs)
        context['accion'] = "Asignar"
        context['titulo'] = "Conductor"
        return context

class GuiaConductorLimpiarView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('comprobante_despacho.change_guia')
    model = Guia
    template_name = "includes/eliminar generico.html"

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)
    
    def get_success_url(self):
        return reverse_lazy('comprobante_despacho_app:guia_detalle', kwargs={'id_guia':self.kwargs['pk']})

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.conductor_tipo_documento = None
        self.object.conductor_numero_documento = None
        self.object.conductor_nombre = None
        self.object.conductor_apellidos = None
        self.object.conductor_numero_licencia = None
        self.object.placa_numero = None
        registro_guardar(self.object, self.request)
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(GuiaConductorLimpiarView, self).get_context_data(**kwargs)
        context['accion'] = "Limpiar"
        context['titulo'] = "datos del Conductor"
        context['dar_baja'] = True
        return context

class GuiaMotivoTrasladoView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('comprobante_despacho.change_guia')
    model = Guia
    template_name = "includes/formulario generico.html"
    form_class = GuiaMotivoTrasladoForm

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)
    
    def get_success_url(self):
        return reverse_lazy('comprobante_despacho_app:guia_detalle', kwargs={'id_guia':self.kwargs['pk']})

    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(GuiaMotivoTrasladoView, self).get_context_data(**kwargs)
        context['accion'] = "Asignar"
        context['titulo'] = "MotivoTraslado"
        return context

class GuiaFechaTrasladoView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('comprobante_despacho.change_guia')
    model = Guia
    template_name = "includes/formulario generico.html"
    form_class = GuiaFechaTrasladoForm
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('comprobante_despacho_app:guia_detalle', kwargs={'id_guia':self.kwargs['pk']})

    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(GuiaFechaTrasladoView, self).get_context_data(**kwargs)
        context['accion'] = "Cambiar"
        context['titulo'] = "Fecha de Traslado"
        return context

class GuiaClienteView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('comprobante_despacho.change_guia')
    model = Guia
    template_name = "comprobante_despacho/guia/form_cliente.html"
    form_class = GuiaClienteForm
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('comprobante_despacho_app:guia_detalle', kwargs={'id_guia':self.kwargs['pk']})

    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        guia = kwargs['instance']
        lista = []
        relaciones = ClienteInterlocutor.objects.filter(cliente = guia.cliente)
        for relacion in relaciones:
            lista.append(relacion.interlocutor.id)

        kwargs['interlocutor_queryset'] = InterlocutorCliente.objects.filter(id__in = lista)
        kwargs['interlocutor'] = guia.cliente_interlocutor
        return kwargs  

    def get_context_data(self, **kwargs):
        context = super(GuiaClienteView, self).get_context_data(**kwargs)
        context['accion'] = "Asignar"
        context['titulo'] = "Interlocutor"
        context['cliente'] = self.object.cliente
        return context


class GuiaGuardarView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('comprobante_despacho.change_guia')
    model = Guia
    template_name = "includes/form generico.html"

    def dispatch(self, request, *args, **kwargs):
        context = {}
        error_direccion_partida = False
        error_direccion_destino = False
        error_ubigeo_partida = False
        error_ubigeo_destino = False
        error_numero_bultos = False
        error_cliente_interlocutor = False
        error_peso = False
        error_transportista_placa_numero = False
        error_transportista_placa_numero_cero_guion = False
        error_transporte_privado = False
        context['titulo'] = 'Error de guardar'
        if not self.get_object().direccion_partida:
            error_direccion_partida = True
        if not self.get_object().direccion_destino:
            error_direccion_destino = True
        if not self.get_object().ubigeo_partida:
            error_ubigeo_partida = True
        if not self.get_object().ubigeo_destino:
            error_ubigeo_destino = True
        if not self.get_object().numero_bultos:
            error_numero_bultos = True
        if not self.get_object().cliente_interlocutor:
            error_cliente_interlocutor = True
        for detalle in self.get_object().detalles:
            if not detalle.peso:
                error_peso = True
        if not self.get_object().transportista: #Transporte privado
            if not self.get_object().placa_numero:
                error_transportista_placa_numero = True
            elif '0'*len(self.get_object().placa_numero) == self.get_object().placa_numero or '-' in self.get_object().placa_numero:
                error_transportista_placa_numero_cero_guion = True
            elif not self.get_object().conductor_tipo_documento or not self.get_object().conductor_numero_documento or not self.get_object().conductor_nombre or not self.get_object().conductor_apellidos or not self.get_object().conductor_numero_licencia:
                error_transporte_privado = True
    

        if error_direccion_partida:
            context['texto'] = 'Ingrese una Dirección de partida'
            return render(request, 'includes/modal sin permiso.html', context)
        if error_direccion_destino:
            context['texto'] = 'Ingrese una Dirección de destino'
            return render(request, 'includes/modal sin permiso.html', context)
        if error_ubigeo_partida:
            context['texto'] = 'Ingrese un Ubigeo de partida'
            return render(request, 'includes/modal sin permiso.html', context)
        if error_ubigeo_destino:
            context['texto'] = 'Ingrese un Ubigeo de destino'
            return render(request, 'includes/modal sin permiso.html', context)
        if error_numero_bultos:
            context['texto'] = 'Ingrese un Número de bultos'
            return render(request, 'includes/modal sin permiso.html', context)
        if error_cliente_interlocutor:
            context['texto'] = 'Ingrese un Interlocutor'
            return render(request, 'includes/modal sin permiso.html', context)
        if error_peso:
            context['texto'] = 'Falta registrar los pesos de los materiales.'
            return render(request, 'includes/modal sin permiso.html', context)
        if error_transportista_placa_numero:
            context['texto'] = 'Registrar la placa del transportista.'
            return render(request, 'includes/modal sin permiso.html', context)
        if error_transportista_placa_numero_cero_guion:
            context['texto'] = 'La placa no deben ser ceros ni debe tener guiones.'
            return render(request, 'includes/modal sin permiso.html', context)
        if error_transporte_privado:
            context['texto'] = 'Ingresar los datos del conductor de transporte privado.'
            return render(request, 'includes/modal sin permiso.html', context)

        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super(GuiaGuardarView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('comprobante_despacho_app:guia_detalle', kwargs={'id_guia':self.kwargs['pk']})

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            obj = self.get_object()
            obj.fecha_emision = date.today()
            if not obj.fecha_traslado:
                obj.fecha_traslado = date.today()
            obj.estado = 2
            obj.numero_guia = Guia.objects.nuevo_numero(obj)
            registro_guardar(obj, self.request)
            obj.save()
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(GuiaGuardarView, self).get_context_data(**kwargs)
        context['accion'] = 'Guardar'
        context['titulo'] = 'Guía de Remisión'
        context['texto'] = '¿Seguro de guardar la Guía de Remisión?'
        context['item'] = self.get_object()
        return context


class GuiaNubeFactEnviarView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('comprobante_despacho.change_guia')
    model = Guia
    template_name = "includes/form generico.html"

    def dispatch(self, request, *args, **kwargs):
        context = {}
        error_nubefact = False
        context['titulo'] = 'Error de guardar'
        if self.get_object().serie_comprobante.NubefactSerieAcceso_serie_comprobante.acceder(self.get_object().sociedad, ContentType.objects.get_for_model(self.get_object())) == 'MANUAL':
            error_nubefact = True
        
        if error_nubefact:
            context['texto'] = 'No hay una ruta para envío a NubeFact'
            return render(request, 'includes/modal sin permiso.html', context)

        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super(GuiaNubeFactEnviarView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('comprobante_despacho_app:guia_detalle', kwargs={'id_guia':self.kwargs['pk']})

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            obj = self.get_object()
            respuesta = guia_nubefact(obj, self.request.user)
            if respuesta.error:
                obj.estado = 6
            elif respuesta.aceptado:
                obj.estado = 4
            else:
                obj.estado = 5
            registro_guardar(obj, self.request)
            obj.save()
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(GuiaNubeFactEnviarView, self).get_context_data(**kwargs)
        context['accion'] = 'Enviar'
        context['titulo'] = 'Guía de Remisión a NubeFact'
        context['texto'] = '¿Seguro de enviar la Guía de Remisión a NubeFact?'
        context['item'] = self.get_object()
        return context


class GuiaNubeFactConsultarView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('comprobante_despacho.change_guia')
    model = Guia
    template_name = "includes/form generico.html"

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('comprobante_despacho_app:guia_detalle', kwargs={'id_guia':self.kwargs['pk']})

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            obj = self.get_object()
            respuesta = consultar_guia(obj, self.request.user)
            if respuesta.error:
                obj.estado = 6
            elif respuesta.aceptado:
                obj.estado = 4
            else:
                obj.estado = 5
            registro_guardar(obj, self.request)
            obj.save()
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(GuiaNubeFactConsultarView, self).get_context_data(**kwargs)
        context['accion'] = 'Consultar'
        context['titulo'] = 'Guía de Remisión a NubeFact'
        context['texto'] = '¿Seguro de consultar la Guía de Remisión a NubeFact?'
        context['item'] = self.get_object()
        return context


class GuiaAnularView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('comprobante_despacho.change_guia')
    model = Guia
    template_name = "includes/form generico.html"

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('comprobante_despacho_app:guia_inicio')

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            obj = self.get_object()
            obj.estado = 3
            obj.despacho.estado = 2
            obj.despacho.save()
            obj.save()
            return HttpResponseRedirect(self.get_success_url())
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(GuiaAnularView, self).get_context_data(**kwargs)
        obj = self.get_object()
        context['accion'] = 'Anular'
        context['titulo'] = 'Guía de Remisión'
        context['texto'] = '¿Seguro de anular la Guía de Remisión?'
        context['item'] = self.get_object()
        return context


class GuiaNubefactRespuestaDetailView(PermissionRequiredMixin, BSModalReadView):
    permission_required = ('comprobante_despacho.view_guia')
    model = Guia
    template_name = "comprobante_venta/nubefact_respuesta.html"

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super(GuiaNubefactRespuestaDetailView, self).get_context_data(**kwargs)
        context['titulo'] = 'Movimientos Nubefact'
        context['movimientos'] = NubefactRespuesta.objects.respuestas(self.get_object())
        return context


class GuiaEliminarView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('comprobante_despacho.delete_guia')
    model = Guia
    template_name = "includes/form generico.html"

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        if self.request.session['id_despacho']:
            return reverse_lazy('logistica_app:despacho_detalle', kwargs={'pk':self.request.session['id_despacho']})
        return reverse_lazy('comprobante_despacho_app:guia_inicio')

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            guia = self.get_object()
            if guia.despacho:
                guia.despacho.estado = 2
                guia.despacho.save()
            return super().delete(request, *args, **kwargs)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(GuiaEliminarView, self).get_context_data(**kwargs)
        obj = self.get_object()
        self.request.session['id_despacho'] = None
        if obj.despacho:
            self.request.session['id_despacho'] = obj.despacho.id
        context['accion'] = 'Eliminar'
        context['titulo'] = 'Guia'
        context['texto'] = '¿Seguro de eliminar la Guia?'
        context['item'] = self.get_object()
        return context


class ClienteInterlocutorForm(forms.Form):
    cliente_interlocutor = forms.ModelChoiceField(queryset = ClienteInterlocutor.objects.all(), required=False)

def ClienteInterlocutorView(request, id_cliente):
    form = ClienteInterlocutorForm()
    lista = []
    relaciones = ClienteInterlocutor.objects.filter(cliente = id_cliente)
    for relacion in relaciones:
        lista.append(relacion.interlocutor.id)

    form.fields['cliente_interlocutor'].queryset = InterlocutorCliente.objects.filter(id__in = lista)
    data = dict()
    if request.method == 'GET':
        template = 'includes/form.html'
        context = {'form':form}

        data['info'] = render_to_string(
            template,
            context,
            request=request
        ).replace('selected', 'selected=""')
        return JsonResponse(data)

