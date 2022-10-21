import requests
from django import forms
from applications.comprobante_venta.funciones import anular_nubefact, guia_nubefact
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
    GuiaClienteForm,
    GuiaConductorForm,
    GuiaDestinoForm,
    GuiaFechaTrasladoForm,
    GuiaMotivoTrasladoForm,
    GuiaPartidaForm,
    GuiaSerieForm,
    GuiaTransportistaForm,
)


class GuiaListView(ListView):
    model = Guia
    template_name = 'comprobante_despacho/guia/inicio.html'
    context_object_name = 'contexto_guia'

def GuiaTabla(request):
    data = dict()
    if request.method == 'GET':
        template = 'comprobante_despacho/guia/inicio_tabla.html'
        context = {}
        context['contexto_guia'] = Guia.objects.all()

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)


class GuiaDetalleView(TemplateView):
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
        context['url_nubefact'] = NubefactRespuesta.objects.respuesta(obj)
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
        context['url_nubefact'] = NubefactRespuesta.objects.respuesta(obj)
        context['respuestas_nubefact'] = NubefactRespuesta.objects.respuestas(obj)

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)


class GuiaCrearView(DeleteView):
    model = Despacho
    template_name = "includes/form generico.html"

    def get_success_url(self, **kwargs):
        return reverse_lazy('comprobante_despacho_app:guia_detalle', kwargs={'id_guia':self.object.id})
   
    def delete(self, request, *args, **kwargs):
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
        return HttpResponseRedirect(reverse_lazy('comprobante_despacho_app:guia_detalle', kwargs={'id_guia':guia.id}))

    def get_context_data(self, **kwargs):
        context = super(GuiaCrearView, self).get_context_data(**kwargs)
        context['accion'] = 'Generar'
        context['titulo'] = 'Guía'
        context['texto'] = '¿Seguro que desea generar Guía?'
        context['item'] = str(self.object.cliente) 
        return context

class GuiaTransportistaView(BSModalUpdateView):
    model = Guia
    template_name = "comprobante_despacho/guia/form.html"
    form_class = GuiaTransportistaForm
    
    def get_success_url(self) -> str:
        return reverse_lazy('comprobante_despacho_app:guia_detalle', kwargs={'id_guia':self.kwargs['pk']})

    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(GuiaTransportistaView, self).get_context_data(**kwargs)
        context['accion'] = "Elegir"
        context['titulo'] = "Transportista"
        return context
        

class GuiaSerieUpdateView(BSModalUpdateView):
    model = Guia
    template_name = "includes/formulario generico.html"
    form_class = GuiaSerieForm
    success_url = '.'
    
    def get_context_data(self, **kwargs):
        context = super(GuiaSerieUpdateView, self).get_context_data(**kwargs)
        context['accion'] = 'Seleccionar'
        context['titulo'] = 'Serie'
        return context


class GuiaPartidaView(BSModalUpdateView):
    model = Guia
    template_name = "comprobante_despacho/guia/form direccion.html"
    form_class = GuiaPartidaForm
    
    def get_success_url(self) -> str:
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

class GuiaDestinoView(BSModalUpdateView):
    model = Guia
    template_name = "comprobante_despacho/guia/form direccion.html"
    form_class = GuiaDestinoForm
    
    def get_success_url(self) -> str:
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

class GuiaBultosView(BSModalUpdateView):
    model = Guia
    template_name = "includes/formulario generico.html"
    form_class = GuiaBultosForm
    
    def get_success_url(self) -> str:
        return reverse_lazy('comprobante_despacho_app:guia_detalle', kwargs={'id_guia':self.kwargs['pk']})

    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(GuiaBultosView, self).get_context_data(**kwargs)
        context['accion'] = "Asignar"
        context['titulo'] = "Número de Bultos"
        return context

class GuiaConductorView(BSModalUpdateView):
    model = Guia
    template_name = "comprobante_despacho/guia/form conductor.html"
    form_class = GuiaConductorForm
    
    def get_success_url(self) -> str:
        return reverse_lazy('comprobante_despacho_app:guia_detalle', kwargs={'id_guia':self.kwargs['pk']})

    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(GuiaConductorView, self).get_context_data(**kwargs)
        context['accion'] = "Asignar"
        context['titulo'] = "Conductor"
        return context

class GuiaMotivoTrasladoView(BSModalUpdateView):
    model = Guia
    template_name = "includes/formulario generico.html"
    form_class = GuiaMotivoTrasladoForm
    
    def get_success_url(self) -> str:
        return reverse_lazy('comprobante_despacho_app:guia_detalle', kwargs={'id_guia':self.kwargs['pk']})

    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(GuiaMotivoTrasladoView, self).get_context_data(**kwargs)
        context['accion'] = "Asignar"
        context['titulo'] = "MotivoTraslado"
        return context

class GuiaFechaTrasladoView(BSModalUpdateView):
    model = Guia
    template_name = "includes/formulario generico.html"
    form_class = GuiaFechaTrasladoForm
    
    def get_success_url(self) -> str:
        return reverse_lazy('comprobante_despacho_app:guia_detalle', kwargs={'id_guia':self.kwargs['pk']})

    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(GuiaFechaTrasladoView, self).get_context_data(**kwargs)
        context['accion'] = "Cambiar"
        context['titulo'] = "Fecha de Traslado"
        return context

class GuiaClienteView(BSModalUpdateView):
    model = Guia
    template_name = "comprobante_despacho/guia/form_cliente.html"
    form_class = GuiaClienteForm
    
    def get_success_url(self) -> str:
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


class GuiaGuardarView(DeleteView):
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
        return super(GuiaGuardarView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self) -> str:
        return reverse_lazy('comprobante_despacho_app:guia_detalle', kwargs={'id_guia':self.kwargs['pk']})

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.fecha_emision = date.today()
        if not obj.fecha_traslado:
            obj.fecha_traslado = date.today()
        obj.estado = 2
        obj.numero_guia = Guia.objects.nuevo_numero(obj)
        registro_guardar(obj, self.request)
        obj.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(GuiaGuardarView, self).get_context_data(**kwargs)
        context['accion'] = 'Guardar'
        context['titulo'] = 'Guía de Remisión'
        context['texto'] = '¿Seguro de guardar la Guía de Remisión?'
        context['item'] = self.get_object()
        return context


class GuiaNubeFactEnviarView(DeleteView):
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
        return super(GuiaNubeFactEnviarView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self) -> str:
        return reverse_lazy('comprobante_despacho_app:guia_detalle', kwargs={'id_guia':self.kwargs['pk']})

    def delete(self, request, *args, **kwargs):
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
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(GuiaNubeFactEnviarView, self).get_context_data(**kwargs)
        context['accion'] = 'Enviar'
        context['titulo'] = 'Guía de Remisión a NubeFact'
        context['texto'] = '¿Seguro de enviar la Guía de Remisión a NubeFact?'
        context['item'] = self.get_object()
        return context


class GuiaAnularView(BSModalDeleteView):
    model = Guia
    template_name = "includes/form generico.html"

    def get_success_url(self) -> str:
        return reverse_lazy('comprobante_despacho_app:guia_inicio')

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.estado = 3
        if obj.serie_comprobante.NubefactSerieAcceso_serie_comprobante.acceder(obj.sociedad, ContentType.objects.get_for_model(obj)) == 'MANUAL':
            obj.save()
            return HttpResponseRedirect(self.get_success_url())

        return super().delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(GuiaAnularView, self).get_context_data(**kwargs)
        obj = self.get_object()
        context['accion'] = 'Anular'
        context['titulo'] = 'Guía de Remisión'
        context['texto'] = '¿Seguro de anular la Guía de Remisión?'
        context['item'] = self.get_object()
        return context


class GuiaNubefactRespuestaDetailView(BSModalReadView):
    model = Guia
    template_name = "comprobante_venta/nubefact_respuesta.html"
    
    def get_context_data(self, **kwargs):
        context = super(GuiaNubefactRespuestaDetailView, self).get_context_data(**kwargs)
        context['titulo'] = 'Movimientos Nubefact'
        context['movimientos'] = NubefactRespuesta.objects.respuestas(self.get_object())
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

