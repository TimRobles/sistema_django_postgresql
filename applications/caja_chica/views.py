from django.shortcuts import render
from applications.importaciones import*
from applications.funciones import registrar_excepcion
from .models import Requerimiento, RequerimientoDocumento, RequerimientoVueltoExtra
from applications.caja_chica.forms import RequerimientoAprobarForm, RequerimientoDocumentoForm, RequerimientoForm, RequerimientoRechazarForm, RequerimientoRechazarRendicionForm


class RequerimientoListView(PermissionRequiredMixin, ListView):
    permission_required = ('caja_chica.view_requerimiento')

    model = Requerimiento
    template_name = "caja_chica/requerimiento/inicio.html"
    context_object_name = 'contexto_requerimientos'
    

def RequerimientoTabla(request):
    data = dict()
    if request.method == 'GET':
        template = 'caja_chica/requerimiento/inicio_tabla.html'
        context = {}
        context['contexto_requerimientos'] = Requerimiento.objects.all()

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)


class RequerimientoCreateView(PermissionRequiredMixin, BSModalCreateView):
    permission_required = ('caja_chica.add_requerimiento')

    model = Requerimiento
    template_name = "includes/formulario generico.html"
    form_class = RequerimientoForm
    success_url = reverse_lazy('caja_chica_app:requerimiento_inicio')

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super(RequerimientoCreateView, self).get_context_data(**kwargs)
        context['accion']="Crear"
        context['titulo']="Requerimiento"
        return context


class RequerimientoUpdateView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('caja_chica.change_requerimiento')

    model = Requerimiento
    template_name = "includes/formulario generico.html"
    form_class = RequerimientoForm
    success_url = reverse_lazy('caja_chica_app:requerimiento_inicio')

    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super(RequerimientoUpdateView, self).get_context_data(**kwargs)
        context['accion']="Actualizar"
        context['titulo'] = "Requerimiento"
        return context


class RequerimientoDeleteView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('caja_chica.delete_requerimiento')

    model = Requerimiento
    template_name = "includes/eliminar generico.html"
    success_url = reverse_lazy('caja_chica_app:requerimiento_inicio')

    def get_context_data(self, **kwargs):
        context = super(RequerimientoDeleteView, self).get_context_data(**kwargs)
        context['accion']="Eliminar"
        context['titulo'] = "Requerimiento"
        context['item'] = self.get_object()
        context['dar_baja'] = "true"
        return context
    

class RequerimientoSolicitarView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('caja_chica.change_requerimiento')
    model = Requerimiento
    template_name = "caja_chica/requerimiento/boton.html"
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('caja_chica_app:requerimiento_inicio')

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            self.object = self.get_object()
            self.object.estado = 2
            registro_guardar(self.object, self.request)
            self.object.save()
            messages.success(request, MENSAJE_SOLICITAR_REQUERIMIENTO)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(RequerimientoSolicitarView, self).get_context_data(**kwargs)
        context['accion'] = "Solicitar"
        context['titulo'] = "Requerimiento"
        context['dar_baja'] = "true"
        context['item'] = str(self.object.concepto) + ' | ' + str(self.object.usuario.username)
        return context


class RequerimientoEditarView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('caja_chica.change_requerimiento')
    model = Requerimiento
    template_name = "caja_chica/requerimiento/boton.html"
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('caja_chica_app:requerimiento_inicio')

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            self.object = self.get_object()
            self.object.estado = 1
            registro_guardar(self.object, self.request)
            self.object.save()
            messages.success(request, MENSAJE_EDITAR_REQUERIMIENTO)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(RequerimientoEditarView, self).get_context_data(**kwargs)
        context['accion'] = "Editar"
        context['titulo'] = "Requerimiento"
        context['dar_baja'] = "true"
        context['item'] = str(self.object.concepto) + ' | ' + str(self.object.usuario.username)
        return context
    

class RequerimientoAprobarView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('caja_chica.change_requerimiento')
    model = Requerimiento
    template_name = "includes/formulario generico.html"
    form_class = RequerimientoAprobarForm
    
    def get_success_url(self, **kwargs):
        return reverse_lazy('caja_chica_app:requerimiento_inicio')

    def get_form_kwargs(self):
        kwargs = super(RequerimientoAprobarView, self).get_form_kwargs()
        requerimiento = Requerimiento.objects.filter(id = self.kwargs['pk'])[0]
        kwargs['moneda'] = requerimiento.moneda
        kwargs['fecha'] = requerimiento.fecha
        return kwargs

    def form_valid(self, form):
        form.instance.estado = 3
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(RequerimientoAprobarView, self).get_context_data(**kwargs)
        context['accion']="Aprobar"
        context['titulo']="Requerimiento"
        return context
    

class RequerimientoRechazarView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('caja_chica.change_requerimiento')
    model = Requerimiento
    template_name = "includes/formulario generico.html"
    form_class = RequerimientoRechazarForm
    
    def get_success_url(self, **kwargs):
        return reverse_lazy('caja_chica_app:requerimiento_inicio')

    def form_valid(self, form):
        form.instance.estado = 4
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(RequerimientoRechazarView, self).get_context_data(**kwargs)
        context['accion']="Rechazar"
        context['titulo']="Requerimiento"
        return context


class RequerimientoRetrocederView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('caja_chica.change_requerimiento')
    model = Requerimiento
    template_name = "caja_chica/requerimiento/boton.html"
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('caja_chica_app:requerimiento_inicio')

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            self.object = self.get_object()
            self.object.monto_final = 0.00
            self.object.concepto_final = None
            self.object.fecha_entrega = None
            self.object.content_type = None
            self.object.id_registro = None
            self.object.motivo_rechazo = None
            self.object.dato_rechazado = None
            self.object.estado = 2
            registro_guardar(self.object, self.request)
            self.object.save()
            messages.success(request, MENSAJE_RETROCEDER_REQUERIMIENTO)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(RequerimientoRetrocederView, self).get_context_data(**kwargs)
        context['accion'] = "Retroceder"
        context['titulo'] = "Requerimiento"
        context['dar_baja'] = "true"
        context['item'] = str(self.object.concepto) + ' | ' + str(self.object.usuario.username)
        return context
    

class RequerimientoFinalizarRendicionView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('caja_chica.change_requerimiento')
    model = Requerimiento
    template_name = "caja_chica/requerimiento/boton.html"

    def get_success_url(self):
        return reverse_lazy('caja_chica_app:requerimiento_inicio')

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            self.object = self.get_object()
            self.object.estado = 5
            registro_guardar(self.object, self.request)
            self.object.save()
            messages.success(request, MENSAJE_FINALIZAR_RENDICION_REQUERIMIENTO)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(RequerimientoFinalizarRendicionView, self).get_context_data(**kwargs)
        context['accion'] = "Finalizar"
        context['titulo'] = "Rendición"
        context['dar_baja'] = "true"
        return context
    

class RequerimientoEditarRendicionView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('caja_chica.change_requerimiento')
    model = Requerimiento
    template_name = "caja_chica/requerimiento/boton.html"
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('caja_chica_app:requerimiento_inicio')

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            self.object = self.get_object()
            self.object.estado = 3
            registro_guardar(self.object, self.request)
            self.object.save()
            messages.success(request, MENSAJE_EDITAR_RENDICION_REQUERIMIENTO)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(RequerimientoEditarRendicionView, self).get_context_data(**kwargs)
        context['accion'] = "Editar"
        context['titulo'] = "Rendición"
        context['dar_baja'] = "true"
        context['item'] = str(self.object.concepto) + ' | ' + str(self.object.usuario.username)
        return context


class RequerimientoAprobarRendicionView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('caja_chica.change_requerimiento')
    model = Requerimiento
    template_name = "caja_chica/requerimiento/boton.html"

    def get_success_url(self):
        return reverse_lazy('caja_chica_app:requerimiento_inicio')

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            self.object = self.get_object()
            self.object.estado = 7
            registro_guardar(self.object, self.request)
            self.object.save()
            messages.success(request, MENSAJE_APROBAR_RENDICION_REQUERIMIENTO)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(RequerimientoAprobarRendicionView, self).get_context_data(**kwargs)
        context['accion'] = "Aprobar"
        context['titulo'] = "Rendición"
        context['dar_baja'] = "true"
        return context


class RequerimientoRechazarRendicionView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('caja_chica.change_requerimiento')
    model = Requerimiento
    template_name = "includes/formulario generico.html"
    form_class = RequerimientoRechazarRendicionForm
    
    def get_success_url(self, **kwargs):
        return reverse_lazy('caja_chica_app:requerimiento_inicio')

    def form_valid(self, form):
        form.instance.estado = 6
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(RequerimientoRechazarRendicionView, self).get_context_data(**kwargs)
        context['accion']="Rechazar"
        context['titulo']="Rendición"
        return context
    

class RequerimientoRetrocederRendicionView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('caja_chica.change_requerimiento')
    model = Requerimiento
    template_name = "caja_chica/requerimiento/boton.html"
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('caja_chica_app:requerimiento_inicio')

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            self.object = self.get_object()
            self.object.estado = 5
            registro_guardar(self.object, self.request)
            self.object.save()
            messages.success(request, MENSAJE_RETROCEDER_RENDICION_REQUERIMIENTO)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(RequerimientoRetrocederRendicionView, self).get_context_data(**kwargs)
        context['accion'] = "Retroceder"
        context['titulo'] = "Requerimiento"
        context['dar_baja'] = "true"
        context['item'] = str(self.object.concepto) + ' | ' + str(self.object.usuario.username)
        return context


class RequerimientoDetalleView(PermissionRequiredMixin, DetailView):
    permission_required = ('caja_chica.view_requerimiento')

    model = Requerimiento
    template_name = "caja_chica/requerimiento/detalle.html"
    context_object_name = 'contexto_requerimiento_detalle'
    
    def get_context_data(self, **kwargs):
        requerimiento = Requerimiento.objects.get(id = self.kwargs['pk'])
        context = super(RequerimientoDetalleView, self).get_context_data(**kwargs)
        context['contexto_documentos'] = RequerimientoDocumento.objects.filter(requerimiento = requerimiento)
        return context


def RequerimientoDetalleTabla(request, pk):
    data = dict()
    if request.method == 'GET':
        template = 'caja_chica/requerimiento/detalle_tabla.html'
        context = {}
        requerimiento = Requerimiento.objects.get(id = pk)
        context['contexto_requerimiento_detalle'] = requerimiento
        context['contexto_documentos'] = RequerimientoDocumento.objects.filter(requerimiento = requerimiento)

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)
    

class RequerimientoDocumentoCreateView(PermissionRequiredMixin, BSModalCreateView):
    permission_required = ('caja_chica.add_requerimientodocumento')
    model = RequerimientoDocumento
    template_name = "caja_chica/requerimiento/documento/form.html"
    form_class = RequerimientoDocumentoForm
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)
    
    def get_success_url(self, **kwargs):
        return reverse_lazy('caja_chica_app:requerimiento_detalle', kwargs={'pk':self.kwargs['requerimiento_id']})

    def get_form_kwargs(self):
        kwargs = super(RequerimientoDocumentoCreateView, self).get_form_kwargs()
        requerimiento = Requerimiento.objects.get(id = self.kwargs['requerimiento_id'])
        kwargs['moneda_requerimiento'] = requerimiento.moneda
        kwargs['tipo_cambio'] = None
        return kwargs

    def form_valid(self, form):
        form.instance.requerimiento = Requerimiento.objects.get(id = self.kwargs['requerimiento_id'])
        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(RequerimientoDocumentoCreateView, self).get_context_data(**kwargs)
        context['accion']="Registrar"
        context['titulo']="Documento"
        return context


class RequerimientoDocumentoUpdateView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('caja_chica.change_requerimientodocumento')
    model = RequerimientoDocumento
    template_name = "caja_chica/requerimiento/documento/form.html"
    form_class = RequerimientoDocumentoForm
    
    def get_success_url(self, **kwargs):
        return reverse_lazy('caja_chica_app:requerimiento_detalle', kwargs={'pk':self.object.requerimiento.id})

    def get_form_kwargs(self):
        kwargs = super(RequerimientoDocumentoUpdateView, self).get_form_kwargs()
        documento = RequerimientoDocumento.objects.get(id = self.kwargs['pk'])
        kwargs['moneda_requerimiento'] = documento.requerimiento.moneda
        kwargs['tipo_cambio'] = documento.tipo_cambio
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(RequerimientoDocumentoUpdateView, self).get_context_data(**kwargs)
        context['accion']="Actualizar"
        context['titulo']="Documento"
        return context
    

class RequerimientoDocumentoDeleteView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('caja_chica.delete_requerimientodocumento')
    model = RequerimientoDocumento
    template_name = "includes/eliminar generico.html"
    # context_object_name = 'contexto_requerimiento_documento' 
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('caja_chica_app:requerimiento_detalle', kwargs={'pk':self.object.requerimiento.id})

    def get_context_data(self, **kwargs):
        context = super(RequerimientoDocumentoDeleteView, self).get_context_data(**kwargs)
        context['accion']="Eliminar"
        context['titulo']="Documento"
        context['item'] = self.get_object()
        context['dar_baja'] = "true"
        return context
    

class RequerimientoDocumentoDetailView(PermissionRequiredMixin, DetailView):
    permission_required = ('caja_chica.view_RequerimientoDocumento')
    model = RequerimientoDocumento
    template_name = "caja_chica/requerimiento/documento/detalle.html"
    context_object_name = 'contexto_documentos_detalle'

    def get_context_data(self, **kwargs):
        documento = RequerimientoDocumento.objects.get(id = self.kwargs['pk'])
        context = super(RequerimientoDocumentoDetailView, self).get_context_data(**kwargs)
        return context


def RequerimientoDocumentoDetailTabla(request, pk):
    data = dict()
    if request.method == 'GET':
        template = 'caja_chica/requerimiento/documento/detalle_tabla.html'
        context = {}
        documento = RequerimientoDocumento.objects.get(id = pk)
        context['contexto_documentos_detalle'] = documento
        
        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)
    