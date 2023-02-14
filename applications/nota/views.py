from decimal import Decimal
from applications.clientes.models import Cliente
from applications.comprobante_venta.models import FacturaVenta
from applications.datos_globales.models import DocumentoFisico, NubefactRespuesta, SeriesComprobante, TipoCambio
from applications.importaciones import *
from django.core.paginator import Paginator
from applications.nota.forms import NotaCreditoBuscarForm, NotaCreditoCrearForm
from applications.nota.models import NotaCredito, NotaCreditoDetalle
from applications.funciones import numeroXn, obtener_totales, registrar_excepcion, slug_aleatorio, tipo_de_cambio


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
        kwargs['filtro_fecha'] = self.request.GET.get('fecha')
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(NotaCreditoView, self).get_context_data(**kwargs)
        notas_credito = NotaCredito.objects.all()

        filtro_cliente = self.request.GET.get('cliente')
        filtro_numero_nota = self.request.GET.get('numero_nota')
        filtro_sociedad = self.request.GET.get('sociedad')
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
        context['matereriales'] = NotaCredito.objects.ver_detalle(nota_credito.id)
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
                    numero_nota = NotaCredito.objects.filter(sociedad=factura.sociedad, serie_comprobante=serie_comprobante,).aggregate(Max('numero_nota'))['numero_nota__max'] + 1
                    nota_credito = NotaCredito.objects.create(
                        sociedad=factura.sociedad,
                        serie_comprobante=serie_comprobante,
                        numero_nota=numero_nota,
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
                        nota_credito_detalle = NotaCreditoDetalle.objects.create(
                            item=detalle.item,
                            content_type=detalle.content_type,
                            id_registro=detalle.id_registro,
                            unidad=detalle.unidad,
                            descripcion_documento=detalle.descripcion_documento,
                            cantidad=detalle.cantidad,
                            precio_unitario_sin_igv=detalle.precio_unitario_sin_igv,
                            precio_unitario_con_igv=detalle.precio_unitario_con_igv,
                            precio_final_con_igv=detalle.precio_final_con_igv,
                            descuento=detalle.descuento,
                            sub_total=detalle.sub_total,
                            tipo_igv=detalle.tipo_igv,
                            igv=detalle.igv,
                            total=detalle.total,
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
        context['titulo'] = 'Serie'
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
        return reverse_lazy('comprobante_venta_app:boleta_venta_detalle', kwargs={'id_boleta_venta':self.kwargs['id_boleta']})

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