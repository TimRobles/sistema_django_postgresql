from applications.funciones import registrar_excepcion
from applications.importaciones import *
from django.shortcuts import render
from django.core.paginator import Paginator
from django.utils import timezone


from .models import (
    DatosUsuario,
    HistoricoUser,
    Vacaciones,
    VacacionesDetalle,
    )

from .forms import (
    DatosUsuarioForm,
    HistoricoUserCreateForm,
    UserPasswordForm,
    HistoricoUserDarBajaForm,
    HistoricoUserDarAltaForm,
    VacacionesBuscarForm,
    VacacionesDetalleForm,
    VacacionesForm,
    VacacionesDetalleForm,
    VacacionesDetalleActualizarForm,
    )

class DatosUsuarioView(LoginRequiredMixin, FormView):
    template_name = "usuario/datos_usuario/update.html"
    form_class = DatosUsuarioForm
    success_url = reverse_lazy('home_app:home')

    def get_form(self, form_class=form_class):
        try:
            contact = DatosUsuario.objects.get(usuario=self.request.user)
            return form_class(instance=contact, **self.get_form_kwargs())
        except DatosUsuario.DoesNotExist:
            return form_class(**self.get_form_kwargs())

    def get_form_kwargs(self):
        kwargs = super(DatosUsuarioView, self).get_form_kwargs()
        kwargs['usuario'] = self.request.user
        return kwargs

    @transaction.atomic
    def form_valid(self, form):
        sid = transaction.savepoint()
        try:
            User = get_user_model()
            usuario_buscar=User.objects.get(id=self.request.user.id)
            form.instance.usuario = self.request.user
            if form.instance.created_by == None:
                form.instance.created_by = self.request.user
            form.instance.updated_by = self.request.user

            usuario_buscar.first_name = self.request.POST['nombres']
            usuario_buscar.last_name = self.request.POST['apellidos']
            usuario_buscar.email = self.request.POST['correo']
            
            usuario_buscar.save()
            form.save()
            messages.success(self.request, 'Datos actualizados correctamente')

            return super(DatosUsuarioView, self).form_valid(form)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())
        
class UserPasswordView(FormView):
    template_name = "usuario/datos_usuario/cambio contraseña.html"
    form_class = UserPasswordForm
    success_url = reverse_lazy('home_app:home')

    @transaction.atomic
    def form_valid(self, form):
        sid = transaction.savepoint()
        try:
            usuario = self.request.user
            nuevo_password = form.cleaned_data['password2']
            usuario.set_password(nuevo_password)
            usuario.save()
            user = authenticate(
                username = usuario.username,
                password = nuevo_password,
            )
            login(self.request, user)
            return super(UserPasswordView, self).form_valid(form)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_form_kwargs(self):
        kwargs = super(UserPasswordView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs   


class HistoricoUserListView(PermissionRequiredMixin, ListView):
    permission_required = ('usuario.view_historicouser')
    model = HistoricoUser
    template_name = "usuario/historico_user/list.html"
    context_object_name = 'contexto_historicouser'

    def get_queryset(self):
        queryset = super(HistoricoUserListView, self).get_queryset()
        queryset = HistoricoUser.objects.exclude(estado = 3)
        return queryset

def HistoricoUserTabla(request):
    data = dict()
    if request.method == 'GET':
        template = 'usuario/historico_user/list_tabla.html'
        context = {}
        context['contexto_historicouser'] = HistoricoUser.objects.exclude(estado = 3)

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)

class HistoricoUserDarBajaView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('usuario.change_historicouser')
    model = HistoricoUser
    template_name = "includes/formulario generico.html"
    form_class = HistoricoUserDarBajaForm
    success_url = reverse_lazy('usuario_app:historico_usuarios')
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)    

    @transaction.atomic
    def form_valid(self, form):
        sid = transaction.savepoint()
        try:
            form.instance.estado = 2
            form.instance.usuario.is_active = False
            form.instance.usuario.save()
            registro_guardar(form.instance, self.request)
            
            return super().form_valid(form)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())
    
    def get_context_data(self, **kwargs):
        context = super(HistoricoUserDarBajaView, self).get_context_data(**kwargs)
        context['accion'] = 'Dar de Baja'
        context['titulo'] = 'Historico Usuario'
        return context
    
class HistoricoUserDarAltaView(PermissionRequiredMixin, BSModalCreateView):
    permission_required = ('usuario.add_historicouser')
    template_name = "includes/formulario generico.html"
    form_class = HistoricoUserDarAltaForm
    success_url = reverse_lazy('usuario_app:historico_usuarios')
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs) 

    @transaction.atomic
    def form_valid(self, form):
        sid = transaction.savepoint()
        try:
            usuario = get_user_model()
            
            buscar_usuario = usuario.objects.get(id = self.kwargs['usuario'])
            form.instance.usuario = buscar_usuario
            historico = HistoricoUser.objects.filter(
                usuario = buscar_usuario,
                estado = 2,
            )
            if historico:
                historico = historico.latest('id')
                historico.estado = 3
                buscar_usuario.is_active = True
                buscar_usuario.save()
                registro_guardar(historico, self.request)
                historico.save()

            registro_guardar(form.instance, self.request)
            
            return super().form_valid(form)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())        

    def get_form_kwargs(self):
        usuario = get_user_model()
        historico = HistoricoUser.objects.filter(
            usuario = usuario.objects.get(id = self.kwargs['usuario']),
            estado = 2,
        )
        kwargs = super(HistoricoUserDarAltaView, self).get_form_kwargs()
        if historico:
            kwargs['fecha_baja'] = historico.latest('id').fecha_baja
        else:
            kwargs['fecha_baja'] = None
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(HistoricoUserDarAltaView, self).get_context_data(**kwargs)
        context['accion'] = 'Dar de Alta'
        context['titulo'] = 'Historico Usuario'
        return context


class HistoricoDetailView(DetailView):
    model = get_user_model()
    template_name = "usuario/historico_user/detail.html"
    context_object_name = 'contexto_historico_user'

    def get_context_data(self, **kwargs):
        # context = super().get_context_data(**kwargs)
        context = super(HistoricoDetailView, self).get_context_data(**kwargs)

        historico_user = HistoricoUser.objects.filter(usuario=self.kwargs['pk'])
        datos_usuario = DatosUsuario.objects.select_related('usuario').filter(usuario=self.kwargs['pk'])
        vacaciones_usuario = Vacaciones.objects.select_related('usuario').filter(usuario=self.kwargs['pk'])

        context['historico_user'] = historico_user
        context['datos_usuario'] = datos_usuario
        context['vacaciones_usuario'] = vacaciones_usuario

        return context

def HistoricoDetailTabla(request, pk):
    data = dict()
    if request.method == 'GET':
        template = 'usuario/historico_user/detail_tabla.html'
        context = {}
        
        historico_user = HistoricoUser.objects.filter(usuario=pk)
        datos_usuario = DatosUsuario.objects.select_related('usuario').filter(usuario=pk)
        vacaciones_usuario = Vacaciones.objects.select_related('usuario').filter(usuario=pk)

        context['contexto_historico_user'] = historico_user
        context['historico_user'] = historico_user
        context['datos_usuario'] = datos_usuario
        context['vacaciones_usuario'] = vacaciones_usuario

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)


class HistoricoUserCreateView(PermissionRequiredMixin, BSModalCreateView):
    permission_required = ('usuario.add_historicouser')
    template_name = "includes/formulario generico.html"
    form_class = HistoricoUserCreateForm
    success_url = reverse_lazy('usuario_app:historico_usuarios')
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs) 

    @transaction.atomic
    def form_valid(self, form):
        sid = transaction.savepoint()
        try:
            form.instance.fecha_baja = None
            registro_guardar(form.instance, self.request)
            
            return super().form_valid(form)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())        

    def get_context_data(self, **kwargs):
        context = super(HistoricoUserCreateView, self).get_context_data(**kwargs)
        context['accion'] = 'Registrar'
        context['titulo'] = 'Historico Usuario'
        return context
    
    ################################# V A C A C I O N E S ################################################

class VacacionesListView(FormView):
    template_name = "usuario/vacaciones_usuario/inicio.html"
    form_class = VacacionesBuscarForm
    success_url = '.'

    def get_form_kwargs(self):
        kwargs = super(VacacionesListView, self).get_form_kwargs()
        kwargs['filtro_estado'] = self.request.GET.get('estado')
        kwargs['filtro_usuario'] = self.request.GET.get('usuario')
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(VacacionesListView,self).get_context_data(**kwargs)
        vacaciones = Vacaciones.objects.all()
        
        filtro_estado = self.request.GET.get('estado')
        filtro_usuario = self.request.GET.get('usuario')
        
        contexto_filtro = []   
        
        if filtro_estado:
            condicion = Q(estado = filtro_estado)
            vacaciones = vacaciones.filter(condicion)
            contexto_filtro.append(f"estado={filtro_estado}")

        if filtro_usuario:
            condicion = Q(usuario = filtro_usuario)
            vacaciones = vacaciones.filter(condicion)
            contexto_filtro.append(f"usuario={filtro_usuario}")

        context['contexto_filtro'] = "&".join(contexto_filtro)

        context['pagina_filtro'] = ""
        if self.request.GET.get('page'):
            if context['contexto_filtro']:
                context['pagina_filtro'] = f'&page={self.request.GET.get("page")}'
            else:
                context['pagina_filtro'] = f'page={self.request.GET.get("page")}'
        context['contexto_filtro'] = '?' + context['contexto_filtro']

        objectsxpage =  20

        if len(vacaciones) > objectsxpage:
            paginator = Paginator(vacaciones, objectsxpage)
            page_number = self.request.GET.get('page')
            vacaciones = paginator.get_page(page_number)
   
        context['contexto_pagina'] = vacaciones
        context['contexto_vacaciones'] = vacaciones
        context['today'] = timezone.now().date().strftime('%d/%m/%Y')
        print('today',context['today'])
        return context

def VacacionesTabla(request):
    data = dict()
    if request.method == 'GET':
        template = 'usuario/vacaciones_usuario/inicio_tabla.html'
        context = {}
        vacaciones = Vacaciones.objects.all()

        filtro_estado = request.GET.get('estado')
        filtro_usuario = request.GET.get('usuario')

        contexto_filtro = []

        if filtro_estado:
            condicion = Q(estado = filtro_estado)
            vacaciones = vacaciones.filter(condicion)
            contexto_filtro.append(f"estado={filtro_estado}")

        if filtro_usuario:
            condicion = Q(usuario = filtro_usuario)
            vacaciones = vacaciones.filter(condicion)
            contexto_filtro.append(f"usuario={filtro_usuario}")

        context['contexto_filtro'] = "&".join(contexto_filtro)

        context['pagina_filtro'] = ""
        if request.GET.get('page'):
            if context['contexto_filtro']:
                context['pagina_filtro'] = f'&page={request.GET.get("page")}'
            else:
                context['pagina_filtro'] = f'page={request.GET.get("page")}'
        context['contexto_filtro'] = '?' + context['contexto_filtro']

        objectsxpage =  20

        if len(vacaciones) > objectsxpage:
            paginator = Paginator(vacaciones, objectsxpage)
            page_number = request.GET.get('page')
            vacaciones = paginator.get_page(page_number)
   
        context['contexto_pagina'] = vacaciones
        context['contexto_vacaciones'] = vacaciones
        context['today'] = timezone.now().date().strftime('%d/%m/%Y')
        print('today',context['today'])

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)


class VacacionesDetailView(DetailView):
    model = Vacaciones
    template_name = "usuario/vacaciones_usuario/detalle.html"
    context_object_name = 'contexto_vacaciones'

    def get_context_data(self, **kwargs):
        vacaciones = Vacaciones.objects.get(id = self.kwargs['pk'])

        context = super(VacacionesDetailView, self).get_context_data(**kwargs)
        context['contexto_vacaciones'] = vacaciones
        context['detalle_vacaciones'] = VacacionesDetalle.objects.filter(vacaciones = vacaciones)
        
        return context
    
def VacacionesDetailTabla(request, pk):
    data = dict()
    if request.method == 'GET':
        template = 'usuario/vacaciones_usuario/detalle_tabla.html'
        context = {}
        vacaciones = Vacaciones.objects.get(id = pk)

        context['contexto_vacaciones'] = vacaciones
        context['detalle_vacaciones'] = VacacionesDetalle.objects.filter(vacaciones = vacaciones)

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)


class VacacionesCreateView(BSModalCreateView):
    model = Vacaciones
    template_name = "includes/formulario generico.html"
    form_class = VacacionesForm
    success_url = reverse_lazy('usuario_app:vacaciones_inicio')

    @transaction.atomic
    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(VacacionesCreateView, self).get_context_data(**kwargs)
        context['accion'] = "Registrar"
        context['titulo'] = "Vacaciones"
        return context

class VacacionesDetalleCreateView(BSModalCreateView):
    model = VacacionesDetalle
    template_name = "includes/formulario generico.html"
    form_class = VacacionesDetalleForm

    def get_success_url(self, **kwargs):
        return reverse_lazy('usuario_app:vacaciones_detalle', kwargs={'pk':self.kwargs['pk']})

    def form_valid(self, form):
        # Obtenemos la instancia de Vacaciones
        vacaciones_instance = Vacaciones.objects.get(id=self.kwargs['pk'])
        form.instance.vacaciones = vacaciones_instance
        
        # Actualizamos el estado de Vacaciones a 2
        form.instance.vacaciones.estado = 2
        form.instance.vacaciones.save()

        # Guardamos el registro
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['usuario'] = Vacaciones.objects.get(id=self.kwargs['pk']).usuario  # Pasa el usuario al formulario
        kwargs['dias_restantes'] = Vacaciones.objects.get(id=self.kwargs['pk']).dias_restantes  
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super(VacacionesDetalleCreateView, self).get_context_data(**kwargs)
        context['accion']="Registrar"
        context['titulo']="Dias"
        return context
    

class VacacionesDetalleUpdateView(BSModalUpdateView):
    model = VacacionesDetalle
    template_name = "includes/formulario generico.html"
    form_class = VacacionesDetalleActualizarForm
    success_url = '.'
    
    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(VacacionesDetalleUpdateView, self).get_context_data(**kwargs)
        context['accion']="Actualizar"
        context['titulo']="Días"
        return context

class VacacionesDetalleDeleteView(BSModalDeleteView):
    model = VacacionesDetalle
    template_name = "includes/eliminar generico.html"
    # success_url = '.'
    def get_success_url(self, **kwargs):
        return reverse_lazy('usuario_app:vacaciones_detalle', kwargs={'pk':self.object.vacaciones.id})

    def get_context_data(self, **kwargs):
        context = super(VacacionesDetalleDeleteView, self).get_context_data(**kwargs)
        context['accion']="Eliminar"
        context['titulo']="Registro"
        return context

    print("H O L A")