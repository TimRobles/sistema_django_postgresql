from os import listxattr
from django.shortcuts import render
from django import forms
from decimal import Decimal
from applications.importaciones import *
from applications.comprobante_despacho.models import Guia, GuiaDetalle
from applications.logistica.models import Despacho, DespachoDetalle, DocumentoPrestamoMateriales, SolicitudPrestamoMateriales, SolicitudPrestamoMaterialesDetalle, NotaSalida, NotaSalidaDetalle
from applications.logistica.forms import DespachoAnularForm, DespachoForm, DocumentoPrestamoMaterialesForm, NotaSalidaAnularForm, NotaSalidaDetalleForm, NotaSalidaDetalleUpdateForm, SolicitudPrestamoMaterialesDetalleForm, SolicitudPrestamoMaterialesDetalleUpdateForm, SolicitudPrestamoMaterialesForm, NotaSalidaForm, SolicitudPrestamoMaterialesAnularForm
from applications.clientes.models import ClienteInterlocutor, InterlocutorCliente
from applications.logistica.pdf import generarSolicitudPrestamoMateriales
from applications.funciones import fecha_en_letras
from applications.almacenes.models import Almacen
from applications.datos_globales.models import SeriesComprobante

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
        materiales = SolicitudPrestamoMaterialesDetalle.objects.filter(solicitud_prestamo_materiales=self.get_object().solicitud_prestamo_materiales)
        contador = 1
        for material in materiales:
            if material == self.get_object():continue
            material.item = contador
            material.save()
            contador += 1
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

class NotaSalidaConcluirView(PermissionRequiredMixin, BSModalDeleteView): #.....XxRonnyxX
    permission_required = ('logistica.delete_notasalida') #.....XxRonnyxX
    model = NotaSalida #.....XxRonnyxX
    template_name = "logistica/nota_salida/boton.html" #.....XxRonnyxX
 #.....XxRonnyxX
    def get_success_url(self, **kwargs): #.....XxRonnyxX
        return reverse_lazy('logistica_app:nota_salida_inicio') #.....XxRonnyxX
 #.....XxRonnyxX
    def delete(self, request, *args, **kwargs): #.....XxRonnyxX
        self.object = self.get_object() #.....XxRonnyxX
        self.object.estado = 2 #.....XxRonnyxX
        registro_guardar(self.object, self.request) #.....XxRonnyxX
        self.object.save() #.....XxRonnyxX
        messages.success(request, MENSAJE_CONCLUIR_NOTA_SALIDA) #.....XxRonnyxX
        return HttpResponseRedirect(self.get_success_url()) #.....XxRonnyxX
 #.....XxRonnyxX
    def get_context_data(self, **kwargs): #.....XxRonnyxX
        context = super(NotaSalidaConcluirView, self).get_context_data(**kwargs) #.....XxRonnyxX
        context['accion'] = "Concluir" #.....XxRonnyxX
        context['titulo'] = "Nota de Salida" #.....XxRonnyxX
        context['dar_baja'] = "true" #.....XxRonnyxX
        context['item'] = self.object.numero_salida #.....XxRonnyxX
        return context #.....XxRonnyxX
 #.....XxRonnyxX
class NotaSalidaAnularView(PermissionRequiredMixin, BSModalUpdateView): #.....XxRonnyxX
    permission_required = ('logistica.delete_notasalida') #.....XxRonnyxX
    model = NotaSalida #.....XxRonnyxX
    template_name = "includes/formulario generico.html" #.....XxRonnyxX
    form_class = NotaSalidaAnularForm #.....XxRonnyxX
 #.....XxRonnyxX
    def dispatch(self, request, *args, **kwargs): #.....XxRonnyxX
        if not self.has_permission(): #.....XxRonnyxX
            return render(request, 'includes/modal sin permiso.html') #.....XxRonnyxX
        return super().dispatch(request, *args, **kwargs) #.....XxRonnyxX
 #.....XxRonnyxX
    def get_success_url(self, **kwargs): #.....XxRonnyxX
        return reverse_lazy('logistica_app:nota_salida_inicio') #.....XxRonnyxX
 #.....XxRonnyxX
    def form_valid(self, form): #.....XxRonnyxX
        form.instance.estado = 3 #.....XxRonnyxX
        registro_guardar(form.instance, self.request) #.....XxRonnyxX
        return super().form_valid(form) #.....XxRonnyxX
 #.....XxRonnyxX
    def get_context_data(self, **kwargs): #.....XxRonnyxX
        context = super(NotaSalidaAnularView, self).get_context_data(**kwargs) #.....XxRonnyxX
        context['accion']="Anular" #.....XxRonnyxX
        context['titulo']="Nota de Salida" #.....XxRonnyxX
        return context #.....XxRonnyxX
 #.....XxRonnyxX
class NotaSalidaDetailView(PermissionRequiredMixin, DetailView): #.....XxRonnyxX
    permission_required = ('logistica.view_notasalida') #.....XxRonnyxX
 #.....XxRonnyxX
    model = NotaSalida #.....XxRonnyxX
    template_name = "logistica/nota_salida/detalle.html" #.....XxRonnyxX
    context_object_name = 'contexto_nota_salida_detalle' #.....XxRonnyxX
 #.....XxRonnyxX
    def get_context_data(self, **kwargs): #.....XxRonnyxX
        context = super(NotaSalidaDetailView, self).get_context_data(**kwargs) #.....XxRonnyxX
        context['materiales'] = self.object.NotaSalidaDetalle_nota_salida.all() #.....XxRonnyxX
 #.....XxRonnyxX
        return context #.....XxRonnyxX
 #.....XxRonnyxX
def NotaSalidaDetailTabla(request, pk): #.....XxRonnyxX
    data = dict() #.....XxRonnyxX
    if request.method == 'GET': #.....XxRonnyxX
        template = 'logistica/nota_salida/detalle_tabla.html' #.....XxRonnyxX
        context = {} #.....XxRonnyxX
        nota_salida = NotaSalida.objects.get(id = pk) #.....XxRonnyxX
        context['contexto_nota_salida_detalle'] = nota_salida #.....XxRonnyxX
        context['materiales'] = NotaSalidaDetalle.objects.filter(nota_salida = nota_salida) #.....XxRonnyxX
 #.....XxRonnyxX
        data['table'] = render_to_string( #.....XxRonnyxX
            template, #.....XxRonnyxX
            context, #.....XxRonnyxX
            request=request #.....XxRonnyxX
        ) #.....XxRonnyxX
        return JsonResponse(data) #.....XxRonnyxX
 #.....XxRonnyxX        
class NotaSalidaDetalleCreateView(PermissionRequiredMixin,BSModalFormView): #.....XxRonnyxX
    permission_required = ('logistica.add_notasalidadetalle') #.....XxRonnyxX
    template_name = "includes/formulario generico.html" #.....XxRonnyxX
    form_class = NotaSalidaDetalleForm #.....XxRonnyxX
 #.....XxRonnyxX
    def dispatch(self, request, *args, **kwargs): #.....XxRonnyxX
        if not self.has_permission(): #.....XxRonnyxX
            return render(request, 'includes/modal sin permiso.html') #.....XxRonnyxX
        return super().dispatch(request, *args, **kwargs) #.....XxRonnyxX
 #.....XxRonnyxX
    def get_success_url(self, **kwargs): #.....XxRonnyxX
        return reverse_lazy('logistica_app:nota_salida_detalle', kwargs={'pk':self.kwargs['nota_salida_id']}) #.....XxRonnyxX
 #.....XxRonnyxX
    def get_form_kwargs(self): #.....XxRonnyxX
        registro = NotaSalida.objects.get(id = self.kwargs['nota_salida_id']) #.....XxRonnyxX
        solicitud = registro.solicitud_prestamo_materiales.id #.....XxRonnyxX
        materiales = SolicitudPrestamoMaterialesDetalle.objects.filter(solicitud_prestamo_materiales__id = solicitud) #.....XxRonnyxX
        lista_materiales = SolicitudPrestamoMaterialesDetalle.objects.filter(solicitud_prestamo_materiales__id = solicitud) #.....XxRonnyxX
        for material in materiales: #.....XxRonnyxX
            salida = material.NotaSalidaDetalle_solicitud_prestamo_materiales_detalle.aggregate(Sum('cantidad_salida'))['cantidad_salida__sum'] #.....XxRonnyxX
            if salida: #.....XxRonnyxX
                if salida == material.cantidad_prestamo: #.....XxRonnyxX
                    lista_materiales = lista_materiales.exclude(id=material.id) #.....XxRonnyxX
 #.....XxRonnyxX
        kwargs = super().get_form_kwargs() #.....XxRonnyxX
        kwargs['materiales'] = lista_materiales #.....XxRonnyxX
        return kwargs #.....XxRonnyxX
 #.....XxRonnyxX
    def form_valid(self, form): #.....XxRonnyxX
        if self.request.session['primero']: #.....XxRonnyxX
            registro = NotaSalida.objects.get(id = self.kwargs['nota_salida_id']) #.....XxRonnyxX
            item = len(registro.NotaSalidaDetalle_nota_salida.all()) #.....XxRonnyxX
            material = form.cleaned_data.get('material') #.....XxRonnyxX
 #.....XxRonnyxX
            nota_salida_detalle = NotaSalidaDetalle.objects.create( #.....XxRonnyxX
                solicitud_prestamo_materiales_detalle = material, #.....XxRonnyxX
                nota_salida = registro, #.....XxRonnyxX
                item = item + 1, #.....XxRonnyxX
                created_by = self.request.user, #.....XxRonnyxX
                updated_by = self.request.user, #.....XxRonnyxX
            ) #.....XxRonnyxX
 #.....XxRonnyxX
            self.request.session['primero'] = False #.....XxRonnyxX
        return super().form_valid(form) #.....XxRonnyxX
 #.....XxRonnyxX
    def get_context_data(self, **kwargs): #.....XxRonnyxX
        self.request.session['primero'] = True #.....XxRonnyxX
        context = super(NotaSalidaDetalleCreateView, self).get_context_data(**kwargs) #.....XxRonnyxX
        context['accion']="Registrar" #.....XxRonnyxX
        context['titulo']="Material" #.....XxRonnyxX
        return context #.....XxRonnyxX
 #.....XxRonnyxX
class NotaSalidaDetalleUpdateView(PermissionRequiredMixin, BSModalUpdateView): #.....XxRonnyxX
    permission_required = ('logistica.change_notasalidadetalle') #.....XxRonnyxX
    model = NotaSalidaDetalle #.....XxRonnyxX
    template_name = "logistica/nota_salida/form_almacen.html" #.....XxRonnyxX
    form_class = NotaSalidaDetalleUpdateForm #.....XxRonnyxX
 #.....XxRonnyxX
    def dispatch(self, request, *args, **kwargs): #.....XxRonnyxX
        if not self.has_permission(): #.....XxRonnyxX
            return render(request, 'includes/modal sin permiso.html') #.....XxRonnyxX
        return super().dispatch(request, *args, **kwargs) #.....XxRonnyxX
 #.....XxRonnyxX
    def get_success_url(self, **kwargs): #.....XxRonnyxX
        return reverse_lazy('logistica_app:nota_salida_detalle', kwargs={'pk':self.object.nota_salida.id}) #.....XxRonnyxX
 #.....XxRonnyxX
    def get_form_kwargs(self, *args, **kwargs): #.....XxRonnyxX
        material = self.object.solicitud_prestamo_materiales_detalle #.....XxRonnyxX
        suma = material.NotaSalidaDetalle_solicitud_prestamo_materiales_detalle.aggregate(Sum('cantidad_salida'))['cantidad_salida__sum'] #.....XxRonnyxX
        cantidad_salida = self.object.cantidad_salida #.....XxRonnyxX
        kwargs = super(NotaSalidaDetalleUpdateView, self).get_form_kwargs(*args, **kwargs) #.....XxRonnyxX
        kwargs['solicitud'] = material #.....XxRonnyxX
        kwargs['suma'] = suma - cantidad_salida #.....XxRonnyxX
        return kwargs #.....XxRonnyxX
 #.....XxRonnyxX
    def form_valid(self, form): #.....XxRonnyxX
        registro_guardar(form.instance, self.request) #.....XxRonnyxX
        return super().form_valid(form) #.....XxRonnyxX
 #.....XxRonnyxX
    def get_context_data(self, **kwargs): #.....XxRonnyxX
        context = super(NotaSalidaDetalleUpdateView, self).get_context_data(**kwargs) #.....XxRonnyxX
        context['accion']="Actualizar" #.....XxRonnyxX
        context['titulo']="Material" #.....XxRonnyxX
        return context #.....XxRonnyxX
 #.....XxRonnyxX
class NotaSalidaDetalleDeleteView(PermissionRequiredMixin, BSModalDeleteView): #.....XxRonnyxX
    permission_required = ('logistica.delete_notasalidadetalle') #.....XxRonnyxX
    model = NotaSalidaDetalle #.....XxRonnyxX
    template_name = "includes/eliminar generico.html" #.....XxRonnyxX
 #.....XxRonnyxX
    def dispatch(self, request, *args, **kwargs): #.....XxRonnyxX
        if not self.has_permission(): #.....XxRonnyxX
            return render(request, 'includes/modal sin permiso.html') #.....XxRonnyxX
        return super().dispatch(request, *args, **kwargs) #.....XxRonnyxX
 #.....XxRonnyxX
    def get_success_url(self, **kwargs): #.....XxRonnyxX
        return reverse_lazy('logistica_app:nota_salida_detalle', kwargs={'pk':self.get_object().nota_salida.id}) #.....XxRonnyxX
 #.....XxRonnyxX
    def delete(self, request, *args, **kwargs): #.....XxRonnyxX
        materiales = NotaSalidaDetalle.objects.filter(nota_salida=self.get_object().nota_salida) #.....XxRonnyxX
        contador = 1 #.....XxRonnyxX
        for material in materiales: #.....XxRonnyxX
            if material == self.get_object():continue #.....XxRonnyxX
            material.item = contador #.....XxRonnyxX
            material.save() #.....XxRonnyxX
            contador += 1 #.....XxRonnyxX
        return super().delete(request, *args, **kwargs) #.....XxRonnyxX 
 #.....XxRonnyxX
    def get_context_data(self, **kwargs): #.....XxRonnyxX
        context = super(NotaSalidaDetalleDeleteView, self).get_context_data(**kwargs) #.....XxRonnyxX
        context['accion'] = "Eliminar" #.....XxRonnyxX
        context['titulo'] = "Material" #.....XxRonnyxX
        context['item'] = self.get_object().solicitud_prestamo_materiales_detalle #.....XxRonnyxX
        context['dar_baja'] = "true" #.....XxRonnyxX
        return context #.....XxRonnyxX
 #.....XxRonnyxX
class AlmacenForm(forms.Form): #.....XxRonnyxX
    almacen = forms.ModelChoiceField(queryset = Almacen.objects.all(), required=False) #.....XxRonnyxX
 #.....XxRonnyxX
def AlmacenView(request, id_sede): #.....XxRonnyxX
    form = AlmacenForm() #.....XxRonnyxX
    form.fields['almacen'].queryset = Almacen.objects.filter(sede = id_sede) #.....XxRonnyxX
 #.....XxRonnyxX
    data = dict() #.....XxRonnyxX
    if request.method == 'GET': #.....XxRonnyxX
        template = 'includes/form.html' #.....XxRonnyxX
        context = {'form':form} #.....XxRonnyxX
 #.....XxRonnyxX
        data['info'] = render_to_string( #.....XxRonnyxX
            template, #.....XxRonnyxX
            context, #.....XxRonnyxX
            request=request #.....XxRonnyxX
        ).replace('selected', 'selected=""') #.....XxRonnyxX
        return JsonResponse(data) #.....XxRonnyxX
 #.....XxRonnyxX
class NotaSalidaGenerarDespachoView(PermissionRequiredMixin, BSModalDeleteView): #.....XxRonnyxX
    permission_required = ('logistica.change_notasalidadetalle') #.....XxRonnyxX
 #.....XxRonnyxX
    model = NotaSalida #.....XxRonnyxX
    template_name = "logistica/nota_salida/boton.html" #.....XxRonnyxX
    success_url = reverse_lazy('logistica_app:despacho_inicio') #.....XxRonnyxX
 #.....XxRonnyxX
    def dispatch(self, request, *args, **kwargs): #.....XxRonnyxX
        if not self.has_permission(): #.....XxRonnyxX
            return render(request, 'includes/modal sin permiso.html') #.....XxRonnyxX
        return super().dispatch(request, *args, **kwargs) #.....XxRonnyxX
 #.....XxRonnyxX
    def delete(self, request, *args, **kwargs): #.....XxRonnyxX
        if self.request.session['primero']: #.....XxRonnyxX
            self.object = self.get_object() #.....XxRonnyxX
            nota_salida = self.get_object() #.....XxRonnyxX
            item = len(Despacho.objects.all()) #.....XxRonnyxX
            despacho = Despacho.objects.create( #.....XxRonnyxX
                sociedad = nota_salida.solicitud_prestamo_materiales.sociedad, #.....XxRonnyxX
                nota_salida = nota_salida, #.....XxRonnyxX
                numero_despacho = item + 1, #.....XxRonnyxX
                cliente = nota_salida.solicitud_prestamo_materiales.cliente, #.....XxRonnyxX
                created_by = self.request.user, #.....XxRonnyxX
                updated_by = self.request.user, #.....XxRonnyxX
            ) #.....XxRonnyxX
 #.....XxRonnyxX
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
                    item = item + 1,
                    content_type = dato.solicitud_prestamo_materiales_detalle.content_type,
                    id_registro = dato.solicitud_prestamo_materiales_detalle.id_registro,
                    cantidad_despachada = material.NotaSalidaDetalle_solicitud_prestamo_materiales_detalle.aggregate(Sum('cantidad_salida'))['cantidad_salida__sum'],
                    despacho = despacho,
                    created_by = self.request.user,
                    updated_by = self.request.user,
                    )
                item += 1
            self.request.session['primero'] = False #.....XxRonnyxX
        registro_guardar(self.object, self.request) #.....XxRonnyxX
        self.object.save() #.....XxRonnyxX
        messages.success(request, MENSAJE_GENERAR_DESPACHO) #.....XxRonnyxX
        return HttpResponseRedirect(self.get_success_url()) #.....XxRonnyxX
 #.....XxRonnyxX
    def get_context_data(self, **kwargs): #.....XxRonnyxX
        self.request.session['primero'] = True #.....XxRonnyxX
        context = super(NotaSalidaGenerarDespachoView, self).get_context_data(**kwargs) #.....XxRonnyxX
        context['accion'] = "Generar" #.....XxRonnyxX
        context['titulo'] = "Despacho" #.....XxRonnyxX
        context['dar_baja'] = "true" #.....XxRonnyxX
        return context #.....XxRonnyxX
 #.....XxRonnyxX
class DespachoListView(PermissionRequiredMixin, ListView): #.....XxRonnyxX
    permission_required = ('logistica.view_despacho') #.....XxRonnyxX
    model = Despacho #.....XxRonnyxX
    template_name = 'logistica/despacho/inicio.html' #.....XxRonnyxX
    context_object_name = 'contexto_despacho' #.....XxRonnyxX
 #.....XxRonnyxX
def DespachoTabla(request): #.....XxRonnyxX
    data = dict() #.....XxRonnyxX
    if request.method == 'GET': #.....XxRonnyxX
        template = 'logistica/despacho/inicio_tabla.html' #.....XxRonnyxX
        context = {} #.....XxRonnyxX
        context['contexto_despacho'] = Despacho.objects.all() #.....XxRonnyxX
 #.....XxRonnyxX
        data['table'] = render_to_string( #.....XxRonnyxX
            template, #.....XxRonnyxX
            context, #.....XxRonnyxX
            request=request #.....XxRonnyxX
        ) #.....XxRonnyxX
        return JsonResponse(data) #.....XxRonnyxX
 #.....XxRonnyxX
class DespachoUpdateView(PermissionRequiredMixin, BSModalUpdateView): #.....XxRonnyxX
    permission_required = ('logistica.change_despacho') #.....XxRonnyxX
 #.....XxRonnyxX
    model = Despacho #.....XxRonnyxX
    template_name = "includes/formulario generico.html" #.....XxRonnyxX
    form_class = DespachoForm #.....XxRonnyxX
    success_url = reverse_lazy('logistica_app:despacho_inicio') #.....XxRonnyxX
 #.....XxRonnyxX
    def get_context_data(self, **kwargs): #.....XxRonnyxX
        context = super(DespachoUpdateView, self).get_context_data(**kwargs) #.....XxRonnyxX
        context['accion'] = "Actualizar" #.....XxRonnyxX
        context['titulo'] = "Despacho" #.....XxRonnyxX
        return context #.....XxRonnyxX
 #.....XxRonnyxX
    def form_valid(self, form): #.....XxRonnyxX
        registro_guardar(form.instance, self.request) #.....XxRonnyxX
        return super().form_valid(form) #.....XxRonnyxX
 #.....XxRonnyxX
class DespachoConcluirView(PermissionRequiredMixin, BSModalDeleteView): #.....XxRonnyxX
    permission_required = ('logistica.delete_despacho') #.....XxRonnyxX
    model = Despacho #.....XxRonnyxX
    template_name = "logistica/despacho/boton.html" #.....XxRonnyxX
 #.....XxRonnyxX
    def get_success_url(self, **kwargs): #.....XxRonnyxX
        return reverse_lazy('logistica_app:despacho_inicio') #.....XxRonnyxX
 #.....XxRonnyxX
    def delete(self, request, *args, **kwargs): #.....XxRonnyxX
        self.object = self.get_object() #.....XxRonnyxX
        self.object.estado = 2 #.....XxRonnyxX
        registro_guardar(self.object, self.request) #.....XxRonnyxX
        self.object.save() #.....XxRonnyxX
        messages.success(request, MENSAJE_CONCLUIR_DESPACHO) #.....XxRonnyxX
        return HttpResponseRedirect(self.get_success_url()) #.....XxRonnyxX
 #.....XxRonnyxX
    def get_context_data(self, **kwargs): #.....XxRonnyxX
        context = super(DespachoConcluirView, self).get_context_data(**kwargs) #.....XxRonnyxX
        context['accion'] = "Concluir" #.....XxRonnyxX
        context['titulo'] = "Despacho" #.....XxRonnyxX
        context['dar_baja'] = "true" #.....XxRonnyxX
        context['item'] = self.object.numero_despacho #.....XxRonnyxX
        return context #.....XxRonnyxX
 #.....XxRonnyxX
class DespachoFinalizarSinGuiaView(PermissionRequiredMixin, BSModalDeleteView): #.....XxRonnyxX
    permission_required = ('logistica.delete_despacho') #.....XxRonnyxX
    model = Despacho #.....XxRonnyxX
    template_name = "logistica/despacho/boton.html" #.....XxRonnyxX
 #.....XxRonnyxX
    def get_success_url(self, **kwargs): #.....XxRonnyxX
        return reverse_lazy('logistica_app:despacho_inicio') #.....XxRonnyxX
 #.....XxRonnyxX
    def delete(self, request, *args, **kwargs): #.....XxRonnyxX
        self.object = self.get_object() #.....XxRonnyxX
        self.object.estado = 4 #.....XxRonnyxX
        registro_guardar(self.object, self.request) #.....XxRonnyxX
        self.object.save() #.....XxRonnyxX
        messages.success(request, MENSAJE_FINALIZAR_SIN_GUIA_DESPACHO) #.....XxRonnyxX
        return HttpResponseRedirect(self.get_success_url()) #.....XxRonnyxX
 #.....XxRonnyxX
    def get_context_data(self, **kwargs): #.....XxRonnyxX
        context = super(DespachoFinalizarSinGuiaView, self).get_context_data(**kwargs) #.....XxRonnyxX
        context['accion'] = "Finalizar" #.....XxRonnyxX
        context['titulo'] = "Despacho sin Guia" #.....XxRonnyxX
        context['dar_baja'] = "true" #.....XxRonnyxX
        context['item'] = self.object.numero_despacho #.....XxRonnyxX
        return context #.....XxRonnyxX
 #.....XxRonnyxX
class DespachoAnularView(PermissionRequiredMixin, BSModalUpdateView): #.....XxRonnyxX
    permission_required = ('logistica.delete_despacho') #.....XxRonnyxX
    model = Despacho #.....XxRonnyxX
    template_name = "includes/formulario generico.html" #.....XxRonnyxX
    form_class = DespachoAnularForm #.....XxRonnyxX
 #.....XxRonnyxX
    def dispatch(self, request, *args, **kwargs): #.....XxRonnyxX
        if not self.has_permission(): #.....XxRonnyxX
            return render(request, 'includes/modal sin permiso.html') #.....XxRonnyxX
        return super().dispatch(request, *args, **kwargs) #.....XxRonnyxX
 #.....XxRonnyxX
    def get_success_url(self, **kwargs): #.....XxRonnyxX
        return reverse_lazy('logistica_app:despacho_inicio') #.....XxRonnyxX
 #.....XxRonnyxX
    def form_valid(self, form): #.....XxRonnyxX
        form.instance.estado = 3 #.....XxRonnyxX
        registro_guardar(form.instance, self.request) #.....XxRonnyxX
        return super().form_valid(form) #.....XxRonnyxX
 #.....XxRonnyxX
    def get_context_data(self, **kwargs): #.....XxRonnyxX
        context = super(DespachoAnularView, self).get_context_data(**kwargs) #.....XxRonnyxX
        context['accion']="Anular" #.....XxRonnyxX
        context['titulo']="Despacho" #.....XxRonnyxX
        return context #.....XxRonnyxX
 #.....XxRonnyxX
class DespachoDetailView(PermissionRequiredMixin, DetailView): #.....XxRonnyxX
    permission_required = ('logistica.view_despacho') #.....XxRonnyxX
    model = Despacho #.....XxRonnyxX
    template_name = "logistica/despacho/detalle.html" #.....XxRonnyxX
    context_object_name = 'contexto_despacho_detalle' #.....XxRonnyxX
 #.....XxRonnyxX
    def get_context_data(self, **kwargs): #.....XxRonnyxX
        # despacho = Despacho.objects.get(id = self.kwargs['pk']) #.....XxRonnyxX
        context = super(DespachoDetailView, self).get_context_data(**kwargs) #.....XxRonnyxX
        context['materiales'] = self.object.DespachoDetalle_despacho.all() #.....XxRonnyxX
 #.....XxRonnyxX
        return context #.....XxRonnyxX
 #.....XxRonnyxX
def DespachoDetailTabla(request, pk): #.....XxRonnyxX
    data = dict() #.....XxRonnyxX
    if request.method == 'GET': #.....XxRonnyxX
        template = 'logistica/despacho/detalle_tabla.html' #.....XxRonnyxX
        context = {} #.....XxRonnyxX
        despacho = Despacho.objects.get(id = pk) #.....XxRonnyxX
        context['contexto_despacho_detalle'] = despacho #.....XxRonnyxX
        context['materiales'] = DespachoDetalle.objects.filter(despacho = despacho) #.....XxRonnyxX
 #.....XxRonnyxX
        data['table'] = render_to_string( #.....XxRonnyxX
            template, #.....XxRonnyxX
            context, #.....XxRonnyxX
            request=request #.....XxRonnyxX
        ) #.....XxRonnyxX
        return JsonResponse(data) #.....XxRonnyxX
 #.....XxRonnyxX
class DespachoGenerarGuiaView(PermissionRequiredMixin, BSModalDeleteView): #.....XxRonnyxX
    permission_required = ('logistica.change_despachodetalle') #.....XxRonnyxX
 #.....XxRonnyxX
    model = Despacho #.....XxRonnyxX
    template_name = "logistica/despacho/boton.html" #.....XxRonnyxX
    success_url = reverse_lazy('comprobante_despacho_app:guia_inicio') #.....XxRonnyxX
 #.....XxRonnyxX
    def dispatch(self, request, *args, **kwargs): #.....XxRonnyxX
        if not self.has_permission(): #.....XxRonnyxX
            return render(request, 'includes/modal sin permiso.html') #.....XxRonnyxX
        return super().dispatch(request, *args, **kwargs) #.....XxRonnyxX
 #.....XxRonnyxX
    def delete(self, request, *args, **kwargs): #.....XxRonnyxX
        self.object = self.get_object() #.....XxRonnyxX
        item = len(Guia.objects.all()) #.....XxRonnyxX
        detalles = self.object.DespachoDetalle_despacho.all() #.....XxRonnyxX
        serie_comprobante = SeriesComprobante.objects.por_defecto(ContentType.objects.get_for_model(Guia)) #.....XxRonnyxX

        guia = Guia.objects.create( #.....XxRonnyxX
            numero_guia = item + 1, #.....XxRonnyxX
            sociedad = self.object.sociedad, #.....XxRonnyxX
            serie_comprobante = serie_comprobante, #.....XxRonnyxX
            cliente = self.object.cliente, #.....XxRonnyxX
            created_by = self.request.user, #.....XxRonnyxX
            updated_by = self.request.user, #.....XxRonnyxX
        )
 #.....XxRonnyxX
        for detalle in detalles: #.....XxRonnyxX
            guia_detalle = GuiaDetalle.objects.create( #.....XxRonnyxX
                item = detalle.item, #.....XxRonnyxX
                content_type = detalle.content_type, #.....XxRonnyxX
                id_registro = detalle.id_registro, #.....XxRonnyxX
                guia=guia, #.....XxRonnyxX
                cantidad=detalle.cantidad_despachada, #.....XxRonnyxX
                unidad=detalle.producto.unidad_base, #.....XxRonnyxX
                descripcion_documento=detalle.producto.descripcion_venta, #.....XxRonnyxX
                peso=detalle.producto.peso_unidad_base, #.....XxRonnyxX
                created_by=self.request.user, #.....XxRonnyxX
                updated_by=self.request.user, #.....XxRonnyxX              
            ) #.....XxRonnyxX
            self.request.session['primero'] = False #.....XxRonnyxX
        registro_guardar(self.object, self.request) #.....XxRonnyxX
        self.object.estado = 5
        self.object.save() #.....XxRonnyxX
        messages.success(request, MENSAJE_GENERAR_GUIA) #.....XxRonnyxX
        return HttpResponseRedirect(self.get_success_url()) #.....XxRonnyxX
 #.....XxRonnyxX
    def get_context_data(self, **kwargs): #.....XxRonnyxX
        self.request.session['primero'] = True #.....XxRonnyxX
        context = super(DespachoGenerarGuiaView, self).get_context_data(**kwargs) #.....XxRonnyxX
        context['accion'] = "Generar" #.....XxRonnyxX
        context['titulo'] = "Guía" #.....XxRonnyxX
        context['dar_baja'] = "true" #.....XxRonnyxX
        return context #.....XxRonnyxX
 #.....XxRonnyxX