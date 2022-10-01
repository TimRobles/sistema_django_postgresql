from urllib import request
from django.shortcuts import render
from applications.cotizacion.models import ConfirmacionVenta
from applications.datos_globales.models import SeriesComprobante, TipoCambio
from applications.funciones import obtener_totales, obtener_totales_soles, slug_aleatorio, tipo_de_cambio
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

        serie_comprobante = SeriesComprobante.objects.filter(tipo_comprobante=ContentType.objects.get_for_model(FacturaVenta)).earliest('created_at')
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
            total_otros_cargos = self.object.otros_cargos,
            observaciones = self.object.observacion,
            total = self.object.total,
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
        context['totales'] = obtener_totales(FacturaVenta.objects.get(id=self.kwargs['id_factura_venta']))
      
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

        serie_comprobante = SeriesComprobante.objects.filter(tipo_comprobante=ContentType.objects.get_for_model(BoletaVenta)).earliest('created_at')

        boleta_venta = BoletaVenta.objects.create(
            sociedad = self.object.sociedad,
            serie_comprobante = serie_comprobante,
            cliente = self.object.cliente,
            cliente_interlocutor = self.object.cliente_interlocutor,
            moneda = self.object.moneda,
            tipo_cambio = self.object.tipo_cambio,
            descuento_global = self.object.descuento_global,
            total = self.object.total,
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
                cantidad=detalle.cantidad_confirmada,
                precio_unitario_sin_igv=detalle.precio_unitario_sin_igv,
                precio_unitario_con_igv=detalle.precio_unitario_con_igv,
                precio_final_con_igv=detalle.precio_final_con_igv,
                descuento=detalle.descuento,
                sub_total=detalle.sub_total,
                tipo_igv=detalle.tipo_igv,
                igv=detalle.igv,
                total=detalle.total,
                boleta_venta=boleta_venta,
                created_by=self.request.user,
                updated_by=self.request.user,
            )

        messages.success(request, MENSAJE_CLONAR_COTIZACION)
        return HttpResponseRedirect(reverse_lazy('comprobante_venta_app:boleta_venta_detalle', kwargs={'id_boleta_venta':boleta_venta.id}))

    def get_context_data(self, **kwargs):
        context = super(BoletaVentaCrearView, self).get_context_data(**kwargs)
        context['accion'] = 'Generar'
        context['titulo'] = 'Boleta de venta'
        context['texto'] = '¿Seguro que desea generar la Boleta de venta?'
        context['item'] = str(self.object.cliente) 
        return context

