from applications.almacenes.models import Almacen
from applications.importaciones import *
from applications.movimiento_almacen.models import MovimientosAlmacen, TipoMovimiento
from applications.nota_ingreso.forms import NotaIngresoAgregarMaterialForm, NotaIngresoFinalizarConteoForm
from applications.nota_ingreso.models import NotaIngreso, NotaIngresoDetalle
from applications.recepcion_compra.models import RecepcionCompra

# Create your views here.

class NotaIngresoView(TemplateView):
    template_name = "nota_ingreso/nota_ingreso/inicio.html"

    def get_context_data(self, **kwargs):
        context = super(NotaIngresoView, self).get_context_data(**kwargs)
        recepcion = RecepcionCompra.objects.get(id=self.kwargs['recepcion_id'])
        context['contexto_nota_ingreso'] = NotaIngreso.objects.filter(recepcion_compra=recepcion)
        context['recepcion'] = recepcion
        context['regresar'] = reverse_lazy('recepcion_compra_app:recepcion_compra_detalle', kwargs={'pk':self.kwargs['recepcion_id']})
        return context


class NotaIngresoDetailView(DetailView):
    model = NotaIngreso
    template_name = "nota_ingreso/nota_ingreso/detalle.html"
    context_object_name = 'contexto_nota_ingreso'

    def get_context_data(self, **kwargs):
        context = super(NotaIngresoDetailView, self).get_context_data(**kwargs)
        context['materiales'] = NotaIngreso.objects.ver_detalle(self.get_object().id)
        context['regresar'] = reverse_lazy('recepcion_compra_app:recepcion_compra_detalle', kwargs={'pk':self.get_object().recepcion_compra.id})
        return context
    

def NotaIngresoDetailTabla(request, recepcion_id):
    data = dict()
    if request.method == 'GET':
        template = 'nota_ingreso/nota_ingreso/detalle_tabla.html'
        context = {}
        nota_ingreso = NotaIngreso.objects.get(id = recepcion_id)
        context['contexto_nota_ingreso'] = nota_ingreso
        context['materiales'] = NotaIngreso.objects.ver_detalle(recepcion_id)
        context['regresar'] = reverse_lazy('recepcion_compra_app:recepcion_compra_detalle', kwargs={'pk':nota_ingreso.recepcion_compra.id})
        
        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)


class NotaIngresoAgregarMaterialView(BSModalFormView):
    template_name = "includes/formulario generico.html"
    form_class = NotaIngresoAgregarMaterialForm
    
    def get_success_url(self, **kwargs):
        return reverse_lazy('nota_ingreso_app:nota_ingreso_detalle', kwargs={'pk':self.kwargs['id_nota_ingreso']})

    def get_form_kwargs(self, *args, **kwargs):
        nota_ingreso = NotaIngreso.objects.get(id=self.kwargs['id_nota_ingreso'])
        productos = []
        for detalle in nota_ingreso.recepcion_compra.documento.detalle:
            valor = "%s|%s" % (ContentType.objects.get_for_model(detalle).id, detalle.id)
            productos.append((valor, detalle.producto))
        almacenes = Almacen.objects.filter(sede__sociedad = nota_ingreso.sociedad)
        kwargs = super(NotaIngresoAgregarMaterialView, self).get_form_kwargs(*args, **kwargs)
        kwargs['productos'] = productos
        kwargs['almacenes'] = almacenes
        return kwargs

    def form_valid(self, form):
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
                comprobante_compra_detalle = comprobante_compra_detalle,
            )

            if buscar:
                contar = buscar.aggregate(Sum('cantidad_conteo'))['cantidad_conteo__sum']
            else:
                contar = 0

            if comprobante_compra_detalle.cantidad < contar + cantidad:
                form.add_error('cantidad', 'Se superó la cantidad adquirida. Máximo: %s. Contado: %s.' % (comprobante_compra_detalle.cantidad, contar + cantidad))
                return super().form_invalid(form)
            
            nota_ingreso_detalle, created = NotaIngresoDetalle.objects.get_or_create(
                comprobante_compra_detalle = comprobante_compra_detalle,
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

    def get_context_data(self, **kwargs):
        self.request.session['primero'] = True
        context = super(NotaIngresoAgregarMaterialView, self).get_context_data(**kwargs)
        context['accion'] = "Contar"
        context['titulo'] = "Material"
        return context


class NotaIngresoActualizarMaterialView(BSModalFormView):
    template_name = "includes/formulario generico.html"
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
        almacenes = Almacen.objects.filter(sede__sociedad = nota_ingreso.sociedad)
        kwargs = super(NotaIngresoActualizarMaterialView, self).get_form_kwargs(*args, **kwargs)
        kwargs['productos'] = productos
        kwargs['almacenes'] = almacenes
        kwargs['nota_ingreso_detalle'] = nota_ingreso_detalle
        return kwargs

    def form_valid(self, form):
        if self.request.session['primero']:
            nota_ingreso_detalle = NotaIngresoDetalle.objects.get(id=self.kwargs['id_nota_ingreso_detalle'])
            cantidad = form.cleaned_data['cantidad']
            producto = form.cleaned_data['producto'].split("|")
            almacen = form.cleaned_data['almacen']
            content_type = ContentType.objects.get(id = int(producto[0]))
            id_registro = int(producto[1])
            comprobante_compra_detalle = content_type.model_class().objects.get(id = id_registro)

            buscar = NotaIngresoDetalle.objects.filter(
                comprobante_compra_detalle = comprobante_compra_detalle,
                almacen = almacen,
                nota_ingreso = nota_ingreso_detalle.nota_ingreso,
            ).exclude(id=nota_ingreso_detalle.id)

            if len(buscar)>0:
                form.add_error('almacen', 'Ya existe ese producto en ese almacén')
                return super().form_invalid(form)

            buscar = NotaIngresoDetalle.objects.filter(
                comprobante_compra_detalle = comprobante_compra_detalle,
            ).exclude(id=nota_ingreso_detalle.id)

            if buscar:
                contar = buscar.aggregate(Sum('cantidad_conteo'))['cantidad_conteo__sum']
            else:
                contar = 0

            if comprobante_compra_detalle.cantidad < contar + cantidad:
                form.add_error('cantidad', 'Se superó la cantidad adquirida. Máximo: %s. Contado: %s.' % (comprobante_compra_detalle.cantidad, contar + cantidad))
                return super().form_invalid(form)
            
            nota_ingreso_detalle.comprobante_compra_detalle = comprobante_compra_detalle
            nota_ingreso_detalle.cantidad_conteo = cantidad
            nota_ingreso_detalle.almacen = almacen
            nota_ingreso_detalle.updated_by = self.request.user
            nota_ingreso_detalle.save()
            
            self.request.session['primero'] = False
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        self.request.session['primero'] = True
        context = super(NotaIngresoActualizarMaterialView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        context['titulo'] = "Material"
        return context


class NotaIngresoDetalleEliminarView(BSModalDeleteView):
    model = NotaIngresoDetalle
    template_name = "includes/eliminar generico.html"
    
    def get_success_url(self, **kwargs):
        nota_ingreso = self.object.nota_ingreso
        return reverse_lazy('nota_ingreso_app:nota_ingreso_detalle', kwargs={'pk':nota_ingreso.id})

    def delete(self, request, *args, **kwargs):
        materiales = NotaIngresoDetalle.objects.filter(nota_ingreso=self.get_object().nota_ingreso)
        contador = 1
        for material in materiales:
            if material == self.get_object():continue
            material.item = contador
            material.save()
            contador += 1
        return super().delete(request, *args, **kwargs)

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

    def form_valid(self, form):
        detalles = form.instance.NotaIngresoDetalle_nota_ingreso.all()
        movimiento_inicial = TipoMovimiento.objects.get(codigo=101)

        for detalle in detalles:
            if detalle.comprobante_compra_detalle.producto.control_calidad:
                movimiento_final = TipoMovimiento.objects.get(codigo=104)
            elif detalle.comprobante_compra_detalle.producto.control_serie:
                movimiento_final = TipoMovimiento.objects.get(codigo=103)
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
            
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(NotaIngresoFinalizarConteoView, self).get_context_data(**kwargs)
        context['accion'] = "Finalizar"
        context['titulo'] = "Conteo"
        return context