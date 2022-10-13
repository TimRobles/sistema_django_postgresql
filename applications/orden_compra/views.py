from decimal import Decimal
from django.shortcuts import render
from applications.comprobante_compra.models import ComprobanteCompraPI, ComprobanteCompraPIDetalle
from applications.funciones import calculos_linea, igv, numeroXn, obtener_totales
from applications.funciones import slug_aleatorio
from applications.importaciones import *
from applications.movimiento_almacen.models import MovimientosAlmacen, TipoMovimiento
from applications.orden_compra.pdf import generarOrdenCompra, generarMotivoAnulacionOrdenCompra
from django.core.mail import EmailMultiAlternatives

# from sistema_django.applications import oferta_proveedor, orden_compra


from .models import (
    OrdenCompra,
    OrdenCompraDetalle,
    OfertaProveedor,
    OfertaProveedorDetalle
)

from .forms import (
    OrdenCompraForm,
    OrdenCompraEnviarCorreoForm,
    OrdenCompraAnularForm,
    OrdenCompraDetalleUpdateForm,
    OrdenCompraDetalleAgregarForm,
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

class OrdenCompraAnularView(BSModalUpdateView):
    model = OrdenCompra
    form_class = OrdenCompraAnularForm    
    template_name = "includes/formulario generico.html"
    success_url = reverse_lazy('orden_compra_app:orden_compra_inicio')

    def form_valid(self, form):
        form.instance.estado = 4
        registro_guardar(form.instance, self.request)
                
        messages.success(self.request, MENSAJE_ANULAR_ORDEN_COMPRA)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(OrdenCompraAnularView, self).get_context_data(**kwargs)
        context['accion'] = 'Anular'
        context['titulo'] = 'Orden de Compra'
        return context

class OrdenCompraMotivoAnulacionPdfView(View):
    def get(self, request, *args, **kwargs):
        color = COLOR_DEFAULT
        titulo = 'Anulación de la Orden de Compra'
        vertical = True
        logo = None
        pie_pagina = PIE_DE_PAGINA_DEFAULT

        obj = OrdenCompra.objects.get(slug=self.kwargs['slug'])

        fecha=datetime.strftime(obj.updated_at,'%d - %m - %Y')

        Texto = titulo + '\n' +str(obj.oferta_proveedor) + '\n' + str(obj.motivo_anulacion) + '\n' + str(fecha)

        TablaEncabezado = ['Item','Material', 'Unidad', 'Cantidad']

        orden_detalle = obj.OrdenCompraDetalle_orden_compra.all()

        TablaDatos = []
        for detalle in orden_detalle:
            fila = []

            detalle.material = detalle.content_type.get_object_for_this_type(id = detalle.id_registro)
            fila.append(detalle.item)
            fila.append(detalle.material)
            fila.append(detalle.material.unidad_base)
            fila.append(detalle.cantidad.quantize(Decimal('0.01')))

            TablaDatos.append(fila)

        buf = generarMotivoAnulacionOrdenCompra(titulo, vertical, logo, pie_pagina, Texto, TablaEncabezado, TablaDatos, color)

        respuesta = HttpResponse(buf.getvalue(), content_type='application/pdf')
        respuesta.headers['content-disposition']='inline; filename=%s.pdf' % titulo

        return respuesta

class OrdenCompraNuevaVersionView(BSModalUpdateView):
    model = OrdenCompra
    form_class = OrdenCompraAnularForm    
    template_name = "orden_compra/orden_compra/nueva_version.html"
    success_url = reverse_lazy('orden_compra_app:orden_compra_inicio')
    context_object_name = 'contexto_orden_compra' 

    def form_valid(self, form):
        if self.request.session['primero']:
            obj = OrdenCompra.objects.get(id = self.kwargs['pk'])
            numero_orden_compra = obj.sociedad.abreviatura + numeroXn(len(OrdenCompra.objects.filter(sociedad = obj.sociedad ))+1, 6)
            orden_compra_anterior = obj
            oferta_proveedor = obj.oferta_proveedor

            form.instance.oferta_proveedor = None
            form.instance.estado = 3
            registro_guardar(form.instance, self.request)
            
            obj.oferta_proveedor = None

            registro_guardar(obj, self.request)
            obj.save()

            orden = OrdenCompra.objects.create(
                internacional_nacional = obj.internacional_nacional,
                incoterms = obj.incoterms,
                numero_orden_compra= numero_orden_compra,
                oferta_proveedor= oferta_proveedor,
                orden_compra_anterior= orden_compra_anterior,
                sociedad= obj.sociedad,
                fecha_orden= obj.fecha_orden,
                moneda= obj.moneda,
                descuento_global = obj.descuento_global ,
                total_descuento = obj.total_descuento,
                total_anticipo = obj.total_anticipo,
                total_gravada = obj.total_gravada,
                total_inafacta = obj.total_inafacta,
                total_exonerada = obj.total_exonerada,
                total_igv = obj.total_igv,
                total_gratuita = obj.total_gratuita,
                total_otros_cargos = obj.total_otros_cargos,
                total_isc = obj.total_isc,
                total = obj.total,
                slug = slug_aleatorio(OrdenCompra),
                condiciones = obj.condiciones,
                estado=0,
            )

            orden_detalle = obj.OrdenCompraDetalle_orden_compra.all()
            for detalle in orden_detalle:
                detalle.material = detalle.content_type.get_object_for_this_type(id = detalle.id_registro)

                orden_detalle = OrdenCompraDetalle.objects.create(
                    item=detalle.item,
                    content_type=detalle.content_type,
                    id_registro=detalle.id_registro,
                    cantidad=detalle.cantidad,
                    precio_unitario_sin_igv = detalle.precio_unitario_sin_igv,
                    precio_unitario_con_igv = detalle.precio_unitario_con_igv,
                    precio_final_con_igv = detalle.precio_final_con_igv,
                    descuento = detalle.descuento,
                    sub_total = detalle.sub_total,
                    igv = detalle.igv,
                    total = detalle.total,
                    tipo_igv = detalle.tipo_igv,
                    orden_compra=orden,
                     
                    )
            messages.success(self.request, MENSAJE_ANULAR_ORDEN_COMPRA)
            self.request.session['primero'] = False
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        self.request.session['primero'] = True
        context = super(OrdenCompraNuevaVersionView, self).get_context_data(**kwargs)
        context['accion'] = 'Nueva Version'
        context['titulo'] = 'Orden de Compra'
        return context


class OrdenCompraDetailView(DetailView):
    model = OrdenCompra
    template_name = "orden_compra/orden_compra/detalle.html"
    context_object_name = 'contexto_orden_compra'

    def get_context_data(self, **kwargs):
        orden_compra = OrdenCompra.objects.get(slug = self.kwargs['slug'])

        context = super(OrdenCompraDetailView, self).get_context_data(**kwargs)
        
        orden_detalle = OrdenCompraDetalle.objects.ver_detalle(orden_compra)
        context['orden_compra_detalle'] = orden_detalle 
        context['totales'] = obtener_totales(OrdenCompra.objects.get(slug=self.kwargs['slug']))

        return context

def OrdenCompraDetailTabla(request, slug):
    data = dict()
    if request.method == 'GET':
        template = 'orden_compra/orden_compra/detalle_tabla.html'
        context = {}
        orden_compra = OrdenCompra.objects.get(slug = slug)
        context['contexto_orden_compra'] = orden_compra
        context['orden_compra_detalle'] = OrdenCompraDetalle.objects.filter(orden_compra = orden_compra)
        context['totales'] = obtener_totales(OrdenCompra.objects.get(slug=slug))

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)

class OrdenCompraPdfView(View):
    def get(self, request, *args, **kwargs):
        obj = OrdenCompra.objects.get(slug=self.kwargs['slug'])
        color = obj.sociedad.color
        titulo = 'Orden de Compra'
        vertical = False
        logo = [obj.sociedad.logo.url]
        pie_pagina = obj.sociedad.pie_pagina

        sociedad = obj.sociedad
        orden = obj
        proveedor = obj.oferta_proveedor.requerimiento_material.proveedor
        interlocutor = obj.oferta_proveedor.requerimiento_material.interlocutor_proveedor
        usuario = request.user

        TablaEncabezado = ['Item',
                            'Material',
                            'Unidad',
                            'Cantidad',
                            'Prec. Unit. sin IGV',
                            'Prec. Unit. con IGV',
                            'Prec. Final con IGV',
                            'Descuento',
                            'Sub Total',
                            'IGV',
                            'Total',
                            ]

        orden_detalle = obj.OrdenCompraDetalle_orden_compra.all()
        TablaDatos = []
        item = 1
        for detalle in orden_detalle:
            fila = []
            calculo = calculos_linea(detalle.cantidad, detalle.precio_unitario_con_igv, detalle.precio_final_con_igv, igv(obj.fecha_orden), detalle.tipo_igv)
            detalle.material = detalle.content_type.get_object_for_this_type(id = detalle.id_registro)
            fila.append(item)
            fila.append(intcomma(detalle.material))
            fila.append(intcomma(detalle.material.unidad_base))
            fila.append(intcomma(detalle.cantidad.quantize(Decimal('0.01'))))
            fila.append("%s %s" % (obj.moneda.simbolo, intcomma(calculo['precio_unitario_sin_igv'].quantize(Decimal('0.01')))))
            fila.append("%s %s" % (obj.moneda.simbolo, intcomma(detalle.precio_unitario_con_igv.quantize(Decimal('0.01')))))
            fila.append("%s %s" % (obj.moneda.simbolo, intcomma(detalle.precio_final_con_igv.quantize(Decimal('0.01')))))
            fila.append("%s %s" % (obj.moneda.simbolo, intcomma(calculo['descuento_con_igv'].quantize(Decimal('0.01')))))
            fila.append("%s %s" % (obj.moneda.simbolo, intcomma(calculo['subtotal'].quantize(Decimal('0.01')))))
            fila.append("%s %s" % (obj.moneda.simbolo, intcomma(calculo['igv'].quantize(Decimal('0.01')))))
            fila.append("%s %s" % (obj.moneda.simbolo, intcomma(calculo['total'].quantize(Decimal('0.01')))))
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

        buf = generarOrdenCompra(titulo, vertical, logo, pie_pagina, sociedad, orden, proveedor, interlocutor, usuario, TablaEncabezado, TablaDatos, TablaTotales, color)

        respuesta = HttpResponse(buf.getvalue(), content_type='application/pdf')
        respuesta.headers['content-disposition']='inline; filename=%s.pdf' % titulo

        return respuesta

class OrdenCompraEnviarCorreoView(BSModalFormView):
    template_name = "includes/formulario generico.html"
    form_class = OrdenCompraEnviarCorreoForm

    def get_success_url(self):
        return reverse_lazy('orden_compra_app:orden_compra_detalle', kwargs={'slug':self.kwargs['slug']})

    def form_valid(self, form):
        if self.request.session['primero']:
            orden = OrdenCompra.objects.get(slug=self.kwargs['slug'])            
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
        kwargs['proveedor'] = OrdenCompra.objects.get(slug=self.kwargs['slug']).oferta_proveedor.requerimiento_material.proveedor 
        return kwargs

    def get_context_data(self, **kwargs):
        self.request.session['primero'] = True
        context = super(OrdenCompraEnviarCorreoView, self).get_context_data(**kwargs)
        context['accion']="Enviar"
        context['titulo']="Correos"
        return context

class OfertaProveedorDetalleUpdateView(BSModalUpdateView):
    model = OrdenCompraDetalle
    template_name = "orden_compra/orden_compra/actualizar.html"
    form_class = OrdenCompraDetalleUpdateForm

    def get_success_url(self, **kwargs):
        return reverse_lazy('orden_compra_app:orden_compra_detalle', kwargs={'slug':self.get_object().orden_compra.slug})

    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(OfertaProveedorDetalleUpdateView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        context['titulo'] = "Precios"
        context['material'] = self.object
        context['valor_igv'] = igv()
        return context


class OfertaProveedorlDetalleCreateView(BSModalFormView):
    template_name = "orden_compra/orden_compra/form_material.html"
    form_class = OrdenCompraDetalleAgregarForm

    success_url = reverse_lazy('orden_compra_app:orden_compra_detalle')

    def form_valid(self, form):
        if self.request.session['primero']:
            orden_compra = OrdenCompra.objects.get(id = self.kwargs['pk'])
            item = len(OrdenCompraDetalle.objects.filter(orden_compra = orden_compra))

            material = form.cleaned_data.get('material')
            cantidad = form.cleaned_data.get('cantidad')

            obj, created = OrdenCompraDetalle.objects.get_or_create(
                content_type = ContentType.objects.get_for_model(material),
                id_registro = material.id,
                orden_compra = orden_compra,
            )
            if created:
                obj.item = item + 1
                obj.cantidad = cantidad
            # else:
                # obj.cantidad = obj.cantidad +cantidad 

            registro_guardar(obj, self.request)
            obj.save()
            self.request.session['primero'] = False
        return HttpResponseRedirect(self.success_url)

    def get_context_data(self, **kwargs):
        self.request.session['primero'] = True
        context = super(OfertaProveedorlDetalleCreateView, self).get_context_data(**kwargs)
        context['titulo'] = 'Agregar Material '
        context['accion'] = 'Guardar'
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
            sociedad = orden.sociedad,
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
                    tipo_stock = movimiento_final.tipo_stock_final,
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
