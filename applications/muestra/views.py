from django.shortcuts import render
from applications.calidad.models import EstadoSerie, HistorialEstadoSerie, Serie
from applications.clientes.models import Cliente
from applications.comprobante_despacho.models import Guia, GuiaDetalle
from applications.datos_globales.models import SeriesComprobante
from applications.funciones import numeroXn, registrar_excepcion
from applications.importaciones import *
from applications.material.models import Material
from applications.movimiento_almacen.models import MovimientosAlmacen, TipoMovimiento, TipoStock
from applications.muestra.forms import DevolucionMuestraAgregarMaterialForm, DevolucionMuestraAnularForm, DevolucionMuestraDetalleSeriesForm, DevolucionMuestraForm, DevolucionMuestraGuardarForm, NotaIngresoMuestraAgregarMaterialForm, NotaIngresoMuestraAnularForm, NotaIngresoMuestraForm, NotaIngresoMuestraGenerarNotaIngresoForm, NotaIngresoMuestraGuardarForm
from applications.muestra.models import DevolucionMuestra, DevolucionMuestraDetalle, NotaIngresoMuestra, NotaIngresoMuestraDetalle, ValidarSerieDevolucionMuestraDetalle
from applications.nota_ingreso.models import NotaIngreso


# Create your views here.
class NotaIngresoMuestraCreateView(PermissionRequiredMixin, BSModalCreateView):
    permission_required = ('muestra.add_notaingresomuestra')
    model = NotaIngresoMuestra
    template_name = "includes/formulario generico.html"
    form_class = NotaIngresoMuestraForm

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('muestra_app:nota_ingreso_muestra_detalle', kwargs={'pk':self.object.id})
    
    def get_context_data(self, **kwargs):
        context = super(NotaIngresoMuestraCreateView, self).get_context_data(**kwargs)
        context['accion']="Crear"
        context['titulo']="Nota de Ingreso de Muestra"
        return context

    def form_valid(self, form):
        nro_nota_ingreso_muestra = 1
        if NotaIngresoMuestra.objects.all():
            nro_nota_ingreso_muestra = NotaIngresoMuestra.objects.all().aggregate(Max('nro_nota_ingreso_muestra'))['nro_nota_ingreso_muestra__max'] + 1
        form.instance.nro_nota_ingreso_muestra = nro_nota_ingreso_muestra
        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)

        return super().form_valid(form)


class NotaIngresoMuestraEliminarView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('muestra.delete_notaingresomuestra')
    model = NotaIngresoMuestra
    template_name = "includes/eliminar generico.html"
    success_url = reverse_lazy('muestra_app:nota_ingreso_muestra_lista_total')

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(NotaIngresoMuestraEliminarView, self).get_context_data(**kwargs)
        context['accion'] = "Eliminar"
        context['titulo'] = "Nota Ingreso de Muestra"
        context['item'] = "%s" % (self.object)
        return context


class NotaIngresoMuestraListaView(PermissionRequiredMixin, TemplateView):
    permission_required = ('muestra.view_notaingresomuestra')
    template_name = "muestra/nota_ingreso_muestra/inicio.html"

    def get_context_data(self, **kwargs):
        context = super(NotaIngresoMuestraListaView, self).get_context_data(**kwargs)
        context['contexto_nota_ingreso_muestra'] = NotaIngresoMuestra.objects.all()
        return context


class NotaIngresoMuestraDetailView(PermissionRequiredMixin, DetailView):
    permission_required = ('muestra.view_notaingresomuestra')
    model = NotaIngresoMuestra
    template_name = "muestra/nota_ingreso_muestra/detalle.html"
    context_object_name = 'contexto_nota_ingreso_muestra'

    def get_context_data(self, **kwargs):
        context = super(NotaIngresoMuestraDetailView, self).get_context_data(**kwargs)
        context['materiales'] = NotaIngresoMuestra.objects.ver_detalle(self.get_object().id)
        context['regresar'] = reverse_lazy('muestra_app:nota_ingreso_muestra_lista_total')
        return context
    

def NotaIngresoMuestraDetailTabla(request, pk):
    data = dict()
    if request.method == 'GET':
        template = 'muestra/nota_ingreso_muestra/detalle_tabla.html'
        context = {}
        nota_ingreso_muestra = NotaIngresoMuestra.objects.get(id = pk)
        context['contexto_nota_ingreso_muestra'] = nota_ingreso_muestra
        context['materiales'] = NotaIngresoMuestra.objects.ver_detalle(pk)
        context['regresar'] = reverse_lazy('muestra_app:nota_ingreso_muestra_lista_total')
        
        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)


class NotaIngresoMuestraAgregarMaterialView(PermissionRequiredMixin, BSModalFormView):
    permission_required = ('muestra.add_notaingresomuestradetalle')
    template_name = "muestra/nota_ingreso_muestra/form.html"
    form_class = NotaIngresoMuestraAgregarMaterialForm

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)
    
    def get_success_url(self, **kwargs):
        return reverse_lazy('muestra_app:nota_ingreso_muestra_detalle', kwargs={'pk':self.kwargs['id_nota_ingreso_muestra']})

    def get_form_kwargs(self, *args, **kwargs):
        productos = []
        for detalle in Material.objects.all():
            valor = "%s|%s" % (ContentType.objects.get_for_model(detalle).id, detalle.id)
            productos.append((valor, detalle.descripcion_venta))
        kwargs = super(NotaIngresoMuestraAgregarMaterialView, self).get_form_kwargs(*args, **kwargs)
        kwargs['productos'] = productos
        return kwargs

    @transaction.atomic
    def form_valid(self, form):
        sid = transaction.savepoint()
        try:
            if self.request.session['primero']:
                nota_ingreso_muestra = NotaIngresoMuestra.objects.get(id=self.kwargs['id_nota_ingreso_muestra'])
                nuevo_item = len(NotaIngresoMuestraDetalle.objects.filter(nota_ingreso_muestra = nota_ingreso_muestra)) + 1
                cantidad = form.cleaned_data['cantidad']
                producto = form.cleaned_data['producto'].split("|")
                content_type = ContentType.objects.get(id = int(producto[0]))
                id_registro = int(producto[1])
                
                nota_ingreso_muestra_detalle, created = NotaIngresoMuestraDetalle.objects.get_or_create(
                    content_type=content_type,
                    id_registro=id_registro,
                    nota_ingreso_muestra = nota_ingreso_muestra,
                )
                if created:
                    nota_ingreso_muestra_detalle.item = nuevo_item
                    nota_ingreso_muestra_detalle.cantidad_total = cantidad
                    nota_ingreso_muestra_detalle.created_by = self.request.user
                    nota_ingreso_muestra_detalle.updated_by = self.request.user
                else:
                    nota_ingreso_muestra_detalle.cantidad_total = nota_ingreso_muestra_detalle.cantidad_total + cantidad
                    nota_ingreso_muestra_detalle.updated_by = self.request.user
                nota_ingreso_muestra_detalle.save()
                
                self.request.session['primero'] = False
                return super().form_valid(form)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        self.request.session['primero'] = True
        context = super(NotaIngresoMuestraAgregarMaterialView, self).get_context_data(**kwargs)
        context['accion'] = "Agregar"
        context['titulo'] = "Material"
        return context


class NotaIngresoMuestraActualizarMaterialView(PermissionRequiredMixin, BSModalFormView):
    permission_required = ('muestra.change_notaingresomuestradetalle')
    template_name = "muestra/nota_ingreso_muestra/form.html"
    form_class = NotaIngresoMuestraAgregarMaterialForm

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)
    
    def get_success_url(self, **kwargs):
        nota_ingreso_muestra_detalle = NotaIngresoMuestraDetalle.objects.get(id=self.kwargs['id_nota_ingreso_muestra_detalle'])
        nota_ingreso_muestra = nota_ingreso_muestra_detalle.nota_ingreso_muestra
        return reverse_lazy('muestra_app:nota_ingreso_muestra_detalle', kwargs={'pk':nota_ingreso_muestra.id})

    def get_form_kwargs(self, *args, **kwargs):
        nota_ingreso_muestra_detalle = NotaIngresoMuestraDetalle.objects.get(id=self.kwargs['id_nota_ingreso_muestra_detalle'])
        productos = []
        for detalle in Material.objects.all():
            valor = "%s|%s" % (ContentType.objects.get_for_model(detalle).id, detalle.id)
            productos.append((valor, detalle.descripcion_venta))
        kwargs = super(NotaIngresoMuestraActualizarMaterialView, self).get_form_kwargs(*args, **kwargs)
        kwargs['productos'] = productos
        kwargs['nota_ingreso_muestra_detalle'] = nota_ingreso_muestra_detalle
        return kwargs

    @transaction.atomic
    def form_valid(self, form):
        sid = transaction.savepoint()
        try:
            if self.request.session['primero']:
                nota_ingreso_muestra_detalle = NotaIngresoMuestraDetalle.objects.get(id=self.kwargs['id_nota_ingreso_muestra_detalle'])
                cantidad = form.cleaned_data['cantidad']
                producto = form.cleaned_data['producto'].split("|")
                content_type = ContentType.objects.get(id = int(producto[0]))
                id_registro = int(producto[1])
                
                nota_ingreso_muestra_detalle.content_type=content_type
                nota_ingreso_muestra_detalle.id_registro=id_registro
                nota_ingreso_muestra_detalle.cantidad_total = cantidad
                nota_ingreso_muestra_detalle.updated_by = self.request.user
                nota_ingreso_muestra_detalle.save()
                
                self.request.session['primero'] = False
                return super().form_valid(form)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        self.request.session['primero'] = True
        context = super(NotaIngresoMuestraActualizarMaterialView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        context['titulo'] = "Material"
        return context


class NotaIngresoMuestraDetalleEliminarView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('muestra.delete_notaingresomuestradetalle')
    model = NotaIngresoMuestraDetalle
    template_name = "includes/eliminar generico.html"

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)
    
    def get_success_url(self, **kwargs):
        nota_ingreso_muestra = self.object.nota_ingreso_muestra
        return reverse_lazy('muestra_app:nota_ingreso_muestra_detalle', kwargs={'pk':nota_ingreso_muestra.id})

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            materiales = NotaIngresoMuestraDetalle.objects.filter(nota_ingreso_muestra=self.get_object().nota_ingreso_muestra)
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
        context = super(NotaIngresoMuestraDetalleEliminarView, self).get_context_data(**kwargs)
        context['accion'] = "Eliminar"
        context['titulo'] = "Detalle"
        context['item'] = "%s" % (self.object)
        return context


class NotaIngresoMuestraGuardarView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('muestra.change_notaingresomuestra')
    model = NotaIngresoMuestra
    template_name = "includes/formulario generico.html"
    form_class = NotaIngresoMuestraGuardarForm

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)
    
    def get_success_url(self, **kwargs):
        return reverse_lazy('muestra_app:nota_ingreso_muestra_detalle', kwargs={'pk':self.object.id})

    @transaction.atomic
    def form_valid(self, form):
        sid = transaction.savepoint()
        try:
            detalles = form.instance.NotaIngresoMuestraDetalle_nota_ingreso_muestra.all()
            movimiento_final = TipoMovimiento.objects.get(codigo=144) #Recepción de Muestra
            
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
        context = super(NotaIngresoMuestraGuardarView, self).get_context_data(**kwargs)
        context['accion'] = "Finalizar"
        context['titulo'] = "Conteo"
        return context


class NotaIngresoMuestraAnularView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('muestra.change_notaingresomuestra')
    model = NotaIngresoMuestra
    template_name = "includes/formulario generico.html"
    form_class = NotaIngresoMuestraAnularForm

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)
    
    def get_success_url(self, **kwargs):
        return reverse_lazy('muestra_app:nota_ingreso_muestra_detalle', kwargs={'pk':self.object.id})

    @transaction.atomic
    def form_valid(self, form):
        sid = transaction.savepoint()
        try:
            detalles = form.instance.NotaIngresoMuestraDetalle_nota_ingreso_muestra.all()

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
        context = super(NotaIngresoMuestraAnularView, self).get_context_data(**kwargs)
        context['accion'] = "Anular"
        context['titulo'] = "Ingreso de Muestra"
        return context


class NotaIngresoMuestraGenerarNotaIngresoView(PermissionRequiredMixin, BSModalFormView):
    permission_required = ('nota_ingreso.add_notaingreso')
    template_name = "includes/formulario generico.html"
    form_class = NotaIngresoMuestraGenerarNotaIngresoForm

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
                nota_stock_inicial = NotaIngresoMuestra.objects.get(id=self.kwargs['pk'])
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
        context = super(NotaIngresoMuestraGenerarNotaIngresoView, self).get_context_data(**kwargs)
        context['accion'] = "Recibir"
        context['titulo'] = "Nota de Ingreso"
        return context


##############################################################################

class DevolucionMuestraCreateView(PermissionRequiredMixin, BSModalCreateView):
    permission_required = ('muestra.add_devolucionmuestra')
    model = DevolucionMuestra
    template_name = "includes/formulario generico.html"
    form_class = DevolucionMuestraForm

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('muestra_app:devolucion_muestra_detalle', kwargs={'pk':self.object.id})
    
    def get_context_data(self, **kwargs):
        context = super(DevolucionMuestraCreateView, self).get_context_data(**kwargs)
        context['accion']="Crear"
        context['titulo']="Devolución de Muestra"
        return context

    def form_valid(self, form):
        numero_devolucion = 1
        if DevolucionMuestra.objects.all():
            numero_devolucion = DevolucionMuestra.objects.all().aggregate(Max('numero_devolucion'))['numero_devolucion__max'] + 1
        form.instance.numero_devolucion = numero_devolucion
        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)

        return super().form_valid(form)


class DevolucionMuestraEliminarView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('muestra.delete_devolucionmuestra')
    model = DevolucionMuestra
    template_name = "includes/eliminar generico.html"
    success_url = reverse_lazy('muestra_app:devolucion_muestra_lista_total')

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(DevolucionMuestraEliminarView, self).get_context_data(**kwargs)
        context['accion'] = "Eliminar"
        context['titulo'] = "Devolución de Muestra"
        context['item'] = "%s" % (self.object)
        return context


class DevolucionMuestraListaView(PermissionRequiredMixin, TemplateView):
    permission_required = ('muestra.view_devolucionmuestra')
    template_name = "muestra/devolucion_muestra/inicio.html"

    def get_context_data(self, **kwargs):
        context = super(DevolucionMuestraListaView, self).get_context_data(**kwargs)
        context['contexto_devolucion_muestra'] = DevolucionMuestra.objects.all()
        return context


class DevolucionMuestraDetailView(PermissionRequiredMixin, DetailView):
    permission_required = ('muestra.view_devolucionmuestra')
    model = DevolucionMuestra
    template_name = "muestra/devolucion_muestra/detalle.html"
    context_object_name = 'contexto_devolucion_muestra'

    def get_context_data(self, **kwargs):
        context = super(DevolucionMuestraDetailView, self).get_context_data(**kwargs)
        context['materiales'] = DevolucionMuestra.objects.ver_detalle(self.get_object().id)
        context['regresar'] = reverse_lazy('muestra_app:devolucion_muestra_lista_total')
        return context
    

def DevolucionMuestraDetailTabla(request, pk):
    data = dict()
    if request.method == 'GET':
        template = 'muestra/devolucion_muestra/detalle_tabla.html'
        context = {}
        devolucion_muestra = DevolucionMuestra.objects.get(id = pk)
        context['contexto_devolucion_muestra'] = devolucion_muestra
        context['materiales'] = DevolucionMuestra.objects.ver_detalle(pk)
        context['regresar'] = reverse_lazy('muestra_app:devolucion_muestra_lista_total')
        
        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)


class DevolucionMuestraAgregarMaterialView(PermissionRequiredMixin, BSModalFormView):
    permission_required = ('muestra.add_devolucionmuestradetalle')
    template_name = "muestra/devolucion_muestra/form.html"
    form_class = DevolucionMuestraAgregarMaterialForm

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)
    
    def get_success_url(self, **kwargs):
        return reverse_lazy('muestra_app:devolucion_muestra_detalle', kwargs={'pk':self.kwargs['id_devolucion_muestra']})

    def get_form_kwargs(self, *args, **kwargs):
        productos = []
        for detalle in Material.objects.all():
            valor = "%s|%s" % (ContentType.objects.get_for_model(detalle).id, detalle.id)
            productos.append((valor, detalle.descripcion_venta))
        kwargs = super(DevolucionMuestraAgregarMaterialView, self).get_form_kwargs(*args, **kwargs)
        kwargs['productos'] = productos
        return kwargs

    @transaction.atomic
    def form_valid(self, form):
        sid = transaction.savepoint()
        try:
            if self.request.session['primero']:
                devolucion_muestra = DevolucionMuestra.objects.get(id=self.kwargs['id_devolucion_muestra'])
                nuevo_item = len(DevolucionMuestraDetalle.objects.filter(devolucion_muestra = devolucion_muestra)) + 1
                cantidad = form.cleaned_data['cantidad']
                producto = form.cleaned_data['producto'].split("|")
                almacen = form.cleaned_data['almacen']
                content_type = ContentType.objects.get(id = int(producto[0]))
                id_registro = int(producto[1])
                
                devolucion_muestra_detalle, created = DevolucionMuestraDetalle.objects.get_or_create(
                    content_type=content_type,
                    id_registro=id_registro,
                    almacen=almacen,
                    devolucion_muestra = devolucion_muestra,
                )
                if created:
                    devolucion_muestra_detalle.item = nuevo_item
                    devolucion_muestra_detalle.cantidad_devolucion = cantidad
                    devolucion_muestra_detalle.created_by = self.request.user
                    devolucion_muestra_detalle.updated_by = self.request.user
                else:
                    devolucion_muestra_detalle.cantidad_devolucion = devolucion_muestra_detalle.cantidad_devolucion + cantidad
                    devolucion_muestra_detalle.updated_by = self.request.user
                devolucion_muestra_detalle.save()
                
                self.request.session['primero'] = False
                return super().form_valid(form)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        self.request.session['primero'] = True
        devolucion_muestra = DevolucionMuestra.objects.get(id=self.kwargs['id_devolucion_muestra'])
        context = super(DevolucionMuestraAgregarMaterialView, self).get_context_data(**kwargs)
        context['accion'] = "Agregar"
        context['titulo'] = "Material"
        context['sede_id'] = devolucion_muestra.sede.id
        context['sociedad_id'] = devolucion_muestra.sociedad.id
        context['tipo_stock_id'] = TipoStock.objects.get(codigo=31).id #MUESTRA
        return context


class DevolucionMuestraActualizarMaterialView(PermissionRequiredMixin, BSModalFormView):
    permission_required = ('muestra.change_devolucionmuestradetalle')
    template_name = "muestra/devolucion_muestra/form.html"
    form_class = DevolucionMuestraAgregarMaterialForm

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)
    
    def get_success_url(self, **kwargs):
        devolucion_muestra_detalle = DevolucionMuestraDetalle.objects.get(id=self.kwargs['id_devolucion_muestra_detalle'])
        devolucion_muestra = devolucion_muestra_detalle.devolucion_muestra
        return reverse_lazy('muestra_app:devolucion_muestra_detalle', kwargs={'pk':devolucion_muestra.id})

    def get_form_kwargs(self, *args, **kwargs):
        devolucion_muestra_detalle = DevolucionMuestraDetalle.objects.get(id=self.kwargs['id_devolucion_muestra_detalle'])
        productos = []
        for detalle in Material.objects.all():
            valor = "%s|%s" % (ContentType.objects.get_for_model(detalle).id, detalle.id)
            productos.append((valor, detalle.descripcion_venta))
        kwargs = super(DevolucionMuestraActualizarMaterialView, self).get_form_kwargs(*args, **kwargs)
        kwargs['productos'] = productos
        kwargs['devolucion_muestra_detalle'] = devolucion_muestra_detalle
        return kwargs

    @transaction.atomic
    def form_valid(self, form):
        sid = transaction.savepoint()
        try:
            if self.request.session['primero']:
                devolucion_muestra_detalle = DevolucionMuestraDetalle.objects.get(id=self.kwargs['id_devolucion_muestra_detalle'])
                cantidad = form.cleaned_data['cantidad']
                producto = form.cleaned_data['producto'].split("|")
                content_type = ContentType.objects.get(id = int(producto[0]))
                id_registro = int(producto[1])
                
                devolucion_muestra_detalle.content_type=content_type
                devolucion_muestra_detalle.id_registro=id_registro
                devolucion_muestra_detalle.cantidad_devolucion = cantidad
                devolucion_muestra_detalle.updated_by = self.request.user
                devolucion_muestra_detalle.save()
                
                self.request.session['primero'] = False
                return super().form_valid(form)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        devolucion_muestra = DevolucionMuestraDetalle.objects.get(id=self.kwargs['id_devolucion_muestra_detalle']).devolucion_muestra
        self.request.session['primero'] = True
        context = super(DevolucionMuestraActualizarMaterialView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        context['titulo'] = "Material"
        context['sede_id'] = devolucion_muestra.sede.id
        context['sociedad_id'] = devolucion_muestra.sociedad.id
        context['tipo_stock_id'] = TipoStock.objects.get(codigo=31).id #MUESTRA
        return context


class DevolucionMuestraDetalleEliminarView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('muestra.delete_devolucionmuestradetalle')
    model = DevolucionMuestraDetalle
    template_name = "includes/eliminar generico.html"

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)
    
    def get_success_url(self, **kwargs):
        devolucion_muestra = self.object.devolucion_muestra
        return reverse_lazy('muestra_app:devolucion_muestra_detalle', kwargs={'pk':devolucion_muestra.id})

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            materiales = DevolucionMuestraDetalle.objects.filter(devolucion_muestra=self.get_object().devolucion_muestra)
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
        context = super(DevolucionMuestraDetalleEliminarView, self).get_context_data(**kwargs)
        context['accion'] = "Eliminar"
        context['titulo'] = "Detalle"
        context['item'] = "%s" % (self.object)
        return context


class DevolucionMuestraGuardarView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('muestra.change_devolucionmuestra')
    model = DevolucionMuestra
    template_name = "includes/formulario generico.html"
    form_class = DevolucionMuestraGuardarForm

    def dispatch(self, request, *args, **kwargs):
        context = {}
        error_cantidad_series = False
        context['titulo'] = 'Error de guardar'
        detalles = self.get_object().DevolucionMuestraDetalle_devolucion_muestra.all()
        for detalle in detalles:
            if detalle.control_serie and detalle.series_validar != detalle.cantidad_devolucion:
                error_cantidad_series = True
        
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')

        if error_cantidad_series:
            context['texto'] = 'Hay Series sin registrar.'
            return render(request, 'includes/modal sin permiso.html', context)
        return super().dispatch(request, *args, **kwargs)
    
    def get_success_url(self, **kwargs):
        return reverse_lazy('muestra_app:devolucion_muestra_detalle', kwargs={'pk':self.object.id})

    @transaction.atomic
    def form_valid(self, form):
        sid = transaction.savepoint()
        try:
            detalles = form.instance.DevolucionMuestraDetalle_devolucion_muestra.all()
            movimiento_final = TipoMovimiento.objects.get(codigo=151) #Devolución de Muestra
            estado_serie = EstadoSerie.objects.get(numero_estado=6) #DEVUELTO
            
            for detalle in detalles:
                movimiento_uno = MovimientosAlmacen.objects.create(
                    content_type_producto = detalle.content_type,
                    id_registro_producto = detalle.id_registro,
                    cantidad = detalle.cantidad_devolucion,
                    tipo_movimiento = movimiento_final,
                    tipo_stock = movimiento_final.tipo_stock_inicial,
                    signo_factor_multiplicador = -1,
                    content_type_documento_proceso = ContentType.objects.get_for_model(form.instance),
                    id_registro_documento_proceso = form.instance.id,
                    sociedad = form.instance.sociedad,
                    almacen = detalle.almacen,
                    movimiento_reversion = False,
                    created_by = self.request.user,
                    updated_by = self.request.user,
                )

                for validar_serie in detalle.ValidarSerieDevolucionMuestraDetalle_devolucion_muestra_detalle.all():
                    serie = validar_serie.serie
                    serie.serie_movimiento_almacen.add(movimiento_uno)

                    HistorialEstadoSerie.objects.create(
                        serie = serie,
                        estado_serie = estado_serie,
                        created_by = self.request.user,
                        updated_by = self.request.user,
                    )
                    validar_serie.delete()

            form.instance.estado = 2
            registro_guardar(form.instance, self.request)
                
            return super().form_valid(form)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(DevolucionMuestraGuardarView, self).get_context_data(**kwargs)
        context['accion'] = "Finalizar"
        context['titulo'] = "Conteo"
        return context


class DevolucionMuestraAnularView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('muestra.change_devolucionmuestra')
    model = DevolucionMuestra
    template_name = "includes/formulario generico.html"
    form_class = DevolucionMuestraAnularForm

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)
    
    def get_success_url(self, **kwargs):
        return reverse_lazy('muestra_app:devolucion_muestra_detalle', kwargs={'pk':self.object.id})

    @transaction.atomic
    def form_valid(self, form):
        sid = transaction.savepoint()
        try:
            detalles = form.instance.DevolucionMuestraDetalle_devolucion_muestra.all()

            for detalle in detalles:
                movimiento_dos = MovimientosAlmacen.objects.get(
                    content_type_producto = detalle.content_type,
                    id_registro_producto = detalle.id_registro,
                    cantidad = detalle.cantidad_devolucion,
                    # tipo_movimiento = movimiento_final,
                    # tipo_stock = movimiento_final.tipo_stock_final,
                    signo_factor_multiplicador = -1,
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
        context = super(DevolucionMuestraAnularView, self).get_context_data(**kwargs)
        context['accion'] = "Anular"
        context['titulo'] = "Devolución de Muestra"
        return context


class DevolucionMuestraGenerarGuiaView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('logistica.change_despachodetalle')
    model = DevolucionMuestra
    template_name = "includes/eliminar generico.html"
    
    def dispatch(self, request, *args, **kwargs):
        context = {}
        error_cliente = False
        context['titulo'] = 'Error de Cliente'
        try:
            Cliente.objects.get(razon_social=self.get_object().proveedor.nombre)
        except:
            error_cliente = True
        
        if error_cliente:
            context['texto'] = 'Debe registrar el proveedor como cliente para generar la guía.'
            return render(request, 'includes/modal sin permiso.html', context)

        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('comprobante_despacho_app:guia_detalle', kwargs={'id_guia':self.kwargs['guia'].id})

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            self.object = self.get_object()
            detalles = self.object.DevolucionMuestraDetalle_devolucion_muestra.all()
            serie_comprobante = SeriesComprobante.objects.por_defecto(ContentType.objects.get_for_model(Guia))
            cliente = Cliente.objects.get(razon_social=self.object.proveedor.nombre)
            observaciones = []
            observaciones.append('DEVOLUCIÓN DE MUESTRAS')
            if self.object.observaciones:
                observaciones.append(self.object.observaciones)

            guia = Guia.objects.create(
                sociedad=self.object.sociedad,
                serie_comprobante=serie_comprobante,
                cliente=cliente,
                motivo_traslado='13',
                observaciones=" | ".join(observaciones),
                created_by=self.request.user,
                updated_by=self.request.user,
            )

            for detalle in detalles:
                guia_detalle = GuiaDetalle.objects.create(
                    item=detalle.item,
                    content_type=detalle.content_type,
                    id_registro=detalle.id_registro,
                    guia=guia,
                    cantidad=detalle.cantidad_devolucion,
                    unidad=detalle.producto.unidad_base,
                    descripcion_documento=detalle.producto.descripcion_venta,
                    peso=detalle.producto.peso_unidad_base,
                    created_by=self.request.user,
                    updated_by=self.request.user,
                )
            self.kwargs['guia'] = guia
            self.request.session['primero'] = False
            messages.success(request, MENSAJE_GENERAR_GUIA)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        self.request.session['primero'] = True
        context = super(DevolucionMuestraGenerarGuiaView, self).get_context_data(**kwargs)
        context['accion'] = "Generar"
        context['titulo'] = "Guía"
        context['dar_baja'] = "true"
        context['item'] = self.get_object()
        return context


class ValidarSeriesDevolucionMuestraDetailView(PermissionRequiredMixin, FormView):
    permission_required = ('muestra.view_devolucionmuestradetalle')
    template_name = "muestra/validar_serie_devolucion_muestra/detalle.html"
    form_class = DevolucionMuestraDetalleSeriesForm
    success_url = '.'

    def form_valid(self, form):
        if self.request.session['primero']:
            serie = form.cleaned_data['serie']
            devolucion_muestra_detalle = DevolucionMuestraDetalle.objects.get(id = self.kwargs['pk'])
            try:
                buscar = Serie.objects.get(
                    serie_base=serie,
                    content_type=ContentType.objects.get_for_model(devolucion_muestra_detalle.producto),
                    id_registro=devolucion_muestra_detalle.producto.id,
                )
                buscar2 = ValidarSerieDevolucionMuestraDetalle.objects.filter(serie = buscar)

                if len(buscar2) != 0:
                    form.add_error('serie', "Serie ya ha sido registrada")
                    return super().form_invalid(form)

                if buscar.estado != 'DISPONIBLE' or buscar.estado != 'REPARADO':
                    form.add_error('serie', "Serie no disponible, su estado es: %s" % buscar.estado)
                    return super().form_invalid(form)
            except:
                form.add_error('serie', "Serie no encontrada: %s" % serie)
                return super().form_invalid(form)

            devolucion_muestra_detalle = DevolucionMuestraDetalle.objects.get(id = self.kwargs['pk'])
            obj, created = ValidarSerieDevolucionMuestraDetalle.objects.get_or_create(
                devolucion_muestra_detalle=devolucion_muestra_detalle,
                serie=buscar,
            )
            if created:
                obj.estado = 1
            self.request.session['primero'] = False
        return super().form_valid(form)

    def get_form_kwargs(self):
        devolucion_muestra_detalle = DevolucionMuestraDetalle.objects.get(id = self.kwargs['pk'])
        cantidad_devolucion = devolucion_muestra_detalle.cantidad_devolucion
        cantidad_ingresada = len(ValidarSerieDevolucionMuestraDetalle.objects.filter(devolucion_muestra_detalle=devolucion_muestra_detalle))
        kwargs = super().get_form_kwargs()
        kwargs['cantidad_devolucion'] = cantidad_devolucion
        kwargs['cantidad_ingresada'] = cantidad_ingresada
        return kwargs

    def get_context_data(self, **kwargs):
        self.request.session['primero'] = True
        devolucion_muestra_detalle = DevolucionMuestraDetalle.objects.get(id = self.kwargs['pk'])
        context = super(ValidarSeriesDevolucionMuestraDetailView, self).get_context_data(**kwargs)
        context['contexto_devolucion_muestra_detalle'] = devolucion_muestra_detalle
        context['contexto_series'] = ValidarSerieDevolucionMuestraDetalle.objects.filter(devolucion_muestra_detalle = devolucion_muestra_detalle)
        return context

def ValidarSeriesDevolucionMuestraDetailTabla(request, pk):
    data = dict()
    if request.method == 'GET':
        template = 'muestra/validar_serie_devolucion_muestra/detalle_tabla.html'
        context = {}
        devolucion_muestra_detalle = DevolucionMuestraDetalle.objects.get(id = pk)
        context['contexto_devolucion_muestra_detalle'] = devolucion_muestra_detalle
        context['contexto_series'] = ValidarSerieDevolucionMuestraDetalle.objects.filter(devolucion_muestra_detalle = devolucion_muestra_detalle)

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)


class ValidarSeriesDevolucionMuestraDetalleDeleteView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('muestra.delete_validarseriesdevolucionmuestradetalle')
    model = ValidarSerieDevolucionMuestraDetalle
    template_name = "includes/eliminar generico.html"

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('muestra_app:validar_series_devolucion_muestra_detalle', kwargs={'pk': self.get_object().devolucion_muestra_detalle.id})

    def get_context_data(self, **kwargs):
        context = super(ValidarSeriesDevolucionMuestraDetalleDeleteView, self).get_context_data(**kwargs)
        context['accion'] = "Eliminar"
        context['titulo'] = "Serie"
        context['item'] = self.get_object().serie
        context['dar_baja'] = "true"
        return context