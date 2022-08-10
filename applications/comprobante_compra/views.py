from applications.comprobante_compra.forms import ArchivoComprobanteCompraPIForm, ComprobanteCompraCIDetalleUpdateForm, ComprobanteCompraCIForm, ComprobanteCompraPIForm, RecepcionComprobanteCompraPIForm
from applications.comprobante_compra.models import ArchivoComprobanteCompraPI, ComprobanteCompraCI, ComprobanteCompraCIDetalle, ComprobanteCompraPI, ComprobanteCompraPIDetalle
from applications.funciones import obtener_totales
from applications.home.templatetags.funciones_propias import filename
from applications.importaciones import *
from applications.movimiento_almacen.models import MovimientosAlmacen, TipoMovimiento
from applications.recepcion_compra.models import RecepcionCompra

# Create your views here.


class ComprobanteCompraPIListView(ListView):
    model = ComprobanteCompraPI
    template_name = "comprobante_compra/comprobante_compra_pi/inicio.html"
    context_object_name = 'contexto_comprobante_compra_pi'


class ComprobanteCompraPIDetailView(DetailView):
    model = ComprobanteCompraPI
    template_name = "comprobante_compra/comprobante_compra_pi/detalle.html"
    context_object_name = 'contexto_comprobante_compra_pi'

    def get_context_data(self, **kwargs):
        context = super(ComprobanteCompraPIDetailView, self).get_context_data(**kwargs)
        context['materiales'] = ComprobanteCompraPIDetalle.objects.ver_detalle(self.get_object())
        context['archivos'] = ArchivoComprobanteCompraPI.objects.filter(comprobante_compra=self.get_object())
        context['totales'] = obtener_totales(self.get_object())
        try:
            context['contexto_recepcion_compra'] = RecepcionCompra.objects.get(
                                                        content_type=ContentType.objects.get_for_model(self.get_object()),
                                                        id_registro=self.get_object().id,
                                                    )
        except:
            context['contexto_recepcion_compra'] = None
        return context
    

def ComprobanteCompraPIDetailTabla(request, slug):
    data = dict()
    if request.method == 'GET':
        template = 'comprobante_compra/comprobante_compra_pi/detalle_tabla.html'
        context = {}
        comprobante_compra = ComprobanteCompraPI.objects.get(slug = slug)
        context['contexto_comprobante_compra_pi'] = comprobante_compra
        context['materiales'] = ComprobanteCompraPIDetalle.objects.ver_detalle(comprobante_compra)
        context['archivos'] = ArchivoComprobanteCompraPI.objects.filter(comprobante_compra=comprobante_compra)
        context['totales'] = obtener_totales(comprobante_compra)

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)


class ComprobanteCompraPIUpdateView(BSModalUpdateView):
    model = ComprobanteCompraPI
    template_name = "includes/formulario generico.html"
    form_class = ComprobanteCompraPIForm
    success_url = '.'

    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super(ComprobanteCompraPIUpdateView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        context['titulo'] = "Comprobante"
        return context
    

class ArchivoComprobanteCompraPICreateView(BSModalCreateView):
    model = ArchivoComprobanteCompraPI
    template_name = "includes/formulario generico.html"
    form_class = ArchivoComprobanteCompraPIForm
    success_url = '.'

    def form_valid(self, form):
        form.instance.comprobante_compra = ComprobanteCompraPI.objects.get(slug=self.kwargs['slug'])
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super(ArchivoComprobanteCompraPICreateView, self).get_context_data(**kwargs)
        context['accion'] = "Agregar"
        context['titulo'] = "Archivo"
        return context
    

class ArchivoComprobanteCompraPIDeleteView(BSModalDeleteView):
    model = ArchivoComprobanteCompraPI
    template_name = "includes/eliminar generico.html"
    
    def get_success_url(self, **kwargs):
        return reverse_lazy('comprobante_compra_app:comprobante_compra_pi_detalle', kwargs={'slug':self.object.comprobante_compra.slug})

    def get_context_data(self, **kwargs):
        context = super(ArchivoComprobanteCompraPIDeleteView, self).get_context_data(**kwargs)
        context['accion'] = "Agregar"
        context['titulo'] = "Archivo"
        context['item'] = filename(self.object.archivo)
        return context


class RecepcionComprobanteCompraPIView(BSModalFormView):
    template_name = "includes/formulario generico.html"
    form_class = RecepcionComprobanteCompraPIForm
    
    def get_success_url(self, **kwargs):
        return reverse_lazy('comprobante_compra_app:comprobante_compra_pi_detalle', kwargs={'slug':self.kwargs['slug']})

    def form_valid(self, form):
        if self.request.session['primero']:
            fecha_recepcion = form.cleaned_data['fecha_recepcion']
            usuario_recepcion = form.cleaned_data['usuario_recepcion']
            nro_bultos = form.cleaned_data['nro_bultos']
            observaciones = form.cleaned_data['observaciones']

            comprobante_pi = ComprobanteCompraPI.objects.get(slug=self.kwargs['slug'])
            detalles = comprobante_pi.ComprobanteCompraPIDetalle_comprobante_compra.all()
            movimiento_inicial = TipoMovimiento.objects.get(codigo=100)
            movimiento_final = TipoMovimiento.objects.get(codigo=101)

            recepcion = RecepcionCompra.objects.create(
                numero_comprobante_compra = comprobante_pi.numero_comprobante_compra,
                content_type = ContentType.objects.get_for_model(comprobante_pi),
                id_registro = comprobante_pi.id,
                fecha_recepcion = fecha_recepcion,
                usuario_recepcion = usuario_recepcion,
                nro_bultos = nro_bultos,
                observaciones = observaciones,
                created_by = self.request.user,
                updated_by = self.request.user,
            )
            for detalle in detalles:
                movimiento_anterior = MovimientosAlmacen.objects.get(
                    content_type_producto = detalle.orden_compra_detalle.content_type,
                    id_registro_producto = detalle.orden_compra_detalle.id_registro,
                    tipo_movimiento = movimiento_inicial,
                    signo_factor_multiplicador = +1,
                    content_type_documento_proceso = ContentType.objects.get_for_model(comprobante_pi),
                    id_registro_documento_proceso = comprobante_pi.id,
                    sociedad = comprobante_pi.sociedad,
                    movimiento_reversion = False,
                )

                movimiento_uno = MovimientosAlmacen.objects.create(
                    content_type_producto = detalle.orden_compra_detalle.content_type,
                    id_registro_producto = detalle.orden_compra_detalle.id_registro,
                    cantidad = detalle.cantidad,
                    tipo_movimiento = movimiento_inicial,
                    signo_factor_multiplicador = -1,
                    content_type_documento_proceso = ContentType.objects.get_for_model(comprobante_pi),
                    id_registro_documento_proceso = comprobante_pi.id,
                    almacen = None,
                    sociedad = comprobante_pi.sociedad,
                    movimiento_anterior = movimiento_anterior,
                    movimiento_reversion = False,
                    created_by = self.request.user,
                    updated_by = self.request.user,
                )
                movimiento_dos = MovimientosAlmacen.objects.create(
                    content_type_producto = detalle.orden_compra_detalle.content_type,
                    id_registro_producto = detalle.orden_compra_detalle.id_registro,
                    cantidad = detalle.cantidad,
                    tipo_movimiento = movimiento_final,
                    signo_factor_multiplicador = +1,
                    content_type_documento_proceso = ContentType.objects.get_for_model(recepcion),
                    id_registro_documento_proceso = recepcion.id,
                    almacen = None,
                    sociedad = comprobante_pi.sociedad,
                    movimiento_anterior = movimiento_uno,
                    movimiento_reversion = False,
                    created_by = self.request.user,
                    updated_by = self.request.user,
                )
            comprobante_pi.estado = 2
            comprobante_pi.total = obtener_totales(comprobante_pi)['total']
            registro_guardar(comprobante_pi, self.request)
            comprobante_pi.save()
            self.request.session['primero'] = False
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        self.request.session['primero'] = True
        context = super(RecepcionComprobanteCompraPIView, self).get_context_data(**kwargs)
        context['accion'] = "Recibir"
        context['titulo'] = "Comprobante de Compra"
        return context


class ComprobanteCompraCIRegistrarView(BSModalFormView):
    template_name = "includes/formulario generico.html"
    form_class = ComprobanteCompraCIForm
    
    def get_success_url(self, **kwargs):
        return reverse_lazy('comprobante_compra_app:comprobante_compra_ci_detalle', kwargs={'slug':self.kwargs['slug']})

    def form_valid(self, form):
        if self.request.session['primero']:
            numero_comprobante_compra = form.cleaned_data['numero_comprobante_compra']
            fecha_comprobante = form.cleaned_data['fecha_comprobante']
            archivo = form.cleaned_data['archivo']

            comprobante_pi = ComprobanteCompraPI.objects.get(slug=self.kwargs['slug'])
            comprobante_ci = ComprobanteCompraCI.objects.create(
                internacional_nacional = comprobante_pi.internacional_nacional,
                incoterms = comprobante_pi.incoterms,
                numero_comprobante_compra = numero_comprobante_compra,
                comprobante_compra_PI = comprobante_pi,
                sociedad = comprobante_pi.sociedad,
                fecha_comprobante = fecha_comprobante,
                moneda = comprobante_pi.moneda,
                slug = comprobante_pi.slug,
                archivo = archivo,
                condiciones = comprobante_pi.condiciones,
                created_by = self.request.user,
                updated_by = self.request.user,
                )
            detalles = comprobante_pi.ComprobanteCompraPIDetalle_comprobante_compra.all()
            
            for detalle in detalles:
                ComprobanteCompraCIDetalle.objects.create(
                    item = detalle.item,
                    content_type = detalle.orden_compra_detalle.content_type,
                    id_registro = detalle.orden_compra_detalle.id_registro,
                    cantidad = detalle.cantidad,
                    precio_unitario_sin_igv = detalle.precio_unitario_sin_igv,
                    precio_unitario_con_igv = detalle.precio_unitario_con_igv,
                    precio_final_con_igv = detalle.precio_final_con_igv,
                    descuento = detalle.descuento,
                    sub_total = detalle.sub_total,
                    igv = detalle.igv,
                    total = detalle.total,
                    tipo_igv = detalle.tipo_igv,
                    comprobante_compra = comprobante_ci,
                    created_by = self.request.user,
                    updated_by = self.request.user,
                )
            self.request.session['primero'] = False
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        self.request.session['primero'] = True
        context = super(ComprobanteCompraCIRegistrarView, self).get_context_data(**kwargs)
        context['accion'] = "Recibir"
        context['titulo'] = "Comprobante de Compra"
        return context


class ComprobanteCompraCIDetailView(DetailView):
    model = ComprobanteCompraCI
    template_name = "comprobante_compra/comprobante_compra_ci/detalle.html"
    context_object_name = 'contexto_comprobante_compra_ci'

    def get_context_data(self, **kwargs):
        context = super(ComprobanteCompraCIDetailView, self).get_context_data(**kwargs)
        context['materiales'] = ComprobanteCompraCIDetalle.objects.ver_detalle(self.get_object())
        context['totales'] = obtener_totales(self.get_object())
        return context
    

def ComprobanteCompraCIDetailTabla(request, slug):
    data = dict()
    if request.method == 'GET':
        template = 'comprobante_compra/comprobante_compra_ci/detalle_tabla.html'
        context = {}
        comprobante_compra = ComprobanteCompraCI.objects.get(slug = slug)
        context['contexto_comprobante_compra_ci'] = comprobante_compra
        context['materiales'] = ComprobanteCompraCIDetalle.objects.ver_detalle(comprobante_compra)
        context['totales'] = obtener_totales(comprobante_compra)

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)


class ComprobanteCompraCIDetalleUpdateView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('oferta_proveedor.change_ofertaproveedordetalle')

    model = ComprobanteCompraCIDetalle
    template_name = "oferta_proveedor/oferta_proveedor/actualizar.html"
    form_class = ComprobanteCompraCIDetalleUpdateForm

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('comprobante_compra_app:comprobante_compra_ci_detalle', kwargs={'slug':self.get_object().comprobante_compra.slug})

    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ComprobanteCompraCIDetalleUpdateView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        context['titulo'] = "Precios"
        context['material'] = str(self.object.content_type.get_object_for_this_type(id = self.object.id_registro))
        return context


class ComprobanteCompraCIFinalizarView(BSModalDeleteView):
    model = ComprobanteCompraCI
    template_name = "includes/eliminar generico.html"
    context_object_name = 'contexto_comprobante_compra_ci'

    # def dispatch(self, request, *args, **kwargs):
    #     if not self.has_permission():
    #         return render(request, 'includes/modal sin permiso.html')
    #     return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('comprobante_compra_app:comprobante_compra_ci_detalle', kwargs={'slug':self.get_object().slug})

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.estado = 2
        registro_guardar(self.object, self.request)
        self.object.save()
        messages.success(request, MENSAJE_COMPROBANTE_COMPRA)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(ComprobanteCompraCIFinalizarView, self).get_context_data(**kwargs)
        context['accion'] = "Finalizar"
        context['titulo'] = "Comprobante"
        context['dar_baja'] = "true"
        context['item'] = self.object.numero_comprobante_compra
        return context