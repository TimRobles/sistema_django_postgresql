import json
from urllib import request
from django.shortcuts import render
from applications.cobranza.funciones import eliminarDeuda, generarDeuda
from applications.comprobante_venta.forms import BoletaVentaAnularForm, BoletaVentaSerieForm
from applications.comprobante_venta.funciones import anular_nubefact, boleta_nubefact
from applications.cotizacion.models import ConfirmacionVenta
from applications.datos_globales.models import NubefactRespuesta, SeriesComprobante, TipoCambio
from applications.funciones import obtener_totales, slug_aleatorio, tipo_de_cambio
from applications.importaciones import *

from . models import(
    BoletaVenta,
    BoletaVentaDetalle,
    FacturaVenta,
    FacturaVentaDetalle,
)

class FacturaVentaListView(ListView):
    model = FacturaVenta
    template_name = 'comprobante_venta/factura_venta/inicio.html'
    context_object_name = 'contexto_factura_venta'

def FacturaVentaTabla(request):
    data = dict()
    if request.method == 'GET':
        template = 'comprobante_venta/factura_venta/inicio_tabla.html'
        context = {}
        context['contexto_factura_venta'] = FacturaVenta.objects.all()

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)

class FacturaVentaDetalleView(TemplateView):
    template_name = "comprobante_venta/factura_venta/detalle.html"

    def get_context_data(self, **kwargs):
        obj = FacturaVenta.objects.get(id = kwargs['id_factura_venta'])

        materiales = None
        try:
            materiales = obj.FacturaVentaDetalle_factura_venta.all()

            for material in materiales:
                material.material = material.content_type.get_object_for_this_type(id = material.id_registro)
        except:
            pass
        
        tipo_cambio_hoy = TipoCambio.objects.tipo_cambio_venta(date.today())
        tipo_cambio = TipoCambio.objects.tipo_cambio_venta(obj.confirmacion.fecha_confirmacion)
        context = super(FacturaVentaDetalleView, self).get_context_data(**kwargs)
        context['factura'] = obj
        context['confirmacion'] = obj.confirmacion
        context['materiales'] = materiales
        context['tipo_cambio_hoy'] = tipo_cambio_hoy
        context['tipo_cambio'] = tipo_cambio
        tipo_cambio = tipo_de_cambio(tipo_cambio, tipo_cambio_hoy)
        context['totales'] = obtener_totales(FacturaVenta.objects.get(id=self.kwargs['id_factura_venta']))

        return context

def FacturaVentaDetalleVerTabla(request, id_factura_venta):
    data = dict()
    if request.method == 'GET':
        template = 'comprobante_venta/factura_venta/detalle_tabla.html'
        obj = FacturaVenta.objects.get(id=id_factura_venta)

        tipo_cambio_hoy = TipoCambio.objects.tipo_cambio_venta(date.today())
        tipo_cambio = TipoCambio.objects.tipo_cambio_venta(obj.confirmacion.fecha_confirmacion)
        materiales = None
        try:
            materiales = obj.FacturaVentaDetalle_factura_venta.all()

            for material in materiales:
                material.material = material.content_type.get_object_for_this_type(id = material.id_registro)
        except:
            pass

        context = {}
        context['factura'] = obj
        context['materiales'] = materiales
        context['tipo_cambio_hoy'] = tipo_cambio_hoy
        context['tipo_cambio'] = tipo_cambio
        tipo_cambio = tipo_de_cambio(tipo_cambio, tipo_cambio_hoy)
        context['totales'] = obtener_totales(obj)     

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)

class FacturaVentaCrearView(DeleteView):
    model = ConfirmacionVenta
    template_name = "includes/form generico.html"

    def get_success_url(self, **kwargs):
        return reverse_lazy('comprobante_venta_app:factura_venta_detalle', kwargs={'id_factura_venta':self.object.id})

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()

        detalles = self.object.ConfirmacionVentaDetalle_confirmacion_venta.all()

        serie_comprobante = SeriesComprobante.objects.por_defecto(ContentType.objects.get_for_model(FacturaVenta))
        factura_venta = FacturaVenta.objects.create(
            confirmacion=self.object,
            sociedad = self.object.sociedad,
            serie_comprobante = serie_comprobante,
            cliente = self.object.cliente,
            cliente_interlocutor = self.object.cliente_interlocutor,
            moneda = self.object.moneda,
            tipo_cambio = self.object.tipo_cambio,
            tipo_venta = self.object.tipo_venta,
            condiciones_pago = self.object.condiciones_pago,
            descuento_global = self.object.descuento_global,
            total_descuento = self.object.total_descuento,
            total_anticipo = self.object.total_anticipo,
            total_gravada = self.object.total_gravada,
            total_inafecta = self.object.total_inafecta,
            total_exonerada = self.object.total_exonerada,
            total_igv = self.object.total_igv,
            total_gratuita = self.object.total_gratuita,
            total_otros_cargos = self.object.otros_cargos,
            total = self.object.total,
            observaciones = self.object.observacion,
            slug = slug_aleatorio(FacturaVenta),
            created_by=self.request.user,
            updated_by=self.request.user,
        )

        for detalle in detalles:
            producto = detalle.content_type.get_object_for_this_type(id = detalle.id_registro)
            factura_venta_detalle = FacturaVentaDetalle.objects.create(
                item=detalle.item,
                content_type=detalle.content_type,
                id_registro=detalle.id_registro,
                unidad=producto.unidad_base,
                descripcion_documento=producto.descripcion_documento,
                cantidad=detalle.cantidad_confirmada,
                precio_unitario_sin_igv=detalle.precio_unitario_sin_igv,
                precio_unitario_con_igv=detalle.precio_unitario_con_igv,
                precio_final_con_igv=detalle.precio_final_con_igv,
                descuento=detalle.descuento,
                sub_total=detalle.sub_total,
                tipo_igv=detalle.tipo_igv,
                igv=detalle.igv,
                total=detalle.total,
                codigo_producto_sunat=producto.codigo_producto_sunat,
                factura_venta=factura_venta,
                created_by=self.request.user,
                updated_by=self.request.user,
            )

        registro_guardar(self.object, self.request)
        self.object.save()

        messages.success(request, MENSAJE_CLONAR_COTIZACION)
        return HttpResponseRedirect(reverse_lazy('comprobante_venta_app:factura_venta_detalle', kwargs={'id_factura_venta':factura_venta.id}))

    def get_context_data(self, **kwargs):
        context = super(FacturaVentaCrearView, self).get_context_data(**kwargs)
        context['accion'] = 'Generar'
        context['titulo'] = 'Factura de venta'
        context['texto'] = '¿Seguro que desea generar la Factura de venta?'
        context['item'] = str(self.object.cliente) 
        return context


class BoletaVentaListView(ListView):
    model = BoletaVenta
    template_name = 'comprobante_venta/boleta_venta/inicio.html'
    context_object_name = 'contexto_boleta_venta'

def BoletaVentaTabla(request):
    data = dict()
    if request.method == 'GET':
        template = 'comprobante_venta/boleta_venta/inicio_tabla.html'
        context = {}
        context['contexto_boleta_venta'] = BoletaVenta.objects.all()

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
    return JsonResponse(data)

class BoletaVentaDetalleView(TemplateView):
    template_name = "comprobante_venta/boleta_venta/detalle.html"

    def get_context_data(self, **kwargs):
        obj = BoletaVenta.objects.get(id = kwargs['id_boleta_venta'])

        materiales = None
        try:
            materiales = obj.BoletaVentaDetalle_boleta_venta.all()

            for material in materiales:
                material.material = material.content_type.get_object_for_this_type(id = material.id_registro)
        except:
            pass

        tipo_cambio_hoy = TipoCambio.objects.tipo_cambio_venta(date.today())
        tipo_cambio = TipoCambio.objects.tipo_cambio_venta(obj.confirmacion.fecha_confirmacion)

        context = super(BoletaVentaDetalleView, self).get_context_data(**kwargs)
        context['boleta'] = obj
        context['materiales'] = materiales
        context['tipo_cambio_hoy'] = tipo_cambio_hoy
        context['tipo_cambio'] = tipo_cambio
        tipo_cambio = tipo_de_cambio(tipo_cambio, tipo_cambio_hoy)
        context['totales'] = obtener_totales(obj)
        context['nubefact_acceso'] = obj.serie_comprobante.NubefactSerieAcceso_serie_comprobante.acceder(obj.sociedad, ContentType.objects.get_for_model(obj))
        context['url_nubefact'] = NubefactRespuesta.objects.respuesta(obj)
      
        return context

def BoletaVentaDetalleVerTabla(request, id_boleta_venta):
    data = dict()
    if request.method == 'GET':
        template = 'comprobante_venta/boleta_venta/detalle_tabla.html'
        obj = BoletaVenta.objects.get(id=id_boleta_venta)
        
        tipo_cambio_hoy = TipoCambio.objects.tipo_cambio_venta(date.today())
        tipo_cambio = TipoCambio.objects.tipo_cambio_venta(obj.confirmacion.fecha_confirmacion)
 
        materiales = None
        try:
            materiales = obj.BoletaVentaDetalle_boleta_venta.all()

            for material in materiales:
                material.material = material.content_type.get_object_for_this_type(id = material.id_registro)
        except:
            pass

        context = {}
        context['boleta'] = obj
        context['materiales'] = materiales
        context['tipo_cambio_hoy'] = tipo_cambio_hoy
        context['tipo_cambio'] = tipo_cambio
        tipo_cambio = tipo_de_cambio(tipo_cambio, tipo_cambio_hoy)
        context['totales'] = obtener_totales(obj)
        context['nubefact_acceso'] = obj.serie_comprobante.NubefactSerieAcceso_serie_comprobante.acceder(obj.sociedad, ContentType.objects.get_for_model(obj))
        context['url_nubefact'] = NubefactRespuesta.objects.respuesta(obj)

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)

class BoletaVentaCrearView(DeleteView):
    model = ConfirmacionVenta
    template_name = "includes/form generico.html"

    def get_success_url(self, **kwargs):
        return reverse_lazy('comprobante_venta_app:boleta_venta_detalle', kwargs={'id_boleta_venta':self.object.id})

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()

        detalles = self.object.ConfirmacionVentaDetalle_confirmacion_venta.all()

        serie_comprobante = SeriesComprobante.objects.por_defecto(ContentType.objects.get_for_model(BoletaVenta))

        boleta_venta = BoletaVenta.objects.create(
            confirmacion=self.object,
            sociedad = self.object.sociedad,
            serie_comprobante = serie_comprobante,
            cliente = self.object.cliente,
            cliente_interlocutor = self.object.cliente_interlocutor,
            moneda = self.object.moneda,
            tipo_cambio = self.object.tipo_cambio,
            tipo_venta = self.object.tipo_venta,
            condiciones_pago = self.object.condiciones_pago,
            descuento_global = self.object.descuento_global,
            total_descuento = self.object.total_descuento,
            total_anticipo = self.object.total_anticipo,
            total_gravada = self.object.total_gravada,
            total_inafecta = self.object.total_inafecta,
            total_exonerada = self.object.total_exonerada,
            total_igv = self.object.total_igv,
            total_gratuita = self.object.total_gratuita,
            total_otros_cargos = self.object.otros_cargos,
            total = self.object.total,
            observaciones = self.object.observacion,
            slug = slug_aleatorio(BoletaVenta),
            created_by=self.request.user,
            updated_by=self.request.user,
        )

        for detalle in detalles:
            producto = detalle.content_type.get_object_for_this_type(id = detalle.id_registro)
            boleta_venta_detalle = BoletaVentaDetalle.objects.create(
                item=detalle.item,
                content_type=detalle.content_type,
                id_registro=detalle.id_registro,
                unidad=producto.unidad_base,
                descripcion_documento=producto.descripcion_documento,
                cantidad=detalle.cantidad_confirmada,
                precio_unitario_sin_igv=detalle.precio_unitario_sin_igv,
                precio_unitario_con_igv=detalle.precio_unitario_con_igv,
                precio_final_con_igv=detalle.precio_final_con_igv,
                descuento=detalle.descuento,
                sub_total=detalle.sub_total,
                tipo_igv=detalle.tipo_igv,
                igv=detalle.igv,
                total=detalle.total,
                codigo_producto_sunat=producto.codigo_producto_sunat,
                boleta_venta=boleta_venta,
                created_by=self.request.user,
                updated_by=self.request.user,
            )
            
        registro_guardar(self.object, self.request)
        self.object.save()

        messages.success(request, MENSAJE_CLONAR_COTIZACION)
        return HttpResponseRedirect(reverse_lazy('comprobante_venta_app:boleta_venta_detalle', kwargs={'id_boleta_venta':boleta_venta.id}))

    def get_context_data(self, **kwargs):
        context = super(BoletaVentaCrearView, self).get_context_data(**kwargs)
        context['accion'] = 'Generar'
        context['titulo'] = 'Boleta de venta'
        context['texto'] = '¿Seguro que desea generar la Boleta de venta?'
        context['item'] = str(self.object.cliente) 
        return context



class BoletaVentaSerieUpdateView(BSModalUpdateView):
    model = BoletaVenta
    template_name = "includes/formulario generico.html"
    form_class = BoletaVentaSerieForm
    success_url = '.'
    
    def get_context_data(self, **kwargs):
        context = super(BoletaVentaSerieUpdateView, self).get_context_data(**kwargs)
        context['accion'] = 'Seleccionar'
        context['titulo'] = 'Serie'
        return context
    

class BoletaVentaGuardarView(DeleteView):
    model = BoletaVenta
    template_name = "includes/form generico.html"

    def dispatch(self, request, *args, **kwargs):
        context = {}
        error_tipo_cambio = False
        context['titulo'] = 'Error de guardar'
        if len(TipoCambio.objects.filter(fecha=datetime.today()))==0:
            error_tipo_cambio = True

        if error_tipo_cambio:
            context['texto'] = 'Ingrese un tipo de cambio para hoy.'
            return render(request, 'includes/modal sin permiso.html', context)
        return super(BoletaVentaGuardarView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self) -> str:
        return reverse_lazy('comprobante_venta_app:boleta_venta_detalle', kwargs={'id_boleta_venta':self.kwargs['pk']})

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        fecha_vencimiento = generarDeuda(obj, self.request)

        obj.fecha_emision = date.today()
        obj.fecha_vencimiento = fecha_vencimiento
        obj.estado = 2
        obj.numero_boleta = BoletaVenta.objects.nuevo_numero(obj)
        registro_guardar(obj, self.request)
        obj.save()
        obj.confirmacion.estado = 2
        obj.confirmacion.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(BoletaVentaGuardarView, self).get_context_data(**kwargs)
        context['accion'] = 'Guardar'
        context['titulo'] = 'Boleta de Venta'
        context['texto'] = '¿Seguro de guardar la Boleta de Venta?'
        context['item'] = self.get_object()
        return context
    

class BoletaVentaAnularView(BSModalUpdateView):
    model = BoletaVenta
    template_name = "includes/formulario generico.html"
    form_class = BoletaVentaAnularForm

    def get_success_url(self) -> str:
        return reverse_lazy('comprobante_venta_app:boleta_venta_detalle', kwargs={'id_boleta_venta':self.kwargs['pk']})

    def form_valid(self, form):
        eliminar = eliminarDeuda(form.instance)
        if eliminar:
            messages.success(self.request, MENSAJE_ELIMINAR_DEUDA)
        else:
            messages.warning(self.request, MENSAJE_ERROR_ELIMINAR_DEUDA)
        form.instance.estado = 3
        form.instance.confirmacion.estado = 1
        form.instance.confirmacion.save()
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(BoletaVentaAnularView, self).get_context_data(**kwargs)
        context['accion'] = 'Anular'
        context['titulo'] = 'Boleta de Venta'
        return context
    

class BoletaVentaNubeFactEnviarView(DeleteView):
    model = BoletaVenta
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
        return super(BoletaVentaNubeFactEnviarView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self) -> str:
        return reverse_lazy('comprobante_venta_app:boleta_venta_detalle', kwargs={'id_boleta_venta':self.kwargs['pk']})

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        respuesta = boleta_nubefact(obj, self.request.user)
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
        context = super(BoletaVentaNubeFactEnviarView, self).get_context_data(**kwargs)
        context['accion'] = 'Enviar'
        context['titulo'] = 'Boleta de Venta a NubeFact'
        context['texto'] = '¿Seguro de enviar la Boleta de Venta a NubeFact?'
        context['item'] = self.get_object()
        return context
    

class BoletaVentaNubeFactAnularView(BSModalUpdateView):
    model = BoletaVenta
    template_name = "includes/formulario generico.html"
    form_class = BoletaVentaAnularForm

    def dispatch(self, request, *args, **kwargs):
        context = {}
        error_fecha = False
        context['titulo'] = 'Error de guardar'
        if (date.today() - self.get_object().fecha_emision).days > 0:
            error_fecha = True

        if error_fecha:
            context['texto'] = 'No se puede anular, realizar nota de crédito.'
            return render(request, 'includes/modal sin permiso.html', context)
        return super(BoletaVentaNubeFactAnularView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self) -> str:
        return reverse_lazy('comprobante_venta_app:boleta_venta_detalle', kwargs={'id_boleta_venta':self.kwargs['pk']})

    def form_valid(self, form):
        respuesta = anular_nubefact(form.instance, self.request.user)
        if respuesta.error:
            form.instance.estado = 6
        else:
            form.instance.estado = 3
        registro_guardar(form.instance, self.request)
        eliminar = eliminarDeuda(form.instance)
        if eliminar:
            messages.success(self.request, MENSAJE_ELIMINAR_DEUDA)
        else:
            messages.warning(self.request, MENSAJE_ERROR_ELIMINAR_DEUDA)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(BoletaVentaNubeFactAnularView, self).get_context_data(**kwargs)
        context['accion'] = 'Anular'
        context['titulo'] = 'Boleta de Venta a NubeFact'
        return context