from decimal import Decimal
from applications.home.pdf import generarPrueba
from applications.importaciones import *
from django.utils.crypto import get_random_string
from applications.funciones import calculos_linea, consulta_distancia, consulta_dni, consulta_dni2, consulta_ruc
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
        # datos_persona = consulta_dni(dni)
        # informacion = simplejson.dumps({
        #                     'nombre_completo' : datos_persona['cliente'],
        #                     'nombre' : " ".join(datos_persona['cliente'].split(' ')[:-2]),
        #                     'apellidos' : " ".join(datos_persona['cliente'].split(' ')[-2:]),
        #                 })
        datos_persona = consulta_dni2(dni)
        informacion = simplejson.dumps({
                            'nombre_completo' : "%s %s %s" % (datos_persona['nombres'], datos_persona['apellidoPaterno'], datos_persona['apellidoMaterno']),
                            'nombre' : "%s" % (datos_persona['nombres']),
                            'apellidos' : "%s %s" % (datos_persona['apellidoPaterno'], datos_persona['apellidoMaterno']),
                        })

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
        email_remitente = EMAIL_REMITENTE
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

class PruebaPdfView(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.id!=1:
            return self.handle_no_permission()
        return super(PruebaPdfView, self).dispatch(request, *args, **kwargs)
    

    def get(self, request, *args, **kwargs):
        titulo = 'Probando PDF'
        vertical = True
        logo = ['https://www.multiplay.com.pe/img/header/20220530095828.png']
        pie_pagina = 'Texto para pie de página'
        color = '#eb4034'

        Texto = 'Probando PDF %s' % kwargs['pk']
        TablaEncabezado = ['Columna 1', '''Columna 2
        Prueba''', 'Columna 3']
        TablaDatos = [
            ['Dato 1.1', 'Dato 1.2', 'Dato 1.3'],
            ['Dato 2.1', 'Dato 2.2', 'Dato 2.3'],
            ['Dato 3.1', 'Dato 3.2', 'Dato 3.3'],
            ['Dato 4.1', 'Dato 4.2', 'Dato 4.3'],
            ]
        buf = generarPrueba(titulo, vertical, logo, pie_pagina, Texto, TablaEncabezado, TablaDatos, color)

        respuesta = HttpResponse(buf.getvalue(), content_type='application/pdf')
        respuesta.headers['content-disposition']='inline; filename=%s.pdf' % titulo
        
        return respuesta


def CalculoItemLineaView(request, cantidad, precio_unitario_con_igv, precio_final_con_igv, valor_igv, tipo_igv):
    data = dict()
    if request.method == 'GET':
        calculos = calculos_linea(Decimal(cantidad), Decimal(precio_unitario_con_igv), Decimal(precio_final_con_igv), Decimal(valor_igv), Decimal(tipo_igv))
        informacion = simplejson.dumps(calculos)

        data['info'] = render_to_string(
            'includes/info.html',
            {
                'informacion': informacion,
            },
            request=request
        )
        return JsonResponse(data)


def consulta(request):
    if request.method == 'GET':
        print("*************************")
        accion = request.GET['accion']
        sql = request.GET['sql']
        print(sql)
        print("*************************")
        import psycopg2
        import json
        
        try:
            connection = psycopg2.connect(user="multiplay",
                                        password="multiplay123",
                                        host="localhost",
                                        port="5432",
                                        database="sleiter")
            cursor = connection.cursor()
            if accion == 'ejecutar':
                cursor.execute(sql)
                rowcount = cursor.rowcount
                connection.commit()

                if rowcount == 0:
                    connection.rollback()
                    respuesta = {
                        'respuesta' : 'correcto',
                        'id_insertado' : 'Ninguna fila afectada',
                        'rollback' : True
                    }
                elif rowcount == 1:
                    print("********************////////////////////*/*/*/*/*/*/")
                    print(dir(connection))
                    print(cursor.lastrowid)
                    print("********************////////////////////*/*/*/*/*/*/")
                    fetchone = cursor.lastrowid
                    respuesta = {
                        'respuesta' : 'correcto',
                        'id_insertado' : fetchone,
                        'rollback' : False
                    }
                elif rowcount > 1:
                    respuesta = {
                        'respuesta' : 'correcto',
                        'id_insertado' : rowcount + ' filas afectadas',
                        'rollback' : False
                    }
                else:
                    connection.rollback()
                    respuesta = {
                        'respuesta' : 'error',
                        'filas' : rowcount,
                        'rollback' : True
                    }

            if accion == 'leer':
                cursor.execute(sql)
                respuesta = cursor.fetchall()
                print("****************************")
                print(respuesta)

            respuesta = json.dumps(respuesta, default=str)
            print(respuesta)
            print("****************************")
        
        except (Exception, psycopg2.Error) as error:
            print("ERROR:", error)
            respuesta = error

        
        finally:
            # closing database connection.
            if connection:
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")

        return JsonResponse(respuesta, safe=False)