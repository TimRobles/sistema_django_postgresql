from decimal import Decimal
from django.shortcuts import render
from django import forms
from applications.importaciones import *
from applications.clientes.models import ClienteInterlocutor, InterlocutorCliente
from applications.datos_globales.models import TipoCambio
from applications.material.funciones import calidad, observacion, reservado, stock, vendible
from applications.movimiento_almacen.models import MovimientosAlmacen, TipoMovimiento
from applications.cotizacion.pdf import generarCotizacionVenta
from applications.funciones import calculos_linea, igv, numeroXn, obtener_totales, obtener_totales_soles, slug_aleatorio, tipo_de_cambio

from applications.sociedad.models import Sociedad

from applications.orden_compra.models import OrdenCompraDetalle
from applications.recepcion_compra.models import RecepcionCompra

from .forms import (
    CotizacionVentaClienteForm,
    CotizacionVentaDescuentoGlobalForm,
    CotizacionVentaDetalleForm,
    CotizacionVentaForm,
    CotizacionVentaMaterialDetalleForm,
    CotizacionVentaMaterialDetalleUpdateForm,
    CotizacionVentaObservacionForm,
    PrecioListaMaterialForm,
)

from .models import (
    CotizacionDescuentoGlobal,
    CotizacionObservacion,
    CotizacionSociedad,
    CotizacionTerminosCondiciones,
    CotizacionVenta,
    CotizacionVentaDetalle,
    PrecioListaMaterial,
)


class CotizacionVentaListView(ListView):
    model = CotizacionVenta
    template_name = ('cotizacion/cotizacion_venta/inicio.html')
    context_object_name = 'contexto_cotizacion_venta'

def CotizacionVentaTabla(request):
    data = dict()
    if request.method == 'GET':
        template = 'cotizacion/cotizacion_venta/inicio_tabla.html'
        context = {}
        context['contexto_cotizacion_venta'] = CotizacionVenta.objects.all()

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)


def CotizacionVentaCreateView(request):
    obj = CotizacionVenta.objects.create(
        slug = slug_aleatorio(CotizacionVenta),
        created_by=request.user,
        updated_by=request.user,
    )
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
    return HttpResponseRedirect(reverse_lazy('cotizacion_app:cotizacion_venta_ver', kwargs={'id_cotizacion':obj.id}))


class CotizacionVentaVerView(TemplateView):
    template_name = "cotizacion/cotizacion_venta/detalle.html"

    def get_context_data(self, **kwargs):
        obj = CotizacionVenta.objects.get(id = kwargs['id_cotizacion'])
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

        context = super(CotizacionVentaVerView, self).get_context_data(**kwargs)
        context['cotizacion'] = obj
        context['materiales'] = materiales
        context['tipo_cambio_hoy'] = tipo_cambio_hoy
        context['tipo_cambio'] = tipo_cambio
        context['totales'] = obtener_totales(CotizacionVenta.objects.get(id=self.kwargs['id_cotizacion']))
        tipo_cambio = tipo_de_cambio(tipo_cambio, tipo_cambio_hoy)
        context['totales_soles'] = obtener_totales_soles(context['totales'], tipo_cambio)
        context['sociedades'] = sociedades

        return context


def CotizacionVentaVerTabla(request, id_cotizacion):
    data = dict()
    if request.method == 'GET':
        template = 'cotizacion/cotizacion_venta/detalle_tabla.html'
        obj = CotizacionVenta.objects.get(id=id_cotizacion)
        tipo_cambio_hoy = TipoCambio.objects.tipo_cambio_venta(date.today())
        tipo_cambio = TipoCambio.objects.tipo_cambio_venta(obj.fecha_cotizacion)
        
        materiales = None
        try:
            materiales = obj.CotizacionVentaDetalle_cotizacion_venta.all()

            for material in materiales:
                material.material = material.content_type.get_object_for_this_type(id = material.id_registro)
        except:
            pass

        sociedades = Sociedad.objects.all()

        context = {}
        context['materiales'] = materiales
        context['cotizacion'] = obj
        context['tipo_cambio_hoy'] = tipo_cambio_hoy
        context['tipo_cambio'] = tipo_cambio
        context['totales'] = obtener_totales(obj)
        tipo_cambio = tipo_de_cambio(tipo_cambio, tipo_cambio_hoy)
        context['totales_soles'] = obtener_totales_soles(context['totales'], tipo_cambio)
        context['sociedades'] = sociedades

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)


class CotizacionVentaClienteView(BSModalUpdateView):
    model = CotizacionVenta
    template_name = "cotizacion/cotizacion_venta/form_cliente.html"
    form_class = CotizacionVentaClienteForm
    success_url = reverse_lazy('cotizacion_app:cotizacion_venta_inicio')

    def form_valid(self, form):
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


class CotizacionVentaMaterialDetalleView(BSModalFormView):
    template_name = "cotizacion/cotizacion_venta/form_material.html"
    form_class = CotizacionVentaMaterialDetalleForm
    success_url = reverse_lazy('cotizacion_app:cotizacion_venta_inicio')

    def form_valid(self, form):

        if self.request.session['primero']:
            cotizacion = CotizacionVenta.objects.get(id = self.kwargs['cotizacion_id'])
            item = len(CotizacionVentaDetalle.objects.filter(cotizacion_venta = cotizacion))

            material = form.cleaned_data.get('material')
            cantidad = form.cleaned_data.get('cantidad')

            obj, created = CotizacionVentaDetalle.objects.get_or_create(
                content_type = ContentType.objects.get_for_model(material),
                id_registro = material.id,
                cotizacion_venta = cotizacion,
            )
            if created:
                obj.item = item + 1
                obj.cantidad = cantidad
                try:
                    precio_unitario_con_igv = material.precio_lista.precio_lista
                    precio_final_con_igv = material.precio_lista.precio_lista
                except:
                    precio_unitario_con_igv = 0
                    precio_final_con_igv = 0

                respuesta = calculos_linea(cantidad, precio_unitario_con_igv, precio_final_con_igv, 0.18)
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
                respuesta = calculos_linea(obj.cantidad, precio_unitario_con_igv, precio_final_con_igv, 0.18)
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
                cantidades[sociedad.abreviatura] = stock(obj.content_type, obj.id_registro, sociedad.id)

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
        return HttpResponseRedirect(self.success_url)

    def get_context_data(self, **kwargs):
        self.request.session['primero'] = True
        context = super(CotizacionVentaMaterialDetalleView, self).get_context_data(**kwargs)
        context['titulo'] = 'Agregar'
        context['accion'] = 'Material'
        return context


class CotizacionSociedadUpdateView(BSModalUpdateView):
    model = CotizacionVentaDetalle
    template_name = "cotizacion/cotizacion_venta/form_sociedad.html"
    form_class = CotizacionVentaDetalleForm
    success_url = '.'

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


class CotizacionDescuentoGlobalUpdateView(BSModalUpdateView):
    model = CotizacionVenta
    template_name = "cotizacion/cotizacion_venta/form_descuento.html"
    form_class = CotizacionVentaDescuentoGlobalForm
    success_url = '.'

    def get_context_data(self, **kwargs):
        context = super(CotizacionDescuentoGlobalUpdateView, self).get_context_data(**kwargs)
        texto = []
        for sociedad in self.object.CotizacionDescuentoGlobal_cotizacion_venta.all():
            texto.append(str(sociedad.descuento_global))

        sociedades = Sociedad.objects.all()
        
        context['titulo'] = "Actualizar Descuento Global"
        context['url_guardar'] = reverse_lazy('cotizacion_app:guardar_cotizacion_venta_descuento_global', kwargs={'monto':1,'id_cotizacion':1,'abreviatura':"a",})[:-6]
        context['sociedades'] = sociedades
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
    obj.descuento_global = monto
    obj.save()
    return HttpResponse('Fin')


class CotizacionObservacionUpdateView(BSModalUpdateView):
    model = CotizacionVenta
    template_name = "cotizacion/cotizacion_venta/form_observacion.html"
    form_class = CotizacionVentaObservacionForm
    success_url = '.'

    def get_context_data(self, **kwargs):
        context = super(CotizacionObservacionUpdateView, self).get_context_data(**kwargs)
        texto = []
        for sociedad in self.object.CotizacionObservacion_cotizacion_venta.all():
            texto.append(str(sociedad.observacion))

        sociedades = Sociedad.objects.all()
        
        context['titulo'] = "Actualizar Observaciones"
        context['url_guardar'] = reverse_lazy('cotizacion_app:guardar_cotizacion_venta_observacion', kwargs={'texto':1,'id_cotizacion':1,'abreviatura':"a",})[:-6]
        context['sociedades'] = sociedades
        context['observaciones'] = "|".join(texto)
        context['id_cotizacion'] = self.object.id
        context['igv'] = igv()
        return context


def GuardarCotizacionObservacion(request, monto, id_cotizacion, abreviatura):
    if monto == 1 and id_cotizacion == 1 and abreviatura == 'a':
        return HttpResponse('Nada')
    cotizacion_venta = CotizacionVenta.objects.get(id=id_cotizacion)
    sociedad = Sociedad.objects.get(abreviatura = abreviatura)

    obj, created = CotizacionObservacion.objects.get_or_create(
        cotizacion_venta = cotizacion_venta,
        sociedad = sociedad,
    )
    obj.observacion = monto
    obj.save()
    return HttpResponse('Fin')


class CotizacionVentaGuardarView(BSModalDeleteView):
    model = CotizacionVenta
    template_name = "cotizacion/cotizacion_venta/form_guardar.html"

    def get_success_url(self, **kwargs):
        return reverse_lazy('cotizacion_app:cotizacion_venta_ver', kwargs={'id_cotizacion':self.object.id})

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.estado = 2
        numero_cotizacion = CotizacionVenta.objects.all().aggregate(Count('numero_cotizacion'))['numero_cotizacion__count'] + 1
        self.object.numero_cotizacion = numeroXn(numero_cotizacion, 6)
        self.object.fecha_cotizacion = datetime. now()

        registro_guardar(self.object, self.request)
        self.object.save()
        messages.success(request, MENSAJE_GUARDAR_COTIZACION)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(CotizacionVentaGuardarView, self).get_context_data(**kwargs)
        context['accion'] = "Guardar"
        context['titulo'] = "Cotización"
        context['guardar'] = "true"
        context['item'] = self.object.cliente
        return context


class CotizacionVentaCosteadorDetalleView(BSModalReadView):
    model = CotizacionVentaDetalle
    template_name = "cotizacion/cotizacion_venta/form-precio.html"

    def get_context_data(self, **kwargs):
        precios = []
        content_type = self.object.content_type
        id_registro = self.object.id_registro
        orden_detalle = OrdenCompraDetalle.objects.filter(
            content_type = content_type,
            id_registro = id_registro,
        )

        for detalle in orden_detalle:
            detalle.cantidad = detalle.ComprobanteCompraPIDetalle_orden_compra_detalle.cantidad
            detalle.precio = detalle.ComprobanteCompraPIDetalle_orden_compra_detalle.precio_final_con_igv

            comprobante_compra = detalle.ComprobanteCompraPIDetalle_orden_compra_detalle.comprobante_compra

            detalle.logistico = comprobante_compra.logistico

            recepcion = RecepcionCompra.objects.get(
                content_type = ContentType.objects.get_for_model(comprobante_compra),
                id_registro = comprobante_compra.id,
                estado = 1,
            )

            detalle.fecha_recepcion = recepcion.fecha_recepcion
            detalle.numero_comprobante_compra = recepcion.numero_comprobante_compra
            valor = "%s|%s|%s|%s" % (comprobante_compra.id, ContentType.objects.get_for_model(comprobante_compra).id, self.object.id_registro, self.object.content_type)
            precios.append((valor, recepcion.numero_comprobante_compra))


        context = super(CotizacionVentaCosteadorDetalleView, self).get_context_data(**kwargs)
        context['accion']="Costeador"
        context['titulo']="Precio"
        context['precios'] = orden_detalle
        return context

class CotizacionVentaDetalleDeleteView(BSModalDeleteView):
    model = CotizacionVentaDetalle
    template_name = "includes/eliminar generico.html"

    def get_success_url(self, **kwargs):
        return reverse_lazy('cotizacion_app:cotizacion_venta_ver', kwargs={'id_cotizacion':self.get_object().cotizacion_venta.id})

    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CotizacionVentaDetalleDeleteView, self).get_context_data(**kwargs)
        context['accion'] = "Eliminar"
        context['titulo'] = "Material"
        context['item'] = self.get_object().content_type.get_object_for_this_type(id = self.get_object().id_registro)

        return context


class CotizacionVentaMaterialDetalleUpdateView(BSModalUpdateView):
    model = CotizacionVentaDetalle
    template_name = "cotizacion/cotizacion_venta/actualizar.html"
    form_class = CotizacionVentaMaterialDetalleUpdateForm

    def get_success_url(self, **kwargs):
        return reverse_lazy('cotizacion_app:cotizacion_venta_ver', kwargs={'id_cotizacion':self.get_object().cotizacion_venta.id})

    def form_valid(self, form):
        precio_unitario_con_igv = form.instance.precio_unitario_con_igv
        precio_final_con_igv = form.instance.precio_final_con_igv
        form.instance.cantidad = form.instance.cantidad
        respuesta = calculos_linea(form.instance.cantidad, precio_unitario_con_igv, precio_final_con_igv, 0.18)
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
            cantidades[sociedad.abreviatura] = stock(form.instance.content_type, form.instance.id_registro, sociedad.id)

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

    def get_context_data(self, **kwargs):
        context = super(CotizacionVentaMaterialDetalleUpdateView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        context['titulo'] = "Precios"
        context['material'] = self.object.content_type.get_object_for_this_type(id = self.object.id_registro)
        return context


class CotizacionVentaReservaView(DeleteView):
    model = CotizacionVenta
    template_name = "includes/form generico.html"

    def get_success_url(self, **kwargs):
        return reverse_lazy('cotizacion_app:cotizacion_venta_ver', kwargs={'id_cotizacion':self.object.id})

    def delete(self, request, *args, **kwargs):
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
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(CotizacionVentaReservaView, self).get_context_data(**kwargs)
        context['accion'] = "Reservar"
        context['titulo'] = "Cotización"
        context['texto'] = "¿Está seguro de Reservar la cotización?"
        context['item'] = "Cotización %s - %s" % (numeroXn(self.object.numero_cotizacion, 6), self.object.cliente)
        return context


class CotizacionVentaReservaAnularView(DeleteView):
    model = CotizacionVenta
    template_name = "includes/form generico.html"

    def get_success_url(self, **kwargs):
        return reverse_lazy('cotizacion_app:cotizacion_venta_ver', kwargs={'id_cotizacion':self.object.id})

    def delete(self, request, *args, **kwargs):
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

        messages.success(request, MENSAJE_RESERVAR_COTIZACION)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(CotizacionVentaReservaAnularView, self).get_context_data(**kwargs)
        context['accion'] = "Anular"
        context['titulo'] = "Reserva de Cotización"
        context['texto'] = "¿Está seguro de Anular la Reserva de la cotización?"
        context['item'] = "Cotización %s - %s" % (numeroXn(self.object.numero_cotizacion, 6), self.object.cliente)
        return context


class CotizacionVentaConfirmarView(DeleteView):
    model = CotizacionVenta
    template_name = "includes/form generico.html"

    def get_success_url(self, **kwargs):
        return reverse_lazy('cotizacion_app:cotizacion_venta_ver', kwargs={'id_cotizacion':self.object.id})

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()

        detalles = self.object.CotizacionVentaDetalle_cotizacion_venta.all()
        print(detalles)



        # if self.object.estado == 3: #Si está reservado
        #     reserva = TipoMovimiento.objects.get(codigo=118)
        #     for detalle in detalles:
        #         sociedades = detalle.CotizacionSociedad_cotizacion_venta_detalle.all()
        #         for cotizacion_sociedad in sociedades:
        #             if cotizacion_sociedad.cantidad > 0:
        #                 movimiento_dos = MovimientosAlmacen.objects.create(
        #                         content_type_producto = detalle.content_type,
        #                         id_registro_producto = detalle.id_registro,
        #                         cantidad = cotizacion_sociedad.cantidad,
        #                         tipo_movimiento = reserva,
        #                         tipo_stock = reserva.tipo_stock_final,
        #                         signo_factor_multiplicador = +1,
        #                         content_type_documento_proceso = ContentType.objects.get_for_model(self.object),
        #                         id_registro_documento_proceso = self.object.id,
        #                         almacen = None,
        #                         sociedad = cotizacion_sociedad.sociedad,
        #                         movimiento_anterior = None,
        #                         movimiento_reversion = False,
        #                         created_by = self.request.user,
        #                         updated_by = self.request.user,
        #                     )
        #     self.object.estado = 4

        registro_guardar(self.object, self.request)
        self.object.save()

        messages.success(request, MENSAJE_RESERVAR_COTIZACION)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(CotizacionVentaConfirmarView, self).get_context_data(**kwargs)
        context['accion'] = "Confirmar"
        context['titulo'] = "Cotización"
        context['texto'] = "¿Está seguro de Confirmar la cotización?"
        context['item'] = "Cotización %s - %s" % (numeroXn(self.object.numero_cotizacion, 6), self.object.cliente)
        return context


class CotizacionVentaConfirmarAnularView(DeleteView):
    model = CotizacionVenta
    template_name = "includes/form generico.html"

    def get_success_url(self, **kwargs):
        return reverse_lazy('cotizacion_app:cotizacion_venta_ver', kwargs={'id_cotizacion':self.object.id})

    def delete(self, request, *args, **kwargs):
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

        messages.success(request, MENSAJE_RESERVAR_COTIZACION)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(CotizacionVentaConfirmarAnularView, self).get_context_data(**kwargs)
        context['accion'] = "Anular"
        context['titulo'] = "Confirmar de Cotización"
        context['texto'] = "¿Está seguro de Anular la Confirmar de la cotización?"
        context['item'] = "Cotización %s - %s" % (numeroXn(self.object.numero_cotizacion, 6), self.object.cliente)
        return context
        

class CotizacionVentaPdfView(View):
    def get(self, request, *args, **kwargs):
        color = COLOR_DEFAULT
        vertical = False
        logo = None
        pie_pagina = PIE_DE_PAGINA_DEFAULT

        obj = CotizacionVenta.objects.get(slug=self.kwargs['slug'])

        titulo = 'Cotización_' + str(obj.numero_cotizacion) + '_' + str(obj.cliente.razon_social)

        nro_cotizacion = 'Nro. de Cotización: ' + str(obj.numero_cotizacion)
        razon_social = 'Razón Social: ' + str(obj.cliente)
        direccion = 'Dirección: ' + str(obj.cliente.direccion_fiscal)
        interlocutor = 'Interlocutor: ' + str(obj.cliente_interlocutor)
        nro_documento = str(DICCIONARIO_TIPO_DOCUMENTO_SUNAT[obj.cliente.tipo_documento]) + ': ' + str(obj.cliente.numero_documento)
        fecha_cotizacion = 'Fecha Cotizacion: ' + str(obj.fecha_cotizacion)
        fecha_validez = 'Fecha Validez: ' + str(obj.fecha_validez)

        Texto = []
        Texto.extend([  nro_cotizacion, 
                        razon_social,
                        direccion, 
                        interlocutor, 
                        nro_documento,
                        fecha_cotizacion,
                        fecha_validez,
                        ])

        TablaEncabezado = [ 'Item',
                            'Descripción',
                            'Unidad',
                            'Cantidad',
                            'Prec. Unit. con IGV',
                            'Prec. Final con IGV',
                            'Descuento',
                            'Total',
                            'Stock',
                            'u',
                            ]

        cotizacion_venta_detalle = obj.CotizacionVentaDetalle_cotizacion_venta.all()
        TablaDatos = []
        for detalle in cotizacion_venta_detalle:
            fila = []

            detalle.material = detalle.content_type.get_object_for_this_type(id = detalle.id_registro)
            fila.append(intcomma(detalle.item))
            fila.append(intcomma(detalle.material))
            fila.append(intcomma(detalle.material.unidad_base))
            fila.append(intcomma(detalle.cantidad.quantize(Decimal('0.01'))))
            fila.append(intcomma(detalle.precio_unitario_con_igv.quantize(Decimal('0.01'))))
            fila.append(intcomma(detalle.precio_final_con_igv.quantize(Decimal('0.01'))))
            fila.append(intcomma(detalle.descuento.quantize(Decimal('0.01'))))
            fila.append(intcomma(detalle.total.quantize(Decimal('0.01'))))

            TablaDatos.append(fila)
        
        totales = obtener_totales(obj)
        lista =[]
        for k,v in totales.items():
            if v==0:continue
            fila = []
            fila.append(k)
            fila.append(v)

            lista.append(fila)

        TablaTotales = []
        for detalle in lista:
            fila = []
            fila.append(DICCIONARIO_TOTALES[detalle[0]])
            fila.append(intcomma(detalle[1]))

            TablaTotales.append(fila)
        
        terminos_condiciones = CotizacionTerminosCondiciones.objects.filter(condicion_visible=True)
        condiciones = ['Condiciones: ']
        for condicion in terminos_condiciones:
            condiciones.append(condicion)

        buf = generarCotizacionVenta(titulo, vertical, logo, pie_pagina, Texto, TablaEncabezado, TablaDatos, color, condiciones, TablaTotales)

        respuesta = HttpResponse(buf.getvalue(), content_type='application/pdf')
        respuesta.headers['content-disposition']='inline; filename=%s.pdf' % titulo

        return respuesta
