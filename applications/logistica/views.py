from django import forms
from decimal import Decimal
from applications.importaciones import *
from applications.comprobante_despacho.models import Guia, GuiaDetalle
from applications.logistica.models import Despacho, DespachoDetalle, DocumentoPrestamoMateriales, \
    SolicitudPrestamoMateriales, SolicitudPrestamoMaterialesDetalle, NotaSalida, NotaSalidaDetalle
from applications.logistica.forms import DespachoAnularForm, DespachoForm, DocumentoPrestamoMaterialesForm, \
    NotaSalidaAnularForm, NotaSalidaDetalleForm, NotaSalidaDetalleUpdateForm, SolicitudPrestamoMaterialesDetalleForm, \
    SolicitudPrestamoMaterialesDetalleUpdateForm, SolicitudPrestamoMaterialesForm, NotaSalidaForm, \
    SolicitudPrestamoMaterialesAnularForm
from applications.clientes.models import ClienteInterlocutor, InterlocutorCliente
from applications.logistica.pdf import generarSolicitudPrestamoMateriales
from applications.funciones import fecha_en_letras, numeroXn
from applications.almacenes.models import Almacen
from applications.datos_globales.models import SeriesComprobante
from applications.movimiento_almacen.models import MovimientosAlmacen, TipoMovimiento


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

    def get_success_url(self, **kwargs):
        return reverse_lazy('logistica_app:solicitud_prestamo_materiales_detalle', kwargs={'pk': self.get_object().id})

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.estado = 2
        registro_guardar(self.object, self.request)
        self.object.save()
        messages.success(request, MENSAJE_FINALIZAR_SOLICITUD_PRESTAMO_MATERIALES)
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

    def get_success_url(self, **kwargs):
        return reverse_lazy('logistica_app:solicitud_prestamo_materiales_detalle', kwargs={'pk': self.get_object().id})

    def delete(self, request, *args, **kwargs):
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

    def form_valid(self, form):
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
        return super().form_valid(form)

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
    permission_required = ('logistica.add_solicitudprestamomaterialdetalle')

    template_name = "logistica/solicitud_prestamo_materiales/form_material.html"
    form_class = SolicitudPrestamoMaterialesDetalleForm

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('logistica_app:solicitud_prestamo_materiales_detalle',
                            kwargs={'pk': self.kwargs['solicitud_prestamo_materiales_id']})

    def form_valid(self, form):
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
        pie_pagina = PIE_DE_PAGINA_DEFAULT

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

    def delete(self, request, *args, **kwargs):
        materiales = SolicitudPrestamoMaterialesDetalle.objects.filter(
            solicitud_prestamo_materiales=self.get_object().solicitud_prestamo_materiales)
        contador = 1
        for material in materiales:
            if material == self.get_object(): continue
            material.item = contador
            material.save()
            contador += 1
        return super().delete(request, *args, **kwargs)

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

    def get_success_url(self, **kwargs):
        return reverse_lazy('logistica_app:solicitud_prestamo_materiales_detalle',
                            kwargs={'pk': self.kwargs['solicitud_prestamo_materiales_id']})

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

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

    def delete(self, request, *args, **kwargs):
        if self.request.session['primero']:
            self.object = self.get_object()
            prestamo = self.get_object()
            item = len(NotaSalida.objects.all())
            nota_salida = NotaSalida.objects.create(
                numero_salida=item + 1,
                solicitud_prestamo_materiales=prestamo,
                observacion_adicional="",
                motivo_anulacion="",
                created_by=self.request.user,
                updated_by=self.request.user,
            )

            self.request.session['primero'] = False
            registro_guardar(self.object, self.request)
            self.object.save()
            messages.success(request, MENSAJE_GENERAR_NOTA_SALIDA)
            return HttpResponseRedirect(
                reverse_lazy('logistica_app:nota_salida_detalle', kwargs={'pk': nota_salida.id}))

    def get_context_data(self, **kwargs):
        self.request.session['primero'] = True
        context = super(SolicitudPrestamoMaterialesGenerarNotaSalidaView, self).get_context_data(**kwargs)
        context['accion'] = "Generar"
        context['titulo'] = "Nota Salida"
        context['dar_baja'] = "true"
        return context


class ClienteForm(forms.Form):
    interlocutor_cliente = forms.ModelChoiceField(queryset=ClienteInterlocutor.objects.all(), required=False)


def ClienteView(request, id_interlocutor_cliente):
    form = ClienteForm()
    lista = []
    relaciones = ClienteInterlocutor.objects.filter(cliente=id_interlocutor_cliente)
    for relacion in relaciones:
        lista.append(relacion.interlocutor.id)
    form.fields['interlocutor_cliente'].queryset = InterlocutorCliente.objects.filter(id__in=lista)
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


class NotaSalidaListView(PermissionRequiredMixin, ListView):
    permission_required = ('logistica.view_notasalida')
    model = NotaSalida
    template_name = "logistica/nota_salida/inicio.html"
    context_object_name = 'contexto_nota_salida'

    def get_queryset(self):
        queryset = super().get_queryset()
        if 'id_solicitud_prestamo' in self.kwargs:
            queryset = queryset.filter(
                solicitud_prestamo_materiales__id=self.kwargs['id_solicitud_prestamo'],
            )
        return queryset


def NotaSalidaTabla(request):
    data = dict()
    if request.method == 'GET':
        template = 'logistica/nota_salida/inicio_tabla.html'
        context = {}
        context['contexto_nota_salida'] = NotaSalida.objects.all()

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

    def get_context_data(self, **kwargs):
        context = super(NotaSalidaUpdateView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        context['titulo'] = "Nota de Salida"
        return context

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)


class NotaSalidaConcluirView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('logistica.delete_notasalida')
    model = NotaSalida
    template_name = "logistica/nota_salida/boton.html"

    def get_success_url(self, **kwargs):
        return reverse_lazy('logistica_app:nota_salida_detalle', kwargs={'pk': self.get_object().id})

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        if self.request.session['primero']:
            sid = transaction.savepoint()
            try:
                self.object = self.get_object()

                detalles = self.object.detalles
                if self.object.solicitud_prestamo_materiales:
                    movimiento_inicial = TipoMovimiento.objects.get(codigo=131)  # Confirmación por préstamo
                    movimiento_final = TipoMovimiento.objects.get(codigo=132)  # Salida por préstamo
                    documento_anterior = self.object.solicitud_prestamo_materiales
            
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
                        cantidad=detalle.cantidad_salida,
                        tipo_movimiento=movimiento_final,
                        tipo_stock=movimiento_final.tipo_stock_inicial,
                        signo_factor_multiplicador=-1,
                        content_type_documento_proceso=ContentType.objects.get_for_model(self.object),
                        id_registro_documento_proceso=self.object.id,
                        almacen=None,
                        sociedad=self.object.sociedad,
                        movimiento_anterior=movimiento_anterior,
                        movimiento_reversion=False,
                        created_by=self.request.user,
                        updated_by=self.request.user,
                    )

                    movimiento_dos = MovimientosAlmacen.objects.create(
                        content_type_producto=detalle.content_type,
                        id_registro_producto=detalle.id_registro,
                        cantidad=detalle.cantidad_salida,
                        tipo_movimiento=movimiento_final,
                        tipo_stock=movimiento_final.tipo_stock_final,
                        signo_factor_multiplicador=+1,
                        content_type_documento_proceso=ContentType.objects.get_for_model(self.object),
                        id_registro_documento_proceso=self.object.id,
                        almacen=detalle.almacen,
                        sociedad=self.object.sociedad,
                        movimiento_anterior=movimiento_uno,
                        movimiento_reversion=False,
                        created_by=self.request.user,
                        updated_by=self.request.user,
                    )
                

                self.object.estado = 2
                registro_guardar(self.object, self.request)
                self.object.save()

                messages.success(request, MENSAJE_CONCLUIR_NOTA_SALIDA)
            except Exception as ex:
                messages.warning(request, ex)
                transaction.savepoint_rollback(sid)
            self.request.session['primero'] = False
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

                for detalle in detalles:
                    movimiento_dos = MovimientosAlmacen.objects.get(
                        content_type_producto=detalle.content_type,
                        id_registro_producto=detalle.id_registro,
                        cantidad=detalle.cantidad_salida,
                        tipo_movimiento=movimiento_final,
                        tipo_stock=movimiento_final.tipo_stock_final,
                        signo_factor_multiplicador=+1,
                        content_type_documento_proceso=ContentType.objects.get_for_model(form.instance),
                        id_registro_documento_proceso=form.instance.id,
                        almacen=detalle.almacen,
                        sociedad=form.instance.sociedad,
                    )
                    movimiento_uno = movimiento_dos.movimiento_anterior

                    movimiento_dos.delete()
                    movimiento_uno.delete()
                a = int('Hola')
            except Exception as ex:
                transaction.savepoint_rollback(sid)
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                messages.warning(self.request, f"{fname} # {exc_tb.tb_lineno} {exc_type} {ex}")
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
        registro = NotaSalida.objects.get(id=self.kwargs['nota_salida_id'])
        solicitud = registro.solicitud_prestamo_materiales.id
        materiales = SolicitudPrestamoMaterialesDetalle.objects.filter(solicitud_prestamo_materiales__id=solicitud)
        lista_materiales = SolicitudPrestamoMaterialesDetalle.objects.filter(
            solicitud_prestamo_materiales__id=solicitud)
        for material in materiales:
            salida = material.NotaSalidaDetalle_solicitud_prestamo_materiales_detalle.exclude(nota_salida__estado=3).aggregate(Sum('cantidad_salida'))[
                'cantidad_salida__sum']
            if salida:
                if salida == material.cantidad_prestamo:
                    lista_materiales = lista_materiales.exclude(id=material.id)

        kwargs = super().get_form_kwargs()
        kwargs['materiales'] = lista_materiales
        return kwargs

    def form_valid(self, form):
        if self.request.session['primero']:
            registro = NotaSalida.objects.get(id=self.kwargs['nota_salida_id'])
            item = len(registro.NotaSalidaDetalle_nota_salida.all())
            material = form.cleaned_data.get('material')

            nota_salida_detalle = NotaSalidaDetalle.objects.create(
                solicitud_prestamo_materiales_detalle=material,
                nota_salida=registro,
                item=item + 1,
                created_by=self.request.user,
                updated_by=self.request.user,
            )

            self.request.session['primero'] = False
        return super().form_valid(form)

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
        material = self.object.solicitud_prestamo_materiales_detalle
        suma = material.NotaSalidaDetalle_solicitud_prestamo_materiales_detalle.exclude(nota_salida__estado=3).aggregate(Sum('cantidad_salida'))[
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

    def delete(self, request, *args, **kwargs):
        materiales = NotaSalidaDetalle.objects.filter(nota_salida=self.get_object().nota_salida)
        contador = 1
        for material in materiales:
            if material == self.get_object(): continue
            material.item = contador
            material.save()
            contador += 1
        return super().delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(NotaSalidaDetalleDeleteView, self).get_context_data(**kwargs)
        context['accion'] = "Eliminar"
        context['titulo'] = "Material"
        context['item'] = self.get_object()
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
    success_url = reverse_lazy('logistica_app:despacho_inicio')

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
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
            for detalle in nota_salida_detalle:
                id_registro = detalle.solicitud_prestamo_materiales_detalle.id_registro
                if id_registro not in lista_id_registro:
                    lista_id_registro.append(id_registro)
                    lista.append(detalle)
            item = 0
            for dato in lista:
                material = dato.solicitud_prestamo_materiales_detalle
                despacho_detalle = DespachoDetalle.objects.create(
                    item=item + 1,
                    content_type=dato.solicitud_prestamo_materiales_detalle.content_type,
                    id_registro=dato.solicitud_prestamo_materiales_detalle.id_registro,
                    cantidad_despachada=
                    material.NotaSalidaDetalle_solicitud_prestamo_materiales_detalle.exclude(nota_salida__estado=3).aggregate(Sum('cantidad_salida'))[
                        'cantidad_salida__sum'],
                    despacho=despacho,
                    created_by=self.request.user,
                    updated_by=self.request.user,
                )
                item += 1
            self.request.session['primero'] = False
        registro_guardar(self.object, self.request)
        self.object.save()
        messages.success(request, MENSAJE_GENERAR_DESPACHO)
        return HttpResponseRedirect(reverse_lazy('logistica_app:despacho_detalle', kwargs={'pk': despacho.id}))

    def get_context_data(self, **kwargs):
        self.request.session['primero'] = True
        context = super(NotaSalidaGenerarDespachoView, self).get_context_data(**kwargs)
        context['accion'] = "Generar"
        context['titulo'] = "Despacho"
        context['dar_baja'] = "true"
        return context


class DespachoListView(PermissionRequiredMixin, ListView):
    permission_required = ('logistica.view_despacho')
    model = Despacho
    template_name = 'logistica/despacho/inicio.html'
    context_object_name = 'contexto_despacho'

    def get_queryset(self):
        queryset = super().get_queryset()
        if 'id_nota_salida' in self.kwargs:
            queryset = queryset.filter(nota_salida__id=self.kwargs['id_nota_salida'])
        return queryset


def DespachoTabla(request):
    data = dict()
    if request.method == 'GET':
        template = 'logistica/despacho/inicio_tabla.html'
        context = {}
        context['contexto_despacho'] = Despacho.objects.all()

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

    def get_context_data(self, **kwargs):
        self.request.session['primero'] = True
        context = super(DespachoUpdateView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        context['titulo'] = "Despacho"
        return context

    def form_valid(self, form):
        if self.request.session['primero']:
            registro_guardar(form.instance, self.request)
            self.request.session['primero'] = False
        return super().form_valid(form)


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
        return super(DespachoConcluirView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('logistica_app:despacho_detalle', kwargs={'pk': self.get_object().id})

    def delete(self, request, *args, **kwargs):
        if self.request.session['primero']:
            self.object = self.get_object()

            detalles = self.object.detalles
            movimiento_inicial = TipoMovimiento.objects.get(codigo=132)  # Salida por préstamo
            movimiento_final = TipoMovimiento.objects.get(codigo=133)  # Despacho por préstamo

            for detalle in detalles:
                movimiento_uno = MovimientosAlmacen.objects.create(
                    content_type_producto=detalle.content_type,
                    id_registro_producto=detalle.id_registro,
                    cantidad=detalle.cantidad_despachada,
                    tipo_movimiento=movimiento_final,
                    tipo_stock=movimiento_final.tipo_stock_inicial,
                    signo_factor_multiplicador=-1,
                    content_type_documento_proceso=ContentType.objects.get_for_model(self.object),
                    id_registro_documento_proceso=self.object.id,
                    almacen=None,
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
                    almacen=None,
                    sociedad=self.object.sociedad,
                    movimiento_anterior=movimiento_uno,
                    movimiento_reversion=False,
                    created_by=self.request.user,
                    updated_by=self.request.user,
                )

            self.object.estado = 2
            registro_guardar(self.object, self.request)
            self.object.save()
            messages.success(request, MENSAJE_CONCLUIR_DESPACHO)
            self.request.session['primero'] = False
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

    def get_success_url(self, **kwargs):
        return reverse_lazy('logistica_app:despacho_detalle', kwargs={'pk': self.get_object().id})

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.estado = 4
        registro_guardar(self.object, self.request)
        self.object.save()
        messages.success(request, MENSAJE_FINALIZAR_SIN_GUIA_DESPACHO)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(DespachoFinalizarSinGuiaView, self).get_context_data(**kwargs)
        context['accion'] = "Finalizar"
        context['titulo'] = "Despacho sin Guia"
        context['dar_baja'] = "true"
        context['item'] = self.object.numero_despacho
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

    def form_valid(self, form):
        if self.request.session['primero']:
            form.instance.estado = 3
            registro_guardar(form.instance, self.request)

            detalles = form.instance.detalles
            movimiento_final = TipoMovimiento.objects.get(codigo=133)  # Despacho por préstamo

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
            self.request.session['primero'] = False
        return super().form_valid(form)

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

        return context


def DespachoDetailTabla(request, pk):
    data = dict()
    if request.method == 'GET':
        template = 'logistica/despacho/detalle_tabla.html'
        context = {}
        despacho = Despacho.objects.get(id=pk)
        context['contexto_despacho_detalle'] = despacho
        context['materiales'] = DespachoDetalle.objects.filter(despacho=despacho)

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
    success_url = reverse_lazy('comprobante_despacho_app:guia_inicio')

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        detalles = self.object.DespachoDetalle_despacho.all()
        serie_comprobante = SeriesComprobante.objects.por_defecto(ContentType.objects.get_for_model(Guia))

        guia = Guia.objects.create(
            sociedad=self.object.sociedad,
            serie_comprobante=serie_comprobante,
            cliente=self.object.cliente,
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
            self.request.session['primero'] = False
        registro_guardar(self.object, self.request)
        self.object.estado = 5
        self.object.save()
        messages.success(request, MENSAJE_GENERAR_GUIA)
        return HttpResponseRedirect(reverse_lazy('comprobante_despacho_app:guia_detalle', kwargs={'id_guia': guia.id}))

    def get_context_data(self, **kwargs):
        self.request.session['primero'] = True
        context = super(DespachoGenerarGuiaView, self).get_context_data(**kwargs)
        context['accion'] = "Generar"
        context['titulo'] = "Guía"
        context['dar_baja'] = "true"
        return context
