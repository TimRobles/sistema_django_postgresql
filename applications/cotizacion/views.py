from django.shortcuts import render
from applications.clientes.models import ClienteInterlocutor, InterlocutorCliente
from applications.funciones import calculos_linea, numeroXn, obtener_totales
from applications.importaciones import *
from django import forms
from applications.material.funciones import calidad, reservado, stock, vendible
from applications.cotizacion.pdf import generarCotizacionVenta

from applications.sociedad.models import Sociedad

from applications.orden_compra.models import OrdenCompraDetalle
from applications.recepcion_compra.models import RecepcionCompra

from .forms import (
    CotizacionVentaClienteForm,
    CotizacionVentaDetalleForm,
    CotizacionVentaForm,
    CotizacionVentaMaterialDetalleForm,
    CotizacionVentaMaterialDetalleUpdateForm,
    PrecioListaMaterialForm,
)
    
from .models import (
    CotizacionSociedad,
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
    obj = CotizacionVenta.objects.create()
    return HttpResponseRedirect(reverse_lazy('cotizacion_app:cotizacion_venta_ver', kwargs={'id_cotizacion':obj.id}))


class CotizacionVentaVerView(TemplateView):
    template_name = "cotizacion/cotizacion_venta/detalle.html"
    
    def get_context_data(self, **kwargs):
        obj = CotizacionVenta.objects.get(id = kwargs['id_cotizacion'])
        materiales = None
        try:
            materiales = obj.CotizacionVentaDetalle_cotizacion_venta.all()

            for material in materiales:
                material.material = material.content_type.get_object_for_this_type(id = material.id_registro)
        except:
            pass

        context = super(CotizacionVentaVerView, self).get_context_data(**kwargs)
        context['cotizacion'] = obj
        context['materiales'] = materiales
        context['totales'] = obtener_totales(CotizacionVenta.objects.get(id=self.kwargs['id_cotizacion']))

        return context


def CotizacionVentaVerTabla(request, id_cotizacion):
    data = dict()
    if request.method == 'GET':
        template = 'cotizacion/cotizacion_venta/inicio_tabla.html'
        context = {}
        context['contexto_cotizacion_venta'] = CotizacionVenta.objects.all()
        context['totales'] = obtener_totales(CotizacionVenta.objects.get(id=id_cotizacion))
        
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


def CotizacionVentaDetalleTabla(request, cotizacion_id):
    data = dict()
    if request.method == 'GET':
        template = 'cotizacion/cotizacion_venta/detalle_tabla.html'
        context = {}
        obj = CotizacionVenta.objects.get(id = cotizacion_id)

        materiales = None
        try:
            materiales = obj.CotizacionVentaDetalle_cotizacion_venta.all()

            for material in materiales:
                material.material = material.content_type.get_object_for_this_type(id = material.id_registro)
        except:
            pass

        context['materiales'] = materiales
        context['cotizacion'] = obj

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
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


class CotizacionVentaGuardarView(BSModalDeleteView):
    model = CotizacionVenta
    template_name = "cotizacion/cotizacion_venta/form_guardar.html"

    def get_success_url(self, **kwargs):
        return reverse_lazy('cotizacion_app:cotizacion_venta_inicio')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.estado = 2
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
        context['item'] = self.get_object().item

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
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(CotizacionVentaMaterialDetalleUpdateView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        context['titulo'] = "Precios"
        context['material'] = self.object.content_type.get_object_for_this_type(id = self.object.id_registro)
        return context


