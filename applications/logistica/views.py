from django import forms
from decimal import Decimal
from django.core.paginator import Paginator
from applications.cotizacion.models import ConfirmacionVenta, ConfirmacionVentaDetalle, confirmacion_venta_detalle_post_save
from applications.importaciones import *
from applications.comprobante_despacho.models import Guia, GuiaDetalle
from applications.calidad.models import EstadoSerie, HistorialEstadoSerie, Serie
from applications.logistica.models import AjusteInventarioMateriales, AjusteInventarioMaterialesDetalle, Despacho, DespachoDetalle, DocumentoPrestamoMateriales, ImagenesDespacho, InventarioMateriales, InventarioMaterialesDetalle, NotaSalidaDocumento, \
    SolicitudPrestamoMateriales, SolicitudPrestamoMaterialesDetalle, NotaSalida, NotaSalidaDetalle, ValidarSerieNotaSalidaDetalle
from applications.logistica.forms import AjusteInventarioMaterialesDetalleForm, AjusteInventarioMaterialesForm, DespachoAnularForm, DespachoBuscarForm, DespachoForm, DocumentoPrestamoMaterialesForm, ImagenesDespachoForm, InventarioMaterialesForm, InventarioMaterialesDetalleForm, InventarioMaterialesUpdateForm, \
    NotaSalidaAnularForm, NotaSalidaBuscarForm, NotaSalidaDetalleForm, NotaSalidaDetalleSeriesForm, NotaSalidaDetalleUpdateForm, SolicitudPrestamoMaterialesDetalleForm, \
    SolicitudPrestamoMaterialesDetalleUpdateForm, SolicitudPrestamoMaterialesForm, NotaSalidaForm, \
    SolicitudPrestamoMaterialesAnularForm
from applications.clientes.models import ClienteInterlocutor, InterlocutorCliente
from applications.logistica.pdf import generarSeries, generarSolicitudPrestamoMateriales
from applications.funciones import fecha_en_letras, numeroXn, registrar_excepcion
from applications.almacenes.models import Almacen
from applications.datos_globales.models import SeriesComprobante
from applications.movimiento_almacen.models import MovimientosAlmacen, TipoMovimiento, TipoStock
from applications.material.funciones import stock_tipo_stock
from django.shortcuts import render

class SolicitudPrestamoMaterialesListView(PermissionRequiredMixin, ListView):
    permission_required = ('logistica.view_solicitudprestamomateriales')
    model = SolicitudPrestamoMateriales
    template_name = "logistica/solicitud_prestamo_materiales/inicio.html"
    context_object_name = 'contexto_solicitud_prestamo_materiales'


def SolicitudPrestamoMaterialesTabla(request):
    data = dict()
    if request.method == 'GET':
        template = 'logistica/solicitud_prestamo_materiales/inicio_tabla.html'
        context = {}
        context['contexto_solicitud_prestamo_materiales'] = SolicitudPrestamoMateriales.objects.all()

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)


class SolicitudPrestamoMaterialesCreateView(PermissionRequiredMixin, BSModalCreateView):
    permission_required = ('logistica.add_solicitudprestamomateriales')
    model = SolicitudPrestamoMateriales
    template_name = "logistica/solicitud_prestamo_materiales/form_cliente.html"
    form_class = SolicitudPrestamoMaterialesForm
    success_url = reverse_lazy('logistica_app:solicitud_prestamo_materiales_inicio')

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(SolicitudPrestamoMaterialesCreateView, self).get_context_data(**kwargs)
        context['accion'] = "Registrar"
        context['titulo'] = "Solicitud Prestamo Materiales"
        return context

    def form_valid(self, form):
        item = len(SolicitudPrestamoMateriales.objects.all())
        form.instance.numero_prestamo = item + 1
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)


class SolicitudPrestamoMaterialesUpdateView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('logistica.change_solicitudprestamomateriales')
    model = SolicitudPrestamoMateriales
    template_name = "logistica/solicitud_prestamo_materiales/form_cliente.html"
    form_class = SolicitudPrestamoMaterialesForm
    success_url = reverse_lazy('logistica_app:solicitud_prestamo_materiales_inicio')

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(SolicitudPrestamoMaterialesUpdateView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        context['titulo'] = "Solicitud Prestamo Materiales"
        return context

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)


class SolicitudPrestamoMaterialesFinalizarView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('logistica.delete_solicitudprestamomateriales')
    model = SolicitudPrestamoMateriales
    template_name = "logistica/solicitud_prestamo_materiales/boton.html"

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('logistica_app:solicitud_prestamo_materiales_detalle', kwargs={'pk': self.get_object().id})

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            self.object = self.get_object()
            self.object.estado = 2
            registro_guardar(self.object, self.request)
            self.object.save()
            messages.success(request, MENSAJE_FINALIZAR_SOLICITUD_PRESTAMO_MATERIALES)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(SolicitudPrestamoMaterialesFinalizarView, self).get_context_data(**kwargs)
        context['accion'] = "Finalizar"
        context['titulo'] = "Solicitud Prestamo Materiales"
        context['dar_baja'] = "true"
        context['item'] = self.object
        return context


class SolicitudPrestamoMaterialesConfirmarView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('logistica.delete_solicitudprestamomateriales')
    model = SolicitudPrestamoMateriales
    template_name = "logistica/solicitud_prestamo_materiales/boton.html"

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('logistica_app:solicitud_prestamo_materiales_detalle', kwargs={'pk': self.get_object().id})

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            self.object = self.get_object()
            self.object.estado = 3
            registro_guardar(self.object, self.request)
            self.object.save()
            messages.success(request, MENSAJE_CONFIRMAR_SOLICITUD_PRESTAMO_MATERIALES)

            materiales = self.object.SolicitudPrestamoMaterialesDetalle_solicitud_prestamo_materiales.all()
            movimiento_final = TipoMovimiento.objects.get(codigo=131)  # Confirmación por préstamo
            for material in materiales:
                movimiento_dos = MovimientosAlmacen.objects.create(
                    content_type_producto=material.content_type,
                    id_registro_producto=material.id_registro,
                    cantidad=material.cantidad_prestamo,
                    tipo_movimiento=movimiento_final,
                    tipo_stock=movimiento_final.tipo_stock_final,
                    signo_factor_multiplicador=+1,
                    content_type_documento_proceso=ContentType.objects.get_for_model(self.object),
                    id_registro_documento_proceso=self.object.id,
                    almacen=None,
                    sociedad=self.object.sociedad,
                    movimiento_anterior=None,
                    movimiento_reversion=False,
                    created_by=self.request.user,
                    updated_by=self.request.user,
                )
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(SolicitudPrestamoMaterialesConfirmarView, self).get_context_data(**kwargs)
        context['accion'] = "Confirmar"
        context['titulo'] = "Solicitud Prestamo Materiales"
        context['dar_baja'] = "true"
        context['item'] = self.object
        return context


class SolicitudPrestamoMaterialesAnularView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('logistica.delete_solicitudprestamomateriales')
    model = SolicitudPrestamoMateriales
    template_name = "includes/formulario generico.html"
    form_class = SolicitudPrestamoMaterialesAnularForm

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('logistica_app:solicitud_prestamo_materiales_detalle', kwargs={'pk': self.object.id})

    @transaction.atomic
    def form_valid(self, form):
        sid = transaction.savepoint()
        try:
            form.instance.estado = 4
            movimiento_final = TipoMovimiento.objects.get(codigo=131)  # Confirmación por préstamo
            movimientos = MovimientosAlmacen.objects.filter(
                tipo_movimiento=movimiento_final,
                tipo_stock=movimiento_final.tipo_stock_final,
                signo_factor_multiplicador=+1,
                content_type_documento_proceso=ContentType.objects.get_for_model(form.instance),
                id_registro_documento_proceso=form.instance.id,
                almacen=None,
                sociedad=form.instance.sociedad,
            )
            for movimiento in movimientos:
                movimiento.delete()
            registro_guardar(form.instance, self.request)
            messages.success(self.request, MENSAJE_ANULAR_SOLICITUD_PRESTAMO_MATERIALES)
            return super().form_valid(form)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
            return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(SolicitudPrestamoMaterialesAnularView, self).get_context_data(**kwargs)
        context['accion'] = "Anular"
        context['titulo'] = "Solicitud Prestamo Materiales"
        return context


class SolicitudPrestamoMaterialesDetailView(PermissionRequiredMixin, DetailView):
    permission_required = ('logistica.view_solicitudprestamomateriales')
    model = SolicitudPrestamoMateriales
    template_name = "logistica/solicitud_prestamo_materiales/detalle.html"
    context_object_name = 'contexto_solicitud_prestamo_materiales_detalle'

    def get_context_data(self, **kwargs):
        obj = SolicitudPrestamoMateriales.objects.get(id=self.kwargs['pk'])
        context = super(SolicitudPrestamoMaterialesDetailView, self).get_context_data(**kwargs)

        materiales = None
        try:
            materiales = obj.SolicitudPrestamoMaterialesDetalle_solicitud_prestamo_materiales.all()
            for material in materiales:
                material.material = material.content_type.get_object_for_this_type(id=material.id_registro)
        except:
            pass

        context['materiales'] = materiales
        context['documentos'] = DocumentoPrestamoMateriales.objects.filter(solicitud_prestamo_materiales=obj)
        return context


def SolicitudPrestamoMaterialesDetailTabla(request, pk):
    data = dict()
    if request.method == 'GET':
        template = 'logistica/solicitud_prestamo_materiales/detalle_tabla.html'
        context = {}
        obj = SolicitudPrestamoMateriales.objects.get(id=pk)

        materiales = None
        try:
            materiales = obj.SolicitudPrestamoMaterialesDetalle_solicitud_prestamo_materiales.all()
            for material in materiales:
                material.material = material.content_type.get_object_for_this_type(id=material.id_registro)
        except:
            pass

        context['contexto_solicitud_prestamo_materiales_detalle'] = obj
        context['materiales'] = materiales
        context['documentos'] = DocumentoPrestamoMateriales.objects.filter(solicitud_prestamo_materiales=obj)

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)


class SolicitudPrestamoMaterialesDetalleCreateView(PermissionRequiredMixin, BSModalFormView):
    permission_required = ('logistica.add_solicitudprestamomaterialesdetalle')
    template_name = "logistica/solicitud_prestamo_materiales/form_material.html"
    form_class = SolicitudPrestamoMaterialesDetalleForm

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('logistica_app:solicitud_prestamo_materiales_detalle',
                            kwargs={'pk': self.kwargs['solicitud_prestamo_materiales_id']})

    @transaction.atomic
    def form_valid(self, form):
        sid = transaction.savepoint()
        try:
            if self.request.session['primero']:
                registro = SolicitudPrestamoMateriales.objects.get(id=self.kwargs['solicitud_prestamo_materiales_id'])
                item = len(SolicitudPrestamoMaterialesDetalle.objects.filter(solicitud_prestamo_materiales=registro))

                material = form.cleaned_data.get('material')
                cantidad_prestamo = form.cleaned_data.get('cantidad_prestamo')
                observacion = form.cleaned_data.get('observacion')

                obj, created = SolicitudPrestamoMaterialesDetalle.objects.get_or_create(
                    content_type=ContentType.objects.get_for_model(material),
                    id_registro=material.id,
                    solicitud_prestamo_materiales=registro,
                )
                if created:
                    obj.item = item + 1
                    obj.cantidad_prestamo = cantidad_prestamo
                    obj.observacion = observacion
                else:
                    if material.stock < obj.cantidad_prestamo + cantidad_prestamo:
                        form.add_error('cantidad_prestamo', 'La cantidad prestada no puede ser mayor al stock disponible.')
                        return super().form_invalid(form)
                    obj.cantidad_prestamo = obj.cantidad_prestamo + cantidad_prestamo
                    if observacion:
                        obj.observacion = obj.observacion + ' | ' + observacion

                registro_guardar(obj, self.request)
                obj.save()
                self.request.session['primero'] = False
            return super().form_valid(form)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        registro = SolicitudPrestamoMateriales.objects.get(id=self.kwargs['solicitud_prestamo_materiales_id'])
        kwargs['id_sociedad'] = registro.sociedad.id
        return kwargs

    def get_context_data(self, **kwargs):
        self.request.session['primero'] = True
        registro = SolicitudPrestamoMateriales.objects.get(id=self.kwargs['solicitud_prestamo_materiales_id'])
        context = super(SolicitudPrestamoMaterialesDetalleCreateView, self).get_context_data(**kwargs)
        context['titulo'] = 'Material'
        context['accion'] = 'Agregar'
        context['id_sociedad'] = registro.sociedad.id
        return context


class SolicitudPrestamoMaterialesDetalleImprimirView(View):
    def get(self, request, *args, **kwargs):
        obj = SolicitudPrestamoMateriales.objects.get(id=self.kwargs['pk'])

        color = obj.sociedad.color
        titulo = 'SOLICITUD DE PRÉSTAMO DE EQUIPOS'
        vertical = False
        logo = [obj.sociedad.logo.url]
        pie_pagina = obj.sociedad.pie_pagina

        titulo = "%s - %s - %s" % (titulo, numeroXn(obj.numero_prestamo, 6), obj.cliente)

        Cabecera = {}
        Cabecera['numero_prestamo'] = numeroXn(obj.numero_prestamo, 6)
        Cabecera['fecha_prestamo'] = fecha_en_letras(obj.fecha_prestamo)
        Cabecera['razon_social'] = str(obj.cliente)
        Cabecera['tipo_documento'] = DICCIONARIO_TIPO_DOCUMENTO_SUNAT[obj.cliente.tipo_documento]
        Cabecera['nro_documento'] = str(obj.cliente.numero_documento)
        Cabecera['direccion'] = str(obj.cliente.direccion_fiscal)
        Cabecera['interlocutor'] = str(obj.interlocutor_cliente)
        Cabecera['comentario'] = str(obj.comentario)

        TablaEncabezado = ['Item',
                           'Descripción',
                           'Unidad',
                           'Cantidad',
                           'Observación',
                           ]

        detalle = obj.SolicitudPrestamoMaterialesDetalle_solicitud_prestamo_materiales
        solicitud_prestamo_materiales = detalle.all()

        TablaDatos = []
        count = 1
        for solicitud in solicitud_prestamo_materiales:
            fila = []
            solicitud.material = solicitud.content_type.get_object_for_this_type(id=solicitud.id_registro)
            fila.append(solicitud.item)
            fila.append(intcomma(solicitud.material))
            fila.append(intcomma(solicitud.material.unidad_base))
            fila.append(intcomma(solicitud.cantidad_prestamo.quantize(Decimal('0.01'))))
            fila.append(solicitud.observacion)

            TablaDatos.append(fila)
            count += 1

        buf = generarSolicitudPrestamoMateriales(titulo, vertical, logo, pie_pagina, Cabecera, TablaEncabezado,
                                                 TablaDatos, color)

        respuesta = HttpResponse(buf.getvalue(), content_type='application/pdf')
        respuesta.headers['content-disposition'] = 'inline; filename=%s.pdf' % titulo

        return respuesta


class SolicitudPrestamoMaterialesDetalleUpdateView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('logistica.change_solicitudprestamomaterialesdetalle')
    model = SolicitudPrestamoMaterialesDetalle
    template_name = "includes/formulario generico.html"
    form_class = SolicitudPrestamoMaterialesDetalleUpdateForm

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('logistica_app:solicitud_prestamo_materiales_inicio')

    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(SolicitudPrestamoMaterialesDetalleUpdateView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        context['titulo'] = "material"
        return context


class SolicitudPrestamoMaterialesDetalleDeleteView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('logistica.delete_solicitudprestamomaterialesdetalle')
    model = SolicitudPrestamoMaterialesDetalle
    template_name = "includes/eliminar generico.html"

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('logistica_app:solicitud_prestamo_materiales_detalle',
                            kwargs={'pk': self.get_object().solicitud_prestamo_materiales.id})

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            materiales = SolicitudPrestamoMaterialesDetalle.objects.filter(
                solicitud_prestamo_materiales=self.get_object().solicitud_prestamo_materiales)
            contador = 1
            for material in materiales:
                if material == self.get_object(): continue
                material.item = contador
                material.save()
                contador += 1
            return super().delete(request, *args, **kwargs)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(SolicitudPrestamoMaterialesDetalleDeleteView, self).get_context_data(**kwargs)
        context['accion'] = "Eliminar"
        context['titulo'] = "Material"
        context['item'] = self.get_object()
        context['dar_baja'] = "true"
        return context


class DocumentoSolicitudPrestamoMaterialesCreateView(PermissionRequiredMixin, BSModalCreateView):
    permission_required = ('logistica.add_documentoprestamomateriales')
    model = DocumentoPrestamoMateriales
    template_name = "includes/formulario generico.html"
    form_class = DocumentoPrestamoMaterialesForm

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('logistica_app:solicitud_prestamo_materiales_detalle',
                            kwargs={'pk': self.kwargs['solicitud_prestamo_materiales_id']})

    def form_valid(self, form):
        form.instance.solicitud_prestamo_materiales = SolicitudPrestamoMateriales.objects.get(
            id=self.kwargs['solicitud_prestamo_materiales_id'])
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(DocumentoSolicitudPrestamoMaterialesCreateView, self).get_context_data(**kwargs)
        context['accion'] = "Agregar"
        context['titulo'] = "Documento"
        return context


class DocumentoSolicitudPrestamoMaterialesDeleteView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('activos.delete_documentoprestamomateriales')
    model = DocumentoPrestamoMateriales
    template_name = "includes/eliminar generico.html"

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('logistica_app:solicitud_prestamo_materiales_detalle',
                            kwargs={'pk': self.object.solicitud_prestamo_materiales.id})

    def get_context_data(self, **kwargs):
        context = super(DocumentoSolicitudPrestamoMaterialesDeleteView, self).get_context_data(**kwargs)
        context['accion'] = "Eliminar"
        context['titulo'] = "Documento"
        return context


class SolicitudPrestamoMaterialesGenerarNotaSalidaView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('logistica.change_solicitudprestamomaterialesdetalle')
    model = SolicitudPrestamoMateriales
    template_name = "logistica/solicitud_prestamo_materiales/boton.html"
    success_url = reverse_lazy('logistica_app:nota_salida_inicio')

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        item = len(NotaSalida.objects.all())
        try:
            if self.request.session['primero']:
                self.object = self.get_object()
                prestamo = self.get_object()
                nota_salida = NotaSalida.objects.create(
                    numero_salida=item + 1,
                    observacion_adicional="",
                    motivo_anulacion="",
                    created_by=self.request.user,
                    updated_by=self.request.user,
                )
                NotaSalidaDocumento.objects.create(
                    content_type=prestamo.content_type,
                    id_registro=prestamo.id,
                    nota_salida=nota_salida,
                    created_by=self.request.user,
                    updated_by=self.request.user,
                )

                self.request.session['primero'] = False
                registro_guardar(self.object, self.request)
                self.object.save()
                messages.success(request, MENSAJE_GENERAR_NOTA_SALIDA)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(reverse_lazy('logistica_app:nota_salida_detalle', kwargs={'pk': nota_salida.id}))

    def get_context_data(self, **kwargs):
        self.request.session['primero'] = True
        context = super(SolicitudPrestamoMaterialesGenerarNotaSalidaView, self).get_context_data(**kwargs)
        context['accion'] = "Generar"
        context['titulo'] = "Nota Salida"
        context['dar_baja'] = "true"
        return context


class NotaSalidaListView(PermissionRequiredMixin, FormView):
    permission_required = ('logistica.view_notasalida')
    form_class = NotaSalidaBuscarForm
    template_name = "logistica/nota_salida/inicio.html"

    def get_form_kwargs(self):
        kwargs = super(NotaSalidaListView, self).get_form_kwargs()
        kwargs['filtro_sociedad'] = self.request.GET.get('sociedad')
        kwargs['filtro_cliente'] = self.request.GET.get('cliente')
        kwargs['filtro_estado'] = self.request.GET.get('estado')
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(NotaSalidaListView,self).get_context_data(**kwargs)
        nota_salida = NotaSalida.objects.all()
        if 'id_solicitud_prestamo' in self.kwargs:
            lista_nota_salida = []
            notas_salida_documento = NotaSalidaDocumento.objects.filter(
                content_type = ContentType.objects.get_for_model(SolicitudPrestamoMateriales),
                id_registro = self.kwargs['id_solicitud_prestamo'],
            )
            for nota_salida_documento in notas_salida_documento:
                lista_nota_salida.append(nota_salida_documento.nota_salida.id)
            nota_salida = nota_salida.filter(
                id__in=lista_nota_salida,
            )

        if 'id_confirmacion' in self.kwargs:
            lista_nota_salida = []
            notas_salida_documento = NotaSalidaDocumento.objects.filter(
                content_type = ContentType.objects.get_for_model(ConfirmacionVenta),
                id_registro = self.kwargs['id_confirmacion'],
            )
            for nota_salida_documento in notas_salida_documento:
                lista_nota_salida.append(nota_salida_documento.nota_salida.id)
            nota_salida = nota_salida.filter(
                id__in=lista_nota_salida,
            )

        filtro_sociedad = self.request.GET.get('sociedad')
        filtro_cliente = self.request.GET.get('cliente')
        filtro_estado = self.request.GET.get('estado')
        
        contexto_filtro = []

        if filtro_sociedad:
            lista_notas = []
            for nota in nota_salida:
                if nota.sociedad == filtro_sociedad:
                    lista_notas.append(nota.id)
            nota_salida = nota_salida.filter(id__in = lista_notas)
            contexto_filtro.append(f"sociedad={filtro_sociedad}")

        if filtro_cliente:
            lista_notas = []
            for nota in nota_salida:
                if nota.cliente == filtro_cliente:
                    lista_notas.append(nota.id)
            nota_salida = nota_salida.filter(id__in = lista_notas)
            contexto_filtro.append(f"cliente={filtro_cliente}")

        if filtro_estado:
            condicion = Q(estado = filtro_estado)
            nota_salida = nota_salida.filter(condicion)
            contexto_filtro.append(f"estado={filtro_estado}")

        context['contexto_filtro'] = "&".join(contexto_filtro)

        context['pagina_filtro'] = ""
        if self.request.GET.get('page'):
            if context['contexto_filtro']:
                context['pagina_filtro'] = f'&page={self.request.GET.get("page")}'
            else:
                context['pagina_filtro'] = f'page={self.request.GET.get("page")}'
        context['contexto_filtro'] = '?' + context['contexto_filtro']

        objectsxpage = 10 # Show 10 objects per page.

        if len(nota_salida) > objectsxpage:
            paginator = Paginator(nota_salida, objectsxpage)
            page_number = self.request.GET.get('page')
            nota_salida = paginator.get_page(page_number)
   
        context['contexto_nota_salida'] = nota_salida
        context['contexto_pagina'] = nota_salida
        return context


def NotaSalidaTabla(request, **kwargs):
    data = dict()
    if request.method == 'GET':
        template = 'logistica/nota_salida/inicio_tabla.html'
        context = {}
        nota_salida = NotaSalida.objects.all()
        if 'id_solicitud_prestamo' in kwargs:
            lista_nota_salida = []
            notas_salida_documento = NotaSalidaDocumento.objects.filter(
                content_type = ContentType.objects.get_for_model(SolicitudPrestamoMateriales),
                id_registro = kwargs['id_solicitud_prestamo'],
            )
            for nota_salida_documento in notas_salida_documento:
                lista_nota_salida.append(nota_salida_documento.nota_salida.id)
            nota_salida = nota_salida.filter(
                id__in=lista_nota_salida,
            )

        if 'id_confirmacion' in kwargs:
            lista_nota_salida = []
            notas_salida_documento = NotaSalidaDocumento.objects.filter(
                content_type = ContentType.objects.get_for_model(ConfirmacionVenta),
                id_registro = kwargs['id_confirmacion'],
            )
            for nota_salida_documento in notas_salida_documento:
                lista_nota_salida.append(nota_salida_documento.nota_salida.id)
            nota_salida = nota_salida.filter(
                id__in=lista_nota_salida,
            )

        filtro_sociedad = request.GET.get('sociedad')
        filtro_cliente = request.GET.get('cliente')
        filtro_estado = request.GET.get('estado')
        
        contexto_filtro = []

        if filtro_sociedad:
            condicion = Q(confirmacion_venta__sociedad = filtro_sociedad) | Q(solicitud_prestamo_materiales__sociedad = filtro_sociedad)
            nota_salida = nota_salida.filter(condicion)
            contexto_filtro.append(f"sociedad={filtro_sociedad}")

        if filtro_cliente:
            condicion = Q(confirmacion_venta__cliente = filtro_cliente) | Q(solicitud_prestamo_materiales__cliente = filtro_cliente)
            nota_salida = nota_salida.filter(condicion)
            contexto_filtro.append(f"cliente={filtro_cliente}")

        if filtro_estado:
            condicion = Q(estado = filtro_estado)
            nota_salida = nota_salida.filter(condicion)
            contexto_filtro.append(f"estado={filtro_estado}")

        context['contexto_filtro'] = "&".join(contexto_filtro)

        context['pagina_filtro'] = ""
        if request.GET.get('page'):
            if context['contexto_filtro']:
                context['pagina_filtro'] = f'&page={request.GET.get("page")}'
            else:
                context['pagina_filtro'] = f'page={request.GET.get("page")}'
        context['contexto_filtro'] = '?' + context['contexto_filtro']

        objectsxpage = 10 # Show 10 objects per page.

        if len(nota_salida) > objectsxpage:
            paginator = Paginator(nota_salida, objectsxpage)
            page_number = request.GET.get('page')
            nota_salida = paginator.get_page(page_number)
   
        context['contexto_nota_salida'] = nota_salida
        context['contexto_pagina'] = nota_salida

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)


class NotaSalidaUpdateView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('logistica.change_notasalida')
    model = NotaSalida
    template_name = "includes/formulario generico.html"
    form_class = NotaSalidaForm
    success_url = reverse_lazy('logistica_app:nota_salida_inicio')

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(NotaSalidaUpdateView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        context['titulo'] = "Nota de Salida"
        return context


class NotaSalidaConcluirView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('logistica.delete_notasalida')
    model = NotaSalida
    template_name = "logistica/nota_salida/boton.html"
    
    def dispatch(self, request, *args, **kwargs):
        context = {}
        error_series = False
        context['titulo'] = 'Error de guardar'
        detalles = self.get_object().NotaSalidaDetalle_nota_salida.all()
        for detalle in detalles:
            if detalle.series_validar != detalle.cantidad_salida and detalle.producto.control_serie:
                error_series = True
        
        if error_series:
            context['texto'] = 'La cantidad de series no coincide.'
            return render(request, 'includes/modal sin permiso.html', context)
        return super().dispatch(request, *args, **kwargs)
    
    def get_success_url(self, **kwargs):
        return reverse_lazy('logistica_app:nota_salida_detalle', kwargs={'pk': self.get_object().id})

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            if self.request.session['primero']:
                sid = transaction.savepoint()
                try:
                    self.object = self.get_object()

                    detalles = self.object.detalles

                    disponible = TipoStock.objects.get(codigo=3) #Disponible
                    if self.object.solicitud_prestamo_materiales:
                        print('Préstamo')
                        movimiento_inicial = TipoMovimiento.objects.get(codigo=131)  # Confirmación por préstamo
                        movimiento_final = TipoMovimiento.objects.get(codigo=132)  # Salida por préstamo
                        documento_anterior = self.object.solicitud_prestamo_materiales
                        estado_serie = EstadoSerie.objects.get(numero_estado=9) #EN PRÉSTAMO
                    else:
                        if self.object.confirmacion_venta.cotizacion_venta.estado == 4: #Confirmado con Reserva
                            print('Confirmación Con Reserva')
                            movimiento_inicial = TipoMovimiento.objects.get(codigo=119)  # Confirmación de reserva por venta
                            movimiento_final = TipoMovimiento.objects.get(codigo=121)  # Salida por venta
                            documento_anterior = self.object.confirmacion_venta
                            estado_serie = EstadoSerie.objects.get(numero_estado=3) #VENDIDO
                        elif self.object.confirmacion_venta.cotizacion_venta.estado == 5: #Confirmado sin Reserva
                            print('Confirmación Sin Reserva')
                            movimiento_inicial = TipoMovimiento.objects.get(codigo=120)  # Confirmado por venta
                            movimiento_final = TipoMovimiento.objects.get(codigo=121)  # Salida por venta
                            documento_anterior = self.object.confirmacion_venta
                            estado_serie = EstadoSerie.objects.get(numero_estado=3) #VENDIDO
                        elif self.object.confirmacion_venta.cotizacion_venta.estado == 6: #Confirmado Anticipado
                            print('Confirmación Anticipada')
                            movimiento_inicial = TipoMovimiento.objects.get(codigo=129)  # Confirmación por venta anticipada
                            movimiento_final = TipoMovimiento.objects.get(codigo=130)  # Confirmación anticipada atendida
                            documento_anterior = self.object.confirmacion_venta
                            estado_serie = EstadoSerie.objects.get(numero_estado=3) #VENDIDO

                    consolidado = {}
                    for detalle in detalles:
                        movimiento_anterior = MovimientosAlmacen.objects.get(
                            content_type_producto=detalle.content_type,
                            id_registro_producto=detalle.id_registro,
                            tipo_movimiento=movimiento_inicial,
                            tipo_stock=movimiento_inicial.tipo_stock_final,
                            signo_factor_multiplicador=+1,
                            content_type_documento_proceso=ContentType.objects.get_for_model(documento_anterior.cotizacion_venta),
                            id_registro_documento_proceso=documento_anterior.cotizacion_venta.id,
                            sociedad=documento_anterior.sociedad,
                            movimiento_reversion=False,
                        )                        

                        movimiento_uno = MovimientosAlmacen.objects.create(
                            content_type_producto=detalle.content_type,
                            id_registro_producto=detalle.id_registro,
                            cantidad=detalle.cantidad_salida,
                            tipo_movimiento=movimiento_final,
                            tipo_stock=disponible,
                            signo_factor_multiplicador=-1,
                            content_type_documento_proceso=ContentType.objects.get_for_model(self.object),
                            id_registro_documento_proceso=self.object.id,
                            almacen=detalle.almacen,
                            sociedad=self.object.sociedad,
                            movimiento_anterior=movimiento_anterior,
                            movimiento_reversion=False,
                            created_by=self.request.user,
                            updated_by=self.request.user,
                        )
                        if not detalle.producto in consolidado:
                            consolidado[detalle.producto] = Decimal('0.00')
                        consolidado[detalle.producto] = consolidado[detalle.producto] + detalle.cantidad_salida

                    for producto, cantidad in consolidado.items():
                        movimiento_dos = MovimientosAlmacen.objects.create(
                            content_type_producto=producto.content_type,
                            id_registro_producto=producto.id,
                            cantidad=cantidad,
                            tipo_movimiento=movimiento_final,
                            tipo_stock=movimiento_final.tipo_stock_inicial,
                            signo_factor_multiplicador=-1,
                            content_type_documento_proceso=ContentType.objects.get_for_model(self.object),
                            id_registro_documento_proceso=self.object.id,
                            sociedad=self.object.sociedad,
                            movimiento_anterior=None,
                            movimiento_reversion=False,
                            created_by=self.request.user,
                            updated_by=self.request.user,
                        )

                        movimiento_tres = MovimientosAlmacen.objects.create(
                            content_type_producto=producto.content_type,
                            id_registro_producto=producto.id,
                            cantidad=cantidad,
                            tipo_movimiento=movimiento_final,
                            tipo_stock=movimiento_final.tipo_stock_final,
                            signo_factor_multiplicador=+1,
                            content_type_documento_proceso=ContentType.objects.get_for_model(self.object),
                            id_registro_documento_proceso=self.object.id,
                            sociedad=self.object.sociedad,
                            movimiento_anterior=movimiento_dos,
                            movimiento_reversion=False,
                            created_by=self.request.user,
                            updated_by=self.request.user,
                        )

                        for detalle in detalles:
                            for validar_serie in detalle.ValidarSerieNotaSalidaDetalle_nota_salida_detalle.all():
                                serie = validar_serie.serie
                                HistorialEstadoSerie.objects.create(
                                    serie=serie,
                                    estado_serie=estado_serie,
                                    created_by=self.request.user,
                                    updated_by=self.request.user,
                                )

                                serie.serie_movimiento_almacen.add(movimiento_dos)
                                serie.serie_movimiento_almacen.add(movimiento_tres)

                                validar_serie.delete()
                        
                    self.object.estado = 2
                    registro_guardar(self.object, self.request)
                    self.object.save()

                    messages.success(request, MENSAJE_CONCLUIR_NOTA_SALIDA)
                except Exception as ex:
                    transaction.savepoint_rollback(sid)
                    registrar_excepcion(self, ex, __file__)
                self.request.session['primero'] = False
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        self.request.session['primero'] = True
        context = super(NotaSalidaConcluirView, self).get_context_data(**kwargs)
        context['accion'] = "Concluir"
        context['titulo'] = "Nota de Salida"
        context['dar_baja'] = "true"
        context['item'] = self.object
        return context


class NotaSalidaAnularView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('logistica.delete_notasalida')
    model = NotaSalida
    template_name = "includes/formulario generico.html"
    form_class = NotaSalidaAnularForm

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('logistica_app:nota_salida_inicio')

    @transaction.atomic
    def form_valid(self, form):
        if self.request.session['primero']:
            sid = transaction.savepoint()
            try:
                form.instance.estado = 3
                registro_guardar(form.instance, self.request)

                detalles = form.instance.detalles
                if form.instance.solicitud_prestamo_materiales:
                    movimiento_final = TipoMovimiento.objects.get(codigo=132)  # Salida por préstamo
                    documento_anterior = form.instance.solicitud_prestamo_materiales
                if form.instance.confirmacion_venta:
                    movimiento_final = TipoMovimiento.objects.get(codigo=121)  # Salida por venta
                    documento_anterior = form.instance.confirmacion_venta

                for detalle in detalles:
                    movimiento_tres = MovimientosAlmacen.objects.get(
                        content_type_producto=detalle.content_type,
                        id_registro_producto=detalle.id_registro,
                        cantidad=detalle.cantidad_salida,
                        tipo_movimiento=movimiento_final,
                        tipo_stock=movimiento_final.tipo_stock_final,
                        signo_factor_multiplicador=+1,
                        content_type_documento_proceso=ContentType.objects.get_for_model(form.instance),
                        id_registro_documento_proceso=form.instance.id,
                        # almacen=detalle.almacen,
                        sociedad=form.instance.sociedad,
                    )
                    movimiento_uno = MovimientosAlmacen.objects.filter(
                        content_type_producto=detalle.content_type,
                        id_registro_producto=detalle.id_registro,
                        # cantidad=detalle.cantidad_salida,
                        tipo_movimiento=movimiento_final,
                        tipo_stock=movimiento_final.tipo_stock_inicial,
                        signo_factor_multiplicador=-1,
                        content_type_documento_proceso=ContentType.objects.get_for_model(documento_anterior),
                        id_registro_documento_proceso=documento_anterior.id,
                        # almacen=detalle.almacen,
                        sociedad=form.instance.sociedad,
                    )
                    movimiento_dos = movimiento_tres.movimiento_anterior
                    #Pendiente eliminar movimiento del historial Serie

                    movimiento_tres.delete()
                    movimiento_dos.delete()
                    for movimiento in movimiento_uno:
                        movimiento.delete()
                messages.success(self.request, MENSAJE_ANULAR_NOTA_SALIDA)
            except Exception as ex:
                transaction.savepoint_rollback(sid)
                registrar_excepcion(self, ex, __file__)
                return HttpResponseRedirect(reverse_lazy('logistica_app:nota_salida_detalle', kwargs={'pk':form.instance.id}))
            self.request.session['primero'] = False
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        self.request.session['primero'] = True
        context = super(NotaSalidaAnularView, self).get_context_data(**kwargs)
        context['accion'] = "Anular"
        context['titulo'] = "Nota de Salida"
        return context


class NotaSalidaDetailView(PermissionRequiredMixin, DetailView):
    permission_required = ('logistica.view_notasalida')
    model = NotaSalida
    template_name = "logistica/nota_salida/detalle.html"
    context_object_name = 'contexto_nota_salida_detalle'

    def get_context_data(self, **kwargs):
        context = super(NotaSalidaDetailView, self).get_context_data(**kwargs)
        context['materiales'] = self.object.NotaSalidaDetalle_nota_salida.all()
        anular_nota = True
        for despacho in self.object.Despacho_nota_salida.all():
            if despacho.estado != 3:
                anular_nota = False
        context['anular_nota'] = anular_nota

        return context


def NotaSalidaDetailTabla(request, pk):
    data = dict()
    if request.method == 'GET':
        template = 'logistica/nota_salida/detalle_tabla.html'
        context = {}
        nota_salida = NotaSalida.objects.get(id=pk)
        context['contexto_nota_salida_detalle'] = nota_salida
        context['materiales'] = nota_salida.NotaSalidaDetalle_nota_salida.all()
        anular_nota = True
        for despacho in nota_salida.Despacho_nota_salida.all():
            if despacho.estado != 3:
                anular_nota = False
        context['anular_nota'] = anular_nota

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)


class NotaSalidaDetalleCreateView(PermissionRequiredMixin, BSModalFormView):
    permission_required = ('logistica.add_notasalidadetalle')
    template_name = "includes/formulario generico.html"
    form_class = NotaSalidaDetalleForm

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('logistica_app:nota_salida_detalle', kwargs={'pk': self.kwargs['nota_salida_id']})

    def get_form_kwargs(self):
        nota_salida = NotaSalida.objects.get(id=self.kwargs['nota_salida_id'])
        if nota_salida.solicitud_prestamo_materiales:
            solicitud = nota_salida.solicitud_prestamo_materiales.id
            materiales = SolicitudPrestamoMaterialesDetalle.objects.filter(solicitud_prestamo_materiales__id=solicitud)
            lista_materiales = SolicitudPrestamoMaterialesDetalle.objects.filter(
                solicitud_prestamo_materiales__id=solicitud)
            for material in materiales:
                salida = material.NotaSalidaDetalle_solicitud_prestamo_materiales_detalle.exclude(nota_salida__estado=3).aggregate(Sum('cantidad_salida'))[
                    'cantidad_salida__sum']
                if salida:
                    if salida == material.cantidad_prestamo:
                        lista_materiales = lista_materiales.exclude(id=material.id)
        else:
            confirmacion = nota_salida.confirmacion_venta.id
            materiales = ConfirmacionVentaDetalle.objects.filter(confirmacion_venta__id=confirmacion)
            lista_materiales = ConfirmacionVentaDetalle.objects.filter(
                confirmacion_venta__id=confirmacion)
            for material in materiales:
                salida = material.NotaSalidaDetalle_confirmacion_venta_detalle.exclude(nota_salida__estado=3).aggregate(Sum('cantidad_salida'))[
                    'cantidad_salida__sum']
                if salida:
                    if salida == material.cantidad_confirmada:
                        lista_materiales = lista_materiales.exclude(id=material.id)
        

        kwargs = super().get_form_kwargs()
        kwargs['materiales'] = lista_materiales
        return kwargs

    @transaction.atomic
    def form_valid(self, form):
        sid = transaction.savepoint()
        try:
            if self.request.session['primero']:
                nota_salida = NotaSalida.objects.get(id=self.kwargs['nota_salida_id'])
                item = len(nota_salida.NotaSalidaDetalle_nota_salida.all())
                material = form.cleaned_data.get('material')

                nota_salida_detalle = NotaSalidaDetalle.objects.create(
                    content_type_detalle=ContentType.objects.get_for_model(material),
                    id_registro_detalle=material.id,
                    nota_salida=nota_salida,
                    item=item + 1,
                    created_by=self.request.user,
                    updated_by=self.request.user,
                )
                
                self.request.session['primero'] = False
            return super().form_valid(form)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        self.request.session['primero'] = True
        context = super(NotaSalidaDetalleCreateView, self).get_context_data(**kwargs)
        context['accion'] = "Registrar"
        context['titulo'] = "Material"
        return context


class NotaSalidaDetalleUpdateView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('logistica.change_notasalidadetalle')
    model = NotaSalidaDetalle
    template_name = "logistica/nota_salida/form_almacen.html"
    form_class = NotaSalidaDetalleUpdateForm

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('logistica_app:nota_salida_detalle', kwargs={'pk': self.object.nota_salida.id})

    def get_form_kwargs(self, *args, **kwargs):
        if self.object.solicitud_prestamo_materiales_detalle:
            material = self.object.solicitud_prestamo_materiales_detalle
            suma = material.NotaSalidaDetalle_solicitud_prestamo_materiales_detalle.exclude(nota_salida__estado=3).aggregate(Sum('cantidad_salida'))[
                'cantidad_salida__sum']
        else:
            material = self.object.confirmacion_venta_detalle
            suma = material.NotaSalidaDetalle_confirmacion_venta_detalle.exclude(nota_salida__estado=3).aggregate(Sum('cantidad_salida'))[
                'cantidad_salida__sum']
        cantidad_salida = self.object.cantidad_salida
        kwargs = super(NotaSalidaDetalleUpdateView, self).get_form_kwargs(*args, **kwargs)
        kwargs['solicitud'] = material
        kwargs['suma'] = suma - cantidad_salida
        kwargs['id_sociedad'] = self.object.nota_salida.sociedad.id
        return kwargs

    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(NotaSalidaDetalleUpdateView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        context['titulo'] = "Material"
        context['id_sociedad'] = self.object.nota_salida.sociedad.id
        context['id_material'] = self.object.producto.id
        context['url_stock'] = reverse_lazy('material_app:stock_disponible', kwargs={'id_material':1})[:-2]
        return context


class NotaSalidaDetalleDeleteView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('logistica.delete_notasalidadetalle')
    model = NotaSalidaDetalle
    template_name = "includes/eliminar generico.html"

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('logistica_app:nota_salida_detalle', kwargs={'pk': self.get_object().nota_salida.id})

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            materiales = NotaSalidaDetalle.objects.filter(nota_salida=self.get_object().nota_salida)
            contador = 1
            for material in materiales:
                if material == self.get_object(): continue
                material.item = contador
                material.save()
                contador += 1
            return super().delete(request, *args, **kwargs)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(NotaSalidaDetalleDeleteView, self).get_context_data(**kwargs)
        context['accion'] = "Eliminar"
        context['titulo'] = "Material"
        context['item'] = self.get_object()
        context['dar_baja'] = "true"
        return context


class ValidarSeriesNotaSalidaDetailView(PermissionRequiredMixin, FormView):
    permission_required = ('logistica.view_notasalidadetalle')
    template_name = "logistica/validar_serie_nota_salida/detalle.html"
    form_class = NotaSalidaDetalleSeriesForm
    success_url = '.'

    def form_valid(self, form):
        if self.request.session['primero']:
            serie = form.cleaned_data['serie']
            nota_salida_detalle = NotaSalidaDetalle.objects.get(id = self.kwargs['pk'])
            try:
                buscar = Serie.objects.get(
                    serie_base=serie,
                    content_type=ContentType.objects.get_for_model(nota_salida_detalle.producto),
                    id_registro=nota_salida_detalle.producto.id,
                )
                buscar2 = ValidarSerieNotaSalidaDetalle.objects.filter(serie = buscar)

                if len(buscar2) != 0:
                    form.add_error('serie', "Serie ya ha sido registrada")
                    return super().form_invalid(form)

                if buscar.estado != 'DISPONIBLE':
                    form.add_error('serie', "Serie no disponible, su estado es: %s" % buscar.estado)
                    return super().form_invalid(form)
            except:
                form.add_error('serie', "Serie no encontrada: %s" % serie)
                return super().form_invalid(form)

            nota_salida_detalle = NotaSalidaDetalle.objects.get(id = self.kwargs['pk'])
            obj, created = ValidarSerieNotaSalidaDetalle.objects.get_or_create(
                nota_salida_detalle=nota_salida_detalle,
                serie=buscar,
            )
            if created:
                obj.estado = 1
            self.request.session['primero'] = False
        return super().form_valid(form)

    def get_form_kwargs(self):
        nota_salida_detalle = NotaSalidaDetalle.objects.get(id = self.kwargs['pk'])
        cantidad_salida = nota_salida_detalle.cantidad_salida
        cantidad_ingresada = len(ValidarSerieNotaSalidaDetalle.objects.filter(nota_salida_detalle=nota_salida_detalle))
        kwargs = super().get_form_kwargs()
        kwargs['cantidad_salida'] = cantidad_salida
        kwargs['cantidad_ingresada'] = cantidad_ingresada
        return kwargs

    def get_context_data(self, **kwargs):
        self.request.session['primero'] = True
        nota_salida_detalle = NotaSalidaDetalle.objects.get(id = self.kwargs['pk'])
        context = super(ValidarSeriesNotaSalidaDetailView, self).get_context_data(**kwargs)
        context['contexto_nota_salida_detalle'] = nota_salida_detalle
        context['contexto_series'] = ValidarSerieNotaSalidaDetalle.objects.filter(nota_salida_detalle = nota_salida_detalle)
        return context

def ValidarSeriesNotaSalidaDetailTabla(request, pk):
    data = dict()
    if request.method == 'GET':
        template = 'logistica/validar_serie_nota_salida/detalle_tabla.html'
        context = {}
        nota_salida_detalle = NotaSalidaDetalle.objects.get(id = pk)
        context['contexto_nota_salida_detalle'] = nota_salida_detalle
        context['contexto_series'] = ValidarSerieNotaSalidaDetalle.objects.filter(nota_salida_detalle = nota_salida_detalle)

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)


class ValidarSeriesNotaSalidaDetalleDeleteView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('logistica.delete_validarserienotasalidadetalle')
    model = ValidarSerieNotaSalidaDetalle
    template_name = "includes/eliminar generico.html"

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('logistica_app:validar_series_detalle', kwargs={'pk': self.get_object().nota_salida_detalle.id})

    def get_context_data(self, **kwargs):
        context = super(ValidarSeriesNotaSalidaDetalleDeleteView, self).get_context_data(**kwargs)
        context['accion'] = "Eliminar"
        context['titulo'] = "Serie"
        context['item'] = self.get_object().serie
        context['dar_baja'] = "true"
        return context


class AlmacenForm(forms.Form):
    almacen = forms.ModelChoiceField(queryset=Almacen.objects.all(), required=False)

def AlmacenView(request, id_sede):
    form = AlmacenForm()
    form.fields['almacen'].queryset = Almacen.objects.filter(sede=id_sede)

    data = dict()
    if request.method == 'GET':
        template = 'includes/form.html'
        context = {'form': form}

        data['info'] = render_to_string(
            template,
            context,
            request=request
        ).replace('selected', 'selected=""')
        return JsonResponse(data)


class NotaSalidaGenerarDespachoView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('logistica.change_notasalidadetalle')
    model = NotaSalida
    template_name = "logistica/nota_salida/boton.html"

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)
    
    def get_success_url(self):
        return reverse_lazy('logistica_app:despacho_detalle', kwargs={'pk':self.kwargs['despacho'].id})

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            if self.request.session['primero']:
                self.object = self.get_object()
                nota_salida = self.get_object()
                item = len(Despacho.objects.all())
                despacho = Despacho.objects.create(
                    sociedad=nota_salida.sociedad,
                    nota_salida=nota_salida,
                    numero_despacho=item + 1,
                    cliente=nota_salida.cliente,
                    created_by=self.request.user,
                    updated_by=self.request.user,
                )

                nota_salida_detalle = nota_salida.NotaSalidaDetalle_nota_salida.all()
                lista = []
                lista_id_registro = []
                lista_nota_salida = []
                if nota_salida.solicitud_prestamo_materiales:
                    for detalle in nota_salida_detalle:
                        id_registro = detalle.solicitud_prestamo_materiales_detalle.id_registro
                        if id_registro not in lista_id_registro:
                            lista_id_registro.append(id_registro)
                            lista.append(detalle)
                    for nota_salida_buscar in nota_salida.solicitud_prestamo_materiales.NotaSalida_solicitud_prestamo_materiales.all().exclude(estado=3):
                        lista_nota_salida.append(nota_salida_buscar.id)
                    item = 0
                    for dato in lista:
                        material = dato.solicitud_prestamo_materiales_detalle
                        cantidad_notas_salida = material.NotaSalidaDetalle_solicitud_prestamo_materiales_detalle.all().exclude(nota_salida__estado=3).aggregate(Sum('cantidad_salida'))['cantidad_salida__sum']
                        cantidad_despachos = DespachoDetalle.objects.filter(despacho__nota_salida__id__in=lista_nota_salida).exclude(despacho__estado=3).filter(content_type=material.content_type, id_registro=material.id_registro).aggregate(Sum('cantidad_despachada'))['cantidad_despachada__sum']
                        cantidad_despachada = cantidad_notas_salida
                        if cantidad_despachos:
                            cantidad_despachada = cantidad_notas_salida - cantidad_despachos
                        despacho_detalle = DespachoDetalle.objects.create(
                            item=item + 1,
                            content_type=dato.solicitud_prestamo_materiales_detalle.content_type,
                            id_registro=dato.solicitud_prestamo_materiales_detalle.id_registro,
                            cantidad_despachada=cantidad_despachada,
                            despacho=despacho,
                            created_by=self.request.user,
                            updated_by=self.request.user,
                        )
                        item += 1
                else:
                    for detalle in nota_salida_detalle:
                        id_registro = detalle.confirmacion_venta_detalle.id_registro
                        if id_registro not in lista_id_registro:
                            lista_id_registro.append(id_registro)
                            lista.append(detalle)
                    for nota_salida_buscar in nota_salida.confirmacion_venta.NotaSalida_confirmacion_venta.all().exclude(estado=3):
                        lista_nota_salida.append(nota_salida_buscar.id)
                    item = 0
                    for dato in lista:
                        material = dato.confirmacion_venta_detalle
                        cantidad_notas_salida = material.NotaSalidaDetalle_confirmacion_venta_detalle.all().exclude(nota_salida__estado=3).aggregate(Sum('cantidad_salida'))['cantidad_salida__sum']
                        cantidad_despachos = DespachoDetalle.objects.filter(despacho__nota_salida__id__in=lista_nota_salida).exclude(despacho__estado=3).filter(content_type=material.content_type, id_registro=material.id_registro).aggregate(Sum('cantidad_despachada'))['cantidad_despachada__sum']
                        cantidad_despachada = cantidad_notas_salida
                        if cantidad_despachos:
                            cantidad_despachada = cantidad_notas_salida - cantidad_despachos
                        despacho_detalle = DespachoDetalle.objects.create(
                            item=item + 1,
                            content_type=dato.confirmacion_venta_detalle.content_type,
                            id_registro=dato.confirmacion_venta_detalle.id_registro,
                            cantidad_despachada=cantidad_despachada,
                            despacho=despacho,
                            created_by=self.request.user,
                            updated_by=self.request.user,
                        )
                        item += 1
                self.request.session['primero'] = False
                self.kwargs['despacho'] = despacho
            registro_guardar(self.object, self.request)
            self.object.save()
            messages.success(request, MENSAJE_GENERAR_DESPACHO)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        self.request.session['primero'] = True
        context = super(NotaSalidaGenerarDespachoView, self).get_context_data(**kwargs)
        context['accion'] = "Generar"
        context['titulo'] = "Despacho"
        context['dar_baja'] = "true"
        return context


class DespachoListView(PermissionRequiredMixin, FormView):
    permission_required = ('logistica.view_despacho')
    form_class = DespachoBuscarForm
    template_name = 'logistica/despacho/inicio.html'

    def get_form_kwargs(self):
        kwargs = super(DespachoListView, self).get_form_kwargs()
        kwargs['filtro_sociedad'] = self.request.GET.get('sociedad')
        kwargs['filtro_cliente'] = self.request.GET.get('cliente')
        kwargs['filtro_estado'] = self.request.GET.get('estado')
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super(DespachoListView,self).get_context_data(**kwargs)
        despacho = Despacho.objects.all()

        if 'id_nota_salida' in self.kwargs:
            despacho = despacho.filter(nota_salida__id=self.kwargs['id_nota_salida'])

        filtro_sociedad = self.request.GET.get('sociedad')
        filtro_cliente = self.request.GET.get('cliente')
        filtro_estado = self.request.GET.get('estado')
        
        contexto_filtro = []

        if filtro_sociedad:
            condicion = Q(sociedad = filtro_sociedad)
            despacho = despacho.filter(condicion)
            contexto_filtro.append(f"sociedad={filtro_sociedad}")

        if filtro_cliente:
            condicion = Q(cliente = filtro_cliente)
            despacho = despacho.filter(condicion)
            contexto_filtro.append(f"cliente={filtro_cliente}")

        if filtro_estado:
            condicion = Q(estado = filtro_estado)
            despacho = despacho.filter(condicion)
            contexto_filtro.append(f"estado={filtro_estado}")

        context['contexto_filtro'] = "&".join(contexto_filtro)

        context['pagina_filtro'] = ""
        if self.request.GET.get('page'):
            if context['contexto_filtro']:
                context['pagina_filtro'] = f'&page={self.request.GET.get("page")}'
            else:
                context['pagina_filtro'] = f'page={self.request.GET.get("page")}'
        context['contexto_filtro'] = '?' + context['contexto_filtro']

        objectsxpage = 10 # Show 10 objects per page.

        if len(despacho) > objectsxpage:
            paginator = Paginator(despacho, objectsxpage)
            page_number = self.request.GET.get('page')
            despacho = paginator.get_page(page_number)
   
        context['contexto_despacho'] = despacho
        context['contexto_pagina'] = despacho
        return context


def DespachoTabla(request, **kwargs):
    data = dict()
    if request.method == 'GET':
        template = 'logistica/despacho/inicio_tabla.html'
        context = {}
        despacho = Despacho.objects.all()

        if 'id_nota_salida' in kwargs:
            despacho = despacho.filter(nota_salida__id=kwargs['id_nota_salida'])

        filtro_sociedad = request.GET.get('sociedad')
        filtro_cliente = request.GET.get('cliente')
        filtro_estado = request.GET.get('estado')
        
        contexto_filtro = []

        if filtro_sociedad:
            condicion = Q(sociedad = filtro_sociedad)
            despacho = despacho.filter(condicion)
            contexto_filtro.append(f"sociedad={filtro_sociedad}")

        if filtro_cliente:
            condicion = Q(cliente = filtro_cliente)
            despacho = despacho.filter(condicion)
            contexto_filtro.append(f"cliente={filtro_cliente}")

        if filtro_estado:
            condicion = Q(estado = filtro_estado)
            despacho = despacho.filter(condicion)
            contexto_filtro.append(f"estado={filtro_estado}")

        context['contexto_filtro'] = "&".join(contexto_filtro)

        context['pagina_filtro'] = ""
        if request.GET.get('page'):
            if context['contexto_filtro']:
                context['pagina_filtro'] = f'&page={request.GET.get("page")}'
            else:
                context['pagina_filtro'] = f'page={request.GET.get("page")}'
        context['contexto_filtro'] = '?' + context['contexto_filtro']

        objectsxpage = 10 # Show 10 objects per page.

        if len(despacho) > objectsxpage:
            paginator = Paginator(despacho, objectsxpage)
            page_number = request.GET.get('page')
            despacho = paginator.get_page(page_number)
   
        context['contexto_despacho'] = despacho
        context['contexto_pagina'] = despacho

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)


class DespachoUpdateView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('logistica.change_despacho')
    model = Despacho
    template_name = "includes/formulario generico.html"
    form_class = DespachoForm
    success_url = reverse_lazy('logistica_app:despacho_inicio')

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        if self.request.session['primero']:
            registro_guardar(form.instance, self.request)
            self.request.session['primero'] = False
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        self.request.session['primero'] = True
        context = super(DespachoUpdateView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        context['titulo'] = "Despacho"
        return context


class DespachoConcluirView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('logistica.delete_despacho')
    model = Despacho
    template_name = "logistica/despacho/boton.html"

    def dispatch(self, request, *args, **kwargs):
        context = {}
        error_fecha = False
        context['titulo'] = 'Error de guardar'
        if not self.get_object().fecha_despacho:
            error_fecha = True

        if error_fecha:
            context['texto'] = 'Ingrese una fecha de despacho.'
            return render(request, 'includes/modal sin permiso.html', context)
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('logistica_app:despacho_detalle', kwargs={'pk': self.get_object().id})

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            if self.request.session['primero']:
                self.object = self.get_object()

                detalles = self.object.detalles
                
                documento_anterior = self.object.nota_salida
                if self.object.nota_salida.solicitud_prestamo_materiales:
                    movimiento_inicial = TipoMovimiento.objects.get(codigo=132)  # Salida por préstamo
                    movimiento_final = TipoMovimiento.objects.get(codigo=133)  # Despacho por préstamo
                elif self.object.nota_salida.confirmacion_venta.cotizacion_venta.estado == 6:
                    movimiento_inicial = TipoMovimiento.objects.get(codigo=130)  # Confirmación anticipada atendida
                    movimiento_final = TipoMovimiento.objects.get(codigo=122)  # Despacho por venta
                else:
                    movimiento_inicial = TipoMovimiento.objects.get(codigo=121)  # Salida por venta
                    movimiento_final = TipoMovimiento.objects.get(codigo=122)  # Despacho por venta
                    
                for detalle in detalles:
                    movimiento_anterior = MovimientosAlmacen.objects.get(
                        content_type_producto=detalle.content_type,
                        id_registro_producto=detalle.id_registro,
                        tipo_movimiento=movimiento_inicial,
                        tipo_stock=movimiento_inicial.tipo_stock_final,
                        signo_factor_multiplicador=+1,
                        content_type_documento_proceso=ContentType.objects.get_for_model(documento_anterior),
                        id_registro_documento_proceso=documento_anterior.id,
                        sociedad=documento_anterior.sociedad,
                        movimiento_reversion=False,
                    )

                    movimiento_uno = MovimientosAlmacen.objects.create(
                        content_type_producto=detalle.content_type,
                        id_registro_producto=detalle.id_registro,
                        cantidad=detalle.cantidad_despachada,
                        tipo_movimiento=movimiento_final,
                        tipo_stock=movimiento_final.tipo_stock_inicial,
                        signo_factor_multiplicador=-1,
                        content_type_documento_proceso=ContentType.objects.get_for_model(self.object),
                        id_registro_documento_proceso=self.object.id,
                        sociedad=self.object.sociedad,
                        movimiento_anterior=None,
                        movimiento_reversion=False,
                        created_by=self.request.user,
                        updated_by=self.request.user,
                    )

                    movimiento_dos = MovimientosAlmacen.objects.create(
                        content_type_producto=detalle.content_type,
                        id_registro_producto=detalle.id_registro,
                        cantidad=detalle.cantidad_despachada,
                        tipo_movimiento=movimiento_final,
                        tipo_stock=movimiento_final.tipo_stock_final,
                        signo_factor_multiplicador=+1,
                        content_type_documento_proceso=ContentType.objects.get_for_model(self.object),
                        id_registro_documento_proceso=self.object.id,
                        sociedad=self.object.sociedad,
                        movimiento_anterior=movimiento_uno,
                        movimiento_reversion=False,
                        created_by=self.request.user,
                        updated_by=self.request.user,
                    )

                    movimientos_serie_buscar = MovimientosAlmacen.objects.filter(
                        tipo_movimiento = movimiento_inicial,
                        tipo_stock = movimiento_inicial.tipo_stock_final,
                        content_type_documento_proceso = documento_anterior.content_type,
                        id_registro_documento_proceso = documento_anterior.id,
                    )
                    for movimientos_serie in movimientos_serie_buscar:
                        for serie in movimientos_serie.Serie_serie_movimiento_almacen.all():
                            if movimiento_uno.content_type_producto == serie.content_type and movimiento_uno.id_registro_producto == serie.id_registro:
                                serie.serie_movimiento_almacen.add(movimiento_uno)
                                serie.serie_movimiento_almacen.add(movimiento_dos)

                confirmacion_venta = self.object.nota_salida.confirmacion_venta
                if confirmacion_venta:
                    if not confirmacion_venta.pendiente_despachar:
                        if confirmacion_venta.estado == 2:
                            confirmacion_venta.estado = 4
                        elif confirmacion_venta.estado == 1:
                            confirmacion_venta.estado = 5
                        registro_guardar(confirmacion_venta, self.request)
                        confirmacion_venta.save()
                self.object.estado = 2
                registro_guardar(self.object, self.request)
                self.object.save()
                messages.success(request, MENSAJE_CONCLUIR_DESPACHO)
                self.request.session['primero'] = False
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        self.request.session['primero'] = True
        context = super(DespachoConcluirView, self).get_context_data(**kwargs)
        context['accion'] = "Concluir"
        context['titulo'] = "Despacho"
        context['dar_baja'] = "true"
        context['item'] = self.object
        return context


class DespachoFinalizarSinGuiaView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('logistica.delete_despacho')
    model = Despacho
    template_name = "logistica/despacho/boton.html"

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('logistica_app:despacho_detalle', kwargs={'pk': self.get_object().id})

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            self.object = self.get_object()
            self.object.estado = 4
            registro_guardar(self.object, self.request)
            self.object.save()
            messages.success(request, MENSAJE_FINALIZAR_SIN_GUIA_DESPACHO)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(DespachoFinalizarSinGuiaView, self).get_context_data(**kwargs)
        context['accion'] = "Finalizar"
        context['titulo'] = "Despacho sin Guia"
        context['dar_baja'] = "true"
        context['item'] = self.object
        return context


class DespachoAnularView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('logistica.delete_despacho')
    model = Despacho
    template_name = "includes/formulario generico.html"
    form_class = DespachoAnularForm

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('logistica_app:despacho_inicio')

    @transaction.atomic
    def form_valid(self, form):
        sid = transaction.savepoint()
        try:
            if self.request.session['primero']:
                form.instance.estado = 3
                registro_guardar(form.instance, self.request)

                detalles = form.instance.detalles
                if self.object.nota_salida.solicitud_prestamo_materiales:
                    movimiento_final = TipoMovimiento.objects.get(codigo=133)  # Despacho por préstamo
                else:
                    movimiento_final = TipoMovimiento.objects.get(codigo=122)  # Despacho por venta

                for detalle in detalles:
                    movimiento_uno = MovimientosAlmacen.objects.get(
                        content_type_producto=detalle.content_type,
                        id_registro_producto=detalle.id_registro,
                        cantidad=detalle.cantidad_despachada,
                        tipo_movimiento=movimiento_final,
                        tipo_stock=movimiento_final.tipo_stock_inicial,
                        signo_factor_multiplicador=-1,
                        content_type_documento_proceso=ContentType.objects.get_for_model(form.instance),
                        id_registro_documento_proceso=form.instance.id,
                        almacen=None,
                        sociedad=form.instance.sociedad,
                    )

                    movimiento_dos = MovimientosAlmacen.objects.get(
                        content_type_producto=detalle.content_type,
                        id_registro_producto=detalle.id_registro,
                        cantidad=detalle.cantidad_despachada,
                        tipo_movimiento=movimiento_final,
                        tipo_stock=movimiento_final.tipo_stock_final,
                        signo_factor_multiplicador=+1,
                        content_type_documento_proceso=ContentType.objects.get_for_model(form.instance),
                        id_registro_documento_proceso=form.instance.id,
                        almacen=None,
                        sociedad=form.instance.sociedad,
                    )
                    movimiento_dos.delete()
                    movimiento_uno.delete()

                confirmacion_venta = form.instance.nota_salida.confirmacion_venta
                if confirmacion_venta:
                    if confirmacion_venta.estado == 4:
                        confirmacion_venta.estado = 2
                    elif confirmacion_venta.estado == 5:
                        confirmacion_venta.estado = 1
                    registro_guardar(confirmacion_venta, self.request)
                    confirmacion_venta.save()
                messages.success(self.request, MENSAJE_ANULAR__DESPACHO)
                self.request.session['primero'] = False
            return super().form_valid(form)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        self.request.session['primero'] = True
        context = super(DespachoAnularView, self).get_context_data(**kwargs)
        context['accion'] = "Anular"
        context['titulo'] = "Despacho"
        return context


class DespachoDetailView(PermissionRequiredMixin, DetailView):
    permission_required = ('logistica.view_despacho')
    model = Despacho
    template_name = "logistica/despacho/detalle.html"
    context_object_name = 'contexto_despacho_detalle'

    def get_context_data(self, **kwargs):
        # despacho = Despacho.objects.get(id = self.kwargs['pk'])
        context = super(DespachoDetailView, self).get_context_data(**kwargs)
        context['materiales'] = self.object.DespachoDetalle_despacho.all()
        if self.object.Guia_despacho.all():
            context['url_guia'] = reverse_lazy('comprobante_despacho_app:guia_detalle', kwargs={'id_guia' : self.object.Guia_despacho.latest('created_at').id})
        return context


def DespachoDetailTabla(request, pk):
    data = dict()
    if request.method == 'GET':
        template = 'logistica/despacho/detalle_tabla.html'
        context = {}
        despacho = Despacho.objects.get(id=pk)
        context['contexto_despacho_detalle'] = despacho
        context['materiales'] = DespachoDetalle.objects.filter(despacho=despacho)
        if despacho.Guia_despacho.all():
            context['url_guia'] = reverse_lazy('comprobante_despacho_app:guia_detalle', kwargs={'id_guia' : despacho.Guia_despacho.latest('created_at').id})

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)


class DespachoGenerarGuiaView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('logistica.change_despachodetalle')
    model = Despacho
    template_name = "logistica/despacho/boton.html"
    
    def dispatch(self, request, *args, **kwargs):
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
            detalles = self.object.DespachoDetalle_despacho.all()
            serie_comprobante = SeriesComprobante.objects.por_defecto(ContentType.objects.get_for_model(Guia))

            guia = Guia.objects.create(
                sociedad=self.object.sociedad,
                serie_comprobante=serie_comprobante,
                cliente=self.object.cliente,
                observaciones=self.object.observacion,
                despacho=self.object,
                created_by=self.request.user,
                updated_by=self.request.user,
            )

            for detalle in detalles:
                guia_detalle = GuiaDetalle.objects.create(
                    item=detalle.item,
                    content_type=detalle.content_type,
                    id_registro=detalle.id_registro,
                    guia=guia,
                    cantidad=detalle.cantidad_despachada,
                    unidad=detalle.producto.unidad_base,
                    descripcion_documento=detalle.producto.descripcion_venta,
                    peso=detalle.producto.peso_unidad_base,
                    created_by=self.request.user,
                    updated_by=self.request.user,
                )
            self.kwargs['guia'] = guia
            self.request.session['primero'] = False
            registro_guardar(self.object, self.request)
            self.object.estado = 5
            self.object.save()
            messages.success(request, MENSAJE_GENERAR_GUIA)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        self.request.session['primero'] = True
        context = super(DespachoGenerarGuiaView, self).get_context_data(**kwargs)
        context['accion'] = "Generar"
        context['titulo'] = "Guía"
        context['dar_baja'] = "true"
        return context


class ImagenesDespachoCreateView(PermissionRequiredMixin, BSModalCreateView):
    permission_required = ('logistica.change_despacho')
    model = ImagenesDespacho
    template_name = "includes/formulario generico.html"
    form_class = ImagenesDespachoForm

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('logistica_app:despacho_inicio')

    @transaction.atomic
    def form_valid(self, form):
        sid = transaction.savepoint()
        try:
            if self.request.session['primero']:
                despacho = Despacho.objects.get(id=self.kwargs['id_despacho'])
                form.instance.despacho = despacho
                registro_guardar(form.instance, self.request)
            return super().form_valid(form)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        self.request.session['primero'] = True
        context = super(ImagenesDespachoCreateView, self).get_context_data(**kwargs)
        context['accion'] = "Agregar"
        context['titulo'] = "Imagen de Despacho"
        return context


class ImagenesDespachoDeleteView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('logistica.delete_despacho')
    model = ImagenesDespacho
    template_name = "includes/eliminar generico.html"

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('logistica_app:despacho_detalle', kwargs={'pk': self.get_object().despacho.id})

    def get_context_data(self, **kwargs):
        context = super(ImagenesDespachoDeleteView, self).get_context_data(**kwargs)
        context['accion'] = "Eliminar"
        context['titulo'] = "Imagen de Despacho"
        context['item'] = self.object
        return context


class NotaSalidaSeriesPdf(View):
    def get(self, request, *args, **kwargs):
        obj = NotaSalida.objects.get(id=self.kwargs['pk'])

        color = obj.sociedad.color
        titulo = 'SERIES DE EQUIPOS'
        vertical = True
        logo = [obj.sociedad.logo.url]
        pie_pagina = obj.sociedad.pie_pagina

        titulo = "%s - %s - %s" % (titulo, numeroXn(obj.numero_salida, 6), obj.cliente)

        movimientos = MovimientosAlmacen.objects.buscar_movimiento(obj, ContentType.objects.get_for_model(NotaSalida))
        series = Serie.objects.buscar_series(movimientos)
        series_unicas = []
        if series:
            series_unicas = series.order_by('id_registro', 'serie_base').distinct()
        
        texto_cabecera = '''La empresa %s certifica la entrega a la empresa indicada en el presente documento de los equipos con sus respectivos números de serie enlistados a continuación:''' %(obj.sociedad.razon_social)
        
        series_final = {}
        for serie in series_unicas:
            if not serie.producto in series_final:
                series_final[serie.producto] = []
            series_final[serie.producto].append(serie.serie_base)

        TablaEncabezado = ['DOCUMENTOS',
                           'FECHA',
                           'RAZÓN SOCIAL',
                           DICCIONARIO_TIPO_DOCUMENTO_SUNAT[obj.cliente.tipo_documento],
                           ]

        TablaDatos = []
        TablaDatos.append("<br/>".join(obj.documentos))
        TablaDatos.append(obj.fecha.strftime('%d/%m/%Y'))
        TablaDatos.append(obj.cliente.razon_social)
        TablaDatos.append(obj.cliente.numero_documento)

        buf = generarSeries(titulo, vertical, logo, pie_pagina, texto_cabecera, TablaEncabezado, TablaDatos, series_final, color)

        respuesta = HttpResponse(buf.getvalue(), content_type='application/pdf')
        respuesta.headers['content-disposition'] = 'inline; filename=%s.pdf' % titulo

        return respuesta


class InventarioMaterialesListView(PermissionRequiredMixin, ListView):
    permission_required = ('logistica.view_inventariomateriales')
    model = InventarioMateriales
    template_name = "logistica/inventario_materiales/inicio.html"
    context_object_name = 'contexto_inventario_materiales'

def InventarioMaterialesTabla(request):
    data = dict()
    if request.method == 'GET':
        template = 'logistica/inventario_materiales/inicio_tabla.html'
        context = {}
        context['contexto_inventario_materiales'] = InventarioMateriales.objects.all()

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)

class InventarioMaterialesCreateView(PermissionRequiredMixin, BSModalCreateView):
    permission_required = ('logistica.view_inventariomateriales')
    model = InventarioMateriales
    template_name = "includes/formulario generico.html"
    form_class = InventarioMaterialesForm
    success_url = reverse_lazy('logistica_app:inventario_materiales_inicio')

    def get_context_data(self, **kwargs):
        context = super(InventarioMaterialesCreateView, self).get_context_data(**kwargs)
        context['accion']="Registrar"
        context['titulo']="Inventario Materiales"
        return context

    def form_valid(self, form):

        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)

        return super().form_valid(form)


class InventarioMaterialesUpdateView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('logistica.change_inventariomateriales')
    model = InventarioMateriales
    template_name = "includes/formulario generico.html"
    form_class = InventarioMaterialesUpdateForm
    success_url = reverse_lazy('logistica_app:inventario_materiales_inicio')

    def get_context_data(self, **kwargs):
        context = super(InventarioMaterialesUpdateView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        context['titulo'] = "Inventario"
        return context

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)
        
        return super().form_valid(form)


class InventarioMaterialesConcluirView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('logistica.change_inventariomateriales')
    model = InventarioMateriales
    template_name = "logistica/inventario_materiales/boton.html"
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('logistica_app:ajuste_inventario_materiales_inicio')

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            self.request.session['primero'] = True
            self.object = self.get_object()
            detalles = self.object.InventarioMaterialesDetalle_inventario_materiales.all()

            ajuste_inventario_materiales = AjusteInventarioMateriales.objects.create(
                sociedad=self.object.sociedad,
                sede=self.object.sede,
                observacion='',
                estado='1',
                inventario_materiales=self.object,
                created_by=self.request.user,
                updated_by=self.request.user,
            )

            for detalle in detalles:
                ajuste_inventario_materiales_detalle = AjusteInventarioMaterialesDetalle.objects.create(
                    item=detalle.item,
                    material=detalle.material,
                    almacen=detalle.almacen,
                    tipo_stock=detalle.tipo_stock,
                    cantidad_stock=stock_tipo_stock(
                        content_type=detalle.material.content_type,
                        id_registro=detalle.material.id,
                        id_sociedad=self.object.sociedad.id,
                        id_almacen=detalle.almacen.id,
                        id_tipo_stock=detalle.tipo_stock.id),
                    cantidad_contada=detalle.cantidad,
                    ajuste_inventario_materiales=ajuste_inventario_materiales,
                    created_by=self.request.user,
                    updated_by=self.request.user,
                )
            self.kwargs['ajuste_inventario_materiales'] = ajuste_inventario_materiales
            self.request.session['primero'] = False
            registro_guardar(self.object, self.request)
            self.object.estado = 2
            self.object.save()
            messages.success(request, MENSAJE_GENERAR_DOCUMENTO_AJUSTE_INVENTARIO)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        self.request.session['primero'] = True
        context = super(InventarioMaterialesConcluirView, self).get_context_data(**kwargs)
        context['accion'] = "Concluir"
        context['titulo'] = "Inventario Materiales"
        context['dar_baja'] = "true"
        return context


class InventarioMaterialesDetailView(PermissionRequiredMixin, DetailView):
    permission_required = ('logistica.view_inventariomaterial')

    model = InventarioMateriales
    template_name = "logistica/inventario_materiales/detalle.html"
    context_object_name = 'contexto_inventario_materiales_detalle'

    def get_context_data(self, **kwargs):
        inventario_materiales = InventarioMateriales.objects.get(id = self.kwargs['pk'])
        context = super(InventarioMaterialesDetailView, self).get_context_data(**kwargs)
        context['inventario_materiales_detalle'] = InventarioMaterialesDetalle.objects.filter(inventario_materiales = inventario_materiales)
        return context


def InventarioMaterialesDetailTabla(request, pk):
    data = dict()
    if request.method == 'GET':
        template = 'logistica/inventario_materiales/detalle_tabla.html'
        context = {}
        inventario_materiales = InventarioMateriales.objects.get(id = pk)
        context['contexto_inventario_materiales_detalle'] = inventario_materiales
        context['inventario_materiales_detalle'] = InventarioMaterialesDetalle.objects.filter(inventario_materiales = inventario_materiales)
        
        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)


class InventarioMaterialesDetalleCreateView(PermissionRequiredMixin, BSModalFormView):
    permission_required = ('logistica.view_inventariomaterialdetalle')
    template_name = "logistica/inventario_materiales/form_material.html"
    form_class = InventarioMaterialesDetalleForm
    success_url = reverse_lazy('logistica_app:inventario_materiales_inicio')

    def get_form_kwargs(self):
        registro = InventarioMateriales.objects.get(id = self.kwargs['inventario_materiales_id'])
        sede = registro.sede.id
        almacenes = Almacen.objects.filter(sede__id = sede)

        kwargs = super().get_form_kwargs()
        kwargs['almacenes'] = almacenes
        return kwargs

    @transaction.atomic
    def form_valid(self, form):
        sid = transaction.savepoint()
        try:
            if self.request.session['primero']:
                inventario_materiales = InventarioMateriales.objects.get(id=self.kwargs['inventario_materiales_id'])
                item = len(InventarioMaterialesDetalle.objects.filter(inventario_materiales = inventario_materiales))

                material = form.cleaned_data.get('material')
                almacen = form.cleaned_data.get('almacen')
                tipo_stock = form.cleaned_data.get('tipo_stock')
                cantidad = form.cleaned_data.get('cantidad')

                obj, created = InventarioMaterialesDetalle.objects.get_or_create(
                    material = material,
                    almacen = almacen,
                    tipo_stock = tipo_stock,
                    inventario_materiales = inventario_materiales,
                )
                
                if created:
                    obj.item = item + 1
                    obj.cantidad = cantidad

                else:
                    obj.cantidad = obj.cantidad + cantidad

                registro_guardar(obj, self.request)
                obj.save()
                self.request.session['primero'] = False
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.success_url)

    def get_context_data(self, **kwargs):
        self.request.session['primero'] = True
        context = super(InventarioMaterialesDetalleCreateView, self).get_context_data(**kwargs)
        context['accion']="Registrar"
        context['titulo']="Material"
        return context


class InventarioMaterialesDetalleUpdateView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('logistica.change_inventariomaterialdetalle')
    model = InventarioMaterialesDetalle
    template_name = "logistica/inventario_materiales/form_material.html"
    form_class = InventarioMaterialesDetalleForm

    def get_success_url(self, **kwargs):
        return reverse_lazy('logistica_app:inventario_materiales_detalle', kwargs={'pk':self.get_object().inventario_materiales_id})

    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_form_kwargs(self):
        registro = InventarioMateriales.objects.get(id = self.get_object().inventario_materiales_id)
        sede = registro.sede.id
        almacenes = Almacen.objects.filter(sede__id = sede)

        kwargs = super().get_form_kwargs()
        kwargs['almacenes'] = almacenes
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(InventarioMaterialesDetalleUpdateView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        context['titulo'] = "Material"
        return context


class InventarioMaterialesDetalleDeleteView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('logistica.delete_inventariomaterialdetalle')
    model = InventarioMaterialesDetalle
    template_name = "includes/eliminar generico.html"

    def get_success_url(self, **kwargs):
        return reverse_lazy('logistica_app:inventario_materiales_detalle', kwargs={'pk': self.get_object().inventario_materiales_id})

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            materiales = InventarioMaterialesDetalle.objects.filter(inventario_materiales=self.get_object().inventario_materiales)
            contador = 1
            for material in materiales:
                if material == self.get_object(): continue
                material.item = contador
                material.save()
                contador += 1
            return super().delete(request, *args, **kwargs)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(InventarioMaterialesDetalleDeleteView, self).get_context_data(**kwargs)
        context['accion'] = "Eliminar"
        context['titulo'] = "Material"
        context['item'] = self.get_object()
        context['dar_baja'] = "true"
        return context


class AjusteInventarioMaterialesListView(PermissionRequiredMixin, ListView):
    permission_required = ('logistica.view_ajusteinventariomateriales')
    model = AjusteInventarioMateriales
    template_name = "logistica/ajuste_inventario_materiales/inicio.html"
    context_object_name = 'contexto_ajuste_inventario_materiales'

def AjusteInventarioMaterialesTabla(request):
    data = dict()
    if request.method == 'GET':
        template = 'logistica/ajuste_inventario_materiales/inicio_tabla.html'
        context = {}
        context['contexto_ajuste_inventario_materiales'] = AjusteInventarioMateriales.objects.all()

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)


class AjusteInventarioMaterialesUpdateView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('logistica.change_ajusteinventariomateriales')
    model = AjusteInventarioMateriales
    template_name = "includes/formulario generico.html"
    form_class = AjusteInventarioMaterialesForm
    success_url = reverse_lazy('logistica_app:ajuste_inventario_materiales_inicio')

    def get_context_data(self, **kwargs):
        context = super(AjusteInventarioMaterialesUpdateView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        context['titulo'] = "Ajuste Inventario"
        return context

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)
        
        return super().form_valid(form)


class AjusteInventarioMaterialesConcluirView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('logistica.change_ajusteinventariomateriales')
    model = AjusteInventarioMateriales
    template_name = "logistica/ajuste_inventario_materiales/boton.html"
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('logistica_app:ajuste_inventario_materiales_inicio')

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            self.request.session['primero'] = True
            self.object = self.get_object()
            self.request.session['primero'] = False
            registro_guardar(self.object, self.request)
         
            tipo_stock_disponible = TipoStock.objects.get(codigo=3) # Disponible

            for detalle in self.object.AjusteInventarioMaterialesDetalle_ajuste_inventario_materiales.all():
                cantidad = detalle.cantidad_stock - detalle.cantidad_contada
                if cantidad > 0:
                    # AJUSTE POR INVENTARIO DISMINUIR STOCK
                    if detalle.material.control_serie and tipo_stock_disponible == detalle.tipo_stock:
                        movimiento_final = TipoMovimiento.objects.get(codigo=154) # Correcion por Inventario, disminuir stock, c/Serie
                    else:
                        movimiento_final = TipoMovimiento.objects.get(codigo=153) # Correcion por Inventario, disminuir stock, s/Serie
                    tipo_stock_inicial = detalle.tipo_stock
                    tipo_stock_final = movimiento_final.tipo_stock_final
                    signo_factor_multiplicador = -1
                else:
                    # AJUSTE POR INVENTARIO AUMENTAR STOCK
                    if detalle.material.control_serie and tipo_stock_disponible == detalle.tipo_stock:
                        movimiento_final = TipoMovimiento.objects.get(codigo=157) # Correccion Inventario con Series, aumentar stock
                        tipo_stock_final = movimiento_final.tipo_stock_final
                    else:
                        movimiento_final = TipoMovimiento.objects.get(codigo=156) #	Correcion por Inventario, aumentar stock, s/Serie
                        tipo_stock_final = detalle.tipo_stock
                    tipo_stock_inicial = movimiento_final.tipo_stock_inicial
                    signo_factor_multiplicador = +1

                movimiento_uno = MovimientosAlmacen.objects.create(
                    content_type_producto = detalle.material.content_type,
                    id_registro_producto = detalle.material.id,
                    cantidad = cantidad,
                    tipo_movimiento = movimiento_final,
                    tipo_stock = tipo_stock_inicial,
                    signo_factor_multiplicador = signo_factor_multiplicador,
                    content_type_documento_proceso = detalle.ajuste_inventario_materiales.content_type,
                    id_registro_documento_proceso = detalle.ajuste_inventario_materiales.id,
                    almacen = detalle.almacen,
                    sociedad = detalle.ajuste_inventario_materiales.sociedad,
                    movimiento_anterior = None,
                    created_by = request.user,
                    updated_by = request.user,
                )
                movimiento_dos = MovimientosAlmacen.objects.create(
                    content_type_producto = detalle.material.content_type,
                    id_registro_producto = detalle.material.id,
                    cantidad = cantidad,
                    tipo_movimiento = movimiento_final,
                    tipo_stock = tipo_stock_final,
                    signo_factor_multiplicador = -1*signo_factor_multiplicador,
                    content_type_documento_proceso = detalle.ajuste_inventario_materiales.content_type,
                    id_registro_documento_proceso = detalle.ajuste_inventario_materiales.id,
                    almacen = detalle.almacen,
                    sociedad = detalle.ajuste_inventario_materiales.sociedad,
                    movimiento_anterior = movimiento_uno,
                    created_by = request.user,
                    updated_by = request.user,
                )            

            self.object.estado = 2  # Concluir
            self.object.save()
            messages.success(request, MENSAJE_AJUSTE_INVENTARIO_MATERIALES)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        self.request.session['primero'] = True
        context = super(AjusteInventarioMaterialesConcluirView, self).get_context_data(**kwargs)
        context['accion'] = "Concluir"
        context['titulo'] = "Ajuste Inventario Materiales"
        context['dar_baja'] = "true"
        return context


class AjusteInventarioMaterialesDetailView(PermissionRequiredMixin, DetailView):
    permission_required = ('logistica.view_ajusteinventariomaterial')

    model = AjusteInventarioMateriales
    template_name = "logistica/ajuste_inventario_materiales/detalle.html"
    context_object_name = 'contexto_ajuste_inventario_materiales_detalle'

    def get_context_data(self, **kwargs):
        ajuste_inventario_materiales = AjusteInventarioMateriales.objects.get(id = self.kwargs['pk'])
        context = super(AjusteInventarioMaterialesDetailView, self).get_context_data(**kwargs)
        context['ajuste_inventario_materiales_detalle'] = AjusteInventarioMaterialesDetalle.objects.filter(ajuste_inventario_materiales = ajuste_inventario_materiales)
        return context


def AjusteInventarioMaterialesDetailTabla(request, pk):
    data = dict()
    if request.method == 'GET':
        template = 'logistica/ajuste_inventario_materiales/detalle_tabla.html'
        context = {}
        ajuste_inventario_materiales = AjusteInventarioMateriales.objects.get(id = pk)
        context['contexto_ajuste_inventario_materiales_detalle'] = ajuste_inventario_materiales
        context['ajuste_inventario_materiales_detalle'] = AjusteInventarioMaterialesDetalle.objects.filter(ajuste_inventario_materiales = ajuste_inventario_materiales)
        
        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)


class AjusteInventarioMaterialesDetalleCreateView(PermissionRequiredMixin, BSModalFormView):
    permission_required = ('logistica.add_ajusteinventariomaterialdetalle')
    template_name = "includes/formulario generico.html"
    form_class = AjusteInventarioMaterialesDetalleForm

    def get_success_url(self, **kwargs):
        return reverse_lazy('logistica_app:ajuste_inventario_materiales_detalle', kwargs={'pk': self.kwargs['ajuste_inventario_materiales_id']})

    def get_form_kwargs(self):
        ajuste_inventario_materiales = AjusteInventarioMateriales.objects.get(id=self.kwargs['ajuste_inventario_materiales_id'])
        inventario_materiales = ajuste_inventario_materiales.inventario_materiales.id
        materiales = ajuste_inventario_materiales.AjusteInventarioMaterialesDetalle_ajuste_inventario_materiales.all()
        lista_materiales = InventarioMaterialesDetalle.objects.filter(inventario_materiales__id=inventario_materiales)
        for material in materiales:
            lista_materiales = lista_materiales.exclude(material_id=material.material.id)
        kwargs = super().get_form_kwargs()
        kwargs['materiales'] = lista_materiales
        return kwargs

    @transaction.atomic
    def form_valid(self, form):
        sid = transaction.savepoint()
        try:
            if self.request.session['primero']:
                ajuste_inventario_materiales = AjusteInventarioMateriales.objects.get(id=self.kwargs['ajuste_inventario_materiales_id'])
                item = len(ajuste_inventario_materiales.AjusteInventarioMaterialesDetalle_ajuste_inventario_materiales.all())
                material = form.cleaned_data.get('producto')
                sociedad = ajuste_inventario_materiales.sociedad

                ajuste_inventario_materiales_detalle = AjusteInventarioMaterialesDetalle.objects.create(
                    ajuste_inventario_materiales=ajuste_inventario_materiales,
                    material = material.material,
                    almacen = ajuste_inventario_materiales.inventario_materiales.InventarioMaterialesDetalle_inventario_materiales.get(material=material.material).almacen,
                    tipo_stock = ajuste_inventario_materiales.inventario_materiales.InventarioMaterialesDetalle_inventario_materiales.get(material=material.material).tipo_stock,
                    cantidad_stock = stock_tipo_stock(
                        material.material.content_type, 
                        material.material.id, 
                        sociedad.id,
                        ajuste_inventario_materiales.inventario_materiales.InventarioMaterialesDetalle_inventario_materiales.get(material=material.material).almacen.id, 
                        ajuste_inventario_materiales.inventario_materiales.InventarioMaterialesDetalle_inventario_materiales.get(material=material.material).tipo_stock.id),
                    cantidad_contada = ajuste_inventario_materiales.inventario_materiales.InventarioMaterialesDetalle_inventario_materiales.get(material=material.material).cantidad,
                    item=item + 1,
                    created_by=self.request.user,
                    updated_by=self.request.user, 
                )

                self.request.session['primero'] = False
            return super().form_valid(form)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        self.request.session['primero'] = True
        context = super(AjusteInventarioMaterialesDetalleCreateView, self).get_context_data(**kwargs)
        context['accion'] = "Registrar"
        context['titulo'] = "Material"
        return context


class AjusteInventarioMaterialesDetalleDeleteView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('logistica.delete_ajusteinventariomaterialdetalle')
    model = AjusteInventarioMaterialesDetalle
    template_name = "includes/eliminar generico.html"

    def get_success_url(self, **kwargs):
        return reverse_lazy('logistica_app:ajuste_inventario_materiales_detalle', kwargs={'pk': self.get_object().ajuste_inventario_materiales_id})

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            materiales = AjusteInventarioMaterialesDetalle.objects.filter(ajuste_inventario_materiales=self.get_object().ajuste_inventario_materiales)
            contador = 1
            for material in materiales:
                if material == self.get_object(): continue
                material.item = contador
                material.save()
                contador += 1
            return super().delete(request, *args, **kwargs)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(AjusteInventarioMaterialesDetalleDeleteView, self).get_context_data(**kwargs)
        context['accion'] = "Eliminar"
        context['titulo'] = "Material"
        context['item'] = self.get_object()
        context['dar_baja'] = "true"
        return context