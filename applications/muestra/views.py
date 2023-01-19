from django.shortcuts import render
from applications.funciones import registrar_excepcion
from applications.importaciones import *
from applications.material.models import Material
from applications.movimiento_almacen.models import MovimientosAlmacen, TipoMovimiento
from applications.muestra.forms import NotaIngresoMuestraAgregarMaterialForm, NotaIngresoMuestraAnularForm, NotaIngresoMuestraForm, NotaIngresoMuestraGenerarNotaIngresoForm, NotaIngresoMuestraGuardarForm
from applications.muestra.models import NotaIngresoMuestra, NotaIngresoMuestraDetalle


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
            movimiento_final = TipoMovimiento.objects.get(codigo=998)
            
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

