from applications.funciones import registrar_excepcion
from applications.importaciones import *
from .forms import (
    SedeCreateForm, SedeUpdateForm
    )
from .models import (
    Sede,
    )

class SedeListView(PermissionRequiredMixin, ListView):
    permission_required = ('sede.view_sede')
    model = Sede
    template_name = "sede/sede/inicio.html"
    context_object_name = 'contexto_sede'

def SedeTabla(request):
    data = dict()
    if request.method == 'GET':
        template = 'sede/sede/inicio_tabla.html'
        context = {}
        context['contexto_sede'] = Sede.objects.all()

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)

class SedeCreateView(PermissionRequiredMixin, BSModalCreateView):
    permission_required = ('sede.add_sede')
    model = Sede
    template_name = "sede/sede/form.html"
    form_class = SedeCreateForm
    success_url = reverse_lazy('sede_app:sede_inicio')
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(SedeCreateView, self).get_context_data(**kwargs)
        context['accion']="Registrar"
        context['titulo']="Sede"
        return context

    def form_valid(self, form):

        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)

        return super().form_valid(form)

class SedeUpdateView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('sede.change_sede')
    model = Sede
    template_name = "sede/sede/form.html"
    form_class = SedeUpdateForm
    success_url = reverse_lazy('sede_app:sede_inicio')
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(SedeUpdateView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        context['titulo'] = "Sede"
        return context

    def form_valid(self, form):

        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)
        
        return super().form_valid(form)

class SedeDarBajaView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('sede.delete_sede')
    model = Sede
    template_name = "includes/eliminar generico.html"
    success_url = reverse_lazy('sede_app:sede_inicio')
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            self.object = self.get_object()
            self.object.estado = 2
            registro_guardar(self.object, self.request)
            self.object.save()
            messages.success(request, MENSAJE_DAR_BAJA)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(SedeDarBajaView, self).get_context_data(**kwargs)
        context['accion'] = "Dar Baja"
        context['titulo'] = "Sede"
        context['dar_baja'] = "true"
        context['item'] = self.object.nombre
        return context

class SedeDarAltaView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('sede.delete_sede')
    model = Sede
    template_name = "includes/eliminar generico.html"
    success_url = reverse_lazy('sede_app:sede_inicio')
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            self.object = self.get_object()
            self.object.estado = 1
            registro_guardar(self.object, self.request)
            self.object.save()
            messages.success(request, MENSAJE_DAR_ALTA)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(SedeDarAltaView, self).get_context_data(**kwargs)
        context['accion']="Dar Alta"
        context['titulo'] = "Sede"
        context['dar_baja'] = "true"
        context['item'] = self.object.nombre
        return context
