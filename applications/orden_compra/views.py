from decimal import Decimal
from django.shortcuts import render
from applications.comprobante_compra.models import ComprobanteCompraPI, ComprobanteCompraPIDetalle
from applications.funciones import slug_aleatorio
from applications.importaciones import *
from applications.movimiento_almacen.models import MovimientosAlmacen, TipoMovimiento
from applications.orden_compra.pdf import generarOrdenCompra, generarMotivoAnulacionOrdenCompra
from django.core.mail import EmailMultiAlternatives

from .models import (
    OrdenCompra,
    OrdenCompraDetalle,
    OfertaProveedor,
    OfertaProveedorDetalle
)

from .forms import (
    OrdenCompraForm,
    OrdenCompraEnviarCorreoForm,
)


class OrdenCompraListView(ListView):
    model = OrdenCompra
    template_name = "orden_compra/orden_compra/inicio.html"
    context_object_name = 'contexto_orden_compra'

def OrdenCompraTabla(request):
    data = dict()
    if request.method == 'GET':
        template = 'orden_compra/orden_compra/inicio_tabla.html'
        context = {}
        context['contexto_orden_compra'] = OrdenCompra.objects.all()

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)

class OrdenCompraDeleteView(BSModalDeleteView):
    model = OrdenCompra
    # template_name = "includes/eliminar generico.html"
    template_name = "includes/formulario generico.html"
    success_url = reverse_lazy('orden_compra_app:orden_compra_inicio')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.estado = 3
        registro_guardar(self.object, self.request)
        self.object.save()
        messages.success(request, MENSAJE_ANULAR_ORDEN_COMPRA)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(OrdenCompraDeleteView, self).get_context_data(**kwargs)
        context['accion'] = 'Anular'
        context['titulo'] = 'Orden de Compra'
        # context['item'] = self.object.id
        return context

class OrdenCompraMotivoAnulacionPdfView(View):
    def get(self, request, *args, **kwargs):
        color = COLOR_DEFAULT
        titulo = 'Anulación de la Orden de Compra'
        vertical = True
        logo = None
        pie_pagina = PIE_DE_PAGINA_DEFAULT

        obj = OrdenCompra.objects.get(slug=self.kwargs['slug'])

        fecha=datetime.strftime(obj.fecha_orden,'%d - %m - %Y')

        Texto = titulo + '\n' +str(obj.oferta_proveedor.requerimiento_material.proveedor) + '\n' + str(fecha)

        TablaEncabezado = ['Item','Material', 'Unidad', 'Cantidad']

        detalle = obj.OrdenCompraDetalle_orden_compra
        materiales = detalle.all()

        TablaDatos = []
        for material in materiales:
            fila = []

            material.material = material.content_type.get_object_for_this_type(id = material.id_registro)
            fila.append(material.item)
            fila.append(material.material)
            fila.append(material.material.unidad_base)
            fila.append(material.cantidad.quantize(Decimal('0.01')))

            TablaDatos.append(fila)

        buf = generarMotivoAnulacionOrdenCompra(titulo, vertical, logo, pie_pagina, Texto, TablaEncabezado, TablaDatos, color)

        respuesta = HttpResponse(buf.getvalue(), content_type='application/pdf')
        respuesta.headers['content-disposition']='inline; filename=%s.pdf' % titulo

        obj.estado = 2
        obj.save()

        return respuesta



class OrdenCompraNuevaVersionView(BSModalDeleteView):
    model = OrdenCompra
    template_name = "orden_compra/orden_compra/nueva_version.html"
    success_url = reverse_lazy('orden_compra_app:orden_compra_inicio')
    context_object_name = 'contexto_orden_compra' 

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()

        oferta_proveedor = self.object.oferta_proveedor
        orden_compra_anterior = self.object
        print('*********************************************')
        print(orden_compra_anterior)
        print('*********************************************')

        self.object.oferta_proveedor = None
        self.object.estado = 3

        registro_guardar(self.object, self.request)
        self.object.save()

        obj = OrdenCompra.objects.get(id = self.kwargs['pk'])

        orden = OrdenCompra.objects.create(
            internacional_nacional=obj.internacional_nacional,
            oferta_proveedor=oferta_proveedor,
            orden_compra_anterior=orden_compra_anterior,
            fecha_orden=obj.fecha_orden,
            moneda=obj.moneda,
            estado=0,
        )

        materiales = obj.OrdenCompraDetalle_orden_compra.all()
        for material in materiales:
            material.material = material.content_type.get_object_for_this_type(id = material.id_registro)

            orden_detalle = OrdenCompraDetalle.objects.create(
                item=material.item,
                content_type=material.content_type,
                id_registro=material.id_registro,
                cantidad=material.cantidad,
                orden_compra=orden,
                )

        messages.success(request, MENSAJE_ANULAR_ORDEN_COMPRA)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(OrdenCompraNuevaVersionView, self).get_context_data(**kwargs)
        context['accion'] = 'Nueva Versión'
        context['titulo'] = 'Orden de Compra'
        return context

class OrdenCompraDetailView(DetailView):
    model = OrdenCompra
    template_name = "orden_compra/orden_compra/detalle.html"
    context_object_name = 'contexto_orden_compra'

    def get_context_data(self, **kwargs):
        context = super(OrdenCompraDetailView, self).get_context_data(**kwargs)
        obj = OrdenCompra.objects.get(id = self.kwargs['pk'])
                
        materiales = obj.OrdenCompraDetalle_orden_compra.all()

        for material in materiales:
            material.material = material.content_type.get_object_for_this_type(id = material.id_registro)
        
        context['detalle_orden_compra'] = materiales 
        return context

def OrdenCompraDetailTabla(request, orden_id):
    data = dict()
    if request.method == 'GET':
        template = 'orden_compra/orden_compra/detalle_orden_compra_tabla.html'
        context = {}
        obj = OrdenCompra.objects.get(id = orden_id)
        context['contexto_orden_compra'] = obj
        context['detalle_orden_compra'] = OrdenCompraDetalle.objects.filter(orden_compra = obj)

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)




class OrdenCompraPdfView(View):
    def get(self, request, *args, **kwargs):
        color = COLOR_DEFAULT
        titulo = 'Orden de Compra'
        vertical = True
        logo = None
        pie_pagina = PIE_DE_PAGINA_DEFAULT

        obj = OrdenCompra.objects.get(slug=self.kwargs['slug'])

        fecha=datetime.strftime(obj.fecha_orden,'%d - %m - %Y')

        Texto = titulo + '\n' +str(obj.oferta_proveedor.requerimiento_material.proveedor) + '\n' + str(fecha)

        TablaEncabezado = ['Item','Material', 'Unidad', 'Cantidad']

        detalle = obj.OrdenCompraDetalle_orden_compra
        materiales = detalle.all()

        TablaDatos = []
        for material in materiales:
            fila = []

            material.material = material.content_type.get_object_for_this_type(id = material.id_registro)
            fila.append(material.item)
            fila.append(material.material)
            fila.append(material.material.unidad_base)
            fila.append(material.cantidad.quantize(Decimal('0.01')))

            TablaDatos.append(fila)

        buf = generarOrdenCompra(titulo, vertical, logo, pie_pagina, Texto, TablaEncabezado, TablaDatos, color)

        respuesta = HttpResponse(buf.getvalue(), content_type='application/pdf')
        respuesta.headers['content-disposition']='inline; filename=%s.pdf' % titulo

        obj.estado = 2
        obj.save()

        return respuesta

class OrdenCompraEnviarCorreoView(BSModalFormView):
    template_name = "includes/formulario generico.html"
    form_class = OrdenCompraEnviarCorreoForm

    def get_success_url(self):
        return reverse_lazy('orden_compra_app:orden_compra_detalle', kwargs={'pk':self.kwargs['orden_id']})

    def form_valid(self, form):
        if self.request.session['primero']:
            orden = OrdenCompra.objects.get(id=self.kwargs['orden_id'])            
            correos_proveedor = form.cleaned_data['correos_proveedor']
            correos_internos = form.cleaned_data['correos_internos']
            self.request.session['primero'] = False

            asunto = "Orden de Compra - %s" % (orden.id)
            mensaje = '<p>Estimado,</p><p>Se le envia la Orden de Compra: <a href="%s%s">%s</a></p>' % (self.request.META['HTTP_ORIGIN'], reverse_lazy('orden_compra_app:orden_compra_pdf', kwargs={'slug':orden.slug}), 'Orden')
            email_remitente = EMAIL_REMITENTE

            correo = EmailMultiAlternatives(subject=asunto, body=mensaje, from_email=email_remitente, to=correos_proveedor, cc=correos_internos,)
            correo.attach_alternative(mensaje, "text/html")
            try:
                correo.send()
                orden.estado = 2
                orden.save()
                
                messages.success(self.request, 'Correo enviado.')
                self.request.session['primero'] = False
            except:
                messages.warning(self.request, 'Hubo un error al enviar el correo.')
        
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(OrdenCompraEnviarCorreoView, self).get_form_kwargs()
        kwargs['proveedor'] = OrdenCompra.objects.get(id=self.kwargs['orden_id']).oferta_proveedor.requerimiento_material.proveedor 
        return kwargs

    def get_context_data(self, **kwargs):
        self.request.session['primero'] = True
        context = super(OrdenCompraEnviarCorreoView, self).get_context_data(**kwargs)
        context['accion']="Enviar"
        context['titulo']="Correos"
        return context


class OrdenCompraGenerarComprobanteTotalView(BSModalDeleteView):
    model = OrdenCompra
    template_name = "includes/eliminar generico.html"
    success_url = reverse_lazy('comprobante_compra_app:comprobante_compra_pi_lista')
    context_object_name = 'contexto_orden_compra' 

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        orden = self.get_object()

        comprobante = ComprobanteCompraPI.objects.create(
            internacional_nacional = orden.internacional_nacional,
            incoterms = orden.incoterms,
            orden_compra = orden,
            sociedad = orden.sociedad_id,
            moneda = orden.moneda,
            slug = slug_aleatorio(ComprobanteCompraPI),
            created_by = self.request.user,
            updated_by = self.request.user,
        )

        materiales = orden.OrdenCompraDetalle_orden_compra.all()
        movimiento_final = TipoMovimiento.objects.get(codigo=100)
        for material in materiales:
            orden_detalle = ComprobanteCompraPIDetalle.objects.create(
                item=material.item,
                orden_compra_detalle = material,
                cantidad = material.cantidad,
                precio_unitario_sin_igv = material.precio_unitario_sin_igv,
                precio_unitario_con_igv = material.precio_unitario_con_igv,
                precio_final_con_igv = material.precio_final_con_igv,
                descuento = material.descuento,
                sub_total = material.sub_total,
                igv = material.igv,
                total = material.total,
                tipo_igv = material.tipo_igv,
                comprobante_compra = comprobante,
                created_by = self.request.user,
                updated_by = self.request.user,
                )
            
            movimiento_dos = MovimientosAlmacen.objects.create(
                    content_type_producto = material.content_type,
                    id_registro_producto = material.id_registro,
                    cantidad = material.cantidad,
                    tipo_movimiento = movimiento_final,
                    signo_factor_multiplicador = +1,
                    content_type_documento_proceso = ContentType.objects.get_for_model(comprobante),
                    id_registro_documento_proceso = comprobante.id,
                    almacen = None,
                    sociedad = comprobante.sociedad,
                    movimiento_anterior = None,
                    movimiento_reversion = False,
                    created_by = self.request.user,
                    updated_by = self.request.user,
                )


        messages.success(request, MENSAJE_GENERAR_COMPROBANTE_COMPRA_PI)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(OrdenCompraGenerarComprobanteTotalView, self).get_context_data(**kwargs)
        context['accion'] = 'Generar'
        context['titulo'] = 'Comprobante Total'
        context['item'] = self.get_object()

        return context
