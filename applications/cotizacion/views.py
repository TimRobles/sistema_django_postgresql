from django.core.paginator import Paginator
from datetime import timedelta
from decimal import Decimal
from django.shortcuts import render
from django import forms
from applications.cobranza.models import SolicitudCredito, SolicitudCreditoCuota
from applications.comprobante_venta.models import FacturaVentaDetalle
from applications.home.templatetags.funciones_propias import nombre_usuario
from applications.importaciones import *
from applications.clientes.models import ClienteInterlocutor, InterlocutorCliente
from applications.datos_globales.models import CuentaBancariaSociedad, Moneda, TipoCambio
from applications.logistica.models import NotaSalida
from applications.material.funciones import calidad, en_camino, observacion, reservado, stock, stock_disponible, stock_vendible, vendible
from applications.movimiento_almacen.models import MovimientosAlmacen, TipoMovimiento
from applications.cotizacion.pdf import generarCotizacionVenta
from applications.funciones import calculos_linea, fecha_en_letras, igv, numeroXn, obtener_totales, obtener_totales_soles, registrar_excepcion, slug_aleatorio, tipo_de_cambio

from applications.sociedad.models import Sociedad

from applications.orden_compra.models import OrdenCompraDetalle
from applications.recepcion_compra.models import RecepcionCompra

from .forms import (
    ConfirmacionClienteForm,
    ConfirmacionOrdenCompraForm,
    ConfirmacionVentaBuscarForm,
    ConfirmacionVentaCuotaForm,
    ConfirmacionVentaFormaPagoForm,
    ConfirmacionVentaGenerarCuotasForm,
    CosteadorForm,
    CotizacionVentaBuscarForm,
    CotizacionVentaClienteForm,
    CotizacionVentaDescuentoGlobalForm,
    CotizacionVentaDetalleForm,
    CotizacionVentaForm,
    CotizacionVentaMaterialDetalleForm,
    CotizacionVentaMaterialDetalleUpdateForm,
    CotizacionVentaMaterialDetalleOfertaForm,
    CotizacionVentaObservacionForm,
    CotizacionVentaOtrosCargosForm,
    CotizacionVentaPdfsForm,
    CotizacionVentaVendedorForm,
    PrecioListaMaterialForm,
    SolicitudCreditoCuotaForm,
    SolicitudCreditoForm,
)

from .models import (
    ConfirmacionOrdenCompra,
    ConfirmacionVenta,
    ConfirmacionVentaCuota,
    ConfirmacionVentaDetalle,
    CotizacionDescuentoGlobal,
    CotizacionObservacion,
    CotizacionOtrosCargos,
    CotizacionSociedad,
    CotizacionTerminosCondiciones,
    CotizacionVenta,
    CotizacionVentaDetalle,
    PrecioListaMaterial,
)


class CotizacionVentaListView(PermissionRequiredMixin, FormView):
    permission_required = ('cotizacion.view_cotizacionventa')
    # model = CotizacionVenta
    template_name = 'cotizacion/cotizacion_venta/inicio.html'
    form_class = CotizacionVentaBuscarForm
    # context_object_name = 'contexto_cotizacion_venta'
    success_url = '.'

    def get_form_kwargs(self):
        kwargs = super(CotizacionVentaListView, self).get_form_kwargs()
        kwargs['filtro_cliente'] = self.request.GET.get('cliente')
        kwargs['filtro_vendedor'] = self.request.GET.get('vendedor')
        kwargs['filtro_fecha_cotizacion'] = self.request.GET.get('fecha_cotizacion')
        kwargs['filtro_fecha_validez'] = self.request.GET.get('fecha_validez')
        kwargs['vendedores'] = get_user_model().objects.filter(id__in = [cotizacion.vendedor.id for cotizacion in CotizacionVenta.objects.all()])
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(CotizacionVentaListView,self).get_context_data(**kwargs)
        cotizacion_ventas = CotizacionVenta.objects.all()

        filtro_cliente = self.request.GET.get('cliente')
        filtro_vendedor = self.request.GET.get('vendedor')
        filtro_fecha_cotizacion = self.request.GET.get('fecha_cotizacion')
        filtro_fecha_validez = self.request.GET.get('fecha_validez')

        contexto_filtro = []

        if filtro_cliente:
            condicion = Q(cliente__razon_social__unaccent__icontains = filtro_cliente.split(" ")[0])
            for palabra in filtro_cliente.split(" ")[1:]:
                condicion &= Q(cliente__razon_social__unaccent__icontains = palabra)
            cotizacion_ventas = cotizacion_ventas.filter(condicion)
            contexto_filtro.append("cliente=" + filtro_cliente)

        if filtro_fecha_cotizacion:
            condicion = Q(fecha_cotizacion = datetime.strptime(filtro_fecha_cotizacion, "%Y-%m-%d").date())
            cotizacion_ventas = cotizacion_ventas.filter(condicion)
            contexto_filtro.append("fecha_cotizacion=" + filtro_fecha_cotizacion)

        if filtro_fecha_validez:
            condicion = Q(fecha_validez = datetime.strptime(filtro_fecha_validez, "%Y-%m-%d").date())
            cotizacion_ventas = cotizacion_ventas.filter(condicion)
            contexto_filtro.append("fecha_validez=" + filtro_fecha_validez)

        if filtro_vendedor:
            condicion = Q(created_by__id = filtro_vendedor)
            cotizacion_ventas = cotizacion_ventas.filter(condicion)
            contexto_filtro.append("vendedor=" + filtro_vendedor)

        context['contexto_filtro'] = "&".join(contexto_filtro)

        context['pagina_filtro'] = ""
        if self.request.GET.get('page'):
            if context['contexto_filtro']:
                context['pagina_filtro'] = f'&page={self.request.GET.get("page")}'
            else:
                context['pagina_filtro'] = f'page={self.request.GET.get("page")}'
        context['contexto_filtro'] = '?' + context['contexto_filtro']

        objectsxpage =  15 # Show 10 objects per page.

        if len(cotizacion_ventas) > objectsxpage:
            paginator = Paginator(cotizacion_ventas, objectsxpage)
            page_number = self.request.GET.get('page')
            cotizacion_ventas = paginator.get_page(page_number)
   
        context['contexto_pagina'] = cotizacion_ventas

        return context


def CotizacionVentaTabla(request):
    data = dict()
    if request.method == 'GET':
        template = 'cotizacion/cotizacion_venta/inicio_tabla.html'
        context = {}
        cotizacion_ventas = CotizacionVenta.objects.all()
        filtro_cliente = request.GET.get('cliente')
        filtro_vendedor = request.GET.get('vendedor')
        filtro_fecha_cotizacion = request.GET.get('fecha_cotizacion')
        filtro_fecha_validez = request.GET.get('fecha_validez')

        contexto_filtro = []

        if filtro_cliente:
            condicion = Q(cliente__razon_social__unaccent__icontains = filtro_cliente.split(" ")[0])
            for palabra in filtro_cliente.split(" ")[1:]:
                condicion &= Q(cliente__razon_social__unaccent__icontains = palabra)
            cotizacion_ventas = cotizacion_ventas.filter(condicion)
            contexto_filtro.append("cliente=" + filtro_cliente)

        if filtro_fecha_cotizacion:
            condicion = Q(fecha_cotizacion = datetime.strptime(filtro_fecha_cotizacion, "%Y-%m-%d").date())
            cotizacion_ventas = cotizacion_ventas.filter(condicion)
            contexto_filtro.append("fecha_cotizacion=" + filtro_fecha_cotizacion)

        if filtro_fecha_validez:
            condicion = Q(fecha_validez = datetime.strptime(filtro_fecha_validez, "%Y-%m-%d").date())
            cotizacion_ventas = cotizacion_ventas.filter(condicion)
            contexto_filtro.append("fecha_validez=" + filtro_fecha_validez)

        if filtro_vendedor:
            condicion = Q(created_by__id = filtro_vendedor)
            cotizacion_ventas = cotizacion_ventas.filter(condicion)
            contexto_filtro.append("vendedor=" + filtro_vendedor)

        context['contexto_filtro'] = "&".join(contexto_filtro)

        context['pagina_filtro'] = ""
        if request.GET.get('page'):
            if context['contexto_filtro']:
                context['pagina_filtro'] = f'&page={request.GET.get("page")}'
            else:
                context['pagina_filtro'] = f'page={request.GET.get("page")}'
        context['contexto_filtro'] = '?' + context['contexto_filtro']

        objectsxpage =  15 # Show 10 objects per page.

        if len(cotizacion_ventas) > objectsxpage:
            paginator = Paginator(cotizacion_ventas, objectsxpage)
            page_number = request.GET.get('page')
            cotizacion_ventas = paginator.get_page(page_number)
   
        context['contexto_pagina'] = cotizacion_ventas

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)


def CotizacionVentaCreateView(request):
    obj = CotizacionVenta.objects.create(
        slug = slug_aleatorio(CotizacionVenta),
        moneda=Moneda.objects.get(principal=True),
        vendedor=request.user,
        created_by=request.user,
        updated_by=request.user,
    )
    obj.save()
    sociedades = Sociedad.objects.all()
    
    for sociedad in sociedades:
        obj2 = CotizacionDescuentoGlobal.objects.create(
            cotizacion_venta = obj,
            sociedad = sociedad,
        )
        obj3 = CotizacionObservacion.objects.create(
            cotizacion_venta = obj,
            sociedad = sociedad,
        )
        obj4 = CotizacionOtrosCargos.objects.create(
            cotizacion_venta = obj,
            sociedad = sociedad,
        )
    return HttpResponseRedirect(reverse_lazy('cotizacion_app:cotizacion_venta_ver', kwargs={'id_cotizacion':obj.id}))


class CotizacionVentaVerView(PermissionRequiredMixin, TemplateView):
    permission_required = ('cotizacion.view_cotizacionventa')
    template_name = "cotizacion/cotizacion_venta/detalle.html"

    def get_context_data(self, **kwargs):
        obj = CotizacionVenta.objects.get(id = kwargs['id_cotizacion'])

        try:
            if obj.SolicitudCredito_cotizacion_venta.estado == 3:
                credito_temporal = obj.SolicitudCredito_cotizacion_venta.total_credito
            else:
                credito_temporal = Decimal('0.00')
        except:
            credito_temporal = Decimal('0.00')
        
        if obj.cliente:
            disponible = obj.cliente.disponible_monto + credito_temporal
        else:
            disponible = Decimal('0.00')
        if disponible < 0:
            disponible = Decimal('0.00')

        tipo_cambio_hoy = TipoCambio.objects.tipo_cambio_venta(date.today())
        tipo_cambio = TipoCambio.objects.tipo_cambio_venta(obj.fecha_cotizacion)
        
        materiales = None
        try:
            materiales = obj.CotizacionVentaDetalle_cotizacion_venta.all()

            for material in materiales:
                material.material = material.content_type.get_object_for_this_type(id = material.id_registro)
        except:
            pass

        sociedades = Sociedad.objects.filter(estado_sunat=1)

        context = super(CotizacionVentaVerView, self).get_context_data(**kwargs)
        context['cotizacion'] = obj
        context['materiales'] = materiales
        context['tipo_cambio_hoy'] = tipo_cambio_hoy
        context['tipo_cambio'] = tipo_cambio
        context['totales'] = obtener_totales(CotizacionVenta.objects.get(id=self.kwargs['id_cotizacion']))
        tipo_cambio = tipo_de_cambio(tipo_cambio, tipo_cambio_hoy)
        context['totales_soles'] = obtener_totales_soles(context['totales'], tipo_cambio)
        context['sociedades'] = sociedades
        context['credito_temporal'] = credito_temporal
        context['disponible'] = disponible

        return context


def CotizacionVentaVerTabla(request, id_cotizacion):
    data = dict()
    if request.method == 'GET':
        template = 'cotizacion/cotizacion_venta/detalle_tabla.html'
        obj = CotizacionVenta.objects.get(id=id_cotizacion)

        try:
            if obj.SolicitudCredito_cotizacion_venta.estado == 3:
                credito_temporal = obj.SolicitudCredito_cotizacion_venta.total_credito
            else:
                credito_temporal = Decimal('0.00')
        except:
            credito_temporal = Decimal('0.00')
        
        if obj.cliente:
            disponible = obj.cliente.disponible_monto + credito_temporal
        else:
            disponible = Decimal('0.00')
        if disponible < 0:
            disponible = Decimal('0.00')

        tipo_cambio_hoy = TipoCambio.objects.tipo_cambio_venta(date.today())
        tipo_cambio = TipoCambio.objects.tipo_cambio_venta(obj.fecha_cotizacion)
        
        materiales = None
        try:
            materiales = obj.CotizacionVentaDetalle_cotizacion_venta.all()

            for material in materiales:
                material.material = material.content_type.get_object_for_this_type(id = material.id_registro)
        except:
            pass

        sociedades = Sociedad.objects.filter(estado_sunat=1)
        for sociedad in sociedades:
            sociedad.observacion = observacion(obj, sociedad)

        context = {}
        context['materiales'] = materiales
        context['cotizacion'] = obj
        context['tipo_cambio_hoy'] = tipo_cambio_hoy
        context['tipo_cambio'] = tipo_cambio
        context['totales'] = obtener_totales(obj)
        tipo_cambio = tipo_de_cambio(tipo_cambio, tipo_cambio_hoy)
        context['totales_soles'] = obtener_totales_soles(context['totales'], tipo_cambio)
        context['sociedades'] = sociedades
        context['credito_temporal'] = credito_temporal
        context['disponible'] = disponible

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)


class CotizacionVentaClienteView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('cotizacion.change_cotizacionventa')
    model = CotizacionVenta
    template_name = "cotizacion/cotizacion_venta/form_cliente.html"
    form_class = CotizacionVentaClienteForm
    success_url = reverse_lazy('cotizacion_app:cotizacion_venta_inicio')

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        cotizacion = kwargs['instance']
        lista = []
        relaciones = ClienteInterlocutor.objects.filter(cliente = cotizacion.cliente)
        for relacion in relaciones:
            lista.append(relacion.interlocutor.id)

        kwargs['interlocutor_queryset'] = InterlocutorCliente.objects.filter(id__in = lista)
        kwargs['interlocutor'] = cotizacion.cliente_interlocutor
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(CotizacionVentaClienteView, self).get_context_data(**kwargs)
        context['accion'] = "Elegir"
        context['titulo'] = "Cliente"
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


class CotizacionVentaMaterialDetalleView(PermissionRequiredMixin, BSModalFormView):
    permission_required = ('cotizacion.add_cotizacionventadetalle')
    template_name = "cotizacion/cotizacion_venta/form_material.html"
    form_class = CotizacionVentaMaterialDetalleForm
    success_url = reverse_lazy('cotizacion_app:cotizacion_venta_inicio')

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    @transaction.atomic
    def form_valid(self, form):
        sid = transaction.savepoint()
        try:
            if self.request.session['primero']:
                cotizacion = CotizacionVenta.objects.get(id = self.kwargs['cotizacion_id'])
                item = len(CotizacionVentaDetalle.objects.filter(cotizacion_venta = cotizacion))

                material = form.cleaned_data.get('material')
                cantidad = form.cleaned_data.get('cantidad')

                print(cotizacion, item, material, cantidad)

                buscar = CotizacionVentaDetalle.objects.filter(
                    content_type = ContentType.objects.get_for_model(material),
                    id_registro = material.id,
                    cotizacion_venta = cotizacion,
                )
                print(buscar)

                obj, created = CotizacionVentaDetalle.objects.get_or_create(
                    content_type = ContentType.objects.get_for_model(material),
                    id_registro = material.id,
                    cotizacion_venta = cotizacion,
                )
                print(obj, created)
                if created:
                    obj.item = item + 1
                    obj.cantidad = cantidad
                    try:
                        precio_unitario_con_igv = material.precio_lista.precio_lista
                        precio_final_con_igv = material.precio_lista.precio_lista
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
                else:
                    precio_unitario_con_igv = obj.precio_unitario_con_igv
                    precio_final_con_igv = obj.precio_final_con_igv
                    obj.cantidad = obj.cantidad + cantidad
                    respuesta = calculos_linea(obj.cantidad, precio_unitario_con_igv, precio_final_con_igv, igv(), obj.tipo_igv)
                    obj.precio_unitario_sin_igv = respuesta['precio_unitario_sin_igv']
                    obj.precio_unitario_con_igv = precio_unitario_con_igv
                    obj.precio_final_con_igv = precio_final_con_igv
                    obj.sub_total = respuesta['subtotal']
                    obj.descuento = respuesta['descuento']
                    obj.igv = respuesta['igv']
                    obj.total = respuesta['total']

                registro_guardar(obj, self.request)
                obj.save()

                cantidad_total = obj.cantidad
                cantidades = {}
                sociedades = Sociedad.objects.all()
                for sociedad in sociedades:
                    cantidades[sociedad.abreviatura] = stock_vendible(obj.content_type, obj.id_registro, sociedad.id)

                cantidades = dict(sorted(cantidades.items(), key=lambda kv: kv[1], reverse=True))

                for sociedad in sociedades:
                    obj2, created = CotizacionSociedad.objects.get_or_create(
                        cotizacion_venta_detalle = obj,
                        sociedad = sociedad,
                    )
                    if cantidades[sociedad.abreviatura] >= cantidad_total:
                        obj2.cantidad = cantidad_total
                        cantidad_total -= cantidad_total
                    else:
                        obj2.cantidad = cantidades[sociedad.abreviatura]
                        cantidad_total -= cantidades[sociedad.abreviatura]
                    obj2.save()

                self.request.session['primero'] = False
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.success_url)

    def get_context_data(self, **kwargs):
        self.request.session['primero'] = True
        context = super(CotizacionVentaMaterialDetalleView, self).get_context_data(**kwargs)
        context['titulo'] = 'Material'
        context['accion'] = 'Agregar'
        return context


class CotizacionSociedadUpdateView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('cotizacion.change_cotizacionventa')
    model = CotizacionVentaDetalle
    template_name = "cotizacion/cotizacion_venta/form_sociedad.html"
    form_class = CotizacionVentaDetalleForm
    success_url = '.'

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CotizacionSociedadUpdateView, self).get_context_data(**kwargs)
        texto = []
        for sociedad in self.object.CotizacionSociedad_cotizacion_venta_detalle.all():
            texto.append(str(sociedad.cantidad))

        sociedades = Sociedad.objects.all()
        for sociedad in sociedades:
            sociedad.vendible = vendible(self.object.content_type, self.object.id_registro, sociedad.id)
            sociedad.calidad = calidad(self.object.content_type, self.object.id_registro, sociedad.id)
            sociedad.reservado = reservado(self.object.content_type, self.object.id_registro, sociedad.id)
            sociedad.stock = stock(self.object.content_type, self.object.id_registro, sociedad.id)
            sociedad.en_camino = en_camino(self.object.content_type, self.object.id_registro, sociedad.id)

        context['titulo'] = "Stock por Sociedad"
        context['url_guardar'] = reverse_lazy('cotizacion_app:guardar_cotizacion_venta_sociedad', kwargs={'cantidad':1,'item':1,'abreviatura':"a",})[:-6]
        context['sociedades'] = sociedades
        context['cantidades'] = "|".join(texto)
        context['item'] = self.object.id
        return context


def GuardarCotizacionSociedad(request, cantidad, item, abreviatura):
    if cantidad == 1 and item == 1 and abreviatura == 'a':
        return HttpResponse('Nada')
    cotizacion_venta_detalle = CotizacionVentaDetalle.objects.get(id=item)
    sociedad = Sociedad.objects.get(abreviatura = abreviatura)

    obj, created = CotizacionSociedad.objects.get_or_create(
        cotizacion_venta_detalle = cotizacion_venta_detalle,
        sociedad = sociedad,
    )
    obj.cantidad = cantidad
    obj.save()
    return HttpResponse('Fin')


class CotizacionDescuentoGlobalUpdateView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('cotizacion.change_cotizacionventa')
    model = CotizacionVenta
    template_name = "cotizacion/cotizacion_venta/form_descuento.html"
    form_class = CotizacionVentaDescuentoGlobalForm
    success_url = '.'

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        respuesta = obtener_totales(form.instance)
        form.instance.total_descuento = respuesta['total_descuento']
        form.instance.total_anticipo = respuesta['total_anticipo']
        form.instance.total_gravada = respuesta['total_gravada']
        form.instance.total_inafecta = respuesta['total_inafecta']
        form.instance.total_exonerada = respuesta['total_exonerada']
        form.instance.total_igv = respuesta['total_igv']
        form.instance.total_gratuita = respuesta['total_gratuita']
        form.instance.total = respuesta['total']
        
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(CotizacionDescuentoGlobalUpdateView, self).get_context_data(**kwargs)
        texto = []
        for sociedad in self.object.CotizacionDescuentoGlobal_cotizacion_venta.all():
            texto.append(str(sociedad.descuento_global_cotizacion))

        context['titulo'] = "Actualizar Descuento Global"
        context['url_guardar'] = reverse_lazy('cotizacion_app:guardar_cotizacion_venta_descuento_global', kwargs={'monto':1,'id_cotizacion':1,'abreviatura':"a",})[:-6]
        context['sociedades'] = self.object.sociedades
        context['descuentos'] = "|".join(texto)
        context['id_cotizacion'] = self.object.id
        context['igv'] = igv()
        return context


def GuardarCotizacionDescuentoGlobal(request, monto, id_cotizacion, abreviatura):
    if monto == 1 and id_cotizacion == 1 and abreviatura == 'a':
        return HttpResponse('Nada')
    cotizacion_venta = CotizacionVenta.objects.get(id=id_cotizacion)
    sociedad = Sociedad.objects.get(abreviatura = abreviatura)

    obj, created = CotizacionDescuentoGlobal.objects.get_or_create(
        cotizacion_venta = cotizacion_venta,
        sociedad = sociedad,
    )
    obj.descuento_global_cotizacion = monto
    obj.save()
    return HttpResponse('Fin')


class CotizacionObservacionUpdateView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('cotizacion.change_cotizacionventa')
    model = CotizacionVenta
    template_name = "cotizacion/cotizacion_venta/form_observacion.html"
    form_class = CotizacionVentaObservacionForm
    success_url = '.'

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CotizacionObservacionUpdateView, self).get_context_data(**kwargs)
        texto = []
        for sociedad in self.object.sociedades:
            if sociedad['observaciones']:
                texto.append(str(sociedad['observaciones']))
            else:
                texto.append("")
        
        context['titulo'] = "Actualizar Observaciones"
        context['url_guardar'] = reverse_lazy('cotizacion_app:guardar_cotizacion_venta_observacion', kwargs={'texto':1,'id_cotizacion':1,'abreviatura':"a",})[:-6]
        context['sociedades'] = self.object.sociedades
        context['observaciones'] = "|".join(texto)
        context['id_cotizacion'] = self.object.id
        context['igv'] = igv()
        return context


def GuardarCotizacionObservacion(request, texto, id_cotizacion, abreviatura):
    if texto == 1 and id_cotizacion == 1 and abreviatura == 'a':
        return HttpResponse('Nada')
    cotizacion_venta = CotizacionVenta.objects.get(id=id_cotizacion)
    sociedad = Sociedad.objects.get(abreviatura = abreviatura)

    obj, created = CotizacionObservacion.objects.get_or_create(
        cotizacion_venta = cotizacion_venta,
        sociedad = sociedad,
    )
    if texto == 'null':
        obj.observacion = None
    else:
        obj.observacion = texto
    obj.save()
    return HttpResponse('Fin')


class CotizacionOtrosCargosUpdateView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('cotizacion.change_cotizacionventa')
    model = CotizacionVenta
    template_name = "cotizacion/cotizacion_venta/form_otros_cargos.html"
    form_class = CotizacionVentaOtrosCargosForm
    success_url = '.'

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        respuesta = obtener_totales(form.instance)
        form.instance.total_descuento = respuesta['total_descuento']
        form.instance.total_anticipo = respuesta['total_anticipo']
        form.instance.total_gravada = respuesta['total_gravada']
        form.instance.total_inafecta = respuesta['total_inafecta']
        form.instance.total_exonerada = respuesta['total_exonerada']
        form.instance.total_igv = respuesta['total_igv']
        form.instance.total_gratuita = respuesta['total_gratuita']
        form.instance.otros_cargos = respuesta['total_otros_cargos']
        form.instance.total = respuesta['total']
        
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(CotizacionOtrosCargosUpdateView, self).get_context_data(**kwargs)
        texto = []
        for sociedad in self.object.CotizacionOtrosCargos_cotizacion_venta.all():
            texto.append(str(sociedad.otros_cargos))

        context['titulo'] = "Actualizar Otros Cargos"
        context['url_guardar'] = reverse_lazy('cotizacion_app:guardar_cotizacion_venta_otros_cargos', kwargs={'monto':1,'id_cotizacion':1,'abreviatura':"a",})[:-6]
        context['sociedades'] = self.object.sociedades
        context['otros_cargos'] = "|".join(texto)
        context['id_cotizacion'] = self.object.id
        context['igv'] = igv()
        return context


def GuardarCotizacionOtrosCargos(request, monto, id_cotizacion, abreviatura):
    if monto == 1 and id_cotizacion == 1 and abreviatura == 'a':
        return HttpResponse('Nada')
    cotizacion_venta = CotizacionVenta.objects.get(id=id_cotizacion)
    sociedad = Sociedad.objects.get(abreviatura = abreviatura)

    obj, created = CotizacionOtrosCargos.objects.get_or_create(
        cotizacion_venta = cotizacion_venta,
        sociedad = sociedad,
    )
    obj.otros_cargos = monto
    obj.save()
    return HttpResponse('Fin')


class CotizacionVentaGuardarView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('cotizacion.change_cotizacionventa')
    model = CotizacionVenta
    template_name = "cotizacion/cotizacion_venta/form_guardar.html"

    def dispatch(self, request, *args, **kwargs):
        context = {}
        error_tipo_cambio = False
        context['titulo'] = 'Error de guardar'
        if len(TipoCambio.objects.filter(fecha=datetime.today()))==0:
            error_tipo_cambio = True

        if error_tipo_cambio:
            context['texto'] = 'Ingrese un tipo de cambio para hoy.'
            return render(request, 'includes/modal sin permiso.html', context)
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)
    
    def get_success_url(self, **kwargs):
        return reverse_lazy('cotizacion_app:cotizacion_venta_ver', kwargs={'id_cotizacion':self.object.id})

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            self.object = self.get_object()
            self.object.estado = 2
            numero_cotizacion = CotizacionVenta.objects.all().aggregate(Count('numero_cotizacion'))['numero_cotizacion__count'] + 1
            self.object.numero_cotizacion = numero_cotizacion
            self.object.fecha_cotizacion = datetime. now()
            self.object.fecha_validez = self.object.fecha_cotizacion + timedelta(7)

            registro_guardar(self.object, self.request)
            self.object.save()
            messages.success(request, MENSAJE_GUARDAR_COTIZACION)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(CotizacionVentaGuardarView, self).get_context_data(**kwargs)
        context['accion'] = "Guardar"
        context['titulo'] = "Cotización"
        context['guardar'] = "true"
        context['item'] = self.object.cliente
        return context


class CotizacionVentaCosteadorDetalleView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('cotizacion.change_cotizacionventa')
    model = CotizacionVentaDetalle
    template_name = "cotizacion/cotizacion_venta/form_precio.html"
    form_class = CosteadorForm
    success_url = '.'

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        if form.cleaned_data.get('precio_final') > form.instance.precio_unitario_con_igv:
            form.add_error('precio_final', 'El precio no puede ser mayor al precio de lista')
            return super().form_invalid(form)
        respuesta = calculos_linea(form.instance.cantidad, form.instance.precio_unitario_con_igv, form.cleaned_data.get('precio_final'), igv(), form.instance.tipo_igv)
        form.instance.precio_final_con_igv = form.cleaned_data.get('precio_final')
        form.instance.sub_total = respuesta['subtotal']
        form.instance.descuento = respuesta['descuento']
        form.instance.igv = respuesta['igv']
        form.instance.total = respuesta['total']
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        precios = []
        content_type = self.object.content_type
        id_registro = self.object.id_registro
        orden_detalle = OrdenCompraDetalle.objects.filter(
            content_type = content_type,
            id_registro = id_registro,
        )

        for detalle in orden_detalle:
            try:
                detalle.cantidad = detalle.ComprobanteCompraPIDetalle_orden_compra_detalle.cantidad
                detalle.precio = detalle.ComprobanteCompraPIDetalle_orden_compra_detalle.precio_final_con_igv

                comprobante_compra = detalle.ComprobanteCompraPIDetalle_orden_compra_detalle.comprobante_compra
            except:
                continue
            
            detalle.logistico = comprobante_compra.logistico
            
            try:
                recepcion = RecepcionCompra.objects.get(
                    content_type = ContentType.objects.get_for_model(comprobante_compra),
                    id_registro = comprobante_compra.id,
                    estado = 1,
                )

                detalle.fecha_recepcion = recepcion.fecha_recepcion
                detalle.numero_comprobante_compra = recepcion.numero_comprobante_compra
                valor = "%s|%s|%s|%s" % (comprobante_compra.id, ContentType.objects.get_for_model(comprobante_compra).id, self.object.id_registro, self.object.content_type.id)
                precios.append((valor, recepcion.numero_comprobante_compra))
            except:
                pass
        
        self.kwargs['precios'] = orden_detalle
        kwargs['precios'] = precios
        kwargs['precio_final'] = self.object.precio_final_con_igv
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(CotizacionVentaCosteadorDetalleView, self).get_context_data(**kwargs)
        context['accion']="Costeador"
        context['titulo']="Precio"
        context['precios'] = self.kwargs['precios']
        context['cotizaciones'] = CotizacionVentaDetalle.objects.filter(
            content_type=self.object.content_type,
            id_registro=self.object.id_registro,
        )
        context['documentos'] = FacturaVentaDetalle.objects.filter(
            content_type=self.object.content_type,
            id_registro=self.object.id_registro,
        )
        return context

class CotizacionVentaDetalleDeleteView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('cotizacion.delete_cotizacionventa')
    model = CotizacionVentaDetalle
    template_name = "includes/eliminar generico.html"

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('cotizacion_app:cotizacion_venta_ver', kwargs={'id_cotizacion':self.get_object().cotizacion_venta.id})

    def get_context_data(self, **kwargs):
        context = super(CotizacionVentaDetalleDeleteView, self).get_context_data(**kwargs)
        context['accion'] = "Eliminar"
        context['titulo'] = "Material"
        context['item'] = self.get_object().content_type.get_object_for_this_type(id = self.get_object().id_registro)

        return context


class CotizacionVentaMaterialDetalleUpdateView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('cotizacion.change_cotizacionventa')
    model = CotizacionVentaDetalle
    template_name = "cotizacion/cotizacion_venta/actualizar.html"
    form_class = CotizacionVentaMaterialDetalleUpdateForm

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('cotizacion_app:cotizacion_venta_ver', kwargs={'id_cotizacion':self.get_object().cotizacion_venta.id})

    @transaction.atomic
    def form_valid(self, form):
        sid = transaction.savepoint()
        try:
            precio_unitario_con_igv = form.instance.precio_unitario_con_igv
            precio_final_con_igv = form.instance.precio_final_con_igv
            form.instance.cantidad = form.instance.cantidad
            respuesta = calculos_linea(form.instance.cantidad, precio_unitario_con_igv, precio_final_con_igv, igv(), form.instance.tipo_igv)
            form.instance.precio_unitario_sin_igv = respuesta['precio_unitario_sin_igv']
            form.instance.precio_unitario_con_igv = precio_unitario_con_igv
            form.instance.precio_final_con_igv = precio_final_con_igv
            form.instance.sub_total = respuesta['subtotal']
            form.instance.descuento = respuesta['descuento']
            form.instance.igv = respuesta['igv']
            form.instance.total = respuesta['total']

            registro_guardar(form.instance, self.request)

            cantidad_total = form.instance.cantidad
            cantidades = {}
            sociedades = Sociedad.objects.all()
            for sociedad in sociedades:
                cantidades[sociedad.abreviatura] = stock_vendible(form.instance.content_type, form.instance.id_registro, sociedad.id)

            cantidades = dict(sorted(cantidades.items(), key=lambda kv: kv[1], reverse=True))

            for sociedad in sociedades:
                obj, created = CotizacionSociedad.objects.get_or_create(
                    cotizacion_venta_detalle = form.instance,
                    sociedad = sociedad,
                )
                if cantidades[sociedad.abreviatura] >= cantidad_total:
                    obj.cantidad = cantidad_total
                    cantidad_total -= cantidad_total
                else:
                    obj.cantidad = cantidades[sociedad.abreviatura]
                    cantidad_total -= cantidades[sociedad.abreviatura]
                obj.save()
            return super().form_valid(form)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(CotizacionVentaMaterialDetalleUpdateView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        context['titulo'] = "Precios"
        context['material'] = self.object.content_type.get_object_for_this_type(id = self.object.id_registro)
        return context


class CotizacionVentaMaterialDetalleOfertaView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('cotizacion.change_cotizacionventa')
    model = CotizacionVentaDetalle
    template_name = "cotizacion/cotizacion_venta/oferta.html"
    form_class = CotizacionVentaMaterialDetalleOfertaForm

    def dispatch(self, request, *args, **kwargs):
        print('Dispatch')
        error_oferta = False
        context = {}
        context['titulo'] = 'Error de Oferta'
        precio_oferta = self.get_object().producto.precio_oferta
        self.kwargs['precio_oferta'] = precio_oferta
        if not precio_oferta:
            error_oferta = True
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        if error_oferta:
            context['texto'] = 'El producto no está en oferta el día de hoy.'
            return render(request, 'includes/modal sin permiso.html', context)
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('cotizacion_app:cotizacion_venta_ver', kwargs={'id_cotizacion':self.get_object().cotizacion_venta.id})

    def get_form_kwargs(self):
        print('Kwargs')
        print(self.kwargs)
        kwargs = super().get_form_kwargs()
        kwargs['precio_lista'] = self.object.precio_unitario_con_igv
        kwargs['precio_oferta'] = self.kwargs['precio_oferta']
        return kwargs

    @transaction.atomic
    def form_valid(self, form):
        sid = transaction.savepoint()
        try:
            if self.request.session['primero']:
                if form.instance.en_oferta:
                    precio_unitario_con_igv = form.instance.precio_unitario_con_igv
                    precio_final_con_igv = precio_unitario_con_igv
                    respuesta = calculos_linea(form.instance.cantidad, precio_unitario_con_igv, precio_final_con_igv, igv(), form.instance.tipo_igv)
                    form.instance.precio_unitario_sin_igv = respuesta['precio_unitario_sin_igv']
                    form.instance.precio_unitario_con_igv = precio_unitario_con_igv
                    form.instance.precio_final_con_igv = precio_final_con_igv
                    form.instance.sub_total = respuesta['subtotal']
                    form.instance.descuento = respuesta['descuento']
                    form.instance.igv = respuesta['igv']
                    form.instance.total = respuesta['total']
                registro_guardar(form.instance, self.request)
                self.request.session['primero'] = False
            return super().form_valid(form)
        except Exception as ex:
            print(ex)
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        self.request.session['primero'] = True
        context = super(CotizacionVentaMaterialDetalleOfertaView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        context['titulo'] = "Precio de Oferta"
        context['material'] = self.object.content_type.get_object_for_this_type(id = self.object.id_registro)
        return context


class CotizacionVentaDeleteView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('cotizacion.delete_cotizacionventa')
    model = CotizacionVenta
    template_name = "includes/eliminar generico.html"
    success_url = reverse_lazy('cotizacion_app:cotizacion_venta_inicio')

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super(CotizacionVentaDeleteView, self).get_context_data(**kwargs)
        context['accion'] = "Eliminar"
        context['titulo'] = "Cotización"
        context['item'] = "Cotización %s - %s" % (numeroXn(self.object.numero_cotizacion, 6), self.object.cliente)
        return context
    

class CotizacionVentaAnularView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('cotizacion.change_cotizacionventa')
    model = CotizacionVenta
    template_name = "includes/form generico.html"

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('cotizacion_app:cotizacion_venta_ver', kwargs={'id_cotizacion':self.object.id})

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            self.object = self.get_object()
            self.object.estado = 9
            registro_guardar(self.object, self.request)
            self.object.save()

            messages.success(request, MENSAJE_ANULAR_COTIZACION)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(CotizacionVentaAnularView, self).get_context_data(**kwargs)
        context['accion'] = "Anular"
        context['titulo'] = "Cotización"
        context['texto'] = "¿Está seguro de Anular la cotización?"
        context['item'] = "Cotización %s - %s" % (numeroXn(self.object.numero_cotizacion, 6), self.object.cliente)
        return context


class CotizacionVentaClonarView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('cotizacion.add_cotizacionventa')
    model = CotizacionVenta
    template_name = "includes/form generico.html"

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('cotizacion_app:cotizacion_venta_ver', kwargs={'id_cotizacion':self.object.id})

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            self.object = self.get_object()
            detalles = self.object.CotizacionVentaDetalle_cotizacion_venta.all()
            descuento_globales = self.object.CotizacionDescuentoGlobal_cotizacion_venta.all()
            otros_cargos = self.object.CotizacionOtrosCargos_cotizacion_venta.all()
            observaciones = self.object.CotizacionObservacion_cotizacion_venta.all()
            nueva_cotizacion = CotizacionVenta.objects.create(
                cliente=self.object.cliente,
                cliente_interlocutor=self.object.cliente_interlocutor,
                moneda=self.object.moneda,
                total=self.object.total,
                slug = slug_aleatorio(CotizacionVenta),
                vendedor=self.request.user,
                created_by=self.request.user,
                updated_by=self.request.user,
            )
            
            for descuento_global in descuento_globales:
                CotizacionDescuentoGlobal.objects.create(
                    cotizacion_venta=nueva_cotizacion,
                    sociedad=descuento_global.sociedad,
                    descuento_global=descuento_global.descuento_global,
                    created_by=self.request.user,
                    updated_by=self.request.user,
                )
            
            for otro_cargo in otros_cargos:
                CotizacionOtrosCargos.objects.create(
                    cotizacion_venta=nueva_cotizacion,
                    sociedad=otro_cargo.sociedad,
                    otros_cargos=otro_cargo.otros_cargos,
                    created_by=self.request.user,
                    updated_by=self.request.user,
                )
            
            for observacion in observaciones:
                CotizacionObservacion.objects.create(
                    cotizacion_venta=nueva_cotizacion,
                    sociedad=observacion.sociedad,
                    observacion=observacion.observacion,
                    created_by=self.request.user,
                    updated_by=self.request.user,
                )

            for detalle in detalles:
                cotizacion_venta_detalle = CotizacionVentaDetalle.objects.create(
                    item=detalle.item,
                    content_type=detalle.content_type,
                    id_registro=detalle.id_registro,
                    cantidad=detalle.cantidad,
                    precio_unitario_sin_igv=detalle.precio_unitario_sin_igv,
                    precio_unitario_con_igv=detalle.precio_unitario_con_igv,
                    precio_final_con_igv=detalle.precio_final_con_igv,
                    descuento=detalle.descuento,
                    sub_total=detalle.sub_total,
                    igv=detalle.igv,
                    total=detalle.total,
                    tipo_igv=detalle.tipo_igv,
                    cotizacion_venta=nueva_cotizacion,
                    created_by=self.request.user,
                    updated_by=self.request.user,
                )
                cotizacion_sociedades = detalle.CotizacionSociedad_cotizacion_venta_detalle.all()
                for cotizacion_sociedad in cotizacion_sociedades:
                    CotizacionSociedad.objects.create(
                        cotizacion_venta_detalle=cotizacion_venta_detalle,
                        sociedad=cotizacion_sociedad.sociedad,
                        cantidad=cotizacion_sociedad.cantidad,
                        created_by=self.request.user,
                        updated_by=self.request.user,
                    )

            messages.success(request, MENSAJE_CLONAR_COTIZACION)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(CotizacionVentaClonarView, self).get_context_data(**kwargs)
        context['accion'] = "Clonar"
        context['titulo'] = "Cotización"
        context['texto'] = "¿Está seguro de Clonar la cotización?"
        context['item'] = "Cotización %s - %s" % (numeroXn(self.object.numero_cotizacion, 6), self.object.cliente)
        return context


class CotizacionVentaVendedorView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('cotizacion.change_cotizacionventa')
    model = CotizacionVenta
    template_name = "cotizacion/cotizacion_venta/form_cliente.html"
    form_class = CotizacionVentaVendedorForm
    success_url = reverse_lazy('cotizacion_app:cotizacion_venta_inicio')

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(CotizacionVentaVendedorView, self).get_context_data(**kwargs)
        context['accion'] = "Elegir"
        context['titulo'] = "Vendedor"
        return context


class CotizacionVentaReservaView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('cotizacion.change_cotizacionventa')
    model = CotizacionVenta
    template_name = "includes/form generico.html"

    def dispatch(self, request, *args, **kwargs):
        error_cantidad_sociedad = False
        context = {}
        context['titulo'] = 'Error de Reserva'
        for detalle in self.get_object().CotizacionVentaDetalle_cotizacion_venta.all():
            sumar = Decimal('0.00')
            for cotizacion_sociedad in detalle.CotizacionSociedad_cotizacion_venta_detalle.all():
                sumar += cotizacion_sociedad.cantidad
            if sumar != detalle.cantidad:
                error_cantidad_sociedad = True
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        if error_cantidad_sociedad:
            context['texto'] = 'Revise las cantidades por Sociedad.'
            return render(request, 'includes/modal sin permiso.html', context)
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('cotizacion_app:cotizacion_venta_ver', kwargs={'id_cotizacion':self.object.id})

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            self.object = self.get_object()

            detalles = self.object.CotizacionVentaDetalle_cotizacion_venta.all()
            reserva = TipoMovimiento.objects.get(codigo=118)
            for detalle in detalles:
                sociedades = detalle.CotizacionSociedad_cotizacion_venta_detalle.all()
                for cotizacion_sociedad in sociedades:
                    if cotizacion_sociedad.cantidad > 0:
                        movimiento_dos = MovimientosAlmacen.objects.create(
                                content_type_producto = detalle.content_type,
                                id_registro_producto = detalle.id_registro,
                                cantidad = cotizacion_sociedad.cantidad,
                                tipo_movimiento = reserva,
                                tipo_stock = reserva.tipo_stock_final,
                                signo_factor_multiplicador = +1,
                                content_type_documento_proceso = ContentType.objects.get_for_model(self.object),
                                id_registro_documento_proceso = self.object.id,
                                almacen = None,
                                sociedad = cotizacion_sociedad.sociedad,
                                movimiento_anterior = None,
                                movimiento_reversion = False,
                                created_by = self.request.user,
                                updated_by = self.request.user,
                            )

            self.object.estado = 3
            registro_guardar(self.object, self.request)
            self.object.save()

            messages.success(request, MENSAJE_RESERVAR_COTIZACION)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(CotizacionVentaReservaView, self).get_context_data(**kwargs)
        context['accion'] = "Reservar"
        context['titulo'] = "Cotización"
        context['texto'] = "¿Está seguro de Reservar la cotización?"
        context['item'] = "Cotización %s - %s" % (numeroXn(self.object.numero_cotizacion, 6), self.object.cliente)
        return context


class CotizacionVentaReservaAnularView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('cotizacion.change_cotizacionventa')
    model = CotizacionVenta
    template_name = "includes/form generico.html"

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('cotizacion_app:cotizacion_venta_ver', kwargs={'id_cotizacion':self.object.id})

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            self.object = self.get_object()

            reserva = TipoMovimiento.objects.get(codigo=118)
            movimientos = MovimientosAlmacen.objects.filter(
                    tipo_movimiento = reserva,
                    tipo_stock = reserva.tipo_stock_final,
                    signo_factor_multiplicador = +1,
                    content_type_documento_proceso = ContentType.objects.get_for_model(self.object),
                    id_registro_documento_proceso = self.object.id,
                    almacen = None,
                )
            for movimiento in movimientos:
                movimiento.delete()

            self.object.estado = 2
            registro_guardar(self.object, self.request)
            self.object.save()

            messages.success(request, MENSAJE_ANULAR_RESERVAR_COTIZACION)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(CotizacionVentaReservaAnularView, self).get_context_data(**kwargs)
        context['accion'] = "Anular"
        context['titulo'] = "Reserva de Cotización"
        context['texto'] = "¿Está seguro de Anular la Reserva de la cotización?"
        context['item'] = "Cotización %s - %s" % (numeroXn(self.object.numero_cotizacion, 6), self.object.cliente)
        return context


class CotizacionVentaConfirmarView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('cotizacion.change_cotizacionventa')
    model = CotizacionVenta
    template_name = "includes/form generico.html"

    def dispatch(self, request, *args, **kwargs):
        error_cantidad_stock = False
        error_cantidad_sociedad = False
        error_tipo_cambio = False
        context = {}
        context['titulo'] = 'Error de Confirmación'
        for detalle in self.get_object().CotizacionVentaDetalle_cotizacion_venta.all():
            sumar = Decimal('0.00')
            for cotizacion_sociedad in detalle.CotizacionSociedad_cotizacion_venta_detalle.all():
                sumar += cotizacion_sociedad.cantidad
                if cotizacion_sociedad.cantidad > stock(detalle.content_type, detalle.id_registro, cotizacion_sociedad.sociedad.id):
                    error_cantidad_stock = True
            if sumar != detalle.cantidad:
                error_cantidad_sociedad = True
        
        if len(TipoCambio.objects.filter(fecha=datetime.today()))==0:
            error_tipo_cambio = True

        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')

        if error_tipo_cambio:
            context['texto'] = 'Ingrese un tipo de cambio para hoy.'
            return render(request, 'includes/modal sin permiso.html', context)

        if error_cantidad_sociedad:
            context['texto'] = 'Revise las cantidades por Sociedad.'
            return render(request, 'includes/modal sin permiso.html', context)

        if error_cantidad_stock and self.get_object().estado != 3:
            context['texto'] = 'No hay stock suficiente en un producto.'
            return render(request, 'includes/modal sin permiso.html', context)
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('cotizacion_app:cotizacion_venta_ver', kwargs={'id_cotizacion':self.object.id})

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            self.object = self.get_object()
            sociedades_confirmar = []
            detalles = self.object.CotizacionVentaDetalle_cotizacion_venta.all()
            
            if self.object.estado == 3: #Si está reservado
                movimiento_inicial = TipoMovimiento.objects.get(codigo=118) #Reservar
                movimiento_final = TipoMovimiento.objects.get(codigo=119) #Confirmación de reserva
                for detalle in detalles:
                    sociedades = detalle.CotizacionSociedad_cotizacion_venta_detalle.all()
                    for cotizacion_sociedad in sociedades:
                        if cotizacion_sociedad.cantidad > 0:
                            if not cotizacion_sociedad.sociedad in sociedades_confirmar: sociedades_confirmar.append(cotizacion_sociedad.sociedad)
                            movimiento_anterior = MovimientosAlmacen.objects.get(
                                content_type_producto = detalle.content_type,
                                id_registro_producto = detalle.id_registro,
                                tipo_movimiento = movimiento_inicial,
                                tipo_stock = movimiento_inicial.tipo_stock_final,
                                signo_factor_multiplicador = +1,
                                content_type_documento_proceso = ContentType.objects.get_for_model(self.object),
                                id_registro_documento_proceso = self.object.id,
                                sociedad = cotizacion_sociedad.sociedad,
                                movimiento_reversion = False,
                            )
                            movimiento_uno = MovimientosAlmacen.objects.create(
                                content_type_producto = detalle.content_type,
                                id_registro_producto = detalle.id_registro,
                                cantidad = cotizacion_sociedad.cantidad,
                                tipo_movimiento = movimiento_final,
                                tipo_stock = movimiento_final.tipo_stock_inicial,
                                signo_factor_multiplicador = -1,
                                content_type_documento_proceso = ContentType.objects.get_for_model(self.object),
                                id_registro_documento_proceso = self.object.id,
                                almacen = None,
                                sociedad = cotizacion_sociedad.sociedad,
                                movimiento_anterior = movimiento_anterior,
                                movimiento_reversion = False,
                                created_by = self.request.user,
                                updated_by = self.request.user,
                            )
                            movimiento_dos = MovimientosAlmacen.objects.create(
                                content_type_producto = detalle.content_type,
                                id_registro_producto = detalle.id_registro,
                                cantidad = cotizacion_sociedad.cantidad,
                                tipo_movimiento = movimiento_final,
                                tipo_stock = movimiento_final.tipo_stock_final,
                                signo_factor_multiplicador = +1,
                                content_type_documento_proceso = ContentType.objects.get_for_model(self.object),
                                id_registro_documento_proceso = self.object.id,
                                almacen = None,
                                sociedad = cotizacion_sociedad.sociedad,
                                movimiento_anterior = movimiento_uno,
                                movimiento_reversion = False,
                                created_by = self.request.user,
                                updated_by = self.request.user,
                            )
                self.object.estado = 4
            else: #Si no está reservado
                movimiento_final = TipoMovimiento.objects.get(codigo=120) #Confirmación de venta
                for detalle in detalles:
                    sociedades = detalle.CotizacionSociedad_cotizacion_venta_detalle.all()
                    for cotizacion_sociedad in sociedades:
                        if cotizacion_sociedad.cantidad > 0:
                            if not cotizacion_sociedad.sociedad in sociedades_confirmar: sociedades_confirmar.append(cotizacion_sociedad.sociedad)
                            movimiento_dos = MovimientosAlmacen.objects.create(
                                content_type_producto = detalle.content_type,
                                id_registro_producto = detalle.id_registro,
                                cantidad = cotizacion_sociedad.cantidad,
                                tipo_movimiento = movimiento_final,
                                tipo_stock = movimiento_final.tipo_stock_final,
                                signo_factor_multiplicador = +1,
                                content_type_documento_proceso = ContentType.objects.get_for_model(self.object),
                                id_registro_documento_proceso = self.object.id,
                                almacen = None,
                                sociedad = cotizacion_sociedad.sociedad,
                                movimiento_anterior = None,
                                movimiento_reversion = False,
                                created_by = self.request.user,
                                updated_by = self.request.user,
                            )
                self.object.estado = 5
            
            for sociedad in sociedades_confirmar:
                cotizacion_observacion = observacion(self.object, sociedad)
                condiciones_pago = None
                tipo_venta = 1

                if hasattr(self.object, 'SolicitudCredito_cotizacion_venta'):
                    if self.object.SolicitudCredito_cotizacion_venta.estado == 3:
                        condiciones_pago = self.object.SolicitudCredito_cotizacion_venta.condiciones_pago
                        tipo_venta = 2
                confirmacion_venta = ConfirmacionVenta.objects.create(
                    cotizacion_venta = self.object,
                    cliente = self.object.cliente,
                    cliente_interlocutor = self.object.cliente_interlocutor,
                    sociedad = sociedad,
                    tipo_cambio = TipoCambio.objects.filter(fecha=datetime.today()).latest('created_at'),
                    moneda = self.object.moneda,
                    observacion = cotizacion_observacion,
                    condiciones_pago = condiciones_pago,
                    tipo_venta = tipo_venta,
                    descuento_global = self.object.descuento_global,
                    otros_cargos = self.object.otros_cargos,
                    total = self.object.total,
                    created_by = self.request.user,
                    updated_by = self.request.user,
                )
                for detalle in detalles:
                    cotizacion_sociedad = detalle.CotizacionSociedad_cotizacion_venta_detalle.get(sociedad=sociedad)
                    if cotizacion_sociedad.cantidad > 0:
                        respuesta = calculos_linea(cotizacion_sociedad.cantidad, detalle.precio_unitario_con_igv, detalle.precio_final_con_igv, igv(), detalle.tipo_igv)
                        ConfirmacionVentaDetalle.objects.create(
                            item = detalle.item,
                            content_type = detalle.content_type,
                            id_registro = detalle.id_registro,
                            cantidad_confirmada = cotizacion_sociedad.cantidad,
                            precio_unitario_sin_igv = respuesta['precio_unitario_sin_igv'],
                            precio_unitario_con_igv = detalle.precio_unitario_con_igv,
                            precio_final_con_igv = detalle.precio_final_con_igv,
                            descuento = respuesta['descuento'],
                            sub_total = respuesta['subtotal'],
                            igv = respuesta['igv'],
                            total = respuesta['total'],
                            tipo_igv = detalle.tipo_igv,
                            confirmacion_venta = confirmacion_venta,
                            created_by = self.request.user,
                            updated_by = self.request.user,
                        )
                

            registro_guardar(self.object, self.request)
            self.object.save()

            messages.success(request, MENSAJE_CONFIRMAR_COTIZACION)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(CotizacionVentaConfirmarView, self).get_context_data(**kwargs)
        context['accion'] = "Confirmar"
        context['titulo'] = "Cotización"
        context['texto'] = "¿Está seguro de Confirmar la cotización?"
        context['item'] = "Cotización %s - %s" % (numeroXn(self.object.numero_cotizacion, 6), self.object.cliente)
        return context


class CotizacionVentaConfirmarAnularView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('cotizacion.change_cotizacionventa')
    model = CotizacionVenta
    template_name = "includes/form generico.html"   

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)
    
    def get_success_url(self, **kwargs):
        return reverse_lazy('cotizacion_app:cotizacion_venta_ver', kwargs={'id_cotizacion':self.object.id})

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            self.object = self.get_object()

            if self.object.estado == 4: #Si partió de reservado
                confirmar = TipoMovimiento.objects.get(codigo=119)
                self.object.estado = 3
            else: #Si no partió de reservado
                confirmar = TipoMovimiento.objects.get(codigo=120)
                self.object.estado = 2

            movimientos = MovimientosAlmacen.objects.filter(
                    tipo_movimiento = confirmar,
                    tipo_stock = confirmar.tipo_stock_final,
                    signo_factor_multiplicador = +1,
                    content_type_documento_proceso = ContentType.objects.get_for_model(self.object),
                    id_registro_documento_proceso = self.object.id,
                    almacen = None,
                )
            for movimiento in movimientos:
                movimiento_uno = movimiento.movimiento_anterior
                movimiento.delete()
                if movimiento_uno:
                    movimiento_uno.delete()

            confirmaciones_venta = ConfirmacionVenta.objects.filter(
                cotizacion_venta = self.object,
            )
            for confirmacion_venta in confirmaciones_venta:
                confirmacion_venta.estado = 3
                confirmacion_venta.save()

            registro_guardar(self.object, self.request)
            self.object.save()

            messages.success(request, MENSAJE_ANULAR_CONFIRMAR_COTIZACION)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(CotizacionVentaConfirmarAnularView, self).get_context_data(**kwargs)
        context['accion'] = "Anular"
        context['titulo'] = "Confirmar de Cotización"
        context['texto'] = "¿Está seguro de Anular la Confirmar de la cotización?"
        context['item'] = "Cotización %s - %s" % (numeroXn(self.object.numero_cotizacion, 6), self.object.cliente)
        return context


class CotizacionVentaConfirmarAnticipoView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('cotizacion.change_cotizacionventa')
    model = CotizacionVenta
    template_name = "includes/form generico.html"

    def dispatch(self, request, *args, **kwargs):
        error_cantidad_sociedad = False
        error_tipo_cambio = False
        context = {}
        context['titulo'] = 'Error de Confirmación'
        for detalle in self.get_object().CotizacionVentaDetalle_cotizacion_venta.all():
            sumar = Decimal('0.00')
            for cotizacion_sociedad in detalle.CotizacionSociedad_cotizacion_venta_detalle.all():
                sumar += cotizacion_sociedad.cantidad
            if sumar != detalle.cantidad:
                error_cantidad_sociedad = True
        
        if len(TipoCambio.objects.filter(fecha=datetime.today()))==0:
            error_tipo_cambio = True

        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')

        if error_tipo_cambio:
            context['texto'] = 'Ingrese un tipo de cambio para hoy.'
            return render(request, 'includes/modal sin permiso.html', context)

        if error_cantidad_sociedad:
            context['texto'] = 'Revise las cantidades por Sociedad.'
            return render(request, 'includes/modal sin permiso.html', context)

        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('cotizacion_app:cotizacion_venta_ver', kwargs={'id_cotizacion':self.object.id})

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            self.object = self.get_object()
            sociedades_confirmar = []
            detalles = self.object.CotizacionVentaDetalle_cotizacion_venta.all()
            
            movimiento_final = TipoMovimiento.objects.get(codigo=129) #Confirmación Anticipada de venta
            for detalle in detalles:
                sociedades = detalle.CotizacionSociedad_cotizacion_venta_detalle.all()
                for cotizacion_sociedad in sociedades:
                    if cotizacion_sociedad.cantidad > 0:
                        if not cotizacion_sociedad.sociedad in sociedades_confirmar: sociedades_confirmar.append(cotizacion_sociedad.sociedad)
                        movimiento_dos = MovimientosAlmacen.objects.create(
                            content_type_producto = detalle.content_type,
                            id_registro_producto = detalle.id_registro,
                            cantidad = cotizacion_sociedad.cantidad,
                            tipo_movimiento = movimiento_final,
                            tipo_stock = movimiento_final.tipo_stock_final,
                            signo_factor_multiplicador = +1,
                            content_type_documento_proceso = ContentType.objects.get_for_model(self.object),
                            id_registro_documento_proceso = self.object.id,
                            almacen = None,
                            sociedad = cotizacion_sociedad.sociedad,
                            movimiento_anterior = None,
                            movimiento_reversion = False,
                            created_by = self.request.user,
                            updated_by = self.request.user,
                        )
            self.object.estado = 6
            
            for sociedad in sociedades_confirmar:
                cotizacion_observacion = observacion(self.object, sociedad)
                confirmacion_venta = ConfirmacionVenta.objects.create(
                    cotizacion_venta = self.object,
                    cliente = self.object.cliente,
                    cliente_interlocutor = self.object.cliente_interlocutor,
                    sociedad = sociedad,
                    tipo_cambio = TipoCambio.objects.filter(fecha=self.object.fecha).latest('created_at'),
                    moneda = self.object.moneda,
                    observacion = cotizacion_observacion,
                    total = self.object.total,
                    sunat_transaction = 4,
                    created_by = self.request.user,
                    updated_by = self.request.user,
                )
                for detalle in detalles:
                    cotizacion_sociedad = detalle.CotizacionSociedad_cotizacion_venta_detalle.get(sociedad=sociedad)
                    if cotizacion_sociedad.cantidad > 0:
                        respuesta = calculos_linea(cotizacion_sociedad.cantidad, detalle.precio_unitario_con_igv, detalle.precio_final_con_igv, igv(), detalle.tipo_igv)
                        ConfirmacionVentaDetalle.objects.create(
                            item = detalle.item,
                            content_type = detalle.content_type,
                            id_registro = detalle.id_registro,
                            cantidad_confirmada = cotizacion_sociedad.cantidad,
                            precio_unitario_sin_igv = respuesta['precio_unitario_sin_igv'],
                            precio_unitario_con_igv = detalle.precio_unitario_con_igv,
                            precio_final_con_igv = detalle.precio_final_con_igv,
                            descuento = respuesta['descuento'],
                            sub_total = respuesta['subtotal'],
                            igv = respuesta['igv'],
                            total = respuesta['total'],
                            tipo_igv = detalle.tipo_igv,
                            confirmacion_venta = confirmacion_venta,
                            created_by = self.request.user,
                            updated_by = self.request.user,
                        )

            registro_guardar(self.object, self.request)
            self.object.save()

            messages.success(request, MENSAJE_CONFIRMAR_COTIZACION)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(CotizacionVentaConfirmarAnticipoView, self).get_context_data(**kwargs)
        context['accion'] = "Confirmar"
        context['titulo'] = "Cotización"
        context['texto'] = "¿Está seguro de Confirmar la cotización?"
        context['item'] = "Cotización %s - %s" % (numeroXn(self.object.numero_cotizacion, 6), self.object.cliente)
        return context


class CotizacionVentaConfirmarAnticipoAnularView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('cotizacion.change_cotizacionventa')
    model = CotizacionVenta
    template_name = "includes/form generico.html"   

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)
    
    def get_success_url(self, **kwargs):
        return reverse_lazy('cotizacion_app:cotizacion_venta_ver', kwargs={'id_cotizacion':self.object.id})

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            self.object = self.get_object()

            confirmar = TipoMovimiento.objects.get(codigo=129)
            self.object.estado = 2

            movimientos = MovimientosAlmacen.objects.filter(
                    tipo_movimiento = confirmar,
                    tipo_stock = confirmar.tipo_stock_final,
                    signo_factor_multiplicador = +1,
                    content_type_documento_proceso = ContentType.objects.get_for_model(self.object),
                    id_registro_documento_proceso = self.object.id,
                    almacen = None,
                )
            for movimiento in movimientos:
                movimiento_uno = movimiento.movimiento_anterior
                movimiento.delete()
                if movimiento_uno:
                    movimiento_uno.delete()

            confirmaciones_venta = ConfirmacionVenta.objects.filter(
                cotizacion_venta = self.object,
            )
            for confirmacion_venta in confirmaciones_venta:
                confirmacion_venta.delete()

            registro_guardar(self.object, self.request)
            self.object.save()

            messages.success(request, MENSAJE_ANULAR_CONFIRMAR_COTIZACION)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(CotizacionVentaConfirmarAnticipoAnularView, self).get_context_data(**kwargs)
        context['accion'] = "Anular"
        context['titulo'] = "Confirmar de Cotización"
        context['texto'] = "¿Está seguro de Anular la Confirmar de la cotización?"
        context['item'] = "Cotización %s - %s" % (numeroXn(self.object.numero_cotizacion, 6), self.object.cliente)
        return context


class CotizacionVentaPdfsView(PermissionRequiredMixin, BSModalFormView):
    permission_required = ('cotizacion.change_cotizacionventa')
    template_name = "cotizacion/cotizacion_venta/form_pdfs.html"
    form_class = CotizacionVentaPdfsForm

    def dispatch(self, request, *args, **kwargs):
        error_cantidad_sociedad = False
        obj = CotizacionVenta.objects.get(slug=self.kwargs['slug'])
        context = {}
        context['titulo'] = 'Error de Confirmación'
        for detalle in obj.CotizacionVentaDetalle_cotizacion_venta.all():
            sumar = Decimal('0.00')
            for cotizacion_sociedad in detalle.CotizacionSociedad_cotizacion_venta_detalle.all():
                sumar += cotizacion_sociedad.cantidad

            if sumar != detalle.cantidad:
                error_cantidad_sociedad = True
        
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')

        if error_cantidad_sociedad:
            context['texto'] = 'Revise las cantidades por Sociedad.'
            return render(request, 'includes/modal sin permiso.html', context)
            
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        obj = CotizacionVenta.objects.get(slug=self.kwargs['slug'])
        context = super(CotizacionVentaPdfsView, self).get_context_data(**kwargs)
        context['titulo'] = 'Ver PDFs'
        context['cotizacion'] = obj
        context['sociedades'] = obj.sociedades
        return context
    

class CotizacionVentaSociedadPdfView(View):
    def get(self, request, *args, **kwargs):
        sociedad = Sociedad.objects.get(abreviatura=self.kwargs['sociedad'])
        color = sociedad.color
        titulo = 'Cotización'
        vertical = False
        alinear = 'right'
        logo = [[sociedad.logo.url, alinear]]
        pie_pagina = sociedad.pie_pagina
        fuenteBase = "ComicNeue"

        obj = CotizacionVenta.objects.get(slug=self.kwargs['slug'])

        moneda = obj.moneda
        titulo = 'Cotización %s%s %s' % (self.kwargs['sociedad'], numeroXn(obj.numero_cotizacion, 6), str(obj.cliente.razon_social))

        Cabecera = {}
        Cabecera['nro_cotizacion'] = '%s%s' % (self.kwargs['sociedad'], numeroXn(obj.numero_cotizacion, 6))
        Cabecera['fecha_cotizacion'] = fecha_en_letras(obj.fecha_cotizacion)
        Cabecera['razon_social'] = str(obj.cliente)
        Cabecera['tipo_documento'] = DICCIONARIO_TIPO_DOCUMENTO_SUNAT[obj.cliente.tipo_documento]
        Cabecera['nro_documento'] = str(obj.cliente.numero_documento)
        Cabecera['direccion'] = str(obj.cliente.direccion_fiscal)
        Cabecera['interlocutor'] = str(obj.cliente_interlocutor)
        Cabecera['fecha_validez'] = obj.fecha_validez.strftime('%d/%m/%Y')
        Cabecera['vendedor'] = str(nombre_usuario(obj.vendedor))

        TablaEncabezado = [ 'Item',
                            'Descripción',
                            'Unidad',
                            'Cantidad',
                            'Prec. Unit. con IGV',
                            'Prec. Final con IGV',
                            'Descuento',
                            'Total',
                            'Stock',
                            '',
                            ]

        cotizacion_venta_detalle = obj.CotizacionVentaDetalle_cotizacion_venta.all()

        TablaDatos = []
        item = 1
        for detalle in cotizacion_venta_detalle:
            fila = []
            confirmacion_detalle = detalle.CotizacionSociedad_cotizacion_venta_detalle.get(sociedad=sociedad)
            if confirmacion_detalle.cantidad == 0: continue
            calculo = calculos_linea(confirmacion_detalle.cantidad, detalle.precio_unitario_con_igv, detalle.precio_final_con_igv, igv(obj.fecha), detalle.tipo_igv)
            detalle.material = detalle.content_type.get_object_for_this_type(id = detalle.id_registro)
            fila.append(item)
            fila.append(detalle.material)
            fila.append(detalle.material.unidad_base)
            fila.append(confirmacion_detalle.cantidad.quantize(Decimal('0.01')))
            fila.append(detalle.precio_unitario_con_igv.quantize(Decimal('0.01')))
            fila.append(detalle.precio_final_con_igv.quantize(Decimal('0.01')))
            fila.append(calculo['descuento_con_igv'].quantize(Decimal('0.01')))
            fila.append(calculo['total'].quantize(Decimal('0.01')))
            stock_disponible = stock(detalle.content_type, detalle.id_registro, sociedad.id)
            if stock_disponible >= confirmacion_detalle.cantidad:
                disponibilidad = "DISPONIBLE"
            elif stock_disponible == 0:
                if detalle.tiempo_entrega:
                    disponibilidad = "LLEGADA EN %s DÍAS" % (detalle.tiempo_entrega)
                else:
                    disponibilidad = "NO DISPONIBLE"
            else:
                if detalle.tiempo_entrega:
                    disponibilidad = "%s DISPONIBLE\nSALDO EN %s DÍAS" % (intcomma((stock_disponible).quantize(Decimal('0.01'))), detalle.tiempo_entrega)
                else:
                    disponibilidad = "%s DISPONIBLE" % (intcomma((stock_disponible).quantize(Decimal('0.01'))))
            fila.append(disponibilidad)

            TablaDatos.append(fila)
            item += 1
        
        totales = obtener_totales(obj, sociedad)

        TablaTotales = []
        for k,v in totales.items():
            if not k in DICCIONARIO_TOTALES: continue
            if v==0:continue
            fila = []
            fila.append(DICCIONARIO_TOTALES[k])
            fila.append(intcomma(v))

            TablaTotales.append(fila)
        
        condiciones = CotizacionTerminosCondiciones.objects.filter(condicion_visible=True)
        
        observaciones = obj.CotizacionObservacion_cotizacion_venta.get(sociedad=sociedad).observacion

        buf = generarCotizacionVenta(titulo, vertical, logo, pie_pagina, Cabecera, TablaEncabezado, TablaDatos, color, condiciones, TablaTotales, fuenteBase, moneda, observaciones)

        respuesta = HttpResponse(buf.getvalue(), content_type='application/pdf')
        respuesta.headers['content-disposition']='inline; filename=%s.pdf' % titulo

        return respuesta


class CotizacionVentaSociedadCuentasPdfView(View):
    def get(self, request, *args, **kwargs):
        sociedad = Sociedad.objects.get(abreviatura=self.kwargs['sociedad'])
        color = sociedad.color
        titulo = 'Cotización'
        vertical = False
        alinear = 'right'
        logo = [[sociedad.logo.url, alinear]]
        pie_pagina = sociedad.pie_pagina
        fuenteBase = "ComicNeue"

        obj = CotizacionVenta.objects.get(slug=self.kwargs['slug'])

        moneda_cotizacion = obj.moneda
        titulo = 'Cotización %s%s %s' % (self.kwargs['sociedad'], numeroXn(obj.numero_cotizacion, 6), str(obj.cliente.razon_social))

        Cabecera = {}
        Cabecera['nro_cotizacion'] = '%s%s' % (self.kwargs['sociedad'], numeroXn(obj.numero_cotizacion, 6))
        Cabecera['fecha_cotizacion'] = fecha_en_letras(obj.fecha_cotizacion)
        Cabecera['razon_social'] = str(obj.cliente)
        Cabecera['tipo_documento'] = DICCIONARIO_TIPO_DOCUMENTO_SUNAT[obj.cliente.tipo_documento]
        Cabecera['nro_documento'] = str(obj.cliente.numero_documento)
        Cabecera['direccion'] = str(obj.cliente.direccion_fiscal)
        Cabecera['interlocutor'] = str(obj.cliente_interlocutor)
        Cabecera['fecha_validez'] = obj.fecha_validez.strftime('%d/%m/%Y')
        Cabecera['vendedor'] = str(nombre_usuario(obj.vendedor))

        TablaEncabezado = [ 'Item',
                            'Descripción',
                            'Unidad',
                            'Cantidad',
                            'Prec. Unit. con IGV',
                            'Prec. Final con IGV',
                            'Descuento',
                            'Total',
                            'Stock',
                            '',
                            ]

        cotizacion_venta_detalle = obj.CotizacionVentaDetalle_cotizacion_venta.all()

        TablaDatos = []
        item = 1
        for detalle in cotizacion_venta_detalle:
            fila = []
            confirmacion_detalle = detalle.CotizacionSociedad_cotizacion_venta_detalle.get(sociedad=sociedad)
            if confirmacion_detalle.cantidad == 0: continue
            calculo = calculos_linea(confirmacion_detalle.cantidad, detalle.precio_unitario_con_igv, detalle.precio_final_con_igv, igv(obj.fecha), detalle.tipo_igv)
            detalle.material = detalle.content_type.get_object_for_this_type(id = detalle.id_registro)
            fila.append(item)
            fila.append(detalle.material)
            fila.append(detalle.material.unidad_base)
            fila.append(confirmacion_detalle.cantidad.quantize(Decimal('0.01')))
            fila.append(detalle.precio_unitario_con_igv.quantize(Decimal('0.01')))
            fila.append(detalle.precio_final_con_igv.quantize(Decimal('0.01')))
            fila.append(calculo['descuento_con_igv'].quantize(Decimal('0.01')))
            fila.append(calculo['total'].quantize(Decimal('0.01')))
            stock_disponible = stock(detalle.content_type, detalle.id_registro, sociedad.id)
            if stock_disponible >= confirmacion_detalle.cantidad:
                disponibilidad = "DISPONIBLE"
            elif stock_disponible == 0:
                if detalle.tiempo_entrega:
                    disponibilidad = "LLEGADA EN %s DÍAS" % (detalle.tiempo_entrega)
                else:
                    disponibilidad = "NO DISPONIBLE"
            else:
                if detalle.tiempo_entrega:
                    disponibilidad = "%s DISPONIBLE\nSALDO EN %s DÍAS" % (intcomma((stock_disponible).quantize(Decimal('0.01'))), detalle.tiempo_entrega)
                else:
                    disponibilidad = "%s DISPONIBLE" % (intcomma((stock_disponible).quantize(Decimal('0.01'))))
            fila.append(disponibilidad)

            TablaDatos.append(fila)
            item += 1
        
        totales = obtener_totales(obj, sociedad)

        TablaTotales = []
        for k,v in totales.items():
            if not k in DICCIONARIO_TOTALES: continue
            if v==0:continue
            fila = []
            fila.append(DICCIONARIO_TOTALES[k])
            fila.append(intcomma(v))

            TablaTotales.append(fila)
        
        condiciones = CotizacionTerminosCondiciones.objects.filter(condicion_visible=True)
        
        observaciones = obj.CotizacionObservacion_cotizacion_venta.get(sociedad=sociedad).observacion

        monedas = Moneda.objects.all()
        tipo_de_cambio_cotizacion = TipoCambio.objects.tipo_cambio_venta(obj.fecha)
        tipo_de_cambio_hoy = TipoCambio.objects.tipo_cambio_venta(date.today())
        tipo_de_cambio_final = tipo_de_cambio(tipo_de_cambio_cotizacion, tipo_de_cambio_hoy)
        for moneda in monedas:
            cotizacion_sociedad = []
            sociedades = Sociedad.objects.all()
            for sociedad in sociedades:
                total = obtener_totales(obj, sociedad)['total']
                if total > 0:
                    if moneda.simbolo == '$':
                        sociedad.total = total
                    else:
                        sociedad.total = (total * tipo_de_cambio_final).quantize(Decimal('0.01'))

                    cotizacion_sociedad.append(sociedad)

            for sociedad in cotizacion_sociedad:
                cuentas = CuentaBancariaSociedad.objects.filter(
                    sociedad=sociedad,
                    moneda=moneda,
                    efectivo=False,
                    estado=1,
                    )
                sociedad.cuentas = cuentas
            moneda.sociedades = cotizacion_sociedad

        buf = generarCotizacionVenta(titulo, vertical, logo, pie_pagina, Cabecera, TablaEncabezado, TablaDatos, color, condiciones, TablaTotales, fuenteBase, moneda_cotizacion, observaciones, monedas)

        respuesta = HttpResponse(buf.getvalue(), content_type='application/pdf')
        respuesta.headers['content-disposition']='inline; filename=%s.pdf' % titulo

        return respuesta


class CotizacionVentaSociedadCuentasSolesPdfView(View):
    def get(self, request, *args, **kwargs):
        sociedad = Sociedad.objects.get(abreviatura=self.kwargs['sociedad'])
        color = sociedad.color
        titulo = 'Cotización'
        vertical = False
        alinear = 'right'
        logo = [[sociedad.logo.url, alinear]]
        pie_pagina = sociedad.pie_pagina
        fuenteBase = "ComicNeue"

        obj = CotizacionVenta.objects.get(slug=self.kwargs['slug'])

        moneda_cotizacion = obj.moneda
        titulo = 'Cotización %s%s %s' % (self.kwargs['sociedad'], numeroXn(obj.numero_cotizacion, 6), str(obj.cliente.razon_social))

        Cabecera = {}
        Cabecera['nro_cotizacion'] = '%s%s' % (self.kwargs['sociedad'], numeroXn(obj.numero_cotizacion, 6))
        Cabecera['fecha_cotizacion'] = fecha_en_letras(obj.fecha_cotizacion)
        Cabecera['razon_social'] = str(obj.cliente)
        Cabecera['tipo_documento'] = DICCIONARIO_TIPO_DOCUMENTO_SUNAT[obj.cliente.tipo_documento]
        Cabecera['nro_documento'] = str(obj.cliente.numero_documento)
        Cabecera['direccion'] = str(obj.cliente.direccion_fiscal)
        Cabecera['interlocutor'] = str(obj.cliente_interlocutor)
        Cabecera['fecha_validez'] = obj.fecha_validez.strftime('%d/%m/%Y')
        Cabecera['vendedor'] = str(nombre_usuario(obj.vendedor))

        TablaEncabezado = [ 'Item',
                            'Descripción',
                            'Unidad',
                            'Cantidad',
                            'Prec. Unit. con IGV',
                            'Prec. Final con IGV',
                            'Descuento',
                            'Total',
                            'Stock',
                            '',
                            ]

        cotizacion_venta_detalle = obj.CotizacionVentaDetalle_cotizacion_venta.all()

        TablaDatos = []
        item = 1
        for detalle in cotizacion_venta_detalle:
            fila = []
            confirmacion_detalle = detalle.CotizacionSociedad_cotizacion_venta_detalle.get(sociedad=sociedad)
            if confirmacion_detalle.cantidad == 0: continue
            calculo = calculos_linea(confirmacion_detalle.cantidad, detalle.precio_unitario_con_igv, detalle.precio_final_con_igv, igv(obj.fecha), detalle.tipo_igv)
            detalle.material = detalle.content_type.get_object_for_this_type(id = detalle.id_registro)
            fila.append(item)
            fila.append(detalle.material)
            fila.append(detalle.material.unidad_base)
            fila.append(confirmacion_detalle.cantidad.quantize(Decimal('0.01')))
            fila.append(detalle.precio_unitario_con_igv.quantize(Decimal('0.01')))
            fila.append(detalle.precio_final_con_igv.quantize(Decimal('0.01')))
            fila.append(calculo['descuento_con_igv'].quantize(Decimal('0.01')))
            fila.append(calculo['total'].quantize(Decimal('0.01')))
            stock_disponible = stock(detalle.content_type, detalle.id_registro, sociedad.id)
            if stock_disponible >= confirmacion_detalle.cantidad:
                disponibilidad = "DISPONIBLE"
            elif stock_disponible == 0:
                if detalle.tiempo_entrega:
                    disponibilidad = "LLEGADA EN %s DÍAS" % (detalle.tiempo_entrega)
                else:
                    disponibilidad = "NO DISPONIBLE"
            else:
                if detalle.tiempo_entrega:
                    disponibilidad = "%s DISPONIBLE\nSALDO EN %s DÍAS" % (intcomma((stock_disponible).quantize(Decimal('0.01'))), detalle.tiempo_entrega)
                else:
                    disponibilidad = "%s DISPONIBLE" % (intcomma((stock_disponible).quantize(Decimal('0.01'))))
            fila.append(disponibilidad)

            TablaDatos.append(fila)
            item += 1
        
        totales = obtener_totales(obj, sociedad)

        TablaTotales = []
        for k,v in totales.items():
            if not k in DICCIONARIO_TOTALES: continue
            if v==0:continue
            fila = []
            fila.append(DICCIONARIO_TOTALES[k])
            fila.append(intcomma(v))

            TablaTotales.append(fila)
        
        condiciones = CotizacionTerminosCondiciones.objects.filter(condicion_visible=True)
        
        observaciones = obj.CotizacionObservacion_cotizacion_venta.get(sociedad=sociedad).observacion

        monedas = Moneda.objects.all()
        tipo_de_cambio_cotizacion = TipoCambio.objects.tipo_cambio_venta(obj.fecha)
        tipo_de_cambio_hoy = TipoCambio.objects.tipo_cambio_venta(date.today())
        tipo_de_cambio_final = tipo_de_cambio(tipo_de_cambio_cotizacion, tipo_de_cambio_hoy)
        for moneda in monedas:
            cotizacion_sociedad = []
            sociedades = Sociedad.objects.all()
            for sociedad in sociedades:
                total = obtener_totales(obj, sociedad)['total']
                if total > 0:
                    if moneda.simbolo == '$':
                        sociedad.total = total
                    else:
                        sociedad.total = (total * tipo_de_cambio_final).quantize(Decimal('0.01'))

                    cotizacion_sociedad.append(sociedad)

            for sociedad in cotizacion_sociedad:
                cuentas = CuentaBancariaSociedad.objects.filter(
                    sociedad=sociedad,
                    moneda=moneda,
                    efectivo=False,
                    estado=1,
                    )
                sociedad.cuentas = cuentas
            moneda.sociedades = cotizacion_sociedad

        buf = generarCotizacionVenta(titulo, vertical, logo, pie_pagina, Cabecera, TablaEncabezado, TablaDatos, color, condiciones, TablaTotales, fuenteBase, moneda_cotizacion, observaciones, monedas, True)

        respuesta = HttpResponse(buf.getvalue(), content_type='application/pdf')
        respuesta.headers['content-disposition']='inline; filename=%s.pdf' % titulo

        return respuesta


class CotizacionVentaResumenView(PermissionRequiredMixin, BSModalReadView):
    permission_required = ('cotizacion.view_cotizacionventa')
    model = CotizacionVenta
    template_name = "cotizacion/cotizacion_venta/form_resumen.html"

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        monedas = Moneda.objects.all()
        tipo_de_cambio_cotizacion = TipoCambio.objects.tipo_cambio_venta(self.object.fecha)
        tipo_de_cambio_hoy = TipoCambio.objects.tipo_cambio_venta(date.today())
        tipo_de_cambio_final = tipo_de_cambio(tipo_de_cambio_cotizacion, tipo_de_cambio_hoy)
        for moneda in monedas:
            cotizacion_sociedad = []
            sociedades = Sociedad.objects.all()
            for sociedad in sociedades:
                total = obtener_totales(self.object, sociedad)['total']
                if total > 0:
                    if moneda.simbolo == '$':
                        sociedad.total = total
                    else:
                        sociedad.total = (total * tipo_de_cambio_final).quantize(Decimal('0.01'))

                    cotizacion_sociedad.append(sociedad)

            for sociedad in cotizacion_sociedad:
                cuentas = CuentaBancariaSociedad.objects.filter(
                    sociedad=sociedad,
                    moneda=moneda,
                    efectivo=False,
                    estado=1,
                    )
                sociedad.cuentas = cuentas
            moneda.sociedades = cotizacion_sociedad

        context = super(CotizacionVentaResumenView, self).get_context_data(**kwargs)
        context['monedas'] = monedas
        context['titulo'] = f'Resumen a Depositar: {self.object}'
        return context
    

#################################################################################################################

class ConfirmacionListView(PermissionRequiredMixin, FormView):
    permission_required = ('cotizacion.view_confirmacionventa')
    template_name = 'cotizacion/confirmacion/inicio.html'
    form_class = ConfirmacionVentaBuscarForm
    success_url = '.'
    
    def get_form_kwargs(self):
        kwargs = super(ConfirmacionListView, self).get_form_kwargs()
        kwargs['filtro_estado'] = self.request.GET.get('estado')
        kwargs['filtro_cliente'] = self.request.GET.get('cliente')
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(ConfirmacionListView, self).get_context_data(**kwargs)
        contexto_cotizacion_venta = ConfirmacionVenta.objects.exclude(estado=3)
        try:
            contexto_cotizacion_venta = contexto_cotizacion_venta.filter(cotizacion_venta__id = self.kwargs['id_cotizacion'])
        except:
            pass
        
        filtro_estado = self.request.GET.get('estado')
        filtro_cliente = self.request.GET.get('cliente')

        contexto_filtro = []

        if filtro_estado:
            condicion = Q(estado = filtro_estado)
            contexto_cotizacion_venta = contexto_cotizacion_venta.filter(condicion)
            contexto_filtro.append("estado=" + filtro_estado)
        if filtro_cliente:
            condicion = Q(cliente = filtro_cliente)
            contexto_cotizacion_venta = contexto_cotizacion_venta.filter(condicion)
            contexto_filtro.append("cliente=" + filtro_cliente)
        
        context['contexto_filtro'] = "&".join(contexto_filtro)

        context['pagina_filtro'] = ""
        if self.request.GET.get('page'):
            if context['contexto_filtro']:
                context['pagina_filtro'] = f'&page={self.request.GET.get("page")}'
            else:
                context['pagina_filtro'] = f'page={self.request.GET.get("page")}'
        context['contexto_filtro'] = '?' + context['contexto_filtro']

        objectsxpage =  10 # Show 10 objects per page.

        if len(contexto_cotizacion_venta) > objectsxpage:
            paginator = Paginator(contexto_cotizacion_venta, objectsxpage)
            page_number = self.request.GET.get('page')
            contexto_cotizacion_venta = paginator.get_page(page_number)

        context['contexto_cotizacion_venta'] = contexto_cotizacion_venta
        context['contexto_pagina'] = contexto_cotizacion_venta
        return context


class ConfirmarVerView(PermissionRequiredMixin, TemplateView):
    permission_required = ('cotizacion.view_confirmacionventa')
    template_name = "cotizacion/confirmacion/detalle.html"
    
    def get_context_data(self, **kwargs):
        obj = ConfirmacionVenta.objects.get(id = kwargs['id_confirmacion'])
        
        try:
            if obj.cotizacion_venta.SolicitudCredito_cotizacion_venta.estado == 3:
                credito_temporal = obj.cotizacion_venta.SolicitudCredito_cotizacion_venta.total_credito
            else:
                credito_temporal = Decimal('0.00')
        except:
            credito_temporal = Decimal('0.00')
        disponible = obj.cliente.disponible_monto + credito_temporal
        if disponible < 0:
            disponible = Decimal('0.00')

        materiales = None
        try:
            materiales = obj.ConfirmacionVentaDetalle_confirmacion_venta.all()

            for material in materiales:
                material.material = material.content_type.get_object_for_this_type(id = material.id_registro)
        except:
            pass

        id_factura = None
        id_factura_anticipo = None
        if len(obj.FacturaVenta_confirmacion.exclude(estado=3)) == 1:
            id_factura = obj.FacturaVenta_confirmacion.exclude(estado=3)[0].id
        elif len(obj.FacturaVenta_confirmacion.exclude(estado=3)) == 2:
            id_factura = obj.FacturaVenta_confirmacion.exclude(estado=3).latest('updated_at').id
            id_factura_anticipo = obj.FacturaVenta_confirmacion.exclude(estado=3).earliest('updated_at').id
        id_boleta = None
        if len(obj.BoletaVenta_confirmacion.exclude(estado=3)) == 1:
            id_boleta = obj.BoletaVenta_confirmacion.exclude(estado=3)[0].id
        permiso_venta = False
        if 'cotizacion.add_confirmacionventa' in self.request.user.get_all_permissions():
            permiso_venta = True
        permiso_logistica = False
        if 'logistica.add_notasalida' in self.request.user.get_all_permissions():
            permiso_logistica = True

        context = super(ConfirmarVerView, self).get_context_data(**kwargs)
        context['confirmacion'] = obj
        context['cotizacion'] = obj.cotizacion_venta
        context['materiales'] = materiales
        context['tipo_cambio'] = obj.tipo_cambio.tipo_cambio_venta
        context['totales'] = obtener_totales(obj)
        context['totales_soles'] = obtener_totales_soles(context['totales'], obj.tipo_cambio.tipo_cambio_venta)
        context['credito_temporal'] = credito_temporal
        context['disponible'] = disponible
        context['id_factura'] = id_factura
        context['id_factura_anticipo'] = id_factura_anticipo
        context['id_boleta'] = id_boleta
        context['permiso_venta'] = permiso_venta
        context['permiso_logistica'] = permiso_logistica
        
        return context


def ConfirmarVerTabla(request, id_confirmacion):
    data = dict()
    if request.method == 'GET':
        template = 'cotizacion/confirmacion/detalle_tabla.html'
        obj = ConfirmacionVenta.objects.get(id=id_confirmacion)

        try:
            if obj.cotizacion_venta.SolicitudCredito_cotizacion_venta.estado == 3:
                credito_temporal = obj.cotizacion_venta.SolicitudCredito_cotizacion_venta.total_credito
            else:
                credito_temporal = Decimal('0.00')
        except:
            credito_temporal = Decimal('0.00')
        disponible = obj.cliente.disponible_monto + credito_temporal
        if disponible < 0:
            disponible = Decimal('0.00')
        
        materiales = None
        try:
            materiales = obj.ConfirmacionVentaDetalle_confirmacion_venta.all()

            for material in materiales:
                material.material = material.content_type.get_object_for_this_type(id = material.id_registro)
        except:
            pass
        
        id_factura = None
        id_factura_anticipo = None
        if len(obj.FacturaVenta_confirmacion.exclude(estado=3)) == 1:
            id_factura = obj.FacturaVenta_confirmacion.exclude(estado=3)[0].id
        elif len(obj.FacturaVenta_confirmacion.exclude(estado=3)) == 2:
            id_factura = obj.FacturaVenta_confirmacion.exclude(estado=3).latest('updated_at').id
            id_factura_anticipo = obj.FacturaVenta_confirmacion.exclude(estado=3).earliest('updated_at').id
        id_boleta = None
        if len(obj.BoletaVenta_confirmacion.exclude(estado=3)) == 1:
            id_boleta = obj.BoletaVenta_confirmacion.exclude(estado=3)[0].id
        permiso_venta = False
        if 'cotizacion.add_confirmacionventa' in request.user.get_all_permissions():
            permiso_venta = True
        permiso_logistica = False
        if 'logistica.add_notasalida' in request.user.get_all_permissions():
            permiso_logistica = True

        context = {}
        context['confirmacion'] = obj
        context['cotizacion'] = obj.cotizacion_venta
        context['materiales'] = materiales
        context['tipo_cambio'] = obj.tipo_cambio.tipo_cambio_venta
        context['totales'] = obtener_totales(obj)
        context['totales_soles'] = obtener_totales_soles(context['totales'], obj.tipo_cambio.tipo_cambio_venta)
        context['credito_temporal'] = credito_temporal
        context['disponible'] = disponible
        context['id_factura'] = id_factura
        context['id_factura_anticipo'] = id_factura_anticipo
        context['id_boleta'] = id_boleta
        context['permiso_venta'] = permiso_venta
        context['permiso_logistica'] = permiso_logistica

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)


class ConfirmacionPendienteSalidaView(PermissionRequiredMixin, FormView):
    permission_required = ('cotizacion.view_confirmacionventa')
    template_name = 'cotizacion/confirmacion/pendiente_salida.html'
    form_class = ConfirmacionVentaBuscarForm
    success_url = '.'
    
    def get_form_kwargs(self):
        kwargs = super(ConfirmacionPendienteSalidaView, self).get_form_kwargs()
        kwargs['filtro_estado'] = self.request.GET.get('estado')
        kwargs['filtro_cliente'] = self.request.GET.get('cliente')
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(ConfirmacionPendienteSalidaView, self).get_context_data(**kwargs)
        contexto_cotizacion_venta = ConfirmacionVenta.objects.filter(Q(estado=1) | Q(estado=2))

        context['contexto_cotizacion_venta'] = contexto_cotizacion_venta
        filtro_estado = self.request.GET.get('estado')
        filtro_cliente = self.request.GET.get('cliente')

        contexto_filtro = []

        if filtro_estado:
            condicion = Q(estado = filtro_estado)
            contexto_cotizacion_venta = contexto_cotizacion_venta.filter(condicion)
            contexto_filtro.append("estado=" + filtro_estado)
        if filtro_cliente:
            condicion = Q(cliente = filtro_cliente)
            contexto_cotizacion_venta = contexto_cotizacion_venta.filter(condicion)
            contexto_filtro.append("cliente=" + filtro_cliente)
        
        context['contexto_filtro'] = "&".join(contexto_filtro)

        context['pagina_filtro'] = ""
        if self.request.GET.get('page'):
            if context['contexto_filtro']:
                context['pagina_filtro'] = f'&page={self.request.GET.get("page")}'
            else:
                context['pagina_filtro'] = f'page={self.request.GET.get("page")}'
        context['contexto_filtro'] = '?' + context['contexto_filtro']

        objectsxpage =  10 # Show 10 objects per page.

        if len(contexto_cotizacion_venta) > objectsxpage:
            paginator = Paginator(contexto_cotizacion_venta, objectsxpage)
            page_number = self.request.GET.get('page')
            contexto_cotizacion_venta = paginator.get_page(page_number)

        context['contexto_cotizacion_venta'] = contexto_cotizacion_venta
        context['contexto_pagina'] = contexto_cotizacion_venta
        return context


class ConfirmacionVentaFormaPagoView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('cotizacion.change_confirmacionventa')
    model = ConfirmacionVenta
    template_name = "cotizacion/confirmacion/form_forma_pago.html"
    form_class = ConfirmacionVentaFormaPagoForm
    success_url = reverse_lazy('cotizacion_app:cotizacion_venta_inicio')

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)
    
    @transaction.atomic
    def form_valid(self, form):
        sid = transaction.savepoint()
        try:
            if form.instance.tipo_venta == 1:
                for cuota in form.instance.ConfirmacionVentaCuota_confirmacion_venta.all():
                    cuota.delete()
            registro_guardar(form.instance, self.request)

            return super().form_valid(form)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(ConfirmacionVentaFormaPagoView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        context['titulo'] = "Forma de Pago"
        context['forma'] = self.object.cliente.linea_credito_condiciones_pago
        return context


class ConfirmacionClienteView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('cotizacion.change_confirmacionventa')
    model = ConfirmacionVenta
    template_name = "cotizacion/cotizacion_venta/form_cliente.html"
    form_class = ConfirmacionClienteForm
    success_url = reverse_lazy('cotizacion_app:cotizacion_venta_inicio')

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        if form.instance.cliente.linea_credito_monto == 0:
            form.instance.tipo_venta = 1
            form.instance.condiciones_pago = None
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        cotizacion = kwargs['instance']
        lista = []
        relaciones = ClienteInterlocutor.objects.filter(cliente = cotizacion.cliente)
        for relacion in relaciones:
            lista.append(relacion.interlocutor.id)

        kwargs['interlocutor_queryset'] = InterlocutorCliente.objects.filter(id__in = lista)
        kwargs['interlocutor'] = cotizacion.cliente_interlocutor
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(ConfirmacionClienteView, self).get_context_data(**kwargs)
        context['accion'] = "Elegir"
        context['titulo'] = "Cliente"
        return context


class ConfirmacionVentaVerCuotaView(PermissionRequiredMixin, BSModalReadView):
    permission_required = ('cotizacion.view_confirmacionventa')
    model = ConfirmacionVenta
    template_name = "cotizacion/confirmacion/modal cuotas.html"

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super(ConfirmacionVentaVerCuotaView, self).get_context_data(**kwargs)
        confirmacion = self.object
        total = confirmacion.ConfirmacionVentaCuota_confirmacion_venta.all().aggregate(Sum('monto'))['monto__sum']
        try:
            if confirmacion.cotizacion_venta.SolicitudCredito_cotizacion_venta.estado == 3:
                credito_temporal = confirmacion.cotizacion_venta.SolicitudCredito_cotizacion_venta.total_credito
            else:
                credito_temporal = Decimal('0.00')
        except:
            credito_temporal = Decimal('0.00')
        disponible = confirmacion.cliente.disponible_monto + credito_temporal
        if disponible < 0:
            disponible = Decimal('0.00')
        context['confirmacion'] = confirmacion
        context['credito_temporal'] = credito_temporal
        context['disponible'] = disponible
        context['total'] = total
        context['titulo'] = 'Cuotas'
        return context


class ConfirmacionVentaCuotaView(PermissionRequiredMixin, TemplateView):
    permission_required = ('cotizacion.view_confirmacionventa')
    template_name = "cotizacion/confirmacion/cuotas.html"
    
    def get_context_data(self, **kwargs):
        context = super(ConfirmacionVentaCuotaView, self).get_context_data(**kwargs)
        confirmacion = ConfirmacionVenta.objects.get(id=self.kwargs['id_confirmacion'])
        total = confirmacion.ConfirmacionVentaCuota_confirmacion_venta.all().aggregate(Sum('monto'))['monto__sum']
        try:
            if confirmacion.cotizacion_venta.SolicitudCredito_cotizacion_venta.estado == 3:
                credito_temporal = confirmacion.cotizacion_venta.SolicitudCredito_cotizacion_venta.total_credito
            else:
                credito_temporal = Decimal('0.00')
        except:
            credito_temporal = Decimal('0.00')
        disponible = confirmacion.cliente.disponible_monto + credito_temporal
        if disponible < 0:
            disponible = Decimal('0.00')
        context['confirmacion'] = confirmacion
        context['credito_temporal'] = credito_temporal
        context['disponible'] = disponible
        context['total'] = total
        return context


def ConfirmacionVentaCuotaTabla(request, id_confirmacion):
    data = dict()
    if request.method == 'GET':
        template = "cotizacion/confirmacion/cuotas_tabla.html"
        context = {}
        confirmacion = ConfirmacionVenta.objects.get(id=id_confirmacion)
        total = confirmacion.ConfirmacionVentaCuota_confirmacion_venta.all().aggregate(Sum('monto'))['monto__sum']
        try:
            if confirmacion.cotizacion_venta.SolicitudCredito_cotizacion_venta.estado == 3:
                credito_temporal = confirmacion.cotizacion_venta.SolicitudCredito_cotizacion_venta.total_credito
            else:
                credito_temporal = Decimal('0.00')
        except:
            credito_temporal = Decimal('0.00')
        disponible = confirmacion.cliente.disponible_monto + credito_temporal
        if disponible < 0:
            disponible = Decimal('0.00')
        context['confirmacion'] = confirmacion
        context['credito_temporal'] = credito_temporal
        context['disponible'] = disponible
        context['total'] = total
        
        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)


class ConfirmacionVentaGenerarCuotasFormView(PermissionRequiredMixin, BSModalFormView):
    permission_required = ('cotizacion.change_confirmacionventa')
    template_name = "includes/formulario generico.html"
    form_class = ConfirmacionVentaGenerarCuotasForm

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)
    
    def get_success_url(self) -> str:
        return reverse_lazy('cotizacion_app:confirmacion_ver', kwargs={'id_confirmacion': self.kwargs['id_confirmacion']})

    @transaction.atomic
    def form_valid(self, form):
        sid = transaction.savepoint()
        try:
            if self.request.session['primero']:
                confirmacion_venta = ConfirmacionVenta.objects.get(id=self.kwargs['id_confirmacion'])
                monto_total = form.cleaned_data['monto_total']
                numero_cuotas = form.cleaned_data['numero_cuotas']
                intervalo_cuotas = form.cleaned_data['intervalo_cuotas']
                dias_pago = 0
                suma = 0
                for i in range(numero_cuotas):
                    if i+1 == numero_cuotas:
                        monto = monto_total - suma
                    else:
                        monto = (monto_total/numero_cuotas).quantize(Decimal('0.01'))
                    suma += monto
                    dias_pago += intervalo_cuotas
                    ConfirmacionVentaCuota.objects.create(
                        confirmacion_venta = confirmacion_venta,
                        monto = monto,
                        dias_pago = dias_pago,
                        fecha_pago = None,
                        dias_calculo = None,
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
        context = super(ConfirmacionVentaGenerarCuotasFormView, self).get_context_data(**kwargs)
        context['accion'] = "Generar"
        context['titulo'] = "Cuotas"
        return context


class ConfirmacionVentaCuotaCreateView(PermissionRequiredMixin, BSModalCreateView):
    permission_required = ('cotizacion.change_confirmacionventa')
    model = ConfirmacionVentaCuota
    template_name = "cotizacion/cotizacion_venta/form_cuotas.html"
    form_class = ConfirmacionVentaCuotaForm
    success_url = '.'

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        form.instance.confirmacion_venta = ConfirmacionVenta.objects.get(id=self.kwargs['id_confirmacion'])
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        obj = ConfirmacionVenta.objects.get(id=self.kwargs['id_confirmacion'])
        solicitado = obj.monto_solicitado
        if obj.ConfirmacionVentaCuota_confirmacion_venta.all():
            suma = obj.ConfirmacionVentaCuota_confirmacion_venta.all().aggregate(Sum('monto'))['monto__sum']
        else:
            suma = Decimal('0.00')
        context = super(ConfirmacionVentaCuotaCreateView, self).get_context_data(**kwargs)
        context['accion'] = "Agregar"
        context['titulo'] = "Cuota"
        context['saldo'] = solicitado - suma
        return context
    

class ConfirmacionVentaCuotaUpdateView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('cotizacion.change_confirmacionventa')
    model = ConfirmacionVentaCuota
    template_name = "cotizacion/cotizacion_venta/form_cuotas.html"
    form_class = ConfirmacionVentaCuotaForm
    success_url = '.'

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        obj = self.object.confirmacion_venta
        solicitado = obj.monto_solicitado
        suma = obj.ConfirmacionVentaCuota_confirmacion_venta.exclude(id=self.object.id).aggregate(Sum('monto'))['monto__sum']
        if not suma:
            suma = Decimal('0.00')
        context = super(ConfirmacionVentaCuotaUpdateView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        context['titulo'] = "Cuota"
        context['saldo'] = solicitado - suma
        return context
    

class ConfirmacionVentaCuotaDeleteView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('cotizacion.change_confirmacionventa')
    model = ConfirmacionVentaCuota
    template_name = "includes/eliminar generico.html"

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('cotizacion_app:confirmacion_cuotas', kwargs={'id_confirmacion':self.get_object().confirmacion_venta.id})
    
    def get_context_data(self, **kwargs):
        context = super(ConfirmacionVentaCuotaDeleteView, self).get_context_data(**kwargs)
        context['accion'] = "Eliminar"
        context['titulo'] = "Cuota"
        context['item'] = self.get_object()
        return context
    

class ConfirmacionVentaOrdenCompraCrearView(PermissionRequiredMixin, BSModalCreateView):
    permission_required = ('cotizacion.change_confirmacionventa')
    model = ConfirmacionOrdenCompra
    template_name = "includes/formulario generico.html"
    form_class = ConfirmacionOrdenCompraForm

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('cotizacion_app:confirmacion_ver', kwargs={'id_confirmacion':self.kwargs['id_confirmacion']})

    def form_valid(self, form):
        form.instance.confirmacion_venta = ConfirmacionVenta.objects.get(id = self.kwargs['id_confirmacion'])
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super(ConfirmacionVentaOrdenCompraCrearView, self).get_context_data(**kwargs)
        context['accion'] = "Guardar"
        context['titulo'] = "Orden de Compra"
        return context


class ConfirmacionVentaOrdenCompraActualizarView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('cotizacion.change_confirmacionventa')
    model = ConfirmacionOrdenCompra
    template_name = "includes/formulario generico.html"
    form_class = ConfirmacionOrdenCompraForm

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('cotizacion_app:confirmacion_ver', kwargs={'id_confirmacion':self.kwargs['id_confirmacion']})

    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super(ConfirmacionVentaOrdenCompraActualizarView, self).get_context_data(**kwargs)
        context['accion'] = "Guardar"
        context['titulo'] = "Orden de Compra"
        return context


class ConfirmacionOrdenCompraDeleteView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('cotizacion.change_confirmacionventa')
    model = ConfirmacionOrdenCompra
    template_name = "includes/eliminar generico.html"

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('cotizacion_app:confirmacion_ver', kwargs={'id_confirmacion':self.kwargs['id_confirmacion']})

    def get_context_data(self, **kwargs):
        context = super(ConfirmacionOrdenCompraDeleteView, self).get_context_data(**kwargs)
        context['accion'] = "Eliminar"
        context['titulo'] = "Orden de Compra"
        context['item'] = self.get_object()
        return context

class SolicitudCreditoView(PermissionRequiredMixin, TemplateView):
    permission_required = ('cobranza.add_solicitudcredito')
    template_name = "cotizacion/cotizacion_venta/form_solicitud_credito.html"
    
    def get_context_data(self, **kwargs):
        context = super(SolicitudCreditoView, self).get_context_data(**kwargs)
        cotizacion = CotizacionVenta.objects.get(id=self.kwargs['id_cotizacion'])
        solicitud_credito, created = SolicitudCredito.objects.get_or_create(cotizacion_venta=cotizacion)
        if created:
            solicitud_credito.total_cotizado = cotizacion.total
            solicitud_credito.interlocutor_solicita = cotizacion.cliente_interlocutor
            solicitud_credito.save()
        total = cotizacion.monto_solicitado

        context['cotizacion'] = cotizacion
        context['total'] = total
        return context


def SolicitudCreditoTabla(request, id_cotizacion):
    data = dict()
    if request.method == 'GET':
        template = "cotizacion/cotizacion_venta/form_solicitud_credito_tabla.html"
        context = {}
        cotizacion = CotizacionVenta.objects.get(id=id_cotizacion)
        total = cotizacion.monto_solicitado
        context['cotizacion'] = cotizacion
        context['total'] = total
        
        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)
    

class SolicitudCreditoUpdateView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('cobranza.change_solicitudcredito')
    model = SolicitudCredito
    template_name = "includes/formulario generico.html"
    form_class = SolicitudCreditoForm
    success_url = '.'

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(SolicitudCreditoUpdateView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        context['titulo'] = "Solicitud de Crédito"
        return context


class SolicitudCreditoEliminarView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('cobranza.change_solicitudcredito')
    model = SolicitudCredito
    template_name = "includes/form generico.html"

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('cotizacion_app:cotizacion_venta_ver', kwargs={'id_cotizacion':self.object.cotizacion_venta.id})

    def get_context_data(self, **kwargs):
        context = super(SolicitudCreditoEliminarView, self).get_context_data(**kwargs)
        context['accion'] = "Eliminar"
        context['titulo'] = "Solicitud de Crédito"
        context['texto'] = "¿Está seguro de Eliminar la Solicitud de Crédito?"
        context['item'] = "%s" % (self.object)
        return context
    

class SolicitudCreditoGenerarCuotasFormView(PermissionRequiredMixin, BSModalFormView):
    permission_required = ('cobranza.change_solicitudcredito')
    template_name = "includes/formulario generico.html"
    form_class = ConfirmacionVentaGenerarCuotasForm

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)
    
    def get_success_url(self) -> str:
        solicitud = SolicitudCredito.objects.get(id=self.kwargs['id_solicitud'])
        return reverse_lazy('cotizacion_app:cotizacion_venta_ver', kwargs={'id_cotizacion': solicitud.cotizacion_venta.id})

    @transaction.atomic
    def form_valid(self, form):
        sid = transaction.savepoint()
        try:
            if self.request.session['primero']:
                solicitud = SolicitudCredito.objects.get(id=self.kwargs['id_solicitud'])
                monto_total = form.cleaned_data['monto_total']
                numero_cuotas = form.cleaned_data['numero_cuotas']
                intervalo_cuotas = form.cleaned_data['intervalo_cuotas']
                dias_pago = 0
                suma = 0
                for i in range(numero_cuotas):
                    if i+1 == numero_cuotas:
                        monto = monto_total - suma
                    else:
                        monto = (monto_total/numero_cuotas).quantize(Decimal('0.01'))
                    suma += monto
                    dias_pago += intervalo_cuotas
                    SolicitudCreditoCuota.objects.create(
                        solicitud_credito = solicitud,
                        monto = monto,
                        dias_pago = dias_pago,
                        fecha_pago = None,
                        dias_calculo = None,
                        fecha_calculo = None,
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
        context = super(SolicitudCreditoGenerarCuotasFormView, self).get_context_data(**kwargs)
        context['accion'] = "Generar"
        context['titulo'] = "Cuotas"
        return context


class SolicitudCreditoCuotaCreateView(PermissionRequiredMixin, BSModalCreateView):
    permission_required = ('cobranza.change_solicitudcredito')
    model = SolicitudCreditoCuota
    template_name = "cotizacion/cotizacion_venta/form_cuotas.html"
    form_class = SolicitudCreditoCuotaForm
    success_url = '.'

    def dispatch(self, request, *args, **kwargs):
        obj = SolicitudCredito.objects.get(id=self.kwargs['id_solicitud'])
        solicitado = obj.total_credito
        if obj.SolicitudCreditoCuota_solicitud_credito.all():
            suma = obj.SolicitudCreditoCuota_solicitud_credito.all().aggregate(Sum('monto'))['monto__sum']
        else:
            suma = Decimal('0.00')
        self.saldo = solicitado - suma
        context = {}
        error_saldo = False
        context['titulo'] = 'Error de guardar'
        if self.saldo == 0:
            error_saldo = True

        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        if error_saldo:
            context['texto'] = 'No hay saldo para agregar más cuotas.'
            return render(request, 'includes/modal sin permiso.html', context)
        return super(SolicitudCreditoCuotaCreateView, self).dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        form.instance.solicitud_credito = SolicitudCredito.objects.get(id=self.kwargs['id_solicitud'])
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(SolicitudCreditoCuotaCreateView, self).get_context_data(**kwargs)
        context['accion'] = "Agregar"
        context['titulo'] = "Cuota"
        context['saldo'] = self.saldo
        return context
    

class SolicitudCreditoCuotaUpdateView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('cobranza.change_solicitudcredito')
    model = SolicitudCreditoCuota
    template_name = "cotizacion/cotizacion_venta/form_cuotas.html"
    form_class = SolicitudCreditoCuotaForm
    success_url = '.'

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        obj = self.object.solicitud_credito
        solicitado = obj.total_credito
        suma = obj.SolicitudCreditoCuota_solicitud_credito.exclude(id=self.object.id).aggregate(Sum('monto'))['monto__sum']
        if not suma:
            suma = Decimal('0.00')
        context = super(SolicitudCreditoCuotaUpdateView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        context['titulo'] = "Cuota"
        context['saldo'] = solicitado - suma
        return context
    

class SolicitudCreditoCuotaDeleteView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('cobranza.change_solicitudcredito')
    model = SolicitudCreditoCuota
    template_name = "includes/eliminar generico.html"

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('cotizacion_app:solicitud_credito', kwargs={'id_cotizacion':self.get_object().solicitud_credito.cotizacion_venta.id})
    
    def get_context_data(self, **kwargs):
        context = super(SolicitudCreditoCuotaDeleteView, self).get_context_data(**kwargs)
        context['accion'] = "Eliminar"
        context['titulo'] = "Cuota"
        context['item'] = self.get_object()
        return context


class SolicitudCreditoFinalizarView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('cobranza.change_solicitudcredito')
    model = SolicitudCredito
    template_name = "includes/form generico.html" 

    def dispatch(self, request, *args, **kwargs):
        context = {}
        error_cuotas = False
        context['titulo'] = 'Error de guardar'
        if self.get_object().total_cuotas == 0 or self.get_object().total_cuotas != self.get_object().total_credito:
            error_cuotas = True

        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        if error_cuotas:
            context['texto'] = 'El total de las cuotas no coincide con el monto solicitado.'
            return render(request, 'includes/modal sin permiso.html', context)
        return super(SolicitudCreditoFinalizarView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('cotizacion_app:solicitud_credito', kwargs={'id_cotizacion':self.get_object().cotizacion_venta.id})

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            self.object = self.get_object()
            self.object.estado = 2
            registro_guardar(self.object, request)
            self.object.save()
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(SolicitudCreditoFinalizarView, self).get_context_data(**kwargs)
        context['accion'] = "Finalizar"
        context['titulo'] = "Solicitud de crédito"
        context['texto'] = "¿Está seguro de Finalizar la Solicitud de crédito?"
        context['item'] = self.object
        return context


class SolicitudCreditoAprobarView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('cobranza.aprobar_solicitudcredito')
    model = SolicitudCredito
    template_name = "includes/form generico.html" 

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('cotizacion_app:solicitud_credito', kwargs={'id_cotizacion':self.get_object().cotizacion_venta.id})

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            self.object = self.get_object()
            self.object.estado = 3
            self.object.aprobado_por = request.user
            registro_guardar(self.object, request)
            self.object.save()
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(SolicitudCreditoAprobarView, self).get_context_data(**kwargs)
        context['accion'] = "Aprobar"
        context['titulo'] = "Solicitud de crédito"
        context['texto'] = "¿Está seguro de Aprobar la Solicitud de crédito?"
        context['item'] = self.object
        return context


class SolicitudCreditoRechazarView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('cobranza.aprobar_solicitudcredito')
    model = SolicitudCredito
    template_name = "includes/form generico.html" 

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('cotizacion_app:solicitud_credito', kwargs={'id_cotizacion':self.get_object().cotizacion_venta.id})

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            self.object = self.get_object()
            self.object.estado = 4
            registro_guardar(self.object, request)
            self.object.save()
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(SolicitudCreditoRechazarView, self).get_context_data(**kwargs)
        context['accion'] = "Rechazar"
        context['titulo'] = "Solicitud de crédito"
        context['texto'] = "¿Está seguro de Rechazar la Solicitud de crédito?"
        context['item'] = self.object
        return context


class ConfirmacionNotaSalidaView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('logistica.add_notasalida')
    model = ConfirmacionVenta
    template_name = "logistica/solicitud_prestamo_materiales/boton.html"
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('logistica_app:nota_salida_detalle', kwargs={'pk':self.nota_salida.id})

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        item = len(NotaSalida.objects.all())
        try:
            if self.request.session['primero']:
                self.object = self.get_object()
                confirmacion_venta = self.get_object()
                nota_salida = NotaSalida.objects.create(
                    numero_salida=item + 1,
                    confirmacion_venta=confirmacion_venta,
                    observacion_adicional=confirmacion_venta.observacion_adicional,
                    motivo_anulacion="",
                    created_by=self.request.user,
                    updated_by=self.request.user,
                )

                self.request.session['primero'] = False
                registro_guardar(self.object, self.request)
                self.object.save()
                messages.success(request, MENSAJE_GENERAR_NOTA_SALIDA)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        self.nota_salida = nota_salida
        return HttpResponseRedirect(reverse_lazy('logistica_app:nota_salida_detalle', kwargs={'pk': nota_salida.id}))

    def get_context_data(self, **kwargs):
        self.request.session['primero'] = True
        context = super(ConfirmacionNotaSalidaView, self).get_context_data(**kwargs)
        context['accion'] = "Generar"
        context['titulo'] = "Nota Salida"
        context['dar_baja'] = "true"
        return context