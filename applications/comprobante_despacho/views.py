import requests
from django import forms
from applications.importaciones import*
from applications.logistica.models import Despacho
from applications.envio_clientes.models import Transportista
from applications.datos_globales.models import SeriesComprobante
from applications.clientes.models import ClienteInterlocutor, InterlocutorCliente

from .models import(
    Guia,
    GuiaDetalle,
)

from .forms import(
    GuiaBultosForm,
    GuiaClienteForm,
    GuiaConductorForm,
    GuiaDestinoForm,
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

        serie_comprobante = SeriesComprobante.objects.filter(tipo_comprobante=ContentType.objects.get_for_model(Guia)).earliest('created_at')

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
    success_url = reverse_lazy('comprobante_despacho_app:guia_inicio')

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
    success_url = reverse_lazy('comprobante_despacho_app:guia_inicio')

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
    success_url = reverse_lazy('comprobante_despacho_app:guia_inicio')

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
    success_url = reverse_lazy('comprobante_despacho_app:guia_inicio')

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
    success_url = reverse_lazy('comprobante_despacho_app:guia_inicio')

    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(GuiaConductorView, self).get_context_data(**kwargs)
        context['accion'] = "Asignar"
        context['titulo'] = "Conductor"
        return context

class GuiaClienteView(BSModalUpdateView):
    model = Guia
    template_name = "comprobante_despacho/guia/form_cliente.html"
    form_class = GuiaClienteForm
    success_url = reverse_lazy('comprobante_despacho_app:guia_inicio')

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
        error_punto_partida = False
        context['titulo'] = 'Error de guardar'
        if not self.get_object().direccion_partida:
            error_punto_partida = True

        if error_punto_partida:
            context['texto'] = 'Ingrese un Punto de partida'
            return render(request, 'includes/modal sin permiso.html', context)
        return super(GuiaGuardarView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self) -> str:
        return reverse_lazy('comprobante_venta_app:factura_venta_detalle', kwargs={'id_factura_venta':self.kwargs['pk']})

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        fecha_vencimiento = generarDeuda(obj, self.request)

        obj.fecha_emision = date.today()
        obj.fecha_vencimiento = fecha_vencimiento
        obj.estado = 2
        obj.numero_factura = Guia.objects.nuevo_numero(obj)
        registro_guardar(obj, self.request)
        obj.save()
        obj.confirmacion.estado = 2
        obj.confirmacion.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(GuiaGuardarView, self).get_context_data(**kwargs)
        context['accion'] = 'Guardar'
        context['titulo'] = 'Factura de Venta'
        context['texto'] = '¿Seguro de guardar la Factura de Venta?'
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

