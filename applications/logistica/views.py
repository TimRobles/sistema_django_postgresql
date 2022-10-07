from os import listxattr
from django.shortcuts import render
from django import forms
from decimal import Decimal
from applications.importaciones import *
from applications.logistica.models import Despacho, DocumentoPrestamoMateriales, SolicitudPrestamoMateriales, SolicitudPrestamoMaterialesDetalle, NotaSalida, NotaSalidaDetalle
from applications.logistica.forms import DocumentoPrestamoMaterialesForm, SolicitudPrestamoMaterialesDetalleForm, SolicitudPrestamoMaterialesDetalleUpdateForm, SolicitudPrestamoMaterialesForm, NotaSalidaForm, SolicitudPrestamoMaterialesAnularForm
from applications.clientes.models import ClienteInterlocutor, InterlocutorCliente
from applications.logistica.pdf import generarSolicitudPrestamoMateriales
from applications.funciones import fecha_en_letras
from applications.sociedad.models import Sociedad

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
        context['accion']="Registrar"
        context['titulo']="Solicitud Prestamo Materiales"
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
        return reverse_lazy('logistica_app:solicitud_prestamo_materiales_inicio')

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
        context['item'] = self.object.numero_prestamo
        return context

class SolicitudPrestamoMaterialesConfirmarView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('logistica.delete_solicitudprestamomateriales')
    model = SolicitudPrestamoMateriales
    template_name = "logistica/solicitud_prestamo_materiales/boton.html"

    def get_success_url(self, **kwargs):
        return reverse_lazy('logistica_app:solicitud_prestamo_materiales_inicio')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.estado = 3
        registro_guardar(self.object, self.request)
        self.object.save()
        messages.success(request, MENSAJE_CONFIRMAR_SOLICITUD_PRESTAMO_MATERIALES)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(SolicitudPrestamoMaterialesConfirmarView, self).get_context_data(**kwargs)
        context['accion'] = "Confirmar"
        context['titulo'] = "Solicitud Prestamo Materiales"
        context['dar_baja'] = "true"
        context['item'] = self.object.numero_prestamo
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
        return reverse_lazy('logistica_app:solicitud_prestamo_materiales_inicio')

    def form_valid(self, form):
        form.instance.estado = 4
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(SolicitudPrestamoMaterialesAnularView, self).get_context_data(**kwargs)
        context['accion']="Anular"
        context['titulo']="Solicitud Prestamo Materiales"
        return context

class SolicitudPrestamoMaterialesDetailView(PermissionRequiredMixin, DetailView):
    permission_required = ('logistica.view_solicitudprestamomateriales')

    model = SolicitudPrestamoMateriales
    template_name = "logistica/solicitud_prestamo_materiales/detalle.html"
    context_object_name = 'contexto_solicitud_prestamo_materiales_detalle'

    def get_context_data(self, **kwargs):
        obj = SolicitudPrestamoMateriales.objects.get(id = self.kwargs['pk'])
        context = super(SolicitudPrestamoMaterialesDetailView, self).get_context_data(**kwargs)

        materiales = None
        try:
            materiales = obj.SolicitudPrestamoMaterialesDetalle_solicitud_prestamo_materiales.all()
            for material in materiales:
                material.material = material.content_type.get_object_for_this_type(id = material.id_registro)
        except:
            pass

        context['materiales'] = materiales
        context['documentos'] = DocumentoPrestamoMateriales.objects.filter(solicitud_prestamo_materiales = obj)
        return context

def SolicitudPrestamoMaterialesDetailTabla(request, pk):
    data = dict()
    if request.method == 'GET':
        template = 'logistica/solicitud_prestamo_materiales/detalle_tabla.html'
        context = {}
        obj = SolicitudPrestamoMateriales.objects.get(id = pk)

        materiales = None
        try:
            materiales = obj.SolicitudPrestamoMaterialesDetalle_solicitud_prestamo_materiales.all()
            for material in materiales:
                material.material = material.content_type.get_object_for_this_type(id = material.id_registro)
        except:
            pass

        context['contexto_solicitud_prestamo_materiales_detalle'] = obj
        context['materiales'] = materiales
        context['documentos'] = DocumentoPrestamoMateriales.objects.filter(solicitud_prestamo_materiales = obj)

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
        return reverse_lazy('logistica_app:solicitud_prestamo_materiales_detalle', kwargs={'pk':self.kwargs['solicitud_prestamo_materiales_id']})

    def form_valid(self, form):
        if self.request.session['primero']:
            registro = SolicitudPrestamoMateriales.objects.get(id = self.kwargs['solicitud_prestamo_materiales_id'])
            item = len(SolicitudPrestamoMaterialesDetalle.objects.filter(solicitud_prestamo_materiales = registro))

            material = form.cleaned_data.get('material')
            cantidad_prestamo = form.cleaned_data.get('cantidad_prestamo')
            observacion = form.cleaned_data.get('observacion')

            obj, created = SolicitudPrestamoMaterialesDetalle.objects.get_or_create(
                content_type = ContentType.objects.get_for_model(material),
                id_registro = material.id,
                solicitud_prestamo_materiales = registro,
            )
            if created:
                obj.item = item + 1
                obj.cantidad_prestamo = cantidad_prestamo
                obj.observacion = observacion
            else:
                obj.cantidad_prestamo = obj.cantidad_prestamo + cantidad_prestamo
                obj.observacion = obj.observacion + ' | ' + observacion

            registro_guardar(obj, self.request)
            obj.save()
            self.request.session['primero'] = False
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        self.request.session['primero'] = True
        context = super(SolicitudPrestamoMaterialesDetalleCreateView, self).get_context_data(**kwargs)
        context['titulo'] = 'Material'
        context['accion'] = 'Agregar'
        return context

class SolicitudPrestamoMaterialesDetalleImprimirView(View):
    def get(self, request, *args, **kwargs):
        color = COLOR_DEFAULT
        titulo = 'SOLICITUD DE PRÉSTAMO DE EQUIPOS'
        vertical = False
        logo = None
        pie_pagina = PIE_DE_PAGINA_DEFAULT

        obj = SolicitudPrestamoMateriales.objects.get(id=self.kwargs['pk'])

        titulo = str(titulo)

        Cabecera = {}
        Cabecera['numero_prestamo'] = str(obj.numero_prestamo)
        Cabecera['fecha_prestamo'] = fecha_en_letras(obj.fecha_prestamo)
        Cabecera['razon_social'] = str(obj.cliente)
        Cabecera['tipo_documento'] = DICCIONARIO_TIPO_DOCUMENTO_SUNAT[obj.cliente.tipo_documento]
        Cabecera['nro_documento'] = str(obj.cliente.numero_documento)
        Cabecera['direccion'] = str(obj.cliente.direccion_fiscal)
        Cabecera['interlocutor'] = str(obj.interlocutor_cliente)

        TablaEncabezado = [ 'Item',
                            'Descripción',
                            'Unidad',
                            'Cantidad',
                            ]

        detalle = obj.SolicitudPrestamoMaterialesDetalle_solicitud_prestamo_materiales
        solicitud_prestamo_materiales = detalle.all()

        TablaDatos = []
        count = 1
        for solicitud in solicitud_prestamo_materiales:
            fila = []
            # confirmacion_detalle = detalle.CotizacionSociedad_cotizacion_venta_detalle.get(sociedad=sociedad)
            solicitud.material = solicitud.content_type.get_object_for_this_type(id = solicitud.id_registro)
            fila.append(solicitud.item)
            fila.append(intcomma(solicitud.material))
            fila.append(intcomma(solicitud.material.unidad_base))
            fila.append(intcomma(solicitud.cantidad_prestamo.quantize(Decimal('0.01'))))

            TablaDatos.append(fila)
            count += 1

        buf = generarSolicitudPrestamoMateriales(titulo, vertical, logo, pie_pagina, Cabecera, TablaEncabezado, TablaDatos, color)

        respuesta = HttpResponse(buf.getvalue(), content_type='application/pdf')
        respuesta.headers['content-disposition']='inline; filename=%s.pdf' % titulo

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
        context['accion']="Actualizar"
        context['titulo']="material"
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
        return reverse_lazy('logistica_app:solicitud_prestamo_materiales_detalle', kwargs={'pk':self.get_object().solicitud_prestamo_materiales.id})

    def delete(self, request, *args, **kwargs):

        return super().delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(SolicitudPrestamoMaterialesDetalleDeleteView, self).get_context_data(**kwargs)
        context['accion'] = "Eliminar"
        context['titulo'] = "Material"
        context['item'] = self.get_object().item
        context['dar_baja'] = "true"
        return context

class DocumentoSolicitudPrestamoMaterialesCreateView(PermissionRequiredMixin, BSModalCreateView):
    permission_required = ('logistica.add_documentoprestamomateriales')
    model = DocumentoPrestamoMateriales
    template_name = "includes/formulario generico.html"
    form_class = DocumentoPrestamoMaterialesForm

    def get_success_url(self, **kwargs):
        return reverse_lazy('logistica_app:solicitud_prestamo_materiales_detalle', kwargs={'pk':self.kwargs['solicitud_prestamo_materiales_id']})

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.solicitud_prestamo_materiales = SolicitudPrestamoMateriales.objects.get(id = self.kwargs['solicitud_prestamo_materiales_id'])
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(DocumentoSolicitudPrestamoMaterialesCreateView, self).get_context_data(**kwargs)
        context['accion']="Agregar"
        context['titulo']="Documento"
        return context

class DocumentoSolicitudPrestamoMaterialesDeleteView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('activos.delete_documentoprestamomateriales')
    model = DocumentoPrestamoMateriales
    template_name = "includes/eliminar generico.html"

    def get_success_url(self, **kwargs):
        return reverse_lazy('logistica_app:solicitud_prestamo_materiales_detalle', kwargs={'pk':self.object.solicitud_prestamo_materiales.id})

    def get_context_data(self, **kwargs):
        context = super(DocumentoSolicitudPrestamoMaterialesDeleteView, self).get_context_data(**kwargs)
        context['accion']="Eliminar"
        context['titulo']="Documento"
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
                numero_salida = item + 1,
                solicitud_prestamo_materiales = prestamo,
                observacion_adicional = "",
                motivo_anulacion = "",
                created_by = self.request.user,
                updated_by = self.request.user,
            )

            # prestamo_detalle = prestamo.SolicitudPrestamoMaterialesDetalle_solicitud_prestamo_materiales.all()
            # for detalle in prestamo_detalle:
            #     nota_salida_detalle = NotaSalidaDetalle.objects.create(
            #         solicitud_prestamo_materiales_detalle = detalle,
            #         nota_salida = nota_salida,
            #         created_by = self.request.user,
            #         updated_by = self.request.user,
            #         )
            self.request.session['primero'] = False
        registro_guardar(self.object, self.request)
        self.object.save()
        messages.success(request, MENSAJE_GENERAR_NOTA_SALIDA)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        self.request.session['primero'] = True
        context = super(SolicitudPrestamoMaterialesGenerarNotaSalidaView, self).get_context_data(**kwargs)
        context['accion'] = "Generar"
        context['titulo'] = "Nota Salida"
        context['dar_baja'] = "true"
        return context

class ClienteForm(forms.Form):
    interlocutor_cliente = forms.ModelChoiceField(queryset = ClienteInterlocutor.objects.all(), required=False)

def ClienteView(request, id_interlocutor_cliente):
    form = ClienteForm()
    lista = []
    relaciones = ClienteInterlocutor.objects.filter(cliente = id_interlocutor_cliente)
    for relacion in relaciones:
        lista.append(relacion.interlocutor.id)
    form.fields['interlocutor_cliente'].queryset = InterlocutorCliente.objects.filter(id__in = lista)
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


class NotaSalidaListView(PermissionRequiredMixin, ListView):
    permission_required = ('logistica.view_notasalida')
    model = NotaSalida
    template_name = "logistica/nota_salida/inicio.html"
    context_object_name = 'contexto_nota_salida'

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

class NotaSalidaDetailView(PermissionRequiredMixin, DetailView):
    permission_required = ('logistica.view_notasalida')

    model = NotaSalida
    template_name = "logistica/nota_salida/detalle.html"
    context_object_name = 'contexto_nota_salida_detalle'

    def get_context_data(self, **kwargs):
        nota_salida = NotaSalida.objects.get(id = self.kwargs['pk'])
        context = super(NotaSalidaDetailView, self).get_context_data(**kwargs)
        return context

def NotaSalidaDetailTabla(request, pk):
    data = dict()
    if request.method == 'GET':
        template = 'logistica/nota_salida/detalle_tabla.html'
        context = {}
        nota_salida = NotaSalida.objects.get(id = pk)
        context['contexto_nota_salida_detalle'] = nota_salida

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)


class DespachoListView(ListView):
    model = Despacho
    template_name = 'logistica/despacho/inicio.html'
    context_object_name = 'contexto_despacho'

def DespachoTabla(request):
    data = dict()
    if request.method == 'GET':
        template = 'logistica/despacho/inicio_tabla.html'
        context = {}
        context['contexto_guia'] = Despacho.objects.all()

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)


class DespachoDetalleView(TemplateView):
    template_name = "logistica/despacho/detalle.html"

    def get_context_data(self, **kwargs):
        obj = Despacho.objects.get(id = kwargs['id_despacho'])

        context = super(DespachoDetalleView, self).get_context_data(**kwargs)
        context['despacho'] = obj
        context['depacho_detalle'] = obj.DespachoDetalle_despacho.all()

        return context

def DespachoDetalleVerTabla(request, id_despacho):
    data = dict()
    if request.method == 'GET':
        template = 'logistica/despacho/detalle_tabla.html'
        obj = Despacho.objects.get(id=id_despacho)

        context = {}
        context['despacho'] = obj
        context['depacho_detalle'] = obj.DespachoDetalle_despacho.all()

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)
