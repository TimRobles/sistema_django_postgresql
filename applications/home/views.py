from applications.funciones import consulta_dni, consulta_ruc
from applications.importaciones import *
from .forms import UserLoginForm


class InicioView(FormView):
    template_name = "home/inicio.html"
    form_class = UserLoginForm

    def form_valid(self, form):
        user = authenticate(
            username = form.cleaned_data['username'],
            password = form.cleaned_data['password'],
        )
        login(self.request, user)
        self.request.session['sociedad'] = form.cleaned_data['sociedad'].razon_social
        '''self.request.session['logo'] = form.cleaned_data['sociedad'].logo.url
        self.request.session['color'] = form.cleaned_data['sociedad'].color'''
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

        data['info'] = render_to_string(
            'includes/info.html',
            {
                'informacion': informacion,
            },
            request=request
        )
        return JsonResponse(data)
