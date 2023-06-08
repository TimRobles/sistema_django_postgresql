from decimal import Decimal
from applications.funciones import numeroXn, registrar_excepcion
from applications.links import link_detalle
from applications.home.templatetags.funciones_propias import filename
from applications.importaciones import *
from applications.movimiento_almacen.models import MovimientosAlmacen
from applications.nota_ingreso.models import NotaIngreso, NotaIngresoDetalle
from applications.recepcion_compra.forms import ArchivoRecepcionCompraForm, FotoRecepcionCompraForm, RecepcionCompraAnularForm, RecepcionCompraGenerarNotaIngresoForm
from .models import DocumentoReclamo, DocumentoReclamoDetalle, FotoRecepcionCompra, RecepcionCompra, ArchivoRecepcionCompra

# Create your views here.

class RecepcionCompraDetailView(PermissionRequiredMixin, DetailView):
    permission_required = ('recepcion_compra.view_recepcioncompra')
    model = RecepcionCompra
    template_name = "recepcion_compra/recepcion_compra/detalle.html"
    context_object_name = 'contexto_recepcion_compra'

    def get_context_data(self, **kwargs):
        context = super(RecepcionCompraDetailView, self).get_context_data(**kwargs)
        context['materiales'] = self.get_object().content_type.model_class().objects.ver_detalle(self.get_object().id_registro)
        context['archivos'] = ArchivoRecepcionCompra.objects.filter(recepcion_compra=self.get_object())
        context['fotos'] = FotoRecepcionCompra.objects.filter(recepcion_compra=self.get_object())
        context['regresar'] = link_detalle(self.get_object().content_type, self.get_object().content_type.get_object_for_this_type(id=self.get_object().id_registro).slug)
        return context
    

def RecepcionCompraDetailTabla(request, pk):
    data = dict()
    if request.method == 'GET':
        template = 'recepcion_compra/recepcion_compra/detalle_tabla.html'
        context = {}
        recepcion_compra = RecepcionCompra.objects.get(id = pk)
        context['contexto_recepcion_compra'] = recepcion_compra
        context['materiales'] = recepcion_compra.content_type.model_class().objects.ver_detalle(recepcion_compra.id_registro)
        context['archivos'] = ArchivoRecepcionCompra.objects.filter(recepcion_compra=recepcion_compra)
        context['fotos'] = FotoRecepcionCompra.objects.filter(recepcion_compra=recepcion_compra)

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)


class RecepcionCompraAnularView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('recepcion_compra.delete_recepcioncompra')
    model = RecepcionCompra
    template_name = "includes/formulario generico.html"
    form_class = RecepcionCompraAnularForm
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)
    
    def get_success_url(self, **kwargs):
        return reverse_lazy('recepcion_compra_app:recepcion_compra_detalle', kwargs={'pk':self.object.id})

    @transaction.atomic
    def form_valid(self, form):
        sid = transaction.savepoint()
        try:
            documento = form.instance.documento
            detalles = documento.detalle
            for detalle in detalles:
                movimiento_dos = MovimientosAlmacen.objects.get(
                    content_type_producto = detalle.orden_compra_detalle.content_type,
                    id_registro_producto = detalle.orden_compra_detalle.id_registro,
                    cantidad = detalle.cantidad,
                    signo_factor_multiplicador = +1,
                    content_type_documento_proceso = ContentType.objects.get_for_model(form.instance),
                    id_registro_documento_proceso = form.instance.id,
                    almacen = None,
                    sociedad = documento.sociedad,
                    movimiento_reversion = False,
                )

                movimiento_uno = movimiento_dos.movimiento_anterior

                movimiento_dos.delete()
                movimiento_uno.delete()

            form.instance.estado = 2
            registro_guardar(form.instance, self.request)
            documento.estado=1
            registro_guardar(documento, self.request)
            documento.save()
            messages.success(self.request, MENSAJE_ANULAR_CONTEO)
            return super().form_valid(form)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
            return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(RecepcionCompraAnularView, self).get_context_data(**kwargs)
        context['accion'] = "Anular"
        context['titulo'] = "Conteo"
        return context


class ArchivoRecepcionCompraCreateView(PermissionRequiredMixin, BSModalCreateView):
    permission_required = ('recepcion_compra.add_archivorecepcioncompra')
    model = ArchivoRecepcionCompra
    template_name = "includes/formulario generico.html"
    form_class = ArchivoRecepcionCompraForm
    success_url = '.'
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.recepcion_compra = RecepcionCompra.objects.get(pk=self.kwargs['pk'])
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super(ArchivoRecepcionCompraCreateView, self).get_context_data(**kwargs)
        context['accion'] = "Agregar"
        context['titulo'] = "Archivo"
        return context
    

class ArchivoRecepcionCompraDeleteView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('recepcion_compra.delete_archivorecepcioncompra')
    model = ArchivoRecepcionCompra
    template_name = "includes/eliminar generico.html"
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)
    
    def get_success_url(self, **kwargs):
        return reverse_lazy('recepcion_compra_app:recepcion_compra_detalle', kwargs={'pk':self.object.recepcion_compra.id})

    def get_context_data(self, **kwargs):
        context = super(ArchivoRecepcionCompraDeleteView, self).get_context_data(**kwargs)
        context['accion'] = "Agregar"
        context['titulo'] = "Archivo"
        context['item'] = filename(self.object.archivo)
        return context


class FotoRecepcionCompraCreateView(PermissionRequiredMixin, BSModalCreateView):
    permission_required = ('recepcion_compra.add_fotorecepcioncompra')
    model = FotoRecepcionCompra
    template_name = "includes/formulario generico.html"
    form_class = FotoRecepcionCompraForm
    success_url = '.'
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.recepcion_compra = RecepcionCompra.objects.get(pk=self.kwargs['pk'])
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super(FotoRecepcionCompraCreateView, self).get_context_data(**kwargs)
        context['accion'] = "Agregar"
        context['titulo'] = "Foto"
        return context
    

class FotoRecepcionCompraDeleteView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('recepcion_compra.delete_fotorecepcioncompra')
    model = FotoRecepcionCompra
    template_name = "includes/eliminar generico.html"
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)
    
    def get_success_url(self, **kwargs):
        return reverse_lazy('recepcion_compra_app:recepcion_compra_detalle', kwargs={'pk':self.object.recepcion_compra.id})

    def get_context_data(self, **kwargs):
        context = super(FotoRecepcionCompraDeleteView, self).get_context_data(**kwargs)
        context['accion'] = "Agregar"
        context['titulo'] = "Foto"
        context['item'] = filename(self.object.foto)
        return context


class RecepcionCompraGenerarNotaIngresoView(PermissionRequiredMixin, BSModalFormView):
    permission_required = ('nota_ingreso.add_notaingreso')
    template_name = "includes/formulario generico.html"
    form_class = RecepcionCompraGenerarNotaIngresoForm
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)
    
    def get_success_url(self, **kwargs):
        return reverse_lazy('nota_ingreso_app:nota_ingreso_detalle', kwargs={'pk':self.kwargs['nota'].id})

    @transaction.atomic
    def form_valid(self, form):
        sid = transaction.savepoint()
        try:
            if self.request.session['primero']:
                recepcion_compra = RecepcionCompra.objects.get(id=self.kwargs['pk'])
                numero_nota = len(NotaIngreso.objects.all()) + 1
                nota = NotaIngreso.objects.create(
                    nro_nota_ingreso = numeroXn(numero_nota, 6),
                    content_type=ContentType.objects.get_for_model(recepcion_compra),
                    id_registro=recepcion_compra.id,
                    sociedad = recepcion_compra.sociedad,
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
        context = super(RecepcionCompraGenerarNotaIngresoView, self).get_context_data(**kwargs)
        context['accion'] = "Recibir"
        context['titulo'] = "Comprobante de Compra"
        return context


class RecepcionCompraGenerarDocumentoReclamoView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('recepcion_compra.view_documentoreclamo')
    template_name = "includes/eliminar generico.html"
    model = RecepcionCompra
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)
    
    def get_success_url(self, **kwargs):
        return reverse_lazy('recepcion_compra_app:documento_reclamo_detalle', kwargs={'pk':self.kwargs['documento'].id})

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            if self.request.session['primero']:
                recepcion_compra = self.get_object()
                numero_documento = len(DocumentoReclamo.objects.all()) + 1
                documento = DocumentoReclamo.objects.create(
                    nro_documento_reclamo = numero_documento,
                    recepcion_compra = recepcion_compra,
                    fecha_documento=date.today(),
                    usuario=self.request.user,
                    estado=1,
                    created_by = self.request.user,
                    updated_by = self.request.user,
                )
                materiales = recepcion_compra.content_type.model_class().objects.ver_detalle(recepcion_compra.id_registro)
                for material in materiales:
                    if material.exceso == Decimal('0.00') and material.pendiente > Decimal('0.00'):
                        cantidad = material.pendiente
                        tipo = -1
                    elif material.exceso > Decimal('0.00') and material.pendiente == Decimal('0.00'):
                        cantidad = material.exceso
                        tipo = 1
                    elif material.exceso == Decimal('0.00') and material.pendiente == Decimal('0.00'):
                        continue

                    DocumentoReclamoDetalle.objects.create(
                        documento_reclamo=documento,
                        item=material.item,
                        content_type=ContentType.objects.get_for_model(material.producto),
                        id_registro=material.producto.id,
                        cantidad=cantidad,
                        tipo=tipo,
                        precio_unitario_sin_igv=material.precio_unitario_sin_igv,
                        precio_unitario_con_igv=material.precio_unitario_con_igv,
                        precio_final_con_igv=material.precio_final_con_igv,
                        descuento=material.descuento,
                        sub_total=material.sub_total,
                        igv=material.igv,
                        total=material.total,
                        tipo_igv=material.tipo_igv,
                        created_by = self.request.user,
                        updated_by = self.request.user,
                    )
                self.kwargs['documento'] = documento
                self.request.session['primero'] = False
            return HttpResponseRedirect(self.get_success_url())
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return reverse_lazy('nota_ingreso_app:nota_ingreso_detalle', kwargs={'pk':self.get_object().id})

    def get_context_data(self, **kwargs):
        self.request.session['primero'] = True
        context = super(RecepcionCompraGenerarDocumentoReclamoView, self).get_context_data(**kwargs)
        context['accion'] = "Generar"
        context['titulo'] = "Documento de Reclamo"
        context['texto'] = ""
        return context


class DocumentoReclamoListView(PermissionRequiredMixin, TemplateView):
    permission_required = ('recepcion_compra.view_documentoreclamo')
    template_name = "recepcion_compra/documento_reclamo/inicio.html"
    
    def get_context_data(self, **kwargs):
        context = super(DocumentoReclamoListView, self).get_context_data(**kwargs)
        recepcion_compra = RecepcionCompra.objects.get(id=self.kwargs['id_recepcion'])
        documento_reclamos = DocumentoReclamo.objects.filter(recepcion_compra=recepcion_compra)
        context['recepcion_compra'] = recepcion_compra
        context['documento_reclamos'] = documento_reclamos
        context['regresar'] = link_detalle(ContentType.objects.get_for_model(documento_reclamos.latest('id')), documento_reclamos.latest('id').recepcion_compra.id)
        return context


class DocumentoReclamoDetailView(PermissionRequiredMixin, DetailView):
    permission_required = ('recepcion_compra.view_documentoreclamo')
    model = DocumentoReclamo
    template_name = "recepcion_compra/documento_reclamo/detalle.html"
    context_object_name = 'contexto_documento_reclamo'

    def get_context_data(self, **kwargs):
        context = super(DocumentoReclamoDetailView, self).get_context_data(**kwargs)
        context['materiales'] = self.get_object().DocumentoReclamoDetalle_documento_reclamo.all()
        context['regresar'] = link_detalle(ContentType.objects.get_for_model(self.get_object()), self.get_object().recepcion_compra.id)
        return context
    

def DocumentoReclamoDetailTabla(request, pk):
    data = dict()
    if request.method == 'GET':
        template = 'recepcion_compra/documento_reclamo/detalle_tabla.html'
        context = {}
        documento_reclamo = DocumentoReclamo.objects.get(id = pk)
        context['contexto_documento_reclamo'] = documento_reclamo
        context['materiales'] = documento_reclamo.DocumentoReclamoDetalle_documento_reclamo.all()
        
        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)


class DocumentoReclamoDeleteView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('recepcion_compra.delete_documentoreclamo')
    model = DocumentoReclamo
    template_name = "includes/eliminar generico.html"

    def get_success_url(self) -> str:
        return link_detalle(ContentType.objects.get_for_model(self.get_object()), self.get_object().recepcion_compra.id)

    def get_context_data(self, **kwargs):
        context = super(DocumentoReclamoDeleteView, self).get_context_data(**kwargs)
        context['accion'] = 'Eliminar'
        context['titulo'] = 'Documento de Reclamo'
        context['item'] = self.get_object()
        return context


class DocumentoReclamoCerrarView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('recepcion_compra.delete_documentoreclamo')
    model = DocumentoReclamo
    template_name = "includes/eliminar generico.html"

    def get_success_url(self) -> str:
        return link_detalle(ContentType.objects.get_for_model(self.get_object()), self.get_object().recepcion_compra.id)

    def get_context_data(self, **kwargs):
        context = super(DocumentoReclamoCerrarView, self).get_context_data(**kwargs)
        context['accion'] = 'Eliminar'
        context['titulo'] = 'Documento de Reclamo'
        context['item'] = self.get_object()
        return context
