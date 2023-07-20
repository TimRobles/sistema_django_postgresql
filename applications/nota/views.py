from decimal import Decimal
from applications.almacenes.models import Almacen
from applications.clientes.models import Cliente
from applications.cobranza.funciones import eliminarNota, generarNota
from applications.comprobante_venta.funciones import anular_nubefact, consultar_documento, nota_credito_nubefact
from applications.comprobante_venta.models import BoletaVenta, FacturaVenta
from applications.datos_globales.models import DocumentoFisico, NubefactRespuesta, SeriesComprobante, TipoCambio
from applications.importaciones import *
from django.core.paginator import Paginator
from applications.movimiento_almacen.models import MovimientosAlmacen, TipoMovimiento
from applications.nota.forms import NotaCreditoAnularForm, NotaCreditoBuscarForm, NotaCreditoCrearForm, NotaCreditoDescripcionForm, NotaCreditoDetalleForm, NotaCreditoMaterialDetalleForm, NotaCreditoObservacionForm, NotaCreditoSerieForm, NotaCreditoTipoForm
from applications.nota.models import NotaCredito, NotaCreditoDetalle, NotaDevolucion, NotaDevolucionDetalle
from applications.funciones import calculos_linea, igv, numeroXn, obtener_totales, registrar_excepcion, slug_aleatorio, tipo_de_cambio


class NotaCreditoView(PermissionRequiredMixin, FormView):
    permission_required = ('nota.view_notacredito')
    template_name = "notas/nota_credito/inicio.html"
    form_class = NotaCreditoBuscarForm
    success_url = '.'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['filtro_cliente'] = self.request.GET.get('cliente')
        kwargs['filtro_numero_nota'] = self.request.GET.get('numero_nota')
        kwargs['filtro_sociedad'] = self.request.GET.get('sociedad')
        kwargs['filtro_tipo_nota_credito'] = self.request.GET.get('tipo_nota_credito')
        kwargs['filtro_fecha'] = self.request.GET.get('fecha')
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(NotaCreditoView, self).get_context_data(**kwargs)
        notas_credito = NotaCredito.objects.all()

        filtro_cliente = self.request.GET.get('cliente')
        filtro_numero_nota = self.request.GET.get('numero_nota')
        filtro_sociedad = self.request.GET.get('sociedad')
        filtro_tipo_nota_credito = self.request.GET.get('tipo_nota_credito')
        filtro_fecha = self.request.GET.get('fecha')

        contexto_filtro = []

        if filtro_cliente:
            condicion = Q(cliente__razon_social__unaccent__icontains = filtro_cliente.split(" ")[0])
            for palabra in filtro_cliente.split(" ")[1:]:
                condicion &= Q(cliente__razon_social__unaccent__icontains = palabra)
            notas_credito = notas_credito.filter(condicion)
            contexto_filtro.append("cliente=" + filtro_cliente)

        if filtro_numero_nota:
            condicion = Q(numero_nota__unaccent__icontains = filtro_numero_nota)
            notas_credito = notas_credito.filter(condicion)
            contexto_filtro.append("numero_nota=" + filtro_cliente)

        if filtro_fecha:
            condicion = Q(fecha_cotizacion = datetime.strptime(filtro_fecha, "%Y-%m-%d").date())
            notas_credito = notas_credito.filter(condicion)
            contexto_filtro.append("fecha=" + filtro_fecha)

        if filtro_sociedad:
            condicion = Q(sociedad__id = filtro_sociedad)
            notas_credito = notas_credito.filter(condicion)
            contexto_filtro.append("sociedad=" + filtro_sociedad)

        if filtro_tipo_nota_credito:
            condicion = Q(tipo_nota_credito = int(filtro_tipo_nota_credito))
            notas_credito = notas_credito.filter(condicion)
            contexto_filtro.append("tipo_nota_credito=" + filtro_tipo_nota_credito)

        context['contexto_filtro'] = "&".join(contexto_filtro)

        context['pagina_filtro'] = ""
        if self.request.GET.get('page'):
            if context['contexto_filtro']:
                context['pagina_filtro'] = f'&page={self.request.GET.get("page")}'
            else:
                context['pagina_filtro'] = f'page={self.request.GET.get("page")}'
        context['contexto_filtro'] = '?' + context['contexto_filtro']

        objectsxpage =  10 # Show 10 objects per page.

        if len(notas_credito) > objectsxpage:
            paginator = Paginator(notas_credito, objectsxpage)
            page_number = self.request.GET.get('page')
            notas_credito = paginator.get_page(page_number)
   
        context['contexto_pagina'] = notas_credito
        context['contexto_nota_credito'] = notas_credito
        
        return context 


def NotaCreditoTabla(request):
    data = dict()
    if request.method == 'GET':
        template = 'notas/nota_credito/inicio_tabla.html'
        context = {}
        notas_credito = NotaCredito.objects.all()

        filtro_cliente = request.GET.get('cliente')
        filtro_numero_nota = request.GET.get('numero_nota')
        filtro_sociedad = request.GET.get('sociedad')
        filtro_tipo_nota_credito = request.GET.get('tipo_nota_credito')
        filtro_fecha = request.GET.get('fecha')

        contexto_filtro = []

        if filtro_cliente:
            condicion = Q(cliente__razon_social__unaccent__icontains = filtro_cliente.split(" ")[0])
            for palabra in filtro_cliente.split(" ")[1:]:
                condicion &= Q(cliente__razon_social__unaccent__icontains = palabra)
            notas_credito = notas_credito.filter(condicion)
            contexto_filtro.append("cliente=" + filtro_cliente)

        if filtro_numero_nota:
            condicion = Q(numero_nota__unaccent__icontains = filtro_numero_nota)
            notas_credito = notas_credito.filter(condicion)
            contexto_filtro.append("numero_nota=" + filtro_cliente)

        if filtro_fecha:
            condicion = Q(fecha_cotizacion = datetime.strptime(filtro_fecha, "%Y-%m-%d").date())
            notas_credito = notas_credito.filter(condicion)
            contexto_filtro.append("fecha=" + filtro_fecha)

        if filtro_sociedad:
            condicion = Q(sociedad__id = filtro_sociedad)
            notas_credito = notas_credito.filter(condicion)
            contexto_filtro.append("sociedad=" + filtro_sociedad)

        if filtro_tipo_nota_credito:
            condicion = Q(tipo_nota_credito__id = int(filtro_tipo_nota_credito))
            notas_credito = notas_credito.filter(condicion)
            contexto_filtro.append("tipo_nota_credito=" + filtro_tipo_nota_credito)

        context['contexto_filtro'] = "&".join(contexto_filtro)

        context['pagina_filtro'] = ""
        if request.GET.get('page'):
            if context['contexto_filtro']:
                context['pagina_filtro'] = f'&page={request.GET.get("page")}'
            else:
                context['pagina_filtro'] = f'page={request.GET.get("page")}'
        context['contexto_filtro'] = '?' + context['contexto_filtro']

        objectsxpage =  10 # Show 10 objects per page.

        if len(notas_credito) > objectsxpage:
            paginator = Paginator(notas_credito, objectsxpage)
            page_number = request.GET.get('page')
            notas_credito = paginator.get_page(page_number)
   
        context['contexto_pagina'] = notas_credito
        context['contexto_nota_credito'] = notas_credito
        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)


class NotaCreditoDetailView(PermissionRequiredMixin, DetailView):
    permission_required = ('nota.view_notacredito')
    model = NotaCredito
    template_name = "notas/nota_credito/detalle.html"
    context_object_name = 'contexto_nota_credito'

    def get_context_data(self, **kwargs):
        nota_credito = self.object
        tipo_cambio_hoy = TipoCambio.objects.tipo_cambio_venta(date.today())
        if nota_credito.tipo_cambio:
            tipo_cambio = nota_credito.tipo_cambio.tipo_cambio_venta
        else:
            tipo_cambio = Decimal('1.00')
        context = super(NotaCreditoDetailView, self).get_context_data(**kwargs)
        context['materiales'] = NotaCredito.objects.ver_detalle(nota_credito.id)
        context['tipo_cambio_hoy'] = tipo_cambio_hoy
        context['tipo_cambio'] = tipo_cambio
        tipo_cambio = tipo_de_cambio(tipo_cambio, tipo_cambio_hoy)
        context['totales'] = obtener_totales(nota_credito)
        if nota_credito.serie_comprobante:
            context['nubefact_acceso'] = nota_credito.serie_comprobante.NubefactSerieAcceso_serie_comprobante.acceder(nota_credito.sociedad, ContentType.objects.get_for_model(nota_credito))
        url_nubefact = NubefactRespuesta.objects.respuesta(nota_credito)
        if url_nubefact:
            context['url_nubefact'] = url_nubefact
        if nota_credito.nubefact:
            context['url_nubefact'] = nota_credito.nubefact
        context['respuestas_nubefact'] = NubefactRespuesta.objects.respuestas(nota_credito)
        permiso_logistica = False
        if 'nota.add_notadevolucion' in self.request.user.get_all_permissions():
            permiso_logistica = True
        context['permiso_logistica'] = permiso_logistica
        return context


def NotaCreditoDetailTabla(request, id):
    data = dict()
    if request.method == 'GET':
        template = 'notas/nota_credito/detalle_tabla.html'
        context = {}
        nota_credito = NotaCredito.objects.get(id = id)
        tipo_cambio_hoy = TipoCambio.objects.tipo_cambio_venta(date.today())
        if nota_credito.tipo_cambio:
            tipo_cambio = nota_credito.tipo_cambio.tipo_cambio_venta
        else:
            tipo_cambio = Decimal('1.00')
        context['materiales'] = NotaCredito.objects.ver_detalle(nota_credito.id)
        context['tipo_cambio_hoy'] = tipo_cambio_hoy
        context['tipo_cambio'] = tipo_cambio
        tipo_cambio = tipo_de_cambio(tipo_cambio, tipo_cambio_hoy)
        context['totales'] = obtener_totales(nota_credito)
        if nota_credito.serie_comprobante:
            context['nubefact_acceso'] = nota_credito.serie_comprobante.NubefactSerieAcceso_serie_comprobante.acceder(nota_credito.sociedad, ContentType.objects.get_for_model(nota_credito))
        url_nubefact = NubefactRespuesta.objects.respuesta(nota_credito)
        if url_nubefact:
            context['url_nubefact'] = url_nubefact
        if nota_credito.nubefact:
            context['url_nubefact'] = nota_credito.nubefact
        context['respuestas_nubefact'] = NubefactRespuesta.objects.respuestas(nota_credito)
        context['contexto_nota_credito'] = nota_credito
        permiso_logistica = False
        if 'nota.add_notadevolucion' in request.user.get_all_permissions():
            permiso_logistica = True
        context['permiso_logistica'] = permiso_logistica
        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)


class NotaCreditoCreateView(PermissionRequiredMixin, BSModalFormView):
    permission_required = ('nota.add_notacredito')
    template_name = "notas/nota_credito/crear.html"
    form_class = NotaCreditoCrearForm

    def get_success_url(self):
        return reverse_lazy('nota_app:nota_credito_inicio')

    @transaction.atomic
    def form_valid(self, form):
        sid = transaction.savepoint()
        try:
            if self.request.session['primero']:
                factura_id = form.cleaned_data.get('factura')
                boleta_id = form.cleaned_data.get('boleta')
                if factura_id:
                    factura = FacturaVenta.objects.get(id=factura_id)
                    serie_comprobante = SeriesComprobante.objects.get(
                        tipo_comprobante=ContentType.objects.get_for_model(NotaCredito),
                        serie=factura.serie_comprobante.serie,
                    )
                    # numero_nota = 0
                    # if NotaCredito.objects.filter(sociedad=factura.sociedad, serie_comprobante=serie_comprobante,):
                    #     numero_nota = NotaCredito.objects.filter(sociedad=factura.sociedad, serie_comprobante=serie_comprobante,).aggregate(Max('numero_nota'))['numero_nota__max']
                    # numero_nota = numero_nota + 1
                    nota_credito = NotaCredito.objects.create(
                        sociedad=factura.sociedad,
                        serie_comprobante=serie_comprobante,
                        # numero_nota=numero_nota,
                        cliente=factura.cliente,
                        cliente_interlocutor=factura.cliente_interlocutor,
                        moneda=factura.moneda,
                        tipo_cambio=factura.tipo_cambio,
                        content_type_documento=DocumentoFisico.objects.get(modelo=ContentType.objects.get_for_model(FacturaVenta)),
                        id_registro_documento=factura.id,
                        slug=slug_aleatorio(NotaCredito),
                        created_by=self.request.user,
                        updated_by=self.request.user,
                    )
                    for detalle in factura.detalles:
                        calculo = calculos_linea(detalle.cantidad, detalle.precio_final_con_igv, detalle.precio_final_con_igv, igv(), detalle.tipo_igv)
                        nota_credito_detalle = NotaCreditoDetalle.objects.create(
                            item=detalle.item,
                            content_type=detalle.content_type,
                            id_registro=detalle.id_registro,
                            unidad=detalle.unidad,
                            descripcion_documento=detalle.descripcion_documento,
                            cantidad=detalle.cantidad,
                            precio_unitario_sin_igv=calculo['precio_unitario_sin_igv'],
                            precio_unitario_con_igv=detalle.precio_final_con_igv,
                            precio_final_con_igv=detalle.precio_final_con_igv,
                            descuento=calculo['descuento'],
                            sub_total=calculo['subtotal'],
                            tipo_igv=calculo['tipo_igv'],
                            igv=calculo['igv'],
                            total=calculo['total'],
                            codigo_producto_sunat=detalle.codigo_producto_sunat,
                            nota_credito=nota_credito,
                            created_by=self.request.user,
                            updated_by=self.request.user,
                        )

                if boleta_id:
                    boleta = BoletaVenta.objects.get(id=boleta_id)
                    serie_comprobante = SeriesComprobante.objects.get(
                        tipo_comprobante=ContentType.objects.get_for_model(NotaCredito),
                        serie=boleta.serie_comprobante.serie,
                    )
                    # numero_nota = 0
                    # if NotaCredito.objects.filter(sociedad=boleta.sociedad, serie_comprobante=serie_comprobante,):
                    #     numero_nota = NotaCredito.objects.filter(sociedad=boleta.sociedad, serie_comprobante=serie_comprobante,).aggregate(Max('numero_nota'))['numero_nota__max']
                    # numero_nota = numero_nota + 1
                    nota_credito = NotaCredito.objects.create(
                        sociedad=boleta.sociedad,
                        serie_comprobante=serie_comprobante,
                        # numero_nota=numero_nota,
                        cliente=boleta.cliente,
                        cliente_interlocutor=boleta.cliente_interlocutor,
                        moneda=boleta.moneda,
                        tipo_cambio=boleta.tipo_cambio,
                        content_type_documento=DocumentoFisico.objects.get(modelo=ContentType.objects.get_for_model(BoletaVenta)),
                        id_registro_documento=boleta.id,
                        slug=slug_aleatorio(NotaCredito),
                        created_by=self.request.user,
                        updated_by=self.request.user,
                    )
                    for detalle in boleta.detalles:
                        calculo = calculos_linea(detalle.cantidad, detalle.precio_final_con_igv, detalle.precio_final_con_igv, igv(), detalle.tipo_igv)
                        nota_credito_detalle = NotaCreditoDetalle.objects.create(
                            item=detalle.item,
                            content_type=detalle.content_type,
                            id_registro=detalle.id_registro,
                            unidad=detalle.unidad,
                            descripcion_documento=detalle.descripcion_documento,
                            cantidad=detalle.cantidad,
                            precio_unitario_sin_igv=calculo['precio_unitario_sin_igv'],
                            precio_unitario_con_igv=detalle.precio_final_con_igv,
                            precio_final_con_igv=detalle.precio_final_con_igv,
                            descuento=calculo['descuento'],
                            sub_total=calculo['subtotal'],
                            tipo_igv=calculo['tipo_igv'],
                            igv=calculo['igv'],
                            total=calculo['total'],
                            codigo_producto_sunat=detalle.codigo_producto_sunat,
                            nota_credito=nota_credito,
                            created_by=self.request.user,
                            updated_by=self.request.user,
                        )
                self.request.session['primero'] = False
                return super().form_valid(form)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        self.request.session['primero'] = True
        context = super(NotaCreditoCreateView, self).get_context_data(**kwargs)
        context['accion'] = 'Seleccionar'
        context['titulo'] = 'Comprobante de Venta'
        return context


class NotaCreditoDeleteView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('nota.delete_notacredito')
    model = NotaCredito
    template_name = "includes/eliminar generico.html"
    success_url = reverse_lazy('nota_app:nota_credito_inicio')

    def get_context_data(self, **kwargs):
        context = super(NotaCreditoDeleteView, self).get_context_data(**kwargs)
        context['accion'] = 'Eliminar'
        context['titulo'] = 'Nota de Crédito'
        context['item'] = self.get_object()
        return context
    

class NotaCreditoDireccionView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('clientes.change_cliente')
    model = Cliente
    template_name = "includes/form generico.html"

    def dispatch(self, request, *args, **kwargs):
        context = {}
        error_tipo_documento = False
        context['titulo'] = 'Error de dirección'
        if self.get_object().tipo_documento!='6':
            error_tipo_documento = True

        if error_tipo_documento:
            context['texto'] = 'El cliente debe tener RUC.'
            return render(request, 'includes/modal sin permiso.html', context)
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)
    
    def get_success_url(self, **kwargs):
        return reverse_lazy('nota_app:nota_credito_detalle', kwargs={'pk':self.kwargs['id_nota']})

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            cliente = self.get_object()
            consulta = cliente.consulta_direccion
            cliente.direccion_fiscal = consulta['direccion']
            cliente.ubigeo = consulta['ubigeo']
            cliente.save()
            messages.success(request, 'Operación exitosa: Dirección actualizada')
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(NotaCreditoDireccionView, self).get_context_data(**kwargs)
        context['accion'] = 'Actualizar'
        context['titulo'] = 'Dirección'
        context['texto'] = f'Dirección anterior: {self.get_object().direccion_anterior}'
        context['item'] = f'Nueva Dirección: {self.get_object().direccion_nueva}'
        return context


class NotaCreditoSerieUpdateView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('nota.change_notacredito')
    model = NotaCredito
    template_name = "includes/formulario generico.html"
    form_class = NotaCreditoSerieForm
    success_url = '.'
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(NotaCreditoSerieUpdateView, self).get_context_data(**kwargs)
        context['accion'] = 'Seleccionar'
        context['titulo'] = 'Serie'
        return context


class NotaCreditoTipoUpdateView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('nota.change_notacredito')
    model = NotaCredito
    template_name = "includes/formulario generico.html"
    form_class = NotaCreditoTipoForm
    success_url = '.'
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(NotaCreditoTipoUpdateView, self).get_context_data(**kwargs)
        context['accion'] = 'Seleccionar'
        context['titulo'] = 'Tipo'
        return context


class NotaCreditoGuardarView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('nota.change_notacredito')
    model = NotaCredito
    template_name = "includes/form generico.html"

    def dispatch(self, request, *args, **kwargs):
        context = {}
        error_tipo_cambio = False
        error_tipo_nota_credito = True
        context['titulo'] = 'Error de guardar'
        if len(TipoCambio.objects.filter(fecha=datetime.today()))==0:
            error_tipo_cambio = True
        if error_tipo_cambio:
            context['texto'] = 'Ingrese un tipo de cambio para hoy.'
            return render(request, 'includes/modal sin permiso.html', context)

        if self.get_object().tipo_nota_credito:
            error_tipo_nota_credito = False
        if error_tipo_nota_credito:
            context['texto'] = 'Ingrese un Tipo de Nota de Crédito.'
            return render(request, 'includes/modal sin permiso.html', context)

        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self) -> str:
        return reverse_lazy('nota_app:nota_credito_detalle', kwargs={'pk':self.kwargs['pk']})

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            obj = self.get_object()
            #Se necesita un documento anterior para generar el saldo a favor y el movimiento
            if not obj.tipo_nota_credito in TIPO_NOTA_CREDITO_SIN_NADA:
                generarNota(obj, self.request)
            # if obj.tipo_nota_credito in TIPO_NOTA_CREDITO_CON_DEVOLUCION:
            #     movimiento_final = TipoMovimiento.objects.get(codigo=159) #Devolución por Nota de Crédito
            #     for detalle in obj.detalles:
            #         movimiento_uno = MovimientosAlmacen.objects.create(
            #             content_type_producto = detalle.content_type,
            #             id_registro_producto = detalle.id_registro,
            #             cantidad = detalle.cantidad,
            #             tipo_movimiento = movimiento_final,
            #             tipo_stock = movimiento_final.tipo_stock_inicial,
            #             signo_factor_multiplicador = -1,
            #             content_type_documento_proceso = ContentType.objects.get_for_model(obj),
            #             id_registro_documento_proceso = obj.id,
            #             almacen = None,
            #             sociedad = obj.sociedad,
            #             movimiento_anterior = None,
            #             movimiento_reversion = False,
            #             created_by = self.request.user,
            #             updated_by = self.request.user,
            #         )
            #         movimiento_dos = MovimientosAlmacen.objects.create(
            #             content_type_producto = detalle.content_type,
            #             id_registro_producto = detalle.id_registro,
            #             cantidad = detalle.cantidad,
            #             tipo_movimiento = movimiento_final,
            #             tipo_stock = movimiento_final.tipo_stock_final,
            #             signo_factor_multiplicador = +1,
            #             content_type_documento_proceso = ContentType.objects.get_for_model(obj),
            #             id_registro_documento_proceso = obj.id,
            #             almacen = Almacen.objects.get(id=1),
            #             sociedad = obj.sociedad,
            #             movimiento_anterior = movimiento_uno,
            #             movimiento_reversion = False,
            #             created_by = self.request.user,
            #             updated_by = self.request.user,
            #         )
            obj.fecha_emision = date.today()
            obj.estado = 2
            obj.numero_nota = NotaCredito.objects.nuevo_numero(obj)
            registro_guardar(obj, self.request)
            obj.save()
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(NotaCreditoGuardarView, self).get_context_data(**kwargs)
        context['accion'] = 'Guardar'
        context['titulo'] = 'Nota de Crédito'
        context['texto'] = '¿Seguro de guardar la Nota de Crédito?'
        context['item'] = self.get_object()
        return context


class NotaCreditoAnularView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('comprobante_venta.change_facturaventa')
    model = NotaCredito
    template_name = "includes/form generico.html"
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self) -> str:
        return reverse_lazy('nota_app:nota_credito_detalle', kwargs={'pk':self.kwargs['pk']})

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            obj = self.get_object()
            eliminar = eliminarNota(obj)
            if eliminar:
                messages.success(self.request, MENSAJE_ELIMINAR_DEUDA)
            else:
                messages.warning(self.request, MENSAJE_ERROR_ELIMINAR_DEUDA)
            obj.estado = 3
            if obj.serie_comprobante.NubefactSerieAcceso_serie_comprobante.acceder(obj.sociedad, ContentType.objects.get_for_model(obj)) == 'MANUAL':
                obj.save()
                return HttpResponseRedirect(self.get_success_url())

            return super().delete(request, *args, **kwargs)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(NotaCreditoAnularView, self).get_context_data(**kwargs)
        obj = self.get_object()
        self.request.session['id_confirmacion'] = obj.confirmacion.id
        context['accion'] = 'Anular'
        context['titulo'] = 'Factura de Venta'
        context['texto'] = '¿Seguro de anular la Factura de Venta?'
        context['item'] = self.get_object()
        return context


class NotaCreditoObservacionUpdateView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('nota.change_notacredito')
    model = NotaCredito
    template_name = "includes/formulario generico.html"
    form_class = NotaCreditoObservacionForm

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self) -> str:
        return reverse_lazy('nota_app:nota_credito_detalle', kwargs={'pk':self.kwargs['pk']})

    def get_context_data(self, **kwargs):
        context = super(NotaCreditoObservacionUpdateView, self).get_context_data(**kwargs)
        context['titulo'] = "Observaciones"
        context['accion'] = "Actualizar"
        return context


class NotaCreditoNubeFactEnviarView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('nota.change_notacredito')
    model = NotaCredito
    template_name = "includes/form generico.html"

    def dispatch(self, request, *args, **kwargs):
        context = {}
        error_nubefact = False
        error_codigo_sunat = False
        context['titulo'] = 'Error de guardar'
        if self.get_object().serie_comprobante.NubefactSerieAcceso_serie_comprobante.acceder(self.get_object().sociedad, ContentType.objects.get_for_model(self.get_object())) == 'MANUAL':
            error_nubefact = True
        for detalle in self.get_object().NotaCreditoDetalle_nota_credito.all():
            if not detalle.codigo_producto_sunat:
                error_codigo_sunat = True

        if error_nubefact:
            context['texto'] = 'No hay una ruta para envío a NubeFact'
            return render(request, 'includes/modal sin permiso.html', context)
        if error_codigo_sunat:
            context['texto'] = 'Hay productos sin Código de Sunat'
            return render(request, 'includes/modal sin permiso.html', context)
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self) -> str:
        return reverse_lazy('nota_app:nota_credito_detalle', kwargs={'pk':self.kwargs['pk']})

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            obj = self.get_object()
            print(obj)
            respuesta = nota_credito_nubefact(obj, self.request.user)
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
        context = super(NotaCreditoNubeFactEnviarView, self).get_context_data(**kwargs)
        context['accion'] = 'Enviar'
        context['titulo'] = 'Nota de Crédito a NubeFact'
        context['texto'] = '¿Seguro de enviar la Nota de Crédito a NubeFact?'
        context['item'] = self.get_object()
        return context


class NotaCreditoNubeFactAnularView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('nota.change_notacredito')
    model = NotaCredito
    template_name = "includes/formulario generico.html"
    form_class = NotaCreditoAnularForm

    def dispatch(self, request, *args, **kwargs):
        context = {}
        error_fecha = False
        context['titulo'] = 'Error de guardar'
        if (date.today() - self.get_object().fecha_emision).days > 7:
            error_fecha = True

        if error_fecha:
            context['texto'] = 'No se puede anular, superó los 7 días.'
            return render(request, 'includes/modal sin permiso.html', context)
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self) -> str:
        return reverse_lazy('nota_app:nota_credito_detalle', kwargs={'pk':self.kwargs['pk']})

    @transaction.atomic
    def form_valid(self, form):
        sid = transaction.savepoint()
        try:
            respuesta = anular_nubefact(form.instance, self.request.user)
            if respuesta.error:
                form.instance.estado = 6
            else:
                form.instance.estado = 3
            registro_guardar(form.instance, self.request)
            eliminar = eliminarNota(form.instance)
            if eliminar:
                messages.success(self.request, MENSAJE_ELIMINAR_DEUDA)
            else:
                messages.warning(self.request, MENSAJE_ERROR_ELIMINAR_DEUDA)
            return super().form_valid(form)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(NotaCreditoNubeFactAnularView, self).get_context_data(**kwargs)
        context['accion'] = 'Anular'
        context['titulo'] = 'Nota de Crédito a NubeFact'
        return context


class NotaCreditoNubefactRespuestaDetailView(PermissionRequiredMixin, BSModalReadView):
    permission_required = ('nota.view_notacredito')
    model = NotaCredito
    template_name = "comprobante_venta/nubefact_respuesta.html"

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super(NotaCreditoNubefactRespuestaDetailView, self).get_context_data(**kwargs)
        context['titulo'] = 'Movimientos Nubefact'
        context['movimientos'] = NubefactRespuesta.objects.respuestas(self.get_object())
        return context


class NotaCreditoNubefactConsultarView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('nota.change_notacredito')
    model = NotaCredito
    template_name = "includes/form generico.html"
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self) -> str:
        return reverse_lazy('nota_app:nota_credito_detalle', kwargs={'pk':self.kwargs['pk']})

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            obj = self.get_object()
            respuesta = consultar_documento(obj, self.request.user)
            if respuesta.envio['operacion'] == 'consultar_anulacion':
                obj.estado = 3
            else:
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
        context = super(NotaCreditoNubefactConsultarView, self).get_context_data(**kwargs)
        context['accion'] = 'Consultar'
        context['titulo'] = 'Nota de Crédito a NubeFact'
        context['texto'] = '¿Seguro de consultar la Nota de Crédito a NubeFact?'
        context['item'] = self.get_object()
        return context

class NotaDevolucionListaView(PermissionRequiredMixin, DetailView):
    permission_required = ('nota.view_notadevolucion')
    model = NotaCredito
    template_name = "notas/nota_devolucion/lista.html"
    context_object_name = 'contexto_nota_credito'

    def get_context_data(self, **kwargs):
        nota_credito = self.object
        context = super(NotaDevolucionListaView, self).get_context_data(**kwargs)
        context['notas_devolucion'] = nota_credito.notas_devolucion
        return context

class NotaDevolucionDetailView(PermissionRequiredMixin, DetailView):
    permission_required = ('nota.view_notadevolucion')
    model = NotaDevolucion
    template_name = "notas/nota_devolucion/detalle.html"
    context_object_name = 'contexto_nota_devolucion'

    def get_context_data(self, **kwargs):
        nota_devolucion = self.object
        context = super(NotaDevolucionDetailView, self).get_context_data(**kwargs)
        context['materiales'] = NotaDevolucion.objects.ver_detalle(nota_devolucion.id)
        return context


def NotaDevolucionDetailTabla(request, id):
    data = dict()
    if request.method == 'GET':
        template = 'notas/nota_devolucion/detalle_tabla.html'
        context = {}
        nota_devolucion = NotaDevolucion.objects.get(id = id)
        context['materiales'] = NotaDevolucion.objects.ver_detalle(nota_devolucion.id)
        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)

class GenerarNotaDevolucionView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('nota.add_notadevolucion')
    model = NotaCredito
    template_name = "includes/eliminar generico.html"
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('nota_app:nota_devolucion_detalle', kwargs={'pk':self.nota_devolucion.id})

    def delete(self, request, *args, **kwargs):
        item = len(NotaDevolucion.objects.all())
        if self.request.session['primero']:
            nota_credito = self.get_object()
            nota_devolucion = NotaDevolucion.objects.create(
                numero_devolucion=item + 1,
                content_type=ContentType.objects.get_for_model(nota_credito),
                id_registro=nota_credito.id,
                observaciones=nota_credito.observaciones,
                motivo_anulacion="",
                sociedad=nota_credito.sociedad,
                created_by=self.request.user,
                updated_by=self.request.user,
            )
            
            item = 0
            for detalle in nota_credito.detalles:
                item += 1
                NotaDevolucionDetalle.objects.create(
                    item=item,
                    content_type=detalle.content_type,
                    id_registro=detalle.id_registro,
                    cantidad_conteo=detalle.cantidad,
                    cliente=nota_credito.cliente,
                    almacen=None,
                    nota_devolucion=nota_devolucion,
                    created_by=self.request.user,
                    updated_by=self.request.user,
                )
                

            self.request.session['primero'] = False
            messages.success(request, MENSAJE_GENERAR_NOTA_DEVOLUCION)
        self.nota_devolucion = nota_devolucion
        return HttpResponseRedirect(reverse_lazy('nota_app:nota_devolucion_detalle', kwargs={'pk': nota_devolucion.id}))

    def get_context_data(self, **kwargs):
        self.request.session['primero'] = True
        context = super(GenerarNotaDevolucionView, self).get_context_data(**kwargs)
        context['accion'] = "Generar"
        context['titulo'] = "Nota Devolución"
        context['dar_baja'] = "true"
        return context


class FinalizarNotaDevolucionView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('nota.add_notadevolucion')
    model = NotaDevolucion
    template_name = "includes/eliminar generico.html"
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('nota_app:nota_devolucion_detalle', kwargs={'pk':self.nota_devolucion.id})

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            if self.request.session['primero']:
                nota_devolucion = self.get_object()
                movimiento_final = TipoMovimiento.objects.get(codigo=159) #Devolución por Nota de Crédito
                for detalle in nota_devolucion.detalles:
                    movimiento_uno = MovimientosAlmacen.objects.create(
                        content_type_producto = detalle.content_type,
                        id_registro_producto = detalle.id_registro,
                        cantidad = detalle.cantidad,
                        tipo_movimiento = movimiento_final,
                        tipo_stock = movimiento_final.tipo_stock_inicial,
                        signo_factor_multiplicador = -1,
                        content_type_documento_proceso = ContentType.objects.get_for_model(nota_devolucion),
                        id_registro_documento_proceso = nota_devolucion.id,
                        almacen = None,
                        sociedad = nota_devolucion.sociedad,
                        movimiento_anterior = None,
                        movimiento_reversion = False,
                        created_by = self.request.user,
                        updated_by = self.request.user,
                    )
                    movimiento_dos = MovimientosAlmacen.objects.create(
                        content_type_producto = detalle.content_type,
                        id_registro_producto = detalle.id_registro,
                        cantidad = detalle.cantidad,
                        tipo_movimiento = movimiento_final,
                        tipo_stock = movimiento_final.tipo_stock_final,
                        signo_factor_multiplicador = +1,
                        content_type_documento_proceso = ContentType.objects.get_for_model(nota_devolucion),
                        id_registro_documento_proceso = nota_devolucion.id,
                        almacen = detalle.almacen,
                        sociedad = nota_devolucion.sociedad,
                        movimiento_anterior = movimiento_uno,
                        movimiento_reversion = False,
                        created_by = self.request.user,
                        updated_by = self.request.user,
                    )
                    

                self.request.session['primero'] = False
                registro_guardar(self.object, self.request)
                self.object.save()
                messages.success(request, MENSAJE_GENERAR_NOTA_DEVOLUCION)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        self.nota_devolucion = nota_devolucion
        return HttpResponseRedirect(reverse_lazy('nota_app:nota_devolucion_detalle', kwargs={'pk': nota_devolucion.id}))

    def get_context_data(self, **kwargs):
        self.request.session['primero'] = True
        context = super(FinalizarNotaDevolucionView, self).get_context_data(**kwargs)
        context['accion'] = "Finalizar"
        context['titulo'] = "Nota Devolución"
        context['dar_baja'] = "true"
        return context


class NotaCreditoDetalleUpdateView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('nota.change_notacredito')
    model = NotaCreditoDetalle
    template_name = "includes/formulario generico.html"
    form_class = NotaCreditoDetalleForm
    success_url = '.'

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        respuesta = calculos_linea(form.instance.cantidad, form.instance.precio_final_con_igv, form.instance.precio_final_con_igv, igv(), form.instance.tipo_igv)
        form.instance.precio_unitario_sin_igv = respuesta['precio_unitario_sin_igv']
        form.instance.precio_unitario_con_igv = form.instance.precio_final_con_igv
        form.instance.precio_final_con_igv = form.instance.precio_final_con_igv
        form.instance.descuento = respuesta['descuento']
        form.instance.sub_total = respuesta['subtotal']
        form.instance.igv = respuesta['igv']
        form.instance.total = respuesta['total']
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(NotaCreditoDetalleUpdateView, self).get_context_data(**kwargs)
        context['accion'] = 'Actualizar'
        context['titulo'] = 'Item'
        return context


class NotaCreditoDescripcionUpdateView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('nota.change_notacredito')
    model = NotaCreditoDetalle
    template_name = "includes/formulario generico.html"
    form_class = NotaCreditoDescripcionForm
    success_url = '.'

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(NotaCreditoDescripcionUpdateView, self).get_context_data(**kwargs)
        context['accion'] = 'Actualizar'
        context['titulo'] = 'Descripción'
        return context


class NotaCreditoDetalleDeleteView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('nota.delete_notacredito')
    model = NotaCreditoDetalle
    template_name = "includes/eliminar generico.html"

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('nota_app:nota_credito_detalle', kwargs={'pk':self.get_object().nota_credito.id})
        
    def get_context_data(self, **kwargs):
        context = super(NotaCreditoDetalleDeleteView, self).get_context_data(**kwargs)
        context['accion'] = "Eliminar"
        context['titulo'] = "Material"
        context['item'] = self.get_object().producto

        return context


class NotaCreditoMaterialDetalleView(PermissionRequiredMixin, BSModalFormView):
    permission_required = ('nota.add_notacreditodetalle')
    template_name = "notas/nota_credito/form_material.html"
    form_class = NotaCreditoMaterialDetalleForm
    success_url = reverse_lazy('nota_app:nota_credito_inicio')

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        lista_materiales = []
        nota = NotaCredito.objects.get(id = self.kwargs['nota_id'])
        for detalle in nota.documento.detalles:
            lista_materiales.append(detalle.id_registro)
        kwargs['lista_materiales'] = lista_materiales

        return kwargs

    @transaction.atomic
    def form_valid(self, form):
        sid = transaction.savepoint()
        try:
            if self.request.session['primero']:
                nota = NotaCredito.objects.get(id = self.kwargs['nota_id'])
                item = len(NotaCreditoDetalle.objects.filter(nota_credito = nota))

                material = form.cleaned_data.get('material')
                cantidad = form.cleaned_data.get('cantidad')
                precio_lista = form.cleaned_data.get('precio_lista')
                print(material, cantidad, precio_lista)

                obj, created = NotaCreditoDetalle.objects.get_or_create(
                    content_type = ContentType.objects.get_for_model(material),
                    id_registro = material.id,
                    nota_credito = nota,
                )
                print(obj, created)
                if created:
                    obj.item = item + 1
                    obj.cantidad = cantidad
                    try:
                        precio_unitario_con_igv = precio_lista
                        precio_final_con_igv = precio_lista
                    except:
                        precio_unitario_con_igv = 0
                        precio_final_con_igv = 0

                    respuesta = calculos_linea(cantidad, precio_unitario_con_igv, precio_final_con_igv, igv(), 1)
                    obj.precio_unitario_sin_igv = respuesta['precio_unitario_sin_igv']
                    obj.precio_unitario_con_igv = precio_unitario_con_igv
                    obj.precio_final_con_igv = precio_final_con_igv
                    obj.sub_total = respuesta['subtotal']
                    obj.descuento = respuesta['descuento']
                    obj.igv = respuesta['igv']
                    obj.total = respuesta['total']
                    obj.codigo_producto_sunat = material.producto_sunat.codigo
                    obj.unidad = material.unidad_base
                    obj.descripcion_documento = material.descripcion_venta
                else:
                    precio_unitario_con_igv = precio_lista
                    precio_final_con_igv = precio_lista
                    obj.cantidad = obj.cantidad + cantidad
                    respuesta = calculos_linea(obj.cantidad, precio_unitario_con_igv, precio_final_con_igv, igv(), obj.tipo_igv)
                    obj.precio_unitario_sin_igv = respuesta['precio_unitario_sin_igv']
                    obj.precio_unitario_con_igv = precio_unitario_con_igv
                    obj.precio_final_con_igv = precio_final_con_igv
                    obj.sub_total = respuesta['subtotal']
                    obj.descuento = respuesta['descuento']
                    obj.igv = respuesta['igv']
                    obj.total = respuesta['total']
                    obj.codigo_producto_sunat = material.producto_sunat.codigo
                    obj.unidad = material.unidad_base
                    obj.descripcion_documento = material.descripcion_venta

                registro_guardar(obj, self.request)
                obj.save()

                self.request.session['primero'] = False
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.success_url)

    def get_context_data(self, **kwargs):
        self.request.session['primero'] = True
        context = super(NotaCreditoMaterialDetalleView, self).get_context_data(**kwargs)
        context['titulo'] = 'Material'
        context['accion'] = 'Agregar'
        return context