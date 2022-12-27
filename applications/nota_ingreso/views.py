from applications.almacenes.models import Almacen
from applications.importaciones import *
from applications.material.models import Material
from applications.movimiento_almacen.models import MovimientosAlmacen, TipoMovimiento
from applications.nota_ingreso.forms import NotaIngresoAgregarMaterialForm, NotaIngresoFinalizarConteoForm, NotaIngresoAnularConteoForm, NotaStockInicialAgregarMaterialForm, NotaStockInicialAnularForm, NotaStockInicialForm, NotaStockInicialGenerarNotaIngresoForm, NotaStockInicialGuardarForm
from applications.nota_ingreso.models import NotaIngreso, NotaIngresoDetalle, NotaStockInicial, NotaStockInicialDetalle
from applications.recepcion_compra.models import RecepcionCompra
from applications.funciones import numeroXn, registrar_excepcion

# Create your views here.

class NotaIngresoView(TemplateView):
    template_name = "nota_ingreso/nota_ingreso/inicio.html"

    def get_context_data(self, **kwargs):
        context = super(NotaIngresoView, self).get_context_data(**kwargs)
        recepcion = RecepcionCompra.objects.get(id=self.kwargs['recepcion_id'])
        context['contexto_nota_ingreso'] = NotaIngreso.objects.filter(
            content_type=ContentType.objects.get_for_model(recepcion),
            id_registro=recepcion.id,
            )
        context['recepcion'] = recepcion
        context['regresar'] = reverse_lazy('recepcion_compra_app:recepcion_compra_detalle', kwargs={'pk':self.kwargs['recepcion_id']})
        return context


class NotaIngresoNotaStockInicialView(TemplateView):
    template_name = "nota_ingreso/nota_ingreso/inicio.html"

    def get_context_data(self, **kwargs):
        context = super(NotaIngresoNotaStockInicialView, self).get_context_data(**kwargs)
        nota_stock_inicial = NotaStockInicial.objects.get(id=self.kwargs['nota_stock_inicial_id'])
        context['contexto_nota_ingreso'] = NotaIngreso.objects.filter(
            content_type=ContentType.objects.get_for_model(nota_stock_inicial),
            id_registro=nota_stock_inicial.id,
            )
        context['recepcion'] = nota_stock_inicial
        context['regresar'] = reverse_lazy('nota_ingreso_app:nota_stock_inicial_detalle', kwargs={'pk':self.kwargs['nota_stock_inicial_id']})
        return context


class NotaIngresoListaView(TemplateView):
    template_name = "nota_ingreso/nota_ingreso/inicio.html"

    def get_context_data(self, **kwargs):
        context = super(NotaIngresoListaView, self).get_context_data(**kwargs)
        context['contexto_nota_ingreso'] = NotaIngreso.objects.all()
        return context


class NotaIngresoDetailView(DetailView):
    model = NotaIngreso
    template_name = "nota_ingreso/nota_ingreso/detalle.html"
    context_object_name = 'contexto_nota_ingreso'

    def get_context_data(self, **kwargs):
        context = super(NotaIngresoDetailView, self).get_context_data(**kwargs)
        context['materiales'] = NotaIngreso.objects.ver_detalle(self.get_object().id)
        if self.get_object().content_type == ContentType.objects.get_for_model(RecepcionCompra):
            context['regresar'] = reverse_lazy('recepcion_compra_app:recepcion_compra_detalle', kwargs={'pk':self.get_object().id_registro})
        else:
            context['regresar'] = reverse_lazy('nota_ingreso_app:nota_stock_inicial_detalle', kwargs={'pk':self.get_object().id_registro})
        return context
    

def NotaIngresoDetailTabla(request, recepcion_id):
    data = dict()
    if request.method == 'GET':
        template = 'nota_ingreso/nota_ingreso/detalle_tabla.html'
        context = {}
        nota_ingreso = NotaIngreso.objects.get(id = recepcion_id)
        context['contexto_nota_ingreso'] = nota_ingreso
        context['materiales'] = NotaIngreso.objects.ver_detalle(recepcion_id)
        if nota_ingreso.content_type == ContentType.objects.get_for_model(RecepcionCompra):
            context['regresar'] = reverse_lazy('recepcion_compra_app:recepcion_compra_detalle', kwargs={'pk':nota_ingreso.id_registro})
        else:
            context['regresar'] = reverse_lazy('nota_ingreso_app:nota_stock_inicial_detalle', kwargs={'pk':nota_ingreso.id_registro})
        
        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)


class NotaIngresoAgregarMaterialView(BSModalFormView):
    template_name = "nota_ingreso/nota_ingreso/form.html"
    form_class = NotaIngresoAgregarMaterialForm
    
    def get_success_url(self, **kwargs):
        return reverse_lazy('nota_ingreso_app:nota_ingreso_detalle', kwargs={'pk':self.kwargs['id_nota_ingreso']})

    def get_form_kwargs(self, *args, **kwargs):
        nota_ingreso = NotaIngreso.objects.get(id=self.kwargs['id_nota_ingreso'])
        productos = []
        for detalle in nota_ingreso.recepcion_compra.documento.detalle:
            valor = "%s|%s" % (ContentType.objects.get_for_model(detalle).id, detalle.id)
            productos.append((valor, detalle.producto))
        kwargs = super(NotaIngresoAgregarMaterialView, self).get_form_kwargs(*args, **kwargs)
        kwargs['productos'] = productos
        return kwargs

    @transaction.atomic
    def form_valid(self, form):
        sid = transaction.savepoint()
        try:
            if self.request.session['primero']:
                nota_ingreso = NotaIngreso.objects.get(id=self.kwargs['id_nota_ingreso'])
                nuevo_item = len(NotaIngresoDetalle.objects.filter(nota_ingreso = nota_ingreso)) + 1
                cantidad = form.cleaned_data['cantidad']
                producto = form.cleaned_data['producto'].split("|")
                almacen = form.cleaned_data['almacen']
                content_type = ContentType.objects.get(id = int(producto[0]))
                id_registro = int(producto[1])
                comprobante_compra_detalle = content_type.model_class().objects.get(id = id_registro)
                
                buscar = NotaIngresoDetalle.objects.filter(
                    content_type=content_type,
                    id_registro=id_registro,
                ).exclude(nota_ingreso__estado=3)

                if buscar:
                    contar = buscar.aggregate(Sum('cantidad_conteo'))['cantidad_conteo__sum']
                else:
                    contar = 0

                if comprobante_compra_detalle.cantidad < contar + cantidad:
                    form.add_error('cantidad', 'Se superó la cantidad adquirida. Máximo: %s. Contado: %s.' % (comprobante_compra_detalle.cantidad, contar + cantidad))
                    return super().form_invalid(form)
                
                nota_ingreso_detalle, created = NotaIngresoDetalle.objects.get_or_create(
                    content_type=content_type,
                    id_registro=id_registro,
                    almacen = almacen,
                    nota_ingreso = nota_ingreso,
                )
                if created:
                    nota_ingreso_detalle.item = nuevo_item
                    nota_ingreso_detalle.cantidad_conteo = cantidad
                    nota_ingreso_detalle.created_by = self.request.user
                    nota_ingreso_detalle.updated_by = self.request.user
                else:
                    nota_ingreso_detalle.cantidad_conteo = nota_ingreso_detalle.cantidad_conteo + cantidad
                    nota_ingreso_detalle.updated_by = self.request.user
                nota_ingreso_detalle.save()
                
                self.request.session['primero'] = False
                return super().form_valid(form)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        self.request.session['primero'] = True
        context = super(NotaIngresoAgregarMaterialView, self).get_context_data(**kwargs)
        context['accion'] = "Contar"
        context['titulo'] = "Material"
        context['url_sede'] = reverse_lazy('logistica_app:almacen', kwargs={'id_sede':1})[:-2]
        return context


class NotaIngresoActualizarMaterialView(BSModalFormView):
    template_name = "nota_ingreso/nota_ingreso/form.html"
    form_class = NotaIngresoAgregarMaterialForm
    
    def get_success_url(self, **kwargs):
        nota_ingreso_detalle = NotaIngresoDetalle.objects.get(id=self.kwargs['id_nota_ingreso_detalle'])
        nota_ingreso = nota_ingreso_detalle.nota_ingreso
        return reverse_lazy('nota_ingreso_app:nota_ingreso_detalle', kwargs={'pk':nota_ingreso.id})

    def get_form_kwargs(self, *args, **kwargs):
        nota_ingreso_detalle = NotaIngresoDetalle.objects.get(id=self.kwargs['id_nota_ingreso_detalle'])
        nota_ingreso = nota_ingreso_detalle.nota_ingreso
        productos = []
        for detalle in nota_ingreso.recepcion_compra.documento.detalle:
            valor = "%s|%s" % (ContentType.objects.get_for_model(detalle).id, detalle.id)
            productos.append((valor, detalle.producto))
        kwargs = super(NotaIngresoActualizarMaterialView, self).get_form_kwargs(*args, **kwargs)
        kwargs['productos'] = productos
        kwargs['nota_ingreso_detalle'] = nota_ingreso_detalle
        return kwargs

    @transaction.atomic
    def form_valid(self, form):
        sid = transaction.savepoint()
        try:
            if self.request.session['primero']:
                nota_ingreso_detalle = NotaIngresoDetalle.objects.get(id=self.kwargs['id_nota_ingreso_detalle'])
                cantidad = form.cleaned_data['cantidad']
                producto = form.cleaned_data['producto'].split("|")
                almacen = form.cleaned_data['almacen']
                content_type = ContentType.objects.get(id = int(producto[0]))
                id_registro = int(producto[1])
                comprobante_compra_detalle = content_type.model_class().objects.get(id = id_registro)

                buscar = NotaIngresoDetalle.objects.filter(
                    content_type=content_type,
                    id_registro=id_registro,
                    almacen = almacen,
                    nota_ingreso = nota_ingreso_detalle.nota_ingreso,
                ).exclude(id=nota_ingreso_detalle.id).exclude(nota_ingreso__estado=3)

                if len(buscar)>0:
                    form.add_error('almacen', 'Ya existe ese producto en ese almacén')
                    return super().form_invalid(form)

                buscar = NotaIngresoDetalle.objects.filter(
                    content_type=content_type,
                    id_registro=id_registro,
                ).exclude(id=nota_ingreso_detalle.id).exclude(nota_ingreso__estado=3)

                if buscar:
                    contar = buscar.aggregate(Sum('cantidad_conteo'))['cantidad_conteo__sum']
                else:
                    contar = 0

                if comprobante_compra_detalle.cantidad < contar + cantidad:
                    form.add_error('cantidad', 'Se superó la cantidad adquirida. Máximo: %s. Contado: %s.' % (comprobante_compra_detalle.cantidad, contar + cantidad))
                    return super().form_invalid(form)
                
                nota_ingreso_detalle.content_type=content_type
                nota_ingreso_detalle.id_registro=id_registro
                nota_ingreso_detalle.cantidad_conteo = cantidad
                nota_ingreso_detalle.almacen = almacen
                nota_ingreso_detalle.updated_by = self.request.user
                nota_ingreso_detalle.save()
                
                self.request.session['primero'] = False
                return super().form_valid(form)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        self.request.session['primero'] = True
        context = super(NotaIngresoActualizarMaterialView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        context['titulo'] = "Material"
        context['url_sede'] = reverse_lazy('logistica_app:almacen', kwargs={'id_sede':1})[:-2]
        return context


class NotaIngresoDetalleEliminarView(BSModalDeleteView):
    model = NotaIngresoDetalle
    template_name = "includes/eliminar generico.html"
    
    def get_success_url(self, **kwargs):
        nota_ingreso = self.object.nota_ingreso
        return reverse_lazy('nota_ingreso_app:nota_ingreso_detalle', kwargs={'pk':nota_ingreso.id})

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            materiales = NotaIngresoDetalle.objects.filter(nota_ingreso=self.get_object().nota_ingreso)
            contador = 1
            for material in materiales:
                if material == self.get_object():continue
                material.item = contador
                material.save()
                contador += 1
            return super().delete(request, *args, **kwargs)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(NotaIngresoDetalleEliminarView, self).get_context_data(**kwargs)
        context['accion'] = "Eliminar"
        context['titulo'] = "Detalle"
        context['item'] = "%s - %s" % (self.object.item, self.object)
        return context


class NotaIngresoFinalizarConteoView(BSModalUpdateView):
    model = NotaIngreso
    template_name = "includes/formulario generico.html"
    form_class = NotaIngresoFinalizarConteoForm
    
    def get_success_url(self, **kwargs):
        return reverse_lazy('nota_ingreso_app:nota_ingreso_detalle', kwargs={'pk':self.object.id})

    @transaction.atomic
    def form_valid(self, form):
        sid = transaction.savepoint()
        try:
            detalles = form.instance.NotaIngresoDetalle_nota_ingreso.all()
            if form.instance.content_type == ContentType.objects.get_for_model(RecepcionCompra):
                movimiento_inicial = TipoMovimiento.objects.get(codigo=101)
            else:
                movimiento_inicial = TipoMovimiento.objects.get(codigo=999)

            for detalle in detalles:
                if detalle.comprobante_compra_detalle.producto.control_calidad or detalle.comprobante_compra_detalle.producto.control_serie:
                    movimiento_final = TipoMovimiento.objects.get(codigo=104)
                else:
                    movimiento_final = TipoMovimiento.objects.get(codigo=102)

                movimiento_anterior = MovimientosAlmacen.objects.get(
                    content_type_producto = detalle.comprobante_compra_detalle.orden_compra_detalle.content_type,
                    id_registro_producto = detalle.comprobante_compra_detalle.orden_compra_detalle.id_registro,
                    tipo_movimiento = movimiento_inicial,
                    tipo_stock = movimiento_inicial.tipo_stock_final,
                    signo_factor_multiplicador = +1,
                    content_type_documento_proceso = ContentType.objects.get_for_model(form.instance.recepcion_compra),
                    id_registro_documento_proceso = form.instance.recepcion_compra.id,
                    sociedad = form.instance.recepcion_compra.documento.sociedad,
                    movimiento_reversion = False,
                )

                movimiento_uno = MovimientosAlmacen.objects.create(
                    content_type_producto = detalle.comprobante_compra_detalle.orden_compra_detalle.content_type,
                    id_registro_producto = detalle.comprobante_compra_detalle.orden_compra_detalle.id_registro,
                    cantidad = detalle.cantidad_conteo,
                    tipo_movimiento = movimiento_final,
                    tipo_stock = movimiento_final.tipo_stock_inicial,
                    signo_factor_multiplicador = -1,
                    content_type_documento_proceso = ContentType.objects.get_for_model(form.instance),
                    id_registro_documento_proceso = form.instance.id,
                    almacen = None,
                    sociedad = form.instance.recepcion_compra.documento.sociedad,
                    movimiento_anterior = movimiento_anterior,
                    movimiento_reversion = False,
                    created_by = self.request.user,
                    updated_by = self.request.user,
                )
                movimiento_dos = MovimientosAlmacen.objects.create(
                    content_type_producto = detalle.comprobante_compra_detalle.orden_compra_detalle.content_type,
                    id_registro_producto = detalle.comprobante_compra_detalle.orden_compra_detalle.id_registro,
                    cantidad = detalle.cantidad_conteo,
                    tipo_movimiento = movimiento_final,
                    tipo_stock = movimiento_final.tipo_stock_final,
                    signo_factor_multiplicador = +1,
                    content_type_documento_proceso = ContentType.objects.get_for_model(form.instance),
                    id_registro_documento_proceso = form.instance.id,
                    almacen = detalle.almacen,
                    sociedad = form.instance.recepcion_compra.documento.sociedad,
                    movimiento_anterior = movimiento_uno,
                    movimiento_reversion = False,
                    created_by = self.request.user,
                    updated_by = self.request.user,
                )

            form.instance.estado = 2
            registro_guardar(form.instance, self.request)
                
            return super().form_valid(form)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(NotaIngresoFinalizarConteoView, self).get_context_data(**kwargs)
        context['accion'] = "Finalizar"
        context['titulo'] = "Conteo"
        return context


class NotaIngresoAnularConteoView(BSModalUpdateView):
    model = NotaIngreso
    template_name = "includes/formulario generico.html"
    form_class = NotaIngresoAnularConteoForm
    
    def get_success_url(self, **kwargs):
        return reverse_lazy('nota_ingreso_app:nota_ingreso_detalle', kwargs={'pk':self.object.id})

    @transaction.atomic
    def form_valid(self, form):
        sid = transaction.savepoint()
        try:
            detalles = form.instance.NotaIngresoDetalle_nota_ingreso.all()

            for detalle in detalles:
                # if detalle.comprobante_compra_detalle.producto.control_calidad:
                #     movimiento_final = TipoMovimiento.objects.get(codigo=104)
                # elif detalle.comprobante_compra_detalle.producto.control_serie:
                #     movimiento_final = TipoMovimiento.objects.get(codigo=103)
                # else:
                #     movimiento_final = TipoMovimiento.objects.get(codigo=102)

                movimiento_dos = MovimientosAlmacen.objects.get(
                    content_type_producto = detalle.comprobante_compra_detalle.orden_compra_detalle.content_type,
                    id_registro_producto = detalle.comprobante_compra_detalle.orden_compra_detalle.id_registro,
                    cantidad = detalle.cantidad_conteo,
                    # tipo_movimiento = movimiento_final,
                    # tipo_stock = movimiento_final.tipo_stock_final,
                    signo_factor_multiplicador = +1,
                    content_type_documento_proceso = ContentType.objects.get_for_model(form.instance),
                    id_registro_documento_proceso = form.instance.id,
                    almacen = detalle.almacen,
                    sociedad = form.instance.recepcion_compra.documento.sociedad,
                    movimiento_reversion = False,
                )

                movimiento_uno = movimiento_dos.movimiento_anterior

                movimiento_dos.delete()
                movimiento_uno.delete()

            form.instance.estado = 3
            registro_guardar(form.instance, self.request)
            messages.success(self.request, MENSAJE_ANULAR_CONTEO)
            return super().form_valid(form)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
            return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(NotaIngresoAnularConteoView, self).get_context_data(**kwargs)
        context['accion'] = "Anular"
        context['titulo'] = "Conteo"
        return context


#####################################################

class NotaStockInicialCreateView(PermissionRequiredMixin, BSModalCreateView):
    permission_required = ('nota_ingreso.add_notastockinicial')

    model = NotaStockInicial
    template_name = "includes/formulario generico.html"
    form_class = NotaStockInicialForm

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('nota_ingreso_app:nota_stock_inicial_detalle', kwargs={'pk':self.object.id})
    
    def get_context_data(self, **kwargs):
        context = super(NotaStockInicialCreateView, self).get_context_data(**kwargs)
        context['accion']="Crear"
        context['titulo']="Nota de Stock Inicial"
        return context

    def form_valid(self, form):
        nro_nota_stock_inicial = NotaStockInicial.objects.all().aggregate(Max('nro_nota_stock_inicial'))['nro_nota_stock_inicial__max'] + 1
        print("**************************")
        print(nro_nota_stock_inicial)
        print("**************************")
        form.instance.nro_nota_stock_inicial = nro_nota_stock_inicial
        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)

        return super().form_valid(form)


class NotaStockInicialEliminarView(BSModalDeleteView):
    model = NotaStockInicial
    template_name = "includes/eliminar generico.html"
    success_url = reverse_lazy('nota_ingreso_app:nota_stock_inicial_lista_total')

    def get_context_data(self, **kwargs):
        context = super(NotaStockInicialEliminarView, self).get_context_data(**kwargs)
        context['accion'] = "Eliminar"
        context['titulo'] = "Nota Stock Inicial"
        context['item'] = "%s" % (self.object)
        return context


class NotaStockInicialListaView(TemplateView):
    template_name = "nota_ingreso/nota_stock_inicial/inicio.html"

    def get_context_data(self, **kwargs):
        context = super(NotaStockInicialListaView, self).get_context_data(**kwargs)
        context['contexto_nota_stock_inicial'] = NotaStockInicial.objects.all()
        return context


class NotaStockInicialDetailView(DetailView):
    model = NotaStockInicial
    template_name = "nota_ingreso/nota_stock_inicial/detalle.html"
    context_object_name = 'contexto_nota_stock_inicial'

    def get_context_data(self, **kwargs):
        context = super(NotaStockInicialDetailView, self).get_context_data(**kwargs)
        context['materiales'] = NotaStockInicial.objects.ver_detalle(self.get_object().id)
        context['regresar'] = reverse_lazy('nota_ingreso_app:nota_stock_inicial_lista_total')
        return context
    

def NotaStockInicialDetailTabla(request, pk):
    data = dict()
    if request.method == 'GET':
        template = 'nota_ingreso/nota_stock_inicial/detalle_tabla.html'
        context = {}
        nota_stock_inicial = NotaStockInicial.objects.get(id = pk)
        context['contexto_nota_stock_inicial'] = nota_stock_inicial
        context['materiales'] = NotaStockInicial.objects.ver_detalle(pk)
        context['regresar'] = reverse_lazy('nota_ingreso_app:nota_stock_inicial_lista_total')
        
        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)


class NotaStockInicialAgregarMaterialView(BSModalFormView):
    template_name = "nota_ingreso/nota_stock_inicial/form.html"
    form_class = NotaStockInicialAgregarMaterialForm
    
    def get_success_url(self, **kwargs):
        return reverse_lazy('nota_ingreso_app:nota_stock_inicial_detalle', kwargs={'pk':self.kwargs['id_nota_stock_inicial']})

    def get_form_kwargs(self, *args, **kwargs):
        productos = []
        for detalle in Material.objects.all():
            valor = "%s|%s" % (ContentType.objects.get_for_model(detalle).id, detalle.id)
            productos.append((valor, detalle.descripcion_venta))
        kwargs = super(NotaStockInicialAgregarMaterialView, self).get_form_kwargs(*args, **kwargs)
        kwargs['productos'] = productos
        return kwargs

    @transaction.atomic
    def form_valid(self, form):
        sid = transaction.savepoint()
        try:
            if self.request.session['primero']:
                nota_stock_inicial = NotaStockInicial.objects.get(id=self.kwargs['id_nota_stock_inicial'])
                nuevo_item = len(NotaStockInicialDetalle.objects.filter(nota_stock_inicial = nota_stock_inicial)) + 1
                cantidad = form.cleaned_data['cantidad']
                producto = form.cleaned_data['producto'].split("|")
                content_type = ContentType.objects.get(id = int(producto[0]))
                id_registro = int(producto[1])
                
                nota_stock_inicial_detalle, created = NotaStockInicialDetalle.objects.get_or_create(
                    content_type=content_type,
                    id_registro=id_registro,
                    nota_stock_inicial = nota_stock_inicial,
                )
                if created:
                    nota_stock_inicial_detalle.item = nuevo_item
                    nota_stock_inicial_detalle.cantidad_total = cantidad
                    nota_stock_inicial_detalle.created_by = self.request.user
                    nota_stock_inicial_detalle.updated_by = self.request.user
                else:
                    nota_stock_inicial_detalle.cantidad_total = nota_stock_inicial_detalle.cantidad_total + cantidad
                    nota_stock_inicial_detalle.updated_by = self.request.user
                nota_stock_inicial_detalle.save()
                
                self.request.session['primero'] = False
                return super().form_valid(form)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        self.request.session['primero'] = True
        context = super(NotaStockInicialAgregarMaterialView, self).get_context_data(**kwargs)
        context['accion'] = "Agregar"
        context['titulo'] = "Material"
        return context


class NotaStockInicialActualizarMaterialView(BSModalFormView):
    template_name = "nota_ingreso/nota_stock_inicial/form.html"
    form_class = NotaStockInicialAgregarMaterialForm
    
    def get_success_url(self, **kwargs):
        nota_stock_inicial_detalle = NotaStockInicialDetalle.objects.get(id=self.kwargs['id_nota_stock_inicial_detalle'])
        nota_stock_inicial = nota_stock_inicial_detalle.nota_stock_inicial
        return reverse_lazy('nota_ingreso_app:nota_stock_inicial_detalle', kwargs={'pk':nota_stock_inicial.id})

    def get_form_kwargs(self, *args, **kwargs):
        nota_stock_inicial_detalle = NotaStockInicialDetalle.objects.get(id=self.kwargs['id_nota_stock_inicial_detalle'])
        productos = []
        for detalle in Material.objects.all():
            valor = "%s|%s" % (ContentType.objects.get_for_model(detalle).id, detalle.id)
            productos.append((valor, detalle.descripcion_venta))
        kwargs = super(NotaStockInicialActualizarMaterialView, self).get_form_kwargs(*args, **kwargs)
        kwargs['productos'] = productos
        kwargs['nota_stock_inicial_detalle'] = nota_stock_inicial_detalle
        return kwargs

    @transaction.atomic
    def form_valid(self, form):
        sid = transaction.savepoint()
        try:
            if self.request.session['primero']:
                nota_stock_inicial_detalle = NotaStockInicialDetalle.objects.get(id=self.kwargs['id_nota_stock_inicial_detalle'])
                cantidad = form.cleaned_data['cantidad']
                producto = form.cleaned_data['producto'].split("|")
                content_type = ContentType.objects.get(id = int(producto[0]))
                id_registro = int(producto[1])
                
                nota_stock_inicial_detalle.content_type=content_type
                nota_stock_inicial_detalle.id_registro=id_registro
                nota_stock_inicial_detalle.cantidad_total = cantidad
                nota_stock_inicial_detalle.updated_by = self.request.user
                nota_stock_inicial_detalle.save()
                
                self.request.session['primero'] = False
                return super().form_valid(form)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        self.request.session['primero'] = True
        context = super(NotaStockInicialActualizarMaterialView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        context['titulo'] = "Material"
        return context


class NotaStockInicialDetalleEliminarView(BSModalDeleteView):
    model = NotaStockInicialDetalle
    template_name = "includes/eliminar generico.html"
    
    def get_success_url(self, **kwargs):
        nota_stock_inicial = self.object.nota_stock_inicial
        return reverse_lazy('nota_ingreso_app:nota_stock_inicial_detalle', kwargs={'pk':nota_stock_inicial.id})

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            materiales = NotaStockInicialDetalle.objects.filter(nota_stock_inicial=self.get_object().nota_stock_inicial)
            contador = 1
            for material in materiales:
                if material == self.get_object():continue
                material.item = contador
                material.save()
                contador += 1
            return super().delete(request, *args, **kwargs)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(NotaStockInicialDetalleEliminarView, self).get_context_data(**kwargs)
        context['accion'] = "Eliminar"
        context['titulo'] = "Detalle"
        context['item'] = "%s" % (self.object)
        return context


class NotaStockInicialGuardarView(BSModalUpdateView):
    model = NotaStockInicial
    template_name = "includes/formulario generico.html"
    form_class = NotaStockInicialGuardarForm
    
    def get_success_url(self, **kwargs):
        return reverse_lazy('nota_ingreso_app:nota_stock_inicial_detalle', kwargs={'pk':self.object.id})

    @transaction.atomic
    def form_valid(self, form):
        sid = transaction.savepoint()
        try:
            detalles = form.instance.NotaStockInicialDetalle_nota_stock_inicial.all()
            movimiento_final = TipoMovimiento.objects.get(codigo=999)
            
            for detalle in detalles:

                movimiento_dos = MovimientosAlmacen.objects.create(
                    content_type_producto = detalle.content_type,
                    id_registro_producto = detalle.id_registro,
                    cantidad = detalle.cantidad_total,
                    tipo_movimiento = movimiento_final,
                    tipo_stock = movimiento_final.tipo_stock_final,
                    signo_factor_multiplicador = +1,
                    content_type_documento_proceso = ContentType.objects.get_for_model(form.instance),
                    id_registro_documento_proceso = form.instance.id,
                    sociedad = form.instance.sociedad,
                    movimiento_reversion = False,
                    created_by = self.request.user,
                    updated_by = self.request.user,
                )

            form.instance.estado = 2
            registro_guardar(form.instance, self.request)
                
            return super().form_valid(form)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(NotaStockInicialGuardarView, self).get_context_data(**kwargs)
        context['accion'] = "Finalizar"
        context['titulo'] = "Conteo"
        return context


class NotaStockInicialAnularView(BSModalUpdateView):
    model = NotaStockInicial
    template_name = "includes/formulario generico.html"
    form_class = NotaStockInicialAnularForm
    
    def get_success_url(self, **kwargs):
        return reverse_lazy('nota_ingreso_app:nota_stock_inicial_detalle', kwargs={'pk':self.object.id})

    @transaction.atomic
    def form_valid(self, form):
        sid = transaction.savepoint()
        try:
            detalles = form.instance.NotaStockInicialDetalle_nota_stock_inicial.all()

            for detalle in detalles:
                movimiento_dos = MovimientosAlmacen.objects.get(
                    content_type_producto = detalle.content_type,
                    id_registro_producto = detalle.id_registro,
                    cantidad = detalle.cantidad_total,
                    # tipo_movimiento = movimiento_final,
                    # tipo_stock = movimiento_final.tipo_stock_final,
                    signo_factor_multiplicador = +1,
                    content_type_documento_proceso = ContentType.objects.get_for_model(form.instance),
                    id_registro_documento_proceso = form.instance.id,
                    sociedad = form.instance.sociedad,
                    movimiento_reversion = False,
                )

                movimiento_dos.delete()
                
            form.instance.estado = 3
            registro_guardar(form.instance, self.request)
            messages.success(self.request, MENSAJE_ANULAR_CONTEO)
            return super().form_valid(form)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
            return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(NotaStockInicialAnularView, self).get_context_data(**kwargs)
        context['accion'] = "Anular"
        context['titulo'] = "Stock Inicial"
        return context


class NotaStockInicialGenerarNotaIngresoView(BSModalFormView):
    template_name = "includes/formulario generico.html"
    form_class = NotaStockInicialGenerarNotaIngresoForm
    
    def get_success_url(self, **kwargs):
        return reverse_lazy('nota_ingreso_app:nota_ingreso_detalle', kwargs={'pk':self.kwargs['nota'].id})

    @transaction.atomic
    def form_valid(self, form):
        sid = transaction.savepoint()
        try:
            if self.request.session['primero']:
                nota_stock_inicial = NotaStockInicial.objects.get(id=self.kwargs['pk'])
                numero_nota = len(NotaIngreso.objects.all()) + 1
                nota = NotaIngreso.objects.create(
                    nro_nota_ingreso = numeroXn(numero_nota, 6),
                    content_type = ContentType.objects.get_for_model(nota_stock_inicial),
                    id_registro = nota_stock_inicial.id,
                    sociedad = nota_stock_inicial.sociedad,
                    fecha_ingreso = form.cleaned_data['fecha_ingreso'],
                    created_by = self.request.user,
                    updated_by = self.request.user,
                )
                self.kwargs['nota']=nota
                self.request.session['primero'] = False
            return super().form_valid(form)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        self.request.session['primero'] = True
        context = super(NotaStockInicialGenerarNotaIngresoView, self).get_context_data(**kwargs)
        context['accion'] = "Recibir"
        context['titulo'] = "Nota de Ingreso"
        return context
