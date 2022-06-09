from applications.importaciones import *
from django.utils.crypto import get_random_string
from applications.funciones import consulta_distancia, consulta_dni, consulta_dni2, consulta_ruc
from .forms import UserLoginForm
from .forms import OlvideContrasenaForm
from .forms import RecuperarContrasenaForm

class InicioView(FormView):
    template_name = "home/inicio.html"
    form_class = UserLoginForm

    def form_valid(self, form):
        user = authenticate(
            username = form.cleaned_data['username'],
            password = form.cleaned_data['password'],
        )
        login(self.request, user)
        self.request.session.set_expiry(0)
        return super(InicioView, self).form_valid(form)

    def get_success_url(self):
        next = self.request.GET.get("next")

        if next:
            return "%s" % (next)
        else:
            return reverse_lazy('home_app:home')

class UserLogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse_lazy('home_app:login'))

class PanelView(LoginRequiredMixin, TemplateView):
    template_name = "home/panel.html"

    def get_context_data(self, **kwargs):
        context = super(PanelView, self).get_context_data(**kwargs)
        group_permissions = self.request.user.get_all_permissions()
        context['Permisos'] = group_permissions
        return context

class SinPermisoView(TemplateView):
    template_name = "403.html"

    def get_context_data(self, **kwargs):
        context = super(SinPermisoView, self).get_context_data(**kwargs)
        context['META'] = self.request.META
        if self.request.META.get('HTTP_REFERER') and self.request.META.get('HTTP_REFERER') != 'http://0.0.0.0:8000/sin-permiso/':
            context['previous'] = self.request.META.get('HTTP_REFERER')
        else:
            context['previous'] = reverse_lazy('home_app:home')
        return context

def ConsultaRucView(request, ruc):
    data = dict()
    if request.method == 'GET':
        datos_empresa = consulta_ruc(ruc)
        informacion = simplejson.dumps({
                            'razon_social' : datos_empresa['nombre'],
                            'direccion' : datos_empresa['direccion'],
                            'ubigeo' : datos_empresa['ubigeo'],
                            'estado' : datos_empresa['estado'],
                            'condicion' : datos_empresa['condicion'],
                            'distrito' : datos_empresa['distrito'],
                            'provincia' : datos_empresa['provincia'],
                            'departamento' : datos_empresa['departamento'],
                        })

        data['info'] = render_to_string(
            'includes/info.html',
            {
                'informacion': informacion,
            },
            request=request
        )
        return JsonResponse(data)

def ConsultaDniView(request, dni):
    data = dict()
    if request.method == 'GET':
        datos_persona = consulta_dni(dni)
        informacion = simplejson.dumps({
                            'nombre_completo' : datos_persona['cliente'],
                        })
        # datos_persona = consulta_dni2(dni)
        # informacion = simplejson.dumps({
        #                     'nombre_completo' : "%s %s %s" % (datos_persona['nombres'], datos_persona['apellidoPaterno'], datos_persona['apellidoMaterno']),
        #                 })

        data['info'] = render_to_string(
            'includes/info.html',
            {
                'informacion': informacion,
            },
            request=request
        )
        return JsonResponse(data)

class OlvideContrasenaView(FormView):
    template_name = "home/olvide contraseña.html"
    form_class = OlvideContrasenaForm
    success_url = reverse_lazy('home_app:recuperar_contraseña')

    def form_valid(self, form):
        User = get_user_model()
        correo = form.cleaned_data['correo']

        try:
            usuario_buscar = User.objects.get(email=correo)
        except:
            form.add_error('correo', 'El correo %s no existe.' % correo)
            return super(OlvideContrasenaView, self).form_invalid(form)

        datos_usuario = usuario_buscar.DatosUsuario_usuario
        password = get_random_string(length=10)
        datos_usuario.recuperar_password = password
        datos_usuario.save()

        asunto = "Recuperación de Contraseña"
        mensaje = "Hola %s\nEl código de recuperación de tu cuenta es: %s\n\nUna vez que ingreses este código, esa será tu nueva contraseña.\nSi no solicitaste el cambio de contraseña, puedes ignorar este correo." % (usuario_buscar.username, password)
        email_remitente = 'no-responder@multiplay.com.pe'
        send_mail(asunto, mensaje, email_remitente, [correo,])

        return super(OlvideContrasenaView, self).form_valid(form)

class RecuperarContrasenaView(FormView):
    template_name = "home/recuperar contraseña.html"
    form_class = RecuperarContrasenaForm
    success_url = reverse_lazy('home_app:home')

    def form_valid(self, form):
        User = get_user_model()
        correo = form.cleaned_data['correo']
        password = form.cleaned_data['password']

        try:
            usuario_buscar = User.objects.get(email=correo)
        except:
            form.add_error('Correo', 'El correo %s no existe.' % correo)
            return super(RecuperarContrasenaView, self).form_invalid(form)

        datos_usuario = usuario_buscar.DatosUsuario_usuario
        if datos_usuario.recuperar_password == password:
            datos_usuario.recuperar_password = None
            datos_usuario.save()
            usuario_buscar.set_password(password)
            usuario_buscar.save()

            asunto = "Cambio de Contraseña"
            mensaje = "Hola %s\nTu contraseña fue actualizada con éxito, te recordamos tu nueva contraseña: %s\n\nPuedes cambiar esta contraseña en cualquier momento." % (usuario_buscar.username, password)
            email_remitente = 'no-responder@multiplay.com.pe'
            send_mail(asunto, mensaje, email_remitente, [correo,])

            messages.success(self.request, 'Contraseña cambiada exitosamente. Nueva contraseña: %s' % password)
        else:
            form.add_error('password', 'El código ingresado es incorrecto.')
            return super(RecuperarContrasenaView, self).form_invalid(form)

        return super(RecuperarContrasenaView, self).form_valid(form)


class PruebaGeolocalizacion(TemplateView):
    template_name = "home/prueba geolocalizacion.html"


def DistanciaGeoLocalizacion(request, longitud, latitud, sede_id):
    if request.method == 'GET':
        distancia = consulta_distancia(longitud, latitud, sede_id)
        return HttpResponse(distancia)