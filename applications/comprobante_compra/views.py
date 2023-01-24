from decimal import Decimal
from applications.cobranza.models import DeudaProveedor
from applications.comprobante_compra.forms import ArchivoComprobanteCompraPIForm, ComprobanteCompraCIDetalleUpdateForm, ComprobanteCompraCIForm, ComprobanteCompraPIForm, RecepcionComprobanteCompraPIForm
from applications.comprobante_compra.models import ArchivoComprobanteCompraPI, ComprobanteCompraCI, ComprobanteCompraCIDetalle, ComprobanteCompraPI, ComprobanteCompraPIDetalle
from applications.funciones import igv, obtener_totales, registrar_excepcion, tipo_de_cambio
from applications.home.templatetags.funciones_propias import filename
from applications.importaciones import *
from applications.movimiento_almacen.models import MovimientosAlmacen, TipoMovimiento
from applications.recepcion_compra.models import RecepcionCompra

# Create your views here.

class ComprobanteCompraPIListView(PermissionRequiredMixin, ListView):
    permission_required = ('comprobante_compra.view_comprobantecomprapi')

    model = ComprobanteCompraPI
    template_name = "comprobante_compra/comprobante_compra_pi/inicio.html"
    context_object_name = 'contexto_comprobante_compra_pi'


class ComprobanteCompraPIDetailView(PermissionRequiredMixin, DetailView):
    permission_required = ('comprobante_compra.view_comprobantecomprapi')

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
                                                        estado=1,
                                                    )
        except:
            context['contexto_recepcion_compra'] = None
        if 'comprobante_compra.add_comprobantecomprapi' in self.request.user.get_all_permissions():
            context['permiso_compras'] = True
        if 'recepcion_compra.add_recepcioncompra' in self.request.user.get_all_permissions():
            context['permiso_logistica'] = True

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
        if 'comprobante_compra.add_comprobantecomprapi' in request.user.get_all_permissions():
            context['permiso_compras'] = True


        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)


class ComprobanteCompraPITraduccionView(PermissionRequiredMixin, DetailView):
    permission_required = ('comprobante_compra.view_comprobantecomprapi')

    model = ComprobanteCompraPI
    template_name = "comprobante_compra/comprobante_compra_pi/traduccion.html"
    context_object_name = 'contexto_comprobante_compra_pi'

    def get_context_data(self, **kwargs):
        context = super(ComprobanteCompraPITraduccionView, self).get_context_data(**kwargs)
        context['materiales'] = ComprobanteCompraPIDetalle.objects.ver_detalle(self.get_object())
        return context


class ComprobanteCompraPIGuardarView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('comprobante_compra.change_comprobantecomprapi')
    model = ComprobanteCompraPI
    template_name = "includes/eliminar generico.html"

    def dispatch(self, request, *args, **kwargs):
        obj = ComprobanteCompraPI.objects.get(slug=self.kwargs['slug'])
        context = {}
        context['titulo'] = 'Error de guardar'
        
        error_fecha = False
        if not obj.fecha:
            error_fecha = True

        error_numero_comprobante_compra = False
        if not obj.numero_comprobante_compra:
            error_numero_comprobante_compra = True

        error_logistico = False
        if obj.logistico == Decimal('0.00'):
            error_logistico = True

        if error_fecha:
            context['texto'] = 'No hay Fecha registrada.'
            return render(request, 'includes/modal sin permiso.html', context)

        if error_numero_comprobante_compra:
            context['texto'] = 'No hay Numero de Comprobante de Compra registrada.'
            return render(request, 'includes/modal sin permiso.html', context)

        if error_logistico:
            context['texto'] = 'No hay Logístico registrado.'
            return render(request, 'includes/modal sin permiso.html', context)

        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super(ComprobanteCompraPIGuardarView, self).dispatch(request, *args, **kwargs)    

    def get_success_url(self):
        return reverse_lazy('comprobante_compra_app:comprobante_compra_pi_detalle', kwargs={'slug':self.kwargs['slug']})

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            self.object = self.get_object()
            totales = obtener_totales(self.object)
            self.object.total_descuento = totales['total_descuento']
            self.object.total_anticipo = totales['total_anticipo']
            self.object.total_gravada = totales['total_gravada']
            self.object.total_inafecta = totales['total_inafecta']
            self.object.total_exonerada = totales['total_exonerada']
            self.object.total_igv = totales['total_igv']
            self.object.total_gratuita = totales['total_gratuita']
            self.object.otros_cargos = totales['total_otros_cargos']
            self.object.total = totales['total']
            self.object.estado = 1
            self.object.save()

            DeudaProveedor.objects.create(
                content_type=ContentType.objects.get_for_model(self.object),
                id_registro=self.object.id,
                monto=self.object.total,
                moneda=self.object.moneda,
                tipo_cambio=tipo_de_cambio(),
                fecha_deuda=date.today(),
                fecha_vencimiento=date.today(),
                sociedad=self.object.orden_compra.sociedad,
                proveedor=self.object.orden_compra.proveedor,
            )

            messages.success(request, MENSAJE_GUARDAR_COMPROBANTE_COMPRA_PI)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())
    
    def get_context_data(self, **kwargs):
        context = super(ComprobanteCompraPIGuardarView, self).get_context_data(**kwargs)
        context['accion'] = "Guardar"
        context['titulo'] = "Comprobante"
        context['dar_baja'] = True
        context['item'] = self.get_object()
        return context


class ComprobanteCompraPIUpdateView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('comprobante_compra.change_comprobantecomprapi')
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


class ComprobanteCompraPIAnularView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('comprobante_compra.change_comprobantecomprapi')
    model = ComprobanteCompraPI
    template_name = "includes/eliminar generico.html"
    success_url = reverse_lazy('comprobante_compra_app:comprobante_compra_pi_lista')
    context_object_name = 'contexto_comprobante_compra' 

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            self.object = self.get_object()
            comprobante = self.get_object()

            materiales = comprobante.ComprobanteCompraPIDetalle_comprobante_compra.all()
            movimiento_final = TipoMovimiento.objects.get(codigo=100) # Tránsito
            for material in materiales:
                movimiento_dos = MovimientosAlmacen.objects.get(
                        content_type_producto = material.orden_compra_detalle.content_type,
                        id_registro_producto = material.orden_compra_detalle.id_registro,
                        cantidad = material.cantidad,
                        tipo_movimiento = movimiento_final,
                        tipo_stock = movimiento_final.tipo_stock_final,
                        signo_factor_multiplicador = +1,
                        content_type_documento_proceso = ContentType.objects.get_for_model(comprobante),
                        id_registro_documento_proceso = comprobante.id,
                        almacen = None,
                        sociedad = comprobante.sociedad,
                        movimiento_anterior = None,
                        movimiento_reversion = False,
                    )
                if len(movimiento_dos.MovimientosAlmacen_movimiento_anterior.all()) > 0:
                    messages.warning(request, MENSAJE_ERROR_ANULAR_COMPROBANTE_COMPRA_PI)
                    return HttpResponseRedirect(reverse_lazy('comprobante_compra_app:comprobante_compra_pi_detalle', kwargs={'slug':comprobante.slug}))

            for material in materiales:
                movimiento_dos = MovimientosAlmacen.objects.get(
                        content_type_producto = material.orden_compra_detalle.content_type,
                        id_registro_producto = material.orden_compra_detalle.id_registro,
                        cantidad = material.cantidad,
                        tipo_movimiento = movimiento_final,
                        tipo_stock = movimiento_final.tipo_stock_final,
                        signo_factor_multiplicador = +1,
                        content_type_documento_proceso = ContentType.objects.get_for_model(comprobante),
                        id_registro_documento_proceso = comprobante.id,
                        almacen = None,
                        sociedad = comprobante.sociedad,
                        movimiento_anterior = None,
                        movimiento_reversion = False,
                    )
                movimiento_dos.delete()
            
            deuda_proveedor = DeudaProveedor.objects.get(
                content_type=ContentType.objects.get_for_model(comprobante),
                id_registro=comprobante.id,
            )

            deuda_proveedor.delete()
            comprobante.delete()

            messages.success(request, MENSAJE_ANULAR_COMPROBANTE_COMPRA_PI)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())
    
    def get_context_data(self, **kwargs):
        context = super(ComprobanteCompraPIAnularView, self).get_context_data(**kwargs)
        context['accion'] = 'Anular'
        context['titulo'] = 'Comprobante de Compra PI'
        context['item'] = self.get_object()

        return context

class ArchivoComprobanteCompraPICreateView(PermissionRequiredMixin, BSModalCreateView):
    permission_required = ('comprobante_compra.add_archivocomprobantecomprapi')
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
    

class ArchivoComprobanteCompraPIDeleteView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('comprobante_compra.delete_archivocomprobantecomprapi')
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


class RecepcionComprobanteCompraPIView(PermissionRequiredMixin, BSModalFormView):
    permission_required = ('comprobante_compra.add_recepcioncomprobantecomprapi')
    template_name = "includes/formulario generico.html"
    form_class = RecepcionComprobanteCompraPIForm
    
    def get_success_url(self, **kwargs):
        return reverse_lazy('comprobante_compra_app:comprobante_compra_pi_detalle', kwargs={'slug':self.kwargs['slug']})

    @transaction.atomic
    def form_valid(self, form):
        sid = transaction.savepoint()
        try:
            if self.request.session['primero']:
                fecha_recepcion = form.cleaned_data['fecha_recepcion']
                usuario_recepcion = form.cleaned_data['usuario_recepcion']
                nro_bultos = form.cleaned_data['nro_bultos']
                observaciones = form.cleaned_data['observaciones']

                comprobante_pi = ComprobanteCompraPI.objects.get(slug=self.kwargs['slug'])
                detalles = comprobante_pi.ComprobanteCompraPIDetalle_comprobante_compra.all()
                movimiento_inicial = TipoMovimiento.objects.get(codigo=100) #Tránsito
                movimiento_final = TipoMovimiento.objects.get(codigo=101) #Disponible

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
                        tipo_stock = movimiento_inicial.tipo_stock_final,
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
                        tipo_movimiento = movimiento_final,
                        tipo_stock = movimiento_final.tipo_stock_inicial,
                        signo_factor_multiplicador = -1,
                        content_type_documento_proceso = ContentType.objects.get_for_model(recepcion),
                        id_registro_documento_proceso = recepcion.id,
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
                        tipo_stock = movimiento_final.tipo_stock_final,
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
                registro_guardar(comprobante_pi, self.request)
                comprobante_pi.save()
                self.request.session['primero'] = False
            return super().form_valid(form)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        self.request.session['primero'] = True
        context = super(RecepcionComprobanteCompraPIView, self).get_context_data(**kwargs)
        context['accion'] = "Recibir"
        context['titulo'] = "Comprobante de Compra"
        return context


class ComprobanteCompraCIRegistrarView(PermissionRequiredMixin, BSModalFormView):
    permission_required = ('comprobante_compra.add_comprobantecompraci')
    template_name = "includes/formulario generico.html"
    form_class = ComprobanteCompraCIForm
    
    def get_success_url(self, **kwargs):
        return reverse_lazy('comprobante_compra_app:comprobante_compra_ci_detalle', kwargs={'slug':self.kwargs['slug']})

    @transaction.atomic
    def form_valid(self, form):
        sid = transaction.savepoint()
        try:
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
                        descripcion = detalle.descripcion_proveedor,
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
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        self.request.session['primero'] = True
        context = super(ComprobanteCompraCIRegistrarView, self).get_context_data(**kwargs)
        context['accion'] = "Recibir"
        context['titulo'] = "Comprobante de Compra"
        return context


class ComprobanteCompraCIDetailView(PermissionRequiredMixin, DetailView):
    permission_required = ('comprobante_compra.view_comprobantecompraci')
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


class ComprobanteCompraCITraduccionView(PermissionRequiredMixin, DetailView):
    permission_required = ('comprobante_compra.view_comprobantecompraci')
    model = ComprobanteCompraCI
    template_name = "comprobante_compra/comprobante_compra_ci/traduccion.html"
    context_object_name = 'contexto_comprobante_compra_ci'

    def get_context_data(self, **kwargs):
        context = super(ComprobanteCompraCITraduccionView, self).get_context_data(**kwargs)
        context['materiales'] = ComprobanteCompraCIDetalle.objects.ver_detalle(self.get_object())
        return context
    

class ComprobanteCompraCIDetalleUpdateView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('oferta_proveedor.change_comprobantecompraci')

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
        context['valor_igv'] = igv()
        return context


class ComprobanteCompraCIFinalizarView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('oferta_proveedor.change_comprobantecompraci')
    model = ComprobanteCompraCI
    template_name = "includes/eliminar generico.html"
    context_object_name = 'contexto_comprobante_compra_ci'

    # def dispatch(self, request, *args, **kwargs):
    #     if not self.has_permission():
    #         return render(request, 'includes/modal sin permiso.html')
    #     return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('comprobante_compra_app:comprobante_compra_ci_detalle', kwargs={'slug':self.get_object().slug})

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            self.object = self.get_object()
            self.object.estado = 2
            registro_guardar(self.object, self.request)
            self.object.save()
            messages.success(request, MENSAJE_COMPROBANTE_COMPRA)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(ComprobanteCompraCIFinalizarView, self).get_context_data(**kwargs)
        context['accion'] = "Finalizar"
        context['titulo'] = "Comprobante"
        context['dar_baja'] = "true"
        context['item'] = self.object.numero_comprobante_compra
        return context