from datetime import timedelta
from decimal import Decimal
from django.shortcuts import render
from django import forms
from applications.importaciones import *
from applications.clientes.models import ClienteInterlocutor, InterlocutorCliente
from applications.datos_globales.models import CuentaBancariaSociedad, Moneda, TipoCambio
from applications.material.funciones import calidad, en_camino, observacion, reservado, stock, vendible
from applications.movimiento_almacen.models import MovimientosAlmacen, TipoMovimiento
from applications.cotizacion.pdf import generarCotizacionVenta
from applications.funciones import calculos_linea, fecha_en_letras, igv, numeroXn, obtener_totales, obtener_totales_soles, slug_aleatorio, tipo_de_cambio

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
    CotizacionVentaOtrosCargosForm,
    CotizacionVentaPdfsForm,
    PrecioListaMaterialForm,
)

from .models import (
    ConfirmacionVenta,
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


class CotizacionVentaListView(ListView):
    model = CotizacionVenta
    template_name = 'cotizacion/cotizacion_venta/inicio.html'
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
            if sociedad.observacion:
                texto.append(str(sociedad.observacion))
            else:
                texto.append("")


        sociedades = Sociedad.objects.all()
        
        context['titulo'] = "Actualizar Observaciones"
        context['url_guardar'] = reverse_lazy('cotizacion_app:guardar_cotizacion_venta_observacion', kwargs={'texto':1,'id_cotizacion':1,'abreviatura':"a",})[:-6]
        context['sociedades'] = sociedades
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


class CotizacionOtrosCargosUpdateView(BSModalUpdateView):
    model = CotizacionVenta
    template_name = "cotizacion/cotizacion_venta/form_otros_cargos.html"
    form_class = CotizacionVentaOtrosCargosForm
    success_url = '.'

    def get_context_data(self, **kwargs):
        context = super(CotizacionOtrosCargosUpdateView, self).get_context_data(**kwargs)
        texto = []
        for sociedad in self.object.CotizacionOtrosCargos_cotizacion_venta.all():
            texto.append(str(sociedad.otros_cargos))

        sociedades = Sociedad.objects.all()
        
        context['titulo'] = "Actualizar Otros Cargos"
        context['url_guardar'] = reverse_lazy('cotizacion_app:guardar_cotizacion_venta_otros_cargos', kwargs={'monto':1,'id_cotizacion':1,'abreviatura':"a",})[:-6]
        context['sociedades'] = sociedades
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
        self.object.fecha_validez = self.object.fecha_cotizacion + timedelta(7)

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


class CotizacionVentaAnularView(DeleteView):
    model = CotizacionVenta
    template_name = "includes/form generico.html"

    def get_success_url(self, **kwargs):
        return reverse_lazy('cotizacion_app:cotizacion_venta_ver', kwargs={'id_cotizacion':self.object.id})

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.estado = 9
        registro_guardar(self.object, self.request)
        self.object.save()

        messages.success(request, MENSAJE_ANULAR_COTIZACION)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(CotizacionVentaAnularView, self).get_context_data(**kwargs)
        context['accion'] = "Anular"
        context['titulo'] = "Cotización"
        context['texto'] = "¿Está seguro de Anular la cotización?"
        context['item'] = "Cotización %s - %s" % (numeroXn(self.object.numero_cotizacion, 6), self.object.cliente)
        return context


class CotizacionVentaClonarView(DeleteView):
    model = CotizacionVenta
    template_name = "includes/form generico.html"

    def get_success_url(self, **kwargs):
        return reverse_lazy('cotizacion_app:cotizacion_venta_ver', kwargs={'id_cotizacion':self.object.id})

    def delete(self, request, *args, **kwargs):
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
        return HttpResponseRedirect(reverse_lazy('cotizacion_app:cotizacion_venta_ver', kwargs={'id_cotizacion':nueva_cotizacion.id}))

    def get_context_data(self, **kwargs):
        context = super(CotizacionVentaClonarView, self).get_context_data(**kwargs)
        context['accion'] = "Clonar"
        context['titulo'] = "Cotización"
        context['texto'] = "¿Está seguro de Clonar la cotización?"
        context['item'] = "Cotización %s - %s" % (numeroXn(self.object.numero_cotizacion, 6), self.object.cliente)
        return context


class CotizacionVentaReservaView(DeleteView):
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
        if error_cantidad_sociedad:
            context['texto'] = 'Revise las cantidades por Sociedad.'
            return render(request, 'includes/modal sin permiso.html', context)
        return super().dispatch(request, *args, **kwargs)

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

        messages.success(request, MENSAJE_ANULAR_RESERVAR_COTIZACION)
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

    def dispatch(self, request, *args, **kwargs):
        error_cantidad_stock = False
        error_cantidad_sociedad = False
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
        
        if error_cantidad_sociedad:
            context['texto'] = 'Revise las cantidades por Sociedad.'
            return render(request, 'includes/modal sin permiso.html', context)

        if error_cantidad_stock:
            context['texto'] = 'No hay stock suficiente en un producto.'
            return render(request, 'includes/modal sin permiso.html', context)
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('cotizacion_app:cotizacion_venta_ver', kwargs={'id_cotizacion':self.object.id})

    def delete(self, request, *args, **kwargs):
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
            confirmacion_venta = ConfirmacionVenta.objects.create(
                cotizacion_venta = self.object,
                sociedad = sociedad,
                tipo_cambio = TipoCambio.objects.get(fecha=datetime.today()),
                observacion = cotizacion_observacion,
                total = self.object.total,
                created_by = self.request.user,
                updated_by = self.request.user,
            )
            for detalle in detalles:
                cotizacion_sociedad = detalle.CotizacionSociedad_cotizacion_venta_detalle.get(sociedad=sociedad)
                if cotizacion_sociedad.cantidad > 0:
                    respuesta = calculos_linea(cotizacion_sociedad.cantidad, detalle.precio_unitario_con_igv, detalle.precio_final_con_igv, igv())
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
            confirmacion_venta.delete()

        registro_guardar(self.object, self.request)
        self.object.save()

        messages.success(request, MENSAJE_ANULAR_CONFIRMAR_COTIZACION)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(CotizacionVentaConfirmarAnularView, self).get_context_data(**kwargs)
        context['accion'] = "Anular"
        context['titulo'] = "Confirmar de Cotización"
        context['texto'] = "¿Está seguro de Anular la Confirmar de la cotización?"
        context['item'] = "Cotización %s - %s" % (numeroXn(self.object.numero_cotizacion, 6), self.object.cliente)
        return context


class CotizacionVentaConfirmarAnticipoView(DeleteView):
    model = CotizacionVenta
    template_name = "includes/form generico.html"

    def dispatch(self, request, *args, **kwargs):
        error_cantidad_sociedad = False
        context = {}
        context['titulo'] = 'Error de Confirmación'
        for detalle in self.get_object().CotizacionVentaDetalle_cotizacion_venta.all():
            sumar = Decimal('0.00')
            for cotizacion_sociedad in detalle.CotizacionSociedad_cotizacion_venta_detalle.all():
                sumar += cotizacion_sociedad.cantidad
            if sumar != detalle.cantidad:
                error_cantidad_sociedad = True
        
        if error_cantidad_sociedad:
            context['texto'] = 'Revise las cantidades por Sociedad.'
            return render(request, 'includes/modal sin permiso.html', context)

        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('cotizacion_app:cotizacion_venta_ver', kwargs={'id_cotizacion':self.object.id})

    def delete(self, request, *args, **kwargs):
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
                sociedad = sociedad,
                tipo_cambio = TipoCambio.objects.get(fecha=self.object.fecha),
                observacion = cotizacion_observacion,
                total = self.object.total,
                created_by = self.request.user,
                updated_by = self.request.user,
            )
            for detalle in detalles:
                cotizacion_sociedad = detalle.CotizacionSociedad_cotizacion_venta_detalle.get(sociedad=sociedad)
                if cotizacion_sociedad.cantidad > 0:
                    respuesta = calculos_linea(cotizacion_sociedad.cantidad, detalle.precio_unitario_con_igv, detalle.precio_final_con_igv, igv())
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
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(CotizacionVentaConfirmarAnticipoView, self).get_context_data(**kwargs)
        context['accion'] = "Confirmar"
        context['titulo'] = "Cotización"
        context['texto'] = "¿Está seguro de Confirmar la cotización?"
        context['item'] = "Cotización %s - %s" % (numeroXn(self.object.numero_cotizacion, 6), self.object.cliente)
        return context


class CotizacionVentaConfirmarAnticipoAnularView(DeleteView):
    model = CotizacionVenta
    template_name = "includes/form generico.html"   

    def get_success_url(self, **kwargs):
        return reverse_lazy('cotizacion_app:cotizacion_venta_ver', kwargs={'id_cotizacion':self.object.id})

    def delete(self, request, *args, **kwargs):
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
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(CotizacionVentaConfirmarAnticipoAnularView, self).get_context_data(**kwargs)
        context['accion'] = "Anular"
        context['titulo'] = "Confirmar de Cotización"
        context['texto'] = "¿Está seguro de Anular la Confirmar de la cotización?"
        context['item'] = "Cotización %s - %s" % (numeroXn(self.object.numero_cotizacion, 6), self.object.cliente)
        return context


class CotizacionVentaPdfsView(BSModalFormView):
    template_name = "cotizacion/cotizacion_venta/form_pdfs.html"
    form_class = CotizacionVentaPdfsForm

    def dispatch(self, request, *args, **kwargs):
        error_cantidad_sociedad = False
        obj = CotizacionVenta.objects.get(id=self.kwargs['pk'])
        context = {}
        context['titulo'] = 'Error de Confirmación'
        for detalle in obj.CotizacionVentaDetalle_cotizacion_venta.all():
            sumar = Decimal('0.00')
            for cotizacion_sociedad in detalle.CotizacionSociedad_cotizacion_venta_detalle.all():
                sumar += cotizacion_sociedad.cantidad

            if sumar != detalle.cantidad:
                error_cantidad_sociedad = True
        
        if error_cantidad_sociedad:
            context['texto'] = 'Revise las cantidades por Sociedad.'
            return render(request, 'includes/modal sin permiso.html', context)
            
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        obj = CotizacionVenta.objects.get(id=self.kwargs['pk'])
        sociedades = []
        for detalle in obj.CotizacionVentaDetalle_cotizacion_venta.all():
            for cotizacion_sociedad in detalle.CotizacionSociedad_cotizacion_venta_detalle.all():
                if cotizacion_sociedad.cantidad > 0:
                    if not cotizacion_sociedad.sociedad in sociedades: sociedades.append(cotizacion_sociedad.sociedad)
        context = super(CotizacionVentaPdfsView, self).get_context_data(**kwargs)
        context['titulo'] = 'Ver PDFs'
        context['cotizacion'] = obj
        context['sociedades'] = sociedades
        return context
    

class CotizacionVentaSociedadPdfView(View):
    def get(self, request, *args, **kwargs):
        sociedad = Sociedad.objects.get(abreviatura=self.kwargs['sociedad'])
        color = sociedad.color
        titulo = 'Cotización'
        vertical = False
        logo = sociedad.logo.url
        pie_pagina = sociedad.pie_pagina
        alinear = 'right'
        fuenteBase = "ComicNeue"

        obj = CotizacionVenta.objects.get(slug=self.kwargs['slug'])

        moneda = obj.moneda
        titulo = 'Cotización %s%s %s' % (self.kwargs['sociedad'], str(obj.numero_cotizacion), str(obj.cliente.razon_social))

        Cabecera = {}
        Cabecera['nro_cotizacion'] = '%s%s' % (self.kwargs['sociedad'], str(obj.numero_cotizacion))
        Cabecera['fecha_cotizacion'] = fecha_en_letras(obj.fecha_cotizacion)
        Cabecera['razon_social'] = str(obj.cliente)
        Cabecera['tipo_documento'] = DICCIONARIO_TIPO_DOCUMENTO_SUNAT[obj.cliente.tipo_documento]
        Cabecera['nro_documento'] = str(obj.cliente.numero_documento)
        Cabecera['direccion'] = str(obj.cliente.direccion_fiscal)
        Cabecera['interlocutor'] = str(obj.cliente_interlocutor)
        Cabecera['fecha_validez'] = obj.fecha_validez.strftime('%d/%m/%Y')

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
            calculo = calculos_linea(confirmacion_detalle.cantidad, detalle.precio_unitario_con_igv, detalle.precio_final_con_igv, igv(obj.fecha))
            detalle.material = detalle.content_type.get_object_for_this_type(id = detalle.id_registro)
            fila.append(item)
            fila.append(intcomma(detalle.material))
            fila.append(intcomma(detalle.material.unidad_base))
            fila.append(intcomma(confirmacion_detalle.cantidad.quantize(Decimal('0.01'))))
            fila.append(intcomma(detalle.precio_unitario_con_igv.quantize(Decimal('0.01'))))
            fila.append(intcomma(detalle.precio_final_con_igv.quantize(Decimal('0.01'))))
            fila.append(intcomma(calculo['descuento_con_igv'].quantize(Decimal('0.01'))))
            fila.append(intcomma(calculo['total'].quantize(Decimal('0.01'))))
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

        buf = generarCotizacionVenta(titulo, vertical, logo, pie_pagina, Cabecera, TablaEncabezado, TablaDatos, color, condiciones, TablaTotales, alinear, fuenteBase, moneda, observaciones)

        respuesta = HttpResponse(buf.getvalue(), content_type='application/pdf')
        respuesta.headers['content-disposition']='inline; filename=%s.pdf' % titulo

        return respuesta



class CotizacionVentaResumenView(BSModalReadView):
    model = CotizacionVenta
    template_name = "cotizacion/cotizacion_venta/form_resumen.html"

    def get_context_data(self, **kwargs):
        monedas = Moneda.objects.all()
        tipo_de_cambio_cotizacion = TipoCambio.objects.tipo_cambio_venta(self.object.fecha)
        tipo_de_cambio_hoy = TipoCambio.objects.tipo_cambio_venta(date.today())
        print(tipo_de_cambio_cotizacion, tipo_de_cambio_hoy)
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
                    )
                sociedad.cuentas = cuentas
            moneda.sociedades = cotizacion_sociedad

        context = super(CotizacionVentaResumenView, self).get_context_data(**kwargs)
        context['monedas'] = monedas
        context['titulo'] = 'Resumen a Depositar'
        return context
    

#################################################################################################################

class ConfirmacionListView(TemplateView):
    template_name = 'cotizacion/confirmacion/inicio.html'

    def get_context_data(self, **kwargs):
        contexto_cotizacion_venta = ConfirmacionVenta.objects.all()
        try:
            contexto_cotizacion_venta = contexto_cotizacion_venta.filter(cotizacion_venta__id = kwargs['id_cotizacion'])
        except:
            print("Error")

        context = super(ConfirmacionListView, self).get_context_data(**kwargs)
        context['contexto_cotizacion_venta'] = contexto_cotizacion_venta
        return context


class ConfirmarVerView(TemplateView):
    template_name = "cotizacion/confirmacion/detalle.html"

    def get_context_data(self, **kwargs):
        obj = ConfirmacionVenta.objects.get(id = kwargs['id_cotizacion'])
        tipo_cambio_hoy = TipoCambio.objects.tipo_cambio_venta(date.today())
        tipo_cambio = TipoCambio.objects.tipo_cambio_venta(obj.fecha_confirmacion)
        
        materiales = None
        try:
            materiales = obj.ConfirmacionVentaDetalle_confirmacion_venta.all()

            for material in materiales:
                material.material = material.content_type.get_object_for_this_type(id = material.id_registro)
        except:
            pass

        context = super(ConfirmarVerView, self).get_context_data(**kwargs)
        context['confirmacion'] = obj
        context['cotizacion'] = obj.cotizacion_venta
        context['materiales'] = materiales
        context['tipo_cambio_hoy'] = tipo_cambio_hoy
        context['tipo_cambio'] = tipo_cambio
        context['totales'] = obtener_totales(obj)
        tipo_cambio = tipo_de_cambio(tipo_cambio, tipo_cambio_hoy)
        context['totales_soles'] = obtener_totales_soles(context['totales'], tipo_cambio)
        
        return context


def ConfirmarVerTabla(request, id_cotizacion):
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

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)