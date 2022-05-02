from applications.importaciones import *

from .models import (
    DatosUsuario,
    HistoricoUser,
    )

from .forms import (
    DatosUsuarioForm,
    UserPasswordForm,
    HistoricoUserDarBajaForm,
    HistoricoUserDarAltaForm,
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

    def form_valid(self, form):
        User = get_user_model()
        usuario_buscar=User.objects.get(id=self.request.user.id)
        form.instance.usuario = self.request.user
        if form.instance.created_by == None:
            form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user

        usuario_buscar.first_name = self.request.POST['Nombres']
        usuario_buscar.last_name = self.request.POST['Apellidos']
        usuario_buscar.email = self.request.POST['Correo']
        
        usuario_buscar.save()
        form.save()
        return super(DatosUsuarioView, self).form_valid(form)

class UserPasswordView(FormView):
    template_name = "usuario/datos_usuario/cambio contraseña.html"
    form_class = UserPasswordForm
    success_url = reverse_lazy('home_app:home')

    def form_valid(self, form):
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

    def get_form_kwargs(self):
        kwargs = super(UserPasswordView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs   

class HistoricoUserListView(ListView):
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

class HistoricoUserDarBajaView(BSModalUpdateView):
    model = HistoricoUser
    template_name = "includes/formulario generico.html"
    form_class = HistoricoUserDarBajaForm
    success_url = reverse_lazy('usuario_app:historico_usuarios')

    def form_valid(self, form):
        form.instance.estado = 2
        form.instance.usuario.is_active = False
        form.instance.usuario.save()
        registro_guardar(form.instance, self.request)
        
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super(HistoricoUserDarBajaView, self).get_context_data(**kwargs)
        context['accion'] = 'Dar de Baja'
        context['titulo'] = 'Historico Usuario'
        return context
    
class HistoricoUserDarAltaView(BSModalCreateView):
    template_name = "includes/formulario generico.html"
    form_class = HistoricoUserDarAltaForm
    success_url = reverse_lazy('usuario_app:historico_usuarios')

    def form_valid(self, form):
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
    context_object_name = 'contexto_user'

    def get_context_data(self, **kwargs):
        contexto_historicouser = HistoricoUser.objects.filter(usuario__id = self.kwargs['pk'])
        try:
            datos_usuario = DatosUsuario.objects.get(usuario__id = self.kwargs['pk'])
        except:
            datos_usuario = None

        context = super(HistoricoDetailView, self).get_context_data(**kwargs)
        context['datos_usuario'] = datos_usuario
        context['contexto_historicouser'] = contexto_historicouser
        return context


