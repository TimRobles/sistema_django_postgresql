from applications.funciones import registrar_excepcion
from applications.importaciones import *
from .forms import (
    CorreoInterlocutorDarBajaForm,
    CorreoInterlocutorForm,
    InterlocutorProveedorUpdateForm,
    ProveedorForm, 
    InterlocutorProveedorForm,
    TelefonoInterlocutorDarBajaForm,
    TelefonoInterlocutorForm,
    )
from .models import (
    CorreoInterlocutorProveedor,
    InterlocutorProveedor,
    Proveedor,
    ProveedorInterlocutor,
    TelefonoInterlocutorProveedor,
    )

class ProveedorListView(PermissionRequiredMixin, ListView):
    permission_required = ('proveedores.view_proveedor')
    model = Proveedor
    template_name = "proveedores/proveedor/inicio.html"
    context_object_name = 'contexto_proveedores'

def ProveedorTabla(request):
    data = dict()
    if request.method == 'GET':
        template = 'proveedores/proveedor/inicio_tabla.html'
        context = {}
        context['contexto_proveedores'] = Proveedor.objects.all()

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)

class ProveedorCreateView(PermissionRequiredMixin, BSModalCreateView):
    permission_required = ('proveedores.add_proveedor')
    model = Proveedor
    template_name = "proveedores/proveedor/form.html"
    form_class = ProveedorForm
    success_url = reverse_lazy('proveedores_app:proveedor_inicio')

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ProveedorCreateView, self).get_context_data(**kwargs)
        context['accion']="Registrar"
        context['titulo']="Proveedor"
        return context

    def form_valid(self, form):

        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)

        return super().form_valid(form)

class ProveedorUpdateView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('proveedores.change_proveedor')
    model = Proveedor
    template_name = "includes/formulario generico.html"
    form_class = ProveedorForm
    success_url = reverse_lazy('proveedores_app:proveedor_inicio')

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ProveedorUpdateView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        context['titulo'] = "Proveedor"
        return context

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)
        
        return super().form_valid(form)

class ProveedorDarBajaView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('proveedores.change_proveedor')
    model = Proveedor
    template_name = "includes/eliminar generico.html"
    success_url = reverse_lazy('proveedores_app:proveedor_inicio')

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
        context = super(ProveedorDarBajaView, self).get_context_data(**kwargs)
        context['accion'] = "Dar Baja"
        context['titulo'] = "Proveedor"
        context['dar_baja'] = "true"
        context['item'] = self.object.nombre
        return context

class ProveedorDarAltaView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('proveedores.change_proveedor')
    model = Proveedor
    template_name = "includes/eliminar generico.html"
    success_url = reverse_lazy('proveedores_app:proveedor_inicio')

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
        context = super(ProveedorDarAltaView, self).get_context_data(**kwargs)
        context['accion']="Dar Alta"
        context['titulo'] = "Proveedor"
        context['dar_baja'] = "true"
        context['item'] = self.object.nombre
        return context

class ProveedorDetailView(PermissionRequiredMixin, DetailView):
    permission_required = ('proveedores.view_proveedorinterlocutor')
    model = Proveedor
    template_name = "proveedores/proveedor/detalle.html"
    context_object_name = 'contexto_proveedores'

    def get_context_data(self, **kwargs):
        proveedor = Proveedor.objects.get(id = self.kwargs['pk'])
        context = super(ProveedorDetailView, self).get_context_data(**kwargs)
        context['interlocutores'] = ProveedorInterlocutor.objects.filter(proveedor = proveedor)
        return context

def ProveedorDetailTabla(request, pk):
    data = dict()
    if request.method == 'GET':
        template = 'proveedores/proveedor/detalle_tabla.html'
        context = {}
        proveedor = Proveedor.objects.get(id = pk)
        context['contexto_proveedores'] = proveedor
        context['interlocutores'] = ProveedorInterlocutor.objects.filter(proveedor = proveedor)
        
        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)

class InterlocutorProveedorCreateView(PermissionRequiredMixin, BSModalFormView):
    permission_required = ('proveedores.add_interlocutorproveedor')
    template_name = "includes/formulario generico.html"
    form_class = InterlocutorProveedorForm

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)
    
    def get_success_url(self, **kwargs):
        return reverse_lazy('proveedores_app:proveedor_detalle', kwargs={'pk':self.kwargs['proveedor_id']})

    @transaction.atomic
    def form_valid(self, form):
        sid = transaction.savepoint()
        try:
            nombres = form.cleaned_data['nombres']
            apellidos = form.cleaned_data['apellidos']
            proveedor = Proveedor.objects.get(id = self.kwargs['proveedor_id'])

            interlocutor, existe = InterlocutorProveedor.objects.get_or_create(
                nombres = nombres.upper(),
                apellidos = apellidos.upper(),
            )
            if not existe:
                interlocutor.created_by = self.request.user
                interlocutor.updated_by = self.request.user
                interlocutor.save()

            relacion, existe = ProveedorInterlocutor.objects.get_or_create(
                interlocutor = interlocutor,
                proveedor = proveedor,
            )

            if not existe:
                relacion.created_by = self.request.user
                relacion.updated_by = self.request.user
                relacion.save()

            return super().form_valid(form) 
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(InterlocutorProveedorCreateView, self).get_context_data(**kwargs)
        context['accion']="Registrar"
        context['titulo']="Interlocutor Proveedor"
        return context

class InterlocutorProveedorUpdateView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('proveedores.change_interlocutorproveedor')
    model = InterlocutorProveedor
    template_name = "includes/formulario generico.html"
    form_class = InterlocutorProveedorUpdateForm

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('home_app:home')

    def get_context_data(self, **kwargs):
        context = super(InterlocutorProveedorUpdateView, self).get_context_data(**kwargs)
        context['accion']="Actualizar"
        context['titulo']="Interlocutor"
        return context
    
    def form_valid(self, form):
        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)

        return super().form_valid(form)

class InterlocutorProveedorDarBajaView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('proveedores.change_proveedorinterlocutor')
    model = ProveedorInterlocutor
    template_name = "includes/eliminar generico.html"

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('proveedores_app:proveedor_detalle', kwargs={'pk':self.object.proveedor.id})

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
        context = super(InterlocutorProveedorDarBajaView, self).get_context_data(**kwargs)
        context['accion'] = "Dar Baja"
        context['titulo'] = "Interlocutor"
        context['dar_baja'] = "true"
        context['item'] = self.object.interlocutor
        return context

class InterlocutorProveedorDarAltaView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('proveedores.change_proveedorinterlocutor')
    model = ProveedorInterlocutor
    template_name = "includes/eliminar generico.html"

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('proveedores_app:proveedor_detalle', kwargs={'pk':self.object.proveedor.id})

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
        context = super(InterlocutorProveedorDarAltaView, self).get_context_data(**kwargs)
        context['accion']="Dar Alta"
        context['titulo'] = "Interlocutor"
        context['dar_baja'] = "true"
        context['item'] = self.object.interlocutor
        return context

class InterlocutorProveedorDetailView(PermissionRequiredMixin, DetailView):
    permission_required = ('proveedores.view_interlocutorproveedor')
    model = InterlocutorProveedor
    template_name = "proveedores/interlocutor/detalle.html"
    context_object_name = 'contexto_interlocutores'

    def get_context_data(self, **kwargs):
        interlocutor = InterlocutorProveedor.objects.get(id = self.kwargs['pk'])
        context = super(InterlocutorProveedorDetailView, self).get_context_data(**kwargs)
        context['telefonos'] = TelefonoInterlocutorProveedor.objects.filter(interlocutor = interlocutor)
        context['correos'] = CorreoInterlocutorProveedor.objects.filter(interlocutor = interlocutor)
        return context

def InterlocutorProveedorDetailTabla(request, pk):
    data = dict()
    if request.method == 'GET':
        template = 'proveedores/interlocutor/detalle_tabla.html'
        context = {}
        interlocutor = InterlocutorProveedor.objects.get(id = pk)
        context['contexto_interlocutores'] = interlocutor
        context['telefonos'] = TelefonoInterlocutorProveedor.objects.filter(interlocutor = interlocutor)
        context['correos'] = CorreoInterlocutorProveedor.objects.filter(interlocutor = interlocutor)
        
        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)

class TelefonoInterlocutorCreateView(PermissionRequiredMixin, BSModalCreateView):
    permission_required = ('proveedores.add_telefonointerlocutorproveedor')
    model = TelefonoInterlocutorProveedor
    template_name = "includes/formulario generico.html"
    form_class = TelefonoInterlocutorForm

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)
    
    def get_success_url(self, **kwargs):
        return reverse_lazy('proveedores_app:interlocutor_detalle', kwargs={'pk':self.kwargs['interlocutor_id']})

    def form_valid(self, form):
        form.instance.interlocutor = InterlocutorProveedor.objects.get(id = self.kwargs['interlocutor_id'])

        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(TelefonoInterlocutorCreateView, self).get_context_data(**kwargs)
        context['accion']="Registrar"
        context['titulo']="Teléfono"
        return context

class TelefonoInterlocutorUpdateView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('proveedores.change_telefonointerlocutorproveedor')
    model = TelefonoInterlocutorProveedor
    template_name = "includes/formulario generico.html"
    form_class = TelefonoInterlocutorForm

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('proveedores_app:interlocutor_detalle', kwargs={'pk':self.object.interlocutor.id})

    def get_context_data(self, **kwargs):
        context = super(TelefonoInterlocutorUpdateView, self).get_context_data(**kwargs)
        context['accion']="Actualizar"
        context['titulo']="Teléfono"
        return context
    
    def form_valid(self, form):
        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)

        return super().form_valid(form)

class TelefonoInterlocutorDarBajaView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('proveedores.change_telefonointerlocutorproveedor')
    model = TelefonoInterlocutorProveedor
    template_name = "includes/formulario generico.html"
    form_class = TelefonoInterlocutorDarBajaForm

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('proveedores_app:interlocutor_detalle', kwargs={'pk':self.object.interlocutor.id})

    def form_valid(self, form):
        form.instance.estado = 2
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(TelefonoInterlocutorDarBajaView, self).get_context_data(**kwargs)
        context['accion']="Dar Baja"
        context['titulo']="Teléfono"
        return context

class CorreoInterlocutorCreateView(PermissionRequiredMixin, BSModalCreateView):
    permission_required = ('proveedores.add_correointerlocutorproveedor')
    model = CorreoInterlocutorProveedor
    template_name = "includes/formulario generico.html"
    form_class = CorreoInterlocutorForm

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)
    
    def get_success_url(self, **kwargs):
        return reverse_lazy('proveedores_app:interlocutor_detalle', kwargs={'pk':self.kwargs['interlocutor_id']})

    def form_valid(self, form):
        form.instance.interlocutor = InterlocutorProveedor.objects.get(id = self.kwargs['interlocutor_id'])

        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(CorreoInterlocutorCreateView, self).get_context_data(**kwargs)
        context['accion']="Registrar"
        context['titulo']="Correo"
        return context

class CorreoInterlocutorUpdateView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('proveedores.change_correointerlocutorproveedor')
    model = CorreoInterlocutorProveedor
    template_name = "includes/formulario generico.html"
    form_class = CorreoInterlocutorForm

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('proveedores_app:interlocutor_detalle', kwargs={'pk':self.object.interlocutor.id})

    def get_context_data(self, **kwargs):
        context = super(CorreoInterlocutorUpdateView, self).get_context_data(**kwargs)
        context['accion']="Actualizar"
        context['titulo']="Correo"
        return context
    
    def form_valid(self, form):
        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)

        return super().form_valid(form)

class CorreoInterlocutorDarBajaView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('proveedores.change_correointerlocutorproveedor')
    model = CorreoInterlocutorProveedor
    template_name = "includes/formulario generico.html"
    form_class = CorreoInterlocutorDarBajaForm

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('proveedores_app:interlocutor_detalle', kwargs={'pk':self.object.interlocutor.id})

    def form_valid(self, form):
        form.instance.estado = 2
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(CorreoInterlocutorDarBajaView, self).get_context_data(**kwargs)
        context['accion']="Dar Baja"
        context['titulo']="Correo"
        return context

class CorreoInterlocutorDarAltaView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('proveedores.change_correointerlocutorproveedor')
    model = CorreoInterlocutorProveedor
    template_name = "includes/form generico.html"

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('proveedores_app:interlocutor_detalle', kwargs={'pk':self.get_object().interlocutor.id})

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            obj = self.get_object()
            obj.fech_baja = None
            obj.estado = 1
            registro_guardar(obj, self.request)
            obj.save()
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(CorreoInterlocutorDarAltaView, self).get_context_data(**kwargs)
        context['accion'] = "Dar Alta"
        context['titulo'] = "Correo"
        context['texto'] = "¿Seguro que desea dar de alta al correo?"
        context['item'] = self.get_object()
        return context