from django.shortcuts import render
from django import forms
from applications.importaciones import *
from applications.logistica.models import SolicitudPrestamoMateriales, SolicitudPrestamoMaterialesDetalle
from applications.logistica.forms import SolicitudPrestamoMaterialesDetalleForm, SolicitudPrestamoMaterialesDetalleUpdateForm, SolicitudPrestamoMaterialesForm
from applications.clientes.models import ClienteInterlocutor, InterlocutorCliente
from applications.logistica.pdf import generarSolicitudPrestamoMateriales

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
        context['titulo'] = 'Agregar Material '
        context['accion'] = 'Guardar'
        return context

class SolicitudPrestamoMaterialesDetalleImprimirView(View):
    def get(self, request, *args, **kwargs):
        color = COLOR_DEFAULT
        titulo = 'SOLICITUD DE PRÉSTAMO DE EQUIPOS'
        vertical = True
        logo = None
        pie_pagina = PIE_DE_PAGINA_DEFAULT

        obj = SolicitudPrestamoMateriales.objects.get(id=self.kwargs['pk'])

        Texto = str(titulo) + '\n' +'Nro.: '+str(obj.numero_prestamo) + '\n' + 'Razón Social: '+str(obj.cliente) + '\n' + 'Contacto :'+str(obj.cliente_interlocutor) + '\n'
        TablaEncabezado = [
            'ITEM', 
            'DESCRIPCIÓN',
            'UNIDAD', 
            'CANTIDAD', 
            ]

        detalle = obj.SolicitudPrestamoMaterialesDetalle_solicitud_prestamo_materiales
        solicitud_prestamo_materiales = detalle.all()

        TablaDatos = []
        count = 1
        for solicitud in solicitud_prestamo_materiales:
            fila = []
            fila.append(solicitud.item)
            # fila.append(solicitud.activo.numero_serie)
            # if activo.activo.marca:
            #     fila.append(activo.activo.marca.nombre)
            # else:
            #     fila.append('-')
            # if activo.activo.color:
            #     fila.append(activo.activo.color)
            # else:
            #     fila.append('-')
            # fila.append(activo.activo.empresa)
            # fila.append(activo.activo.piso)
            # fila.append(activo.activo.colaborador)
            # if activo.observacion:
            #     fila.append(activo.observacion)
            # else:
            #     fila.append('-')
            # fila.append('')
            TablaDatos.append(fila)
            count += 1

        buf = generarSolicitudPrestamoMateriales(titulo, vertical, logo, pie_pagina, Texto, TablaEncabezado, TablaDatos, color)

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


class ClienteForm(forms.Form):
    cliente_interlocutor = forms.ModelChoiceField(queryset = ClienteInterlocutor.objects.all(), required=False)

def ClienteView(request, id_cliente_interlocutor):
    form = ClienteForm()
    lista = []
    relaciones = ClienteInterlocutor.objects.filter(cliente = id_cliente_interlocutor)
    for relacion in relaciones:
        lista.append(relacion.interlocutor.id)
    form.fields['cliente_interlocutor'].queryset = InterlocutorCliente.objects.filter(id__in = lista)
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

