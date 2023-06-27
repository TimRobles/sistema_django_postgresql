from decimal import Decimal
from django.shortcuts import render
from applications.caja_chica.funciones import movimientos_caja_chica
from applications.caja_chica.pdf import generarCajaChicaPdf
from applications.home.templatetags.funciones_propias import nombre_usuario
from applications.importaciones import *
from applications.funciones import registrar_excepcion
from applications.contabilidad.models import ReciboServicio
from applications.sociedad.models import Sociedad

from .models import (
    Requerimiento, 
    RequerimientoDocumento, 
    RequerimientoDocumentoDetalle,
    RequerimientoVueltoExtra,
    CajaChica, 
    CajaChicaPrestamo, 
    ReciboCajaChica)

from applications.caja_chica.forms import (
    RequerimientoAprobarForm, 
    RequerimientoDocumentoDetalleForm, 
    RequerimientoDocumentoForm, 
    RequerimientoFinalizarRendicionForm,
    RequerimientoForm,
    RequerimientoRechazarForm,
    RequerimientoRechazarRendicionForm,
    CajaChicaCrearForm,
    CajaChicaPrestamoCrearForm,
    ReciboCajaChicaCrearForm,
    RequerimientoVueltoExtraForm,
    CajaChicaReciboCrearForm,
    CajaChicaReciboServicioAgregarForm,
    CajaChicaReciboServicioUpdateForm,)

class RequerimientoListView(PermissionRequiredMixin, ListView):
    permission_required = ('caja_chica.view_requerimiento')

    model = Requerimiento
    template_name = "caja_chica/requerimiento/inicio.html"
    context_object_name = 'contexto_requerimientos'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = Requerimiento.objects.filter(
            usuario=self.request.user,
            )
        return queryset
    

def RequerimientoTabla(request):
    data = dict()
    if request.method == 'GET':
        template = 'caja_chica/requerimiento/inicio_tabla.html'
        context = {}
        context['contexto_requerimientos'] = Requerimiento.objects.filter(
            usuario=request.user,
            )

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)


class RequerimientoRecibidoListView(PermissionRequiredMixin, ListView):
    permission_required = ('caja_chica.view_requerimiento')

    model = Requerimiento
    template_name = "caja_chica/requerimiento/recibido.html"
    context_object_name = 'contexto_requerimientos'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = Requerimiento.objects.filter(
            usuario_pedido=self.request.user,
            estado__gt=1,
            estado__lt=7,
            )
        return queryset
    

def RequerimientoRecibidoTabla(request):
    data = dict()
    if request.method == 'GET':
        template = 'caja_chica/requerimiento/recibido_tabla.html'
        context = {}
        context['contexto_requerimientos'] = Requerimiento.objects.filter(
            usuario_pedido=request.user,
            estado__gt=1,
            estado__lt=7,
            )

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

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        caja_chicas = CajaChica.objects.filter(
            estado=1,
        )
        usuario_pedido = []
        for caja_chica in caja_chicas:
            if not caja_chica.usuario.id in usuario_pedido:
                usuario_pedido.append(caja_chica.usuario.id)
        kwargs['usuario_pedido'] = get_user_model().objects.filter(id__in = usuario_pedido)
        return kwargs

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

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        caja_chicas = CajaChica.objects.filter(
            estado=1,
        )
        usuario_pedido = []
        for caja_chica in caja_chicas:
            if not caja_chica.usuario.id in usuario_pedido:
                usuario_pedido.append(caja_chica.usuario.id)
        kwargs['usuario_pedido'] = get_user_model().objects.filter(id__in = usuario_pedido)
        return kwargs

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
        return reverse_lazy('caja_chica_app:requerimiento_detalle', kwargs={'pk':self.get_object().id})

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
        return reverse_lazy('caja_chica_app:requerimiento_detalle', kwargs={'pk':self.get_object().id})

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
    template_name = "caja_chica/requerimiento/aprobar.html"
    form_class = RequerimientoAprobarForm
    
    def get_success_url(self, **kwargs):
        return reverse_lazy('caja_chica_app:requerimiento_detalle', kwargs={'pk':self.get_object().id})

    def get_form_kwargs(self):
        kwargs = super(RequerimientoAprobarView, self).get_form_kwargs()
        requerimiento = Requerimiento.objects.filter(id = self.kwargs['pk'])[0]
        caja=[]
        for caja_chica in CajaChica.objects.filter(estado=1, usuario=self.request.user):
            caja.append((f'{ContentType.objects.get_for_model(caja_chica).id}|{caja_chica.id}', caja_chica.__str__()))
        cheque=[]
        kwargs['moneda'] = requerimiento.moneda
        kwargs['fecha'] = requerimiento.fecha
        kwargs['caja'] = caja
        kwargs['cheque'] = cheque
        return kwargs

    def form_valid(self, form):
        caja_cheque = form.cleaned_data.get('caja_cheque')
        form.instance.estado = 3
        form.instance.content_type = ContentType.objects.get(id=int(caja_cheque.split('|')[0]))
        form.instance.id_registro = int(caja_cheque.split('|')[1])
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(RequerimientoAprobarView, self).get_context_data(**kwargs)
        context['accion']="Aprobar"
        context['titulo']="Requerimiento"
        context['requerimiento'] = self.get_object()
        return context
    

class RequerimientoRechazarView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('caja_chica.change_requerimiento')
    model = Requerimiento
    template_name = "includes/formulario generico.html"
    form_class = RequerimientoRechazarForm
    
    def get_success_url(self, **kwargs):
        return reverse_lazy('caja_chica_app:requerimiento_detalle', kwargs={'pk':self.get_object().id})

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
        return reverse_lazy('caja_chica_app:requerimiento_detalle', kwargs={'pk':self.get_object().id})

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
    

class RequerimientoFinalizarRendicionView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('caja_chica.change_requerimiento')
    model = Requerimiento
    form_class = RequerimientoFinalizarRendicionForm
    template_name = "caja_chica/requerimiento/finalizar_rendicion.html"

    def get_success_url(self):
        return reverse_lazy('caja_chica_app:requerimiento_detalle', kwargs={'pk':self.get_object().id})

    @transaction.atomic
    def form_valid(self, form):
        sid = transaction.savepoint()
        try:
            print(form.cleaned_data.get('utilizado'))
            form.instance.monto_usado = form.cleaned_data.get('utilizado')
            form.instance.estado = 5
            registro_guardar(form.instance, self.request)
            return super().form_valid(form)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
            return super().form_invalid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        requerimiento = self.get_object()
        kwargs['utilizado'] = requerimiento.utilizado
        kwargs['vuelto_extra'] = requerimiento.vuelto_extra
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(RequerimientoFinalizarRendicionView, self).get_context_data(**kwargs)
        context['accion'] = "Finalizar"
        context['titulo'] = "Rendición"
        context['dar_baja'] = "true"
        context['url_vuelto_extra'] = "true"
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
        return reverse_lazy('caja_chica_app:requerimiento_detalle', kwargs={'pk':self.get_object().id})

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
        return reverse_lazy('caja_chica_app:requerimiento_detalle', kwargs={'pk':self.get_object().id})

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
        return reverse_lazy('caja_chica_app:requerimiento_detalle', kwargs={'pk':self.get_object().id})

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
        return reverse_lazy('caja_chica_app:requerimiento_detalle', kwargs={'pk':self.get_object().id})

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
        # caja = CajaChica.objects.get(id = requerimiento.id_registro)
        usuario_pedido = requerimiento.usuario_pedido
        context = super(RequerimientoDetalleView, self).get_context_data(**kwargs)
        context['contexto_documentos'] = RequerimientoDocumento.objects.filter(requerimiento = requerimiento)
        context['contexto_vuelto_extra'] = RequerimientoVueltoExtra.objects.filter(requerimiento = requerimiento)
        context['usuario_pedido'] = usuario_pedido

        return context


def RequerimientoDetalleTabla(request, pk):
    data = dict()
    if request.method == 'GET':
        template = 'caja_chica/requerimiento/detalle_tabla.html'
        context = {}
        requerimiento = Requerimiento.objects.get(id = pk)
        # caja = CajaChica.objects.get(id = requerimiento.id_registro)
        usuario_pedido = requerimiento.usuario_pedido
        context['contexto_requerimiento_detalle'] = requerimiento
        context['contexto_documentos'] = RequerimientoDocumento.objects.filter(requerimiento = requerimiento)
        context['contexto_vuelto_extra'] = RequerimientoVueltoExtra.objects.filter(requerimiento = requerimiento)
        context['usuario_pedido'] = usuario_pedido
        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)
    

class RequerimientoVueltoExtraCreateView(PermissionRequiredMixin, BSModalCreateView):
    permission_required = ('caja_chica.add_requerimientovueltoextra')
    model = RequerimientoVueltoExtra
    template_name = "caja_chica/requerimiento/vuelto_extra.html"
    form_class = RequerimientoVueltoExtraForm
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)
    
    def get_success_url(self, **kwargs):
        return reverse_lazy('caja_chica_app:requerimiento_detalle', kwargs={'pk':self.kwargs['requerimiento_id']})

    def get_form_kwargs(self):
        kwargs = super(RequerimientoVueltoExtraCreateView, self).get_form_kwargs()
        requerimiento = Requerimiento.objects.get(id = self.kwargs['requerimiento_id'])
        kwargs['moneda_requerimiento'] = requerimiento.moneda
        return kwargs

    def form_valid(self, form):
        requerimiento = Requerimiento.objects.get(id = self.kwargs['requerimiento_id'])
        form.instance.requerimiento = requerimiento
        print(form.instance.vuelto_original)
        print(form.instance.vuelto_extra)
        print(form.instance.moneda)
        print(form.instance.tipo_cambio)
        print(form.instance.requerimiento)
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(RequerimientoVueltoExtraCreateView, self).get_context_data(**kwargs)
        context['accion']="Registrar"
        context['titulo']="Vuelto Extra"
        return context


class RequerimientoVueltoExtraUpdateView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('caja_chica.change_requerimientovueltoextra')
    model = RequerimientoVueltoExtra
    template_name = "caja_chica/requerimiento/vuelto_extra.html"
    form_class = RequerimientoVueltoExtraForm
    
    def get_success_url(self, **kwargs):
        return reverse_lazy('caja_chica_app:requerimiento_detalle', kwargs={'pk': self.object.requerimiento.id})

    def get_form_kwargs(self):
        kwargs = super(RequerimientoVueltoExtraUpdateView, self).get_form_kwargs()
        requerimiento = RequerimientoVueltoExtra.objects.get(id = self.kwargs['pk'])
        kwargs['moneda_requerimiento'] = requerimiento.requerimiento.moneda
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(RequerimientoVueltoExtraUpdateView, self).get_context_data(**kwargs)
        context['accion']="Actualizar"
        context['titulo']="Vuelto Extra"
        return context


class RequerimientoVueltoExtraDeleteView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('caja_chica.delete_requerimientovueltoextra')
    model = RequerimientoVueltoExtra
    template_name = "includes/eliminar generico.html"
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('caja_chica_app:requerimiento_detalle', kwargs={'pk':self.object.requerimiento.id})

    def get_context_data(self, **kwargs):
        context = super(RequerimientoVueltoExtraDeleteView, self).get_context_data(**kwargs)
        context['accion']="Eliminar"
        context['titulo']="Vuelto Extra"
        context['item'] = self.get_object()
        context['dar_baja'] = "true"
        return context
    

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
        if form.instance.tipo != 3:
            if form.instance.numero == None or form.instance.numero == "":
                form.add_error('numero', 'Ingresar un número de documento.')
                return super().form_invalid(form)
            if form.instance.sociedad == None or form.instance.sociedad == "":
                form.add_error('sociedad', 'Ingresar una Sociedad.')
                return super().form_invalid(form)
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
        return reverse_lazy('caja_chica_app:requerimiento_detalle', kwargs={'pk': self.object.requerimiento.id})

    def get_form_kwargs(self):
        kwargs = super(RequerimientoDocumentoUpdateView, self).get_form_kwargs()
        documento = RequerimientoDocumento.objects.get(id = self.kwargs['pk'])
        kwargs['moneda_requerimiento'] = documento.requerimiento.moneda
        kwargs['tipo_cambio'] = documento.tipo_cambio
        return kwargs

    @transaction.atomic
    def form_valid(self, form):
        sid = transaction.savepoint()
        try:
            print(form)
            if self.request.session['primero']:
                print('********************************************')
                print(form.instance.tipo_cambio)
                print('********************************************')
                if form.instance.tipo != 3:
                    if form.instance.numero == None or form.instance.numero == "":
                        form.add_error('numero', 'Ingresar un número de documento.')
                        return super().form_invalid(form)
                    if form.instance.sociedad == None or form.instance.sociedad == "":
                        form.add_error('sociedad', 'Ingresar una Sociedad.')
                        return super().form_invalid(form)
                registro_guardar(form.instance, self.request)
                self.request.session['primero'] = False
            return super().form_valid(form)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        self.request.session['primero'] = True
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
    permission_required = ('caja_chica.view_requerimientodocumento')
    model = RequerimientoDocumento
    template_name = "caja_chica/requerimiento/documento/detalle.html"
    context_object_name = 'contexto_documento_detalle'

    def get_context_data(self, **kwargs):
        documento_requerimiento = RequerimientoDocumento.objects.get(id = self.kwargs['pk'])
        context = super(RequerimientoDocumentoDetailView, self).get_context_data(**kwargs)
        context['contexto_item'] = RequerimientoDocumentoDetalle.objects.filter(documento_requerimiento = documento_requerimiento)

        return context


def RequerimientoDocumentoDetailTabla(request, pk):
    data = dict()
    if request.method == 'GET':
        template = 'caja_chica/requerimiento/documento/detalle_tabla.html'
        context = {}
        documento_requerimiento = RequerimientoDocumento.objects.get(id = pk)
        context['contexto_documento_detalle'] = documento_requerimiento
        context['contexto_item'] = RequerimientoDocumentoDetalle.objects.filter(documento_requerimiento = documento_requerimiento)

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)


class RequerimientoDocumentoDetalleCreateView(PermissionRequiredMixin, BSModalCreateView):
    permission_required = ('caja_chica.view_requerimientodocumentodetalle')

    model = RequerimientoDocumentoDetalle
    template_name = "includes/formulario generico.html"
    form_class = RequerimientoDocumentoDetalleForm

    def get_success_url(self, **kwargs):
        return reverse_lazy('caja_chica_app:requerimiento_documento_detalle', kwargs={'pk':self.kwargs['pk']})

    def get_form_kwargs(self):
        kwargs = super(RequerimientoDocumentoDetalleCreateView, self).get_form_kwargs()
        kwargs['producto'] = None
        kwargs['cantidad'] = None
        kwargs['unidad'] = None
        kwargs['precio_unitario'] = None
        kwargs['foto'] = None
        return kwargs

    def form_valid(self, form):
        documento_requerimiento = RequerimientoDocumento.objects.get(id = self.kwargs['pk'])
        form.instance.documento_requerimiento = documento_requerimiento
        max_item = RequerimientoDocumentoDetalle.objects.filter(documento_requerimiento = documento_requerimiento).aggregate(Max('item'))['item__max']
        if max_item:
            form.instance.item = max_item + 1
        else:
            form.instance.item = 1
        form.save()
        return super(RequerimientoDocumentoDetalleCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(RequerimientoDocumentoDetalleCreateView, self).get_context_data(**kwargs)
        context['accion'] = "Crear"
        context['titulo'] = "Item"
        return context


class RequerimientoDocumentoDetalleUpdateView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('caja_chica.view_requerimiento')

    model = RequerimientoDocumentoDetalle
    template_name = "includes/formulario generico.html"
    form_class = RequerimientoDocumentoDetalleForm

    def get_success_url(self, **kwargs):
        documento_detalle = RequerimientoDocumentoDetalle.objects.get(id = self.kwargs['pk'])
        return reverse_lazy('caja_chica_app:requerimiento_documento_detalle', kwargs={'pk':documento_detalle.documento_requerimiento.id})

    def get_form_kwargs(self):
        kwargs = super(RequerimientoDocumentoDetalleUpdateView, self).get_form_kwargs()
        documento_detalle = RequerimientoDocumentoDetalle.objects.get(id = self.kwargs['pk'])
        kwargs['producto'] = documento_detalle.producto
        kwargs['cantidad'] = documento_detalle.cantidad
        kwargs['unidad'] = documento_detalle.unidad
        kwargs['precio_unitario'] = documento_detalle.precio_unitario
        kwargs['foto'] = documento_detalle.foto
        return kwargs

    def get_context_data(self, **kwargs):        
        context = super(RequerimientoDocumentoDetalleUpdateView, self).get_context_data(**kwargs)
        context['accion']="Actualizar"
        context['titulo']="Item"
        return context


class RequerimientoDocumentoDetalleDeleteView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('caja_chica.view_requerimiento')

    model = RequerimientoDocumentoDetalle
    template_name = "includes/eliminar generico.html"
    
    def get_success_url(self, **kwargs):
        documento_detalle = RequerimientoDocumentoDetalle.objects.get(id = self.kwargs['pk'])
        return reverse_lazy('caja_chica_app:requerimiento_documento_detalle', kwargs={'pk':documento_detalle.documento_requerimiento.id})

    def delete(self, *args, **kwargs):
        detalle = RequerimientoDocumentoDetalle.objects.get(id = self.kwargs['pk'])
        documento_detalles = RequerimientoDocumentoDetalle.objects.filter(documento_requerimiento = detalle.documento_requerimiento).order_by('item')
        i = 1
        for detalle in documento_detalles:
            if detalle == detalle: continue
            detalle.item = i
            i += 1
            detalle.save()

        return super(RequerimientoDocumentoDetalleDeleteView, self).delete(*args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super(RequerimientoDocumentoDetalleDeleteView, self).get_context_data(**kwargs)
        context['accion']="Eliminar"
        context['titulo']="Item"
        context['item'] = self.get_object()
        context['dar_baja'] = "true"
        return context


#__CajaChica___________________________________________________________________________

class CajaChicaListView(PermissionRequiredMixin, ListView):
    permission_required = ('caja_chica.view_cajachica')
    model = CajaChica
    template_name = "caja_chica/caja_chica/inicio.html"
    context_object_name = 'contexto_caja_chica'
    
def CajaChicaTabla(request):
    data = dict()
    if request.method == 'GET':
        template = 'caja_chica/caja_chica/inicio_tabla.html'
        context = {}
        context['contexto_caja_chica'] = CajaChica.objects.all()

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)

class CajaChicaCreateView(PermissionRequiredMixin, BSModalCreateView):
    permission_required = ('caja_chica.add_cajachica')
    model = CajaChica
    template_name = "includes/formulario generico.html"
    form_class = CajaChicaCrearForm
    success_url = reverse_lazy('caja_chica_app:caja_chica_inicio')

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        caja_chicas = CajaChica.objects.filter(
            usuario=self.request.user,
            estado=2,
        )
        kwargs['caja_chicas'] = caja_chicas
        return kwargs

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super(CajaChicaCreateView, self).get_context_data(**kwargs)
        context['accion']="Crear"
        context['titulo']="Caja Chica"
        return context

class CajaChicaUpdateView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('caja_chica.change_cajachica')
    model = CajaChica
    template_name = "includes/formulario generico.html"
    form_class = CajaChicaCrearForm
    success_url = reverse_lazy('caja_chica_app:caja_chica_inicio')

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        caja_chicas = CajaChica.objects.filter(
            usuario=self.request.user,
            estado=2,
        ).exclude(
            id=self.get_object().id
        )
        kwargs['caja_chicas'] = caja_chicas
        return kwargs

    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super(CajaChicaUpdateView, self).get_context_data(**kwargs)
        context['accion']="Actualizar"
        context['titulo'] = "Caja Chica"
        return context

class CajaChicaDeleteView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('caja_chica.delete_cajachica')
    model = CajaChica
    template_name = "includes/eliminar generico.html"
    success_url = reverse_lazy('caja_chica_app:caja_chica_inicio')

    def get_context_data(self, **kwargs):
        context = super(CajaChicaDeleteView, self).get_context_data(**kwargs)
        context['accion']="Eliminar"
        context['titulo'] = "Caja Chica"
        context['item'] = self.get_object()
        context['dar_baja'] = "true"
        return context


class CajaChicaDetalleView(PermissionRequiredMixin, DetailView):
    permission_required = ('caja_chica.view_cajachica')
    model = CajaChica
    template_name = "caja_chica/caja_chica/detalle.html"
    context_object_name = 'cajachica'

    def get_context_data(self, **kwargs):
        caja_chica = self.get_object()
        caja_chica_pk = CajaChica.objects.get(id = self.kwargs['pk'])
        context = super(CajaChicaDetalleView, self).get_context_data(**kwargs)
        movimientos = movimientos_caja_chica(caja_chica)

        saldo_acumulado = Decimal('0.00')
        for movimiento in movimientos:
            saldo_acumulado = saldo_acumulado + movimiento[3] - movimiento[4]
            movimiento[5] = saldo_acumulado

        context['movimientos'] = movimientos
        context['recibos'] =  ReciboCajaChica.objects.filter(caja_chica=caja_chica_pk)
        context['recibos_servicio'] = ReciboServicio.objects.filter(content_type = ContentType.objects.get_for_model(caja_chica), id_registro = caja_chica.id)

        return context

def CajaChicaDetalleTabla(request, pk):
    data = dict()
    if request.method == 'GET':
        caja_chica = CajaChica.objects.get(id = pk)
        template = 'caja_chica/caja_chica/detalle_tabla.html'
        context = {}

        movimientos = []
        
        #Saldo inicial
        fecha = date(caja_chica.year, caja_chica.month, 1)
        concepto = 'SALDO INICIAL'
        estado = 'ACTIVO'
        ingreso = caja_chica.saldo_inicial
        egreso = Decimal('0.00')
        saldo = Decimal('0.00')
        fila = []
        fila.append(fecha)
        fila.append(concepto)
        fila.append(estado)
        fila.append(ingreso)
        fila.append(egreso)
        fila.append(saldo)
        movimientos.append(fila)

        #Requerimientos
        for requerimiento in Requerimiento.objects.filter(content_type=ContentType.objects.get_for_model(caja_chica), id_registro=caja_chica.id,):

            fecha = requerimiento.fecha
            concepto = requerimiento.concepto
            estado = requerimiento.get_estado_display()
            ingreso = Decimal('0.00')
            egreso = requerimiento.monto
            saldo = Decimal('0.00')
            if requerimiento.estado > 2 and requerimiento.estado != 4:
                concepto = requerimiento.concepto_final
                egreso = requerimiento.monto_final
            if requerimiento.estado == 7:
                egreso = requerimiento.monto_usado
            moneda = requerimiento.moneda
            tipo_cambio = requerimiento.tipo_cambio
            if moneda != caja_chica.moneda:
                if moneda.id == 2: #Dólares
                    egreso = (egreso * tipo_cambio).quantize(Decimal('0.01'))
            fila = []
            fila.append(fecha)
            fila.append(concepto)
            fila.append(estado)
            fila.append(ingreso)
            fila.append(egreso)
            fila.append(saldo)
            movimientos.append(fila)

        movimientos.sort(key = lambda i: i[3], reverse=True)
        movimientos.sort(key = lambda i: i[0])

        # #Recibos Caja Chica

        #________________________________________________________________________________
        saldo_acumulado = Decimal('0.00')
        for movimiento in movimientos:
            saldo_acumulado = saldo_acumulado + movimiento[3] - movimiento[4]
            movimiento[5] = saldo_acumulado

        context['cajachica'] = caja_chica
        context['movimientos'] = movimientos
        context['recibos'] =  ReciboCajaChica.objects.filter(caja_chica=caja_chica)
        context['recibos_servicio'] = ReciboServicio.objects.filter(content_type = ContentType.objects.get_for_model(caja_chica), id_registro = caja_chica.id)

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)


class CajaChicaReciboCreateView(BSModalCreateView):
    model = ReciboCajaChica
    template_name = "includes/formulario generico.html"
    form_class = CajaChicaReciboCrearForm

    def get_success_url(self, **kwargs):
        return reverse_lazy('caja_chica_app:caja_chica_detalle', kwargs={'pk':self.kwargs['cajachica_id']})

    def form_valid(self, form):
        caja =CajaChica.objects.get(id = self.kwargs['cajachica_id'])
        form.instance.caja_chica = caja
        form.instance.moneda = caja.moneda
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)


    def get_context_data(self, **kwargs):
        context = super(CajaChicaReciboCreateView, self).get_context_data(**kwargs)
        context['accion']="Recibo"
        context['titulo']="Caja Chica"
        return context

class CajaChicaReciboDeleteView(BSModalDeleteView):
    model = ReciboCajaChica
    template_name = "includes/eliminar generico.html"

    def get_success_url(self, **kwargs):
        return reverse_lazy('caja_chica_app:caja_chica_detalle', kwargs={'pk':self.kwargs['cajachica_id']})

    def get_context_data(self, **kwargs):
        context = super(CajaChicaReciboDeleteView, self).get_context_data(**kwargs)
        context['accion']="Eliminar"
        context['titulo'] = "Recibo Caja Chica"
        context['item'] = self.get_object().concepto +' - '+str(self.get_object().moneda.simbolo) +' '+ str(self.get_object().monto)
        context['dar_baja'] = "true"
        return context

class CajaChicaReciboPendienteView(BSModalDeleteView):
    model = ReciboCajaChica
    template_name = "includes/eliminar generico.html"

    def get_success_url(self, **kwargs):
        return reverse_lazy('caja_chica_app:caja_chica_detalle', kwargs={'pk':self.kwargs['cajachica_id']})

    def get_context_data(self, **kwargs):
        context = super(CajaChicaReciboPendienteView, self).get_context_data(**kwargs)
        context['accion']=" Cambiar"
        context['titulo'] = "Recibo Caja Chica de estado Borrador a Pendiente "
        context['item'] = self.get_object().concepto +' - '+str(self.get_object().moneda.simbolo) +' '+ str(self.get_object().monto)
        context['dar_baja'] = "true"
        return context

class CajaChicaReciboUpdateView(BSModalUpdateView):
    model = ReciboCajaChica
    template_name = 'includes/formulario generico.html'
    form_class = CajaChicaReciboCrearForm

    def get_success_url(self, **kwargs):
        return reverse_lazy('caja_chica_app:caja_chica_detalle', kwargs={'pk':self.kwargs['cajachica_id']})
    
    def form_valid(self, form):
        caja_chica = CajaChica.objects.get(id=self.kwargs['cajachica_id'])
        caja_chica.save()
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(CajaChicaReciboUpdateView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        context['titulo'] = "Recibo Boleta de Pago"
        return context

    
class CajaChicaReciboServicioAgregarView(BSModalFormView):
    template_name = 'includes/formulario generico.html'
    form_class = CajaChicaReciboServicioAgregarForm

    def get_success_url(self, **kwargs):
        return reverse_lazy('caja_chica_app:caja_chica_detalle', kwargs={'pk':self.kwargs['cajachica_id']})

    @transaction.atomic
    def form_valid(self, form):
        sid = transaction.savepoint()
        try:
            if self.request.session['primero']:
                caja_chica = CajaChica.objects.get(id = self.kwargs['cajachica_id'])
                recibo_servicio = form.cleaned_data.get('recibo_servicio')
                recibo_servicio.content_type = ContentType.objects.get_for_model(caja_chica)
                recibo_servicio.id_registro = caja_chica.id
                registro_guardar(recibo_servicio, self.request)
                recibo_servicio.save()
                self.request.session['primero'] = False
            return super().form_valid(form)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_form_kwargs(self):
        recibos = ReciboServicio.objects.filter(content_type = None, id_registro = None)
        kwargs = super().get_form_kwargs()
        kwargs['recibos'] = recibos
        return kwargs

    def get_context_data(self, **kwargs):
        self.request.session['primero'] = True
        context = super(CajaChicaReciboServicioAgregarView, self).get_context_data(**kwargs)
        context['accion'] = 'Agregar'
        context['titulo'] = 'Recibo Servicio'
        return context

class CajaChicaReciboServicioUpdateView(BSModalUpdateView):
    model = ReciboServicio
    template_name = 'includes/formulario generico.html'
    form_class = CajaChicaReciboServicioUpdateForm

    def get_success_url(self, **kwargs):
        return reverse_lazy('caja_chica_app:caja_chica_detalle', kwargs={'pk':self.kwargs['cajachica_id']})
    
    def form_valid(self, form):
        caja_chica = CajaChica.objects.get(id=self.kwargs['cajachica_id'])
        recibo_servicio = ReciboServicio.objects.filter(
            content_type = ContentType.objects.get_for_model(caja_chica),
            id_registro = caja_chica.id,
            ).filter(
                ~Q(id=form.instance.id)
                )
        monto_usado = 0
        if recibo_servicio:
            for boleta_pago in recibo_servicio:
                monto_usado += boleta_pago.monto_pagado
        caja_chica.monto_usado = monto_usado + form.cleaned_data.get('monto_pagado')
        caja_chica.save()
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(CajaChicaReciboServicioUpdateView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        context['titulo'] = "Recibo Boleta de Pago"
        return context


class CajaChicaPdfView(View):
    def get(self, request, *args, **kwargs):
        caja = CajaChica.objects.get(id = kwargs['pk'])
        movimientos = movimientos_caja_chica(caja)
        
        titulo = 'Cierre de caja - %s - %s' % (caja.periodo, nombre_usuario(caja.usuario))
        vertical = False
        sociedad_MPL = Sociedad.objects.get(abreviatura='MPL')
        sociedad_MCA = Sociedad.objects.get(abreviatura='MCA')
        color = COLOR_DEFAULT
        logo = [sociedad_MPL.logo.url, sociedad_MCA.logo.url]
        pie_pagina = PIE_DE_PAGINA_DEFAULT
        buf = generarCajaChicaPdf(titulo, vertical, logo, pie_pagina, movimientos, caja, color)

        respuesta = HttpResponse(buf.getvalue(), content_type='application/pdf')
        respuesta.headers['content-disposition']='inline; filename=%s.pdf' % titulo
        
        return respuesta



#__CajaChicaPrestamo_____________________________________________________________________
class CajaChicaPrestamoListView(ListView):
    model = CajaChicaPrestamo
    template_name = "caja_chica/prestamo/inicio.html"
    context_object_name = 'contexto_prestamo'
    
def CajaChicaPrestamoTabla(request):
    data = dict()
    if request.method == 'GET':
        template = 'caja_chica/prestamo/inicio_tabla.html'
        context = {}
        context['contexto_prestamo'] = CajaChicaPrestamo.objects.all()

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)

class CajaChicaPrestamoCreateView(BSModalCreateView):
    model = CajaChicaPrestamo
    template_name = "includes/formulario generico.html"
    form_class = CajaChicaPrestamoCrearForm
    success_url = reverse_lazy('caja_chica_app:prestamo_inicio')

    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super(CajaChicaPrestamoCreateView, self).get_context_data(**kwargs)
        context['accion']="Prestamo"
        context['titulo']="Caja Chica"
        return context

class CajaChicaPrestamoUpdateView(BSModalUpdateView):
    model = CajaChicaPrestamo
    template_name = "includes/formulario generico.html"
    form_class = CajaChicaPrestamoCrearForm
    success_url = reverse_lazy('caja_chica_app:prestamo_inicio')

    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super(CajaChicaPrestamoUpdateView, self).get_context_data(**kwargs)
        context['accion']="Actualizar"
        context['titulo'] = "Prestamo Caja Chica"
        return context

class CajaChicaPrestamoDeleteView(BSModalDeleteView):
    model = CajaChicaPrestamo
    template_name = "includes/eliminar generico.html"
    success_url = reverse_lazy('caja_chica_app:prestamo_inicio')

    def get_context_data(self, **kwargs):
        context = super(CajaChicaPrestamoDeleteView, self).get_context_data(**kwargs)
        context['accion']="Eliminar"
        context['titulo'] = "Prestamo Caja Chica"
        context['item'] = self.get_object()
        context['dar_baja'] = "true"
        return context


#__ReciboCajaChica_________________________________________________
class ReciboCajaChicaListView(ListView):
    model = ReciboCajaChica
    template_name = "caja_chica/recibo/inicio.html"
    context_object_name = 'contexto_recibo'    

def ReciboCajaChicaTabla(request):
    data = dict()
    if request.method == 'GET':
        template = 'caja_chica/recibo/inicio_tabla.html'
        context = {}
        context['contexto_recibo'] = ReciboCajaChica.objects.all()

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)

class ReciboCajaChicaCreateView(BSModalCreateView):
    model = ReciboCajaChica
    template_name = "includes/formulario generico.html"
    form_class = ReciboCajaChicaCrearForm
    success_url = reverse_lazy('caja_chica_app:recibo_inicio')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['caja_chica'] = CajaChica.objects.filter(estado=1, usuario=self.request.user)
        return kwargs

    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super(ReciboCajaChicaCreateView, self).get_context_data(**kwargs)
        context['accion']="Recibo"
        context['titulo']="Caja Chica"
        return context

class ReciboCajaChicaUpdateView(BSModalUpdateView):
    model = ReciboCajaChica
    template_name = "includes/formulario generico.html"
    form_class = ReciboCajaChicaCrearForm
    success_url = reverse_lazy('caja_chica_app:recibo_inicio')

    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['caja_chica'] = CajaChica.objects.filter(estado=1, usuario=self.request.user)
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super(ReciboCajaChicaUpdateView, self).get_context_data(**kwargs)
        context['accion']="Actualizar"
        context['titulo'] = "Recibo Caja Chica"
        return context

class ReciboCajaChicaDeleteView(BSModalDeleteView):
    model = ReciboCajaChica
    template_name = "includes/eliminar generico.html"
    success_url = reverse_lazy('caja_chica_app:recibo_inicio')

    def get_context_data(self, **kwargs):
        context = super(ReciboCajaChicaDeleteView, self).get_context_data(**kwargs)
        context['accion']="Eliminar"
        context['titulo'] = "Recibo Caja Chica"
        context['item'] = self.get_object()
        context['dar_baja'] = "true"
        return context


#__CajaChica_Requerimientos_____________
class CajaChicaRequerimientoView(DetailView):
    model = CajaChica
    template_name = "caja_chica/caja_chica_requerimiento/inicio.html"
    context_object_name = 'contexto_caja_detalle'

    def get_context_data(self, **kwargs):
        caja = CajaChica.objects.get(id = self.kwargs['pk'])
        context = super(CajaChicaRequerimientoView, self).get_context_data(**kwargs)
        # context['contexto_requerimientos'] = Requerimiento.objects.filter(content_type = ContentType.objects.get_for_model(caja), id_registro = caja.id)
        context['contexto_usuario_pedido'] = Requerimiento.objects.filter(usuario_pedido = caja.usuario)

        return context

def CajaChicaRequerimientoTabla(request, pk):
    data = dict()
    if request.method == 'GET':
        template = 'caja_chica/caja_chica_requerimiento/inicio_tabla.html'
        context = {}
        caja = CajaChica.objects.get(id = pk)
        # context['contexto_requerimientos'] = Requerimiento.objects.filter(content_type = ContentType.objects.get_for_model(caja), id_registro = caja.id)
        context['contexto_usuario_pedido'] = Requerimiento.objects.filter(usuario_pedido = caja.usuario)

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)
