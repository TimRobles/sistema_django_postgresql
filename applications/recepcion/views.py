from datetime import datetime, time

from django.conf import settings
from applications.importaciones import *
from applications.colaborador.models import DatosContratoHonorarios, DatosContratoPlanilla

from .forms import (
    VisitaForm,VisitaBuscarForm,
    AsistenciaForm,AsistenciaBuscarForm,AsistenciaPersonalBuscarForm,AsistenciaSalidaForm
    )

from .models import (
    IpPublica,
    ResponsableAsistencia,
    Visita,
    Asistencia,
    )

class VisitaListView(PermissionRequiredMixin, FormView):
    permission_required = ('recepcion.view_visita')
    template_name = "recepcion/visita/inicio.html"
    form_class = VisitaBuscarForm
    success_url = '.'

    def get_form_kwargs(self):
        kwargs = super(VisitaListView, self).get_form_kwargs()
        kwargs['filtro_nombre'] = self.request.GET.get('nombre')
        kwargs['filtro_fecha'] = self.request.GET.get('fecha')
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(VisitaListView,self).get_context_data(**kwargs)
        visitas = Visita.objects.all()
        filtro_nombre = self.request.GET.get('nombre')
        filtro_fecha = self.request.GET.get('fecha')
        if filtro_nombre and filtro_fecha:
            condicion = Q(nombre__unaccent__icontains = filtro_nombre.split(" ")[0]) & Q(fecha_registro = datetime.strptime(filtro_fecha, "%Y-%m-%d").date())
            for palabra in filtro_nombre.split(" ")[1:]:
                condicion &= Q(nombre__unaccent__icontains = palabra) & Q(fecha_registro = datetime.strptime(filtro_fecha, "%Y-%m-%d").date())
            visitas = visitas.filter(condicion)
            context['contexto_filtro'] = "?nombre=" + filtro_nombre + '&fecha=' + filtro_fecha   
        elif filtro_fecha:
            condicion = Q(fecha_registro = datetime.strptime(filtro_fecha, "%Y-%m-%d").date())
            visitas = visitas.filter(condicion)
            context['contexto_filtro'] = "?nombre=" + filtro_nombre + '&fecha=' + filtro_fecha
        elif filtro_nombre:
            condicion = Q(nombre__unaccent__icontains = filtro_nombre.split(" ")[0])
            for palabra in filtro_nombre.split(" ")[1:]:
                condicion &= Q(nombre__unaccent__icontains = palabra)
            visitas = visitas.filter(condicion)
            context['contexto_filtro'] = "?nombre=" + filtro_nombre + '&fecha=' + filtro_fecha
   
        context['contexto_visita'] = visitas
        return context

def VisitaTabla(request):
    data = dict()
    if request.method == 'GET':
        template = 'recepcion/visita/inicio_tabla.html'
        context = {}
        visitas = Visita.objects.all()
        filtro_nombre = request.GET.get('nombre')
        filtro_fecha = request.GET.get('fecha')
        if filtro_nombre and filtro_fecha:
            condicion = Q(nombre__unaccent__icontains = filtro_nombre.split(" ")[0]) & Q(fecha_registro = datetime.strptime(filtro_fecha, "%Y-%m-%d").date())
            for palabra in filtro_nombre.split(" ")[1:]:
                condicion &= Q(nombre__unaccent__icontains = palabra) & Q(fecha_registro = datetime.strptime(filtro_fecha, "%Y-%m-%d").date())
            visitas = visitas.filter(condicion)
 
        elif filtro_fecha:
            condicion = Q(fecha_registro = datetime.strptime(filtro_fecha, "%Y-%m-%d").date())
            visitas = visitas.filter(condicion)

        elif filtro_nombre:
            condicion = Q(nombre__unaccent__icontains = filtro_nombre.split(" ")[0])
            for palabra in filtro_nombre.split(" ")[1:]:
                condicion &= Q(nombre__unaccent__icontains = palabra)
            visitas = visitas.filter(condicion)

        context['contexto_visita'] = visitas

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)

class VisitaCreateView(PermissionRequiredMixin, BSModalCreateView):
    permission_required = ('recepcion.add_visita')
    model = Visita
    template_name = "recepcion/visita/registrar.html"
    form_class = VisitaForm
    success_url = reverse_lazy('recepcion_app:visita_inicio')

    def get_context_data(self, **kwargs):
        context = super(VisitaCreateView, self).get_context_data(**kwargs)
        context['accion']="Registrar"
        context['titulo']="Visita"
        return context

    def form_valid(self, form):

        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)

        return super().form_valid(form)

class VisitaRegistrarSalidaView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('recepcion.change_visita')
    model = Visita
    template_name = "includes/eliminar generico.html"
    success_url = reverse_lazy('recepcion_app:visita_inicio')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        hour = datetime.now()
        self.object.hora_salida = hour.strftime("%H:%M")
        registro_guardar(self.object, self.request)
        self.object.save()
        messages.success(request, MENSAJE_REGISTRAR_SALIDA)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(VisitaRegistrarSalidaView, self).get_context_data(**kwargs)
        context['accion'] = "Registrar Salida"
        context['titulo'] = "Visita"
        context['dar_baja'] = "true"
        context['item'] = self.object.nombre
        return context


class AsistenciaListView(FormView):
    template_name = "recepcion/asistencia/inicio.html"
    form_class = AsistenciaBuscarForm
    success_url = '.'

    def get_form_kwargs(self):
        kwargs = super(AsistenciaListView, self).get_form_kwargs()
        kwargs['filtro_nombre'] = self.request.GET.get('nombre')
        kwargs['filtro_fecha'] = self.request.GET.get('fecha')
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(AsistenciaListView,self).get_context_data(**kwargs)
        asistencias = Asistencia.objects.all()
        filtro_nombre = self.request.GET.get('nombre')
        filtro_fecha = self.request.GET.get('fecha')

        if filtro_nombre and filtro_fecha:
            condicion = (Q(usuario__first_name__unaccent__icontains = filtro_nombre.split(" ")[0]) | Q(usuario__last_name__unaccent__icontains = filtro_nombre.split(" ")[0])) |Q(usuario__username__unaccent__icontains = filtro_nombre) & Q(fecha_registro = datetime.strptime(filtro_fecha, "%Y-%m-%d").date())  
            for palabra in filtro_nombre.split(" ")[1:]:
                condicion &= (Q(usuario__first_name__unaccent__icontains = palabra) | Q(usuario__last_name__unaccent__icontains = palabra)) & Q(fecha_registro = datetime.strptime(filtro_fecha, "%Y-%m-%d").date())  
            asistencias = asistencias.filter(condicion)
            context['contexto_filtro'] = "?nombre=" + filtro_nombre + '&fecha=' + filtro_fecha 

        elif filtro_fecha:
            condicion = Q(fecha_registro = datetime.strptime(filtro_fecha, "%Y-%m-%d").date())
            asistencias = asistencias.filter(condicion)
            context['contexto_filtro'] = "?nombre=" + filtro_nombre + '&fecha=' + filtro_fecha
        
        elif filtro_nombre:
            condicion = (Q(usuario__first_name__unaccent__icontains = filtro_nombre.split(" ")[0]) | Q(usuario__last_name__unaccent__icontains = filtro_nombre.split(" ")[0])) |Q(usuario__username__unaccent__icontains = filtro_nombre) 
            for palabra in filtro_nombre.split(" ")[1:]:
                condicion &= (Q(usuario__first_name__unaccent__icontains = palabra) | Q(usuario__last_name__unaccent__icontains = palabra))
            asistencias = asistencias.filter(condicion)
            context['contexto_filtro'] = "?nombre=" + filtro_nombre + '&fecha=' + filtro_fecha
   
        context['contexto_asistencia'] = asistencias
        return context

def AsistenciaTabla(request):
    data = dict()
    if request.method == 'GET':
        template = 'recepcion/asistencia/inicio_tabla.html'
        context = {}
        asistencias = Asistencia.objects.all()
        filtro_nombre = request.GET.get('nombre')
        filtro_fecha = request.GET.get('fecha')

        if filtro_nombre and filtro_fecha:
            condicion = (Q(usuario__first_name__unaccent__icontains = filtro_nombre.split(" ")[0]) | Q(usuario__last_name__unaccent__icontains = filtro_nombre.split(" ")[0])) |Q(usuario__username__unaccent__icontains = filtro_nombre) & Q(fecha_registro = datetime.strptime(filtro_fecha, "%Y-%m-%d").date())  
            for palabra in filtro_nombre.split(" ")[1:]:
                condicion &= (Q(usuario__first_name__unaccent__icontains = palabra) | Q(usuario__last_name__unaccent__icontains = palabra)) & Q(fecha_registro = datetime.strptime(filtro_fecha, "%Y-%m-%d").date())  
            asistencias = asistencias.filter(condicion) 

        elif filtro_fecha:
            condicion = Q(fecha_registro = datetime.strptime(filtro_fecha, "%Y-%m-%d").date())
            asistencias = asistencias.filter(condicion)
        
        elif filtro_nombre:
            condicion = (Q(usuario__first_name__unaccent__icontains = filtro_nombre.split(" ")[0]) | Q(usuario__last_name__unaccent__icontains = filtro_nombre.split(" ")[0])) |Q(usuario__username__unaccent__icontains = filtro_nombre)
            for palabra in filtro_nombre.split(" ")[1:]:
                condicion &= (Q(usuario__first_name__unaccent__icontains = palabra) | Q(usuario__last_name__unaccent__icontains = palabra))
            asistencias = asistencias.filter(condicion)
   
        context['contexto_asistencia'] = asistencias

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)

class AsistenciaPersonalView(PermissionRequiredMixin, FormView):
    permission_required = ('recepcion.view_asistencia')

    template_name = "recepcion/asistencia/inicio_personal.html"
    form_class = AsistenciaPersonalBuscarForm
    success_url = '.'

    def get_form_kwargs(self):
        kwargs = super(AsistenciaPersonalView, self).get_form_kwargs()
        kwargs['filtro_nombre'] = self.request.GET.get('nombre')
        kwargs['filtro_fecha'] = self.request.GET.get('fecha')
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(AsistenciaPersonalView,self).get_context_data(**kwargs)
        usuarios = list(ResponsableAsistencia.objects.get(usuario_responsable = self.request.user).usuario_a_registrar.all())
        asistencias = Asistencia.objects.filter(usuario__in=usuarios)
        filtro_nombre = self.request.GET.get('nombre')
        filtro_fecha = self.request.GET.get('fecha')

        if filtro_nombre and filtro_fecha:
            condicion = (Q(usuario__first_name__unaccent__icontains = filtro_nombre.split(" ")[0]) | Q(usuario__last_name__unaccent__icontains = filtro_nombre.split(" ")[0])) |Q(usuario__username__unaccent__icontains = filtro_nombre) & Q(fecha_registro = datetime.strptime(filtro_fecha, "%Y-%m-%d").date())  
            for palabra in filtro_nombre.split(" ")[1:]:
                condicion &= (Q(usuario__first_name__unaccent__icontains = palabra) | Q(usuario__last_name__unaccent__icontains = palabra)) & Q(fecha_registro = datetime.strptime(filtro_fecha, "%Y-%m-%d").date())  
            asistencias = asistencias.filter(condicion)
            context['contexto_filtro'] = "?nombre=" + filtro_nombre + '&fecha=' + filtro_fecha 

        elif filtro_fecha:
            condicion = Q(fecha_registro = datetime.strptime(filtro_fecha, "%Y-%m-%d").date())
            asistencias = asistencias.filter(condicion)
            context['contexto_filtro'] = "?nombre=" + filtro_nombre + '&fecha=' + filtro_fecha
        
        elif filtro_nombre:
            condicion = (Q(usuario__first_name__unaccent__icontains = filtro_nombre.split(" ")[0]) | Q(usuario__last_name__unaccent__icontains = filtro_nombre.split(" ")[0])) |Q(usuario__username__unaccent__icontains = filtro_nombre) 
            for palabra in filtro_nombre.split(" ")[1:]:
                condicion &= (Q(usuario__first_name__unaccent__icontains = palabra) | Q(usuario__last_name__unaccent__icontains = palabra))
            asistencias = asistencias.filter(condicion)
            context['contexto_filtro'] = "?nombre=" + filtro_nombre + '&fecha=' + filtro_fecha

        context['contexto_asistencia_personal'] = asistencias
        return context

def AsistenciaPersonalTabla(request):
    data = dict()
    if request.method == 'GET':
        template = 'recepcion/asistencia/inicio_personal_tabla.html'
        context = {}
        usuarios = list(ResponsableAsistencia.objects.get(usuario_responsable = request.user).usuario_a_registrar.all())

        asistencias = Asistencia.objects.filter(usuario__in=usuarios)
        filtro_nombre = request.GET.get('nombre')
        filtro_fecha = request.GET.get('fecha')

        if filtro_nombre and filtro_fecha:
            condicion = (Q(usuario__first_name__unaccent__icontains = filtro_nombre.split(" ")[0]) | Q(usuario__last_name__unaccent__icontains = filtro_nombre.split(" ")[0])) |Q(usuario__username__unaccent__icontains = filtro_nombre) & Q(fecha_registro = datetime.strptime(filtro_fecha, "%Y-%m-%d").date())  
            for palabra in filtro_nombre.split(" ")[1:]:
                condicion &= (Q(usuario__first_name__unaccent__icontains = palabra) | Q(usuario__last_name__unaccent__icontains = palabra)) & Q(fecha_registro = datetime.strptime(filtro_fecha, "%Y-%m-%d").date())  
            asistencias = asistencias.filter(condicion) 

        elif filtro_fecha:
            condicion = Q(fecha_registro = datetime.strptime(filtro_fecha, "%Y-%m-%d").date())
            asistencias = asistencias.filter(condicion)
        
        elif filtro_nombre:
            condicion = (Q(usuario__first_name__unaccent__icontains = filtro_nombre.split(" ")[0]) | Q(usuario__last_name__unaccent__icontains = filtro_nombre.split(" ")[0])) |Q(usuario__username__unaccent__icontains = filtro_nombre)
            for palabra in filtro_nombre.split(" ")[1:]:
                condicion &= (Q(usuario__first_name__unaccent__icontains = palabra) | Q(usuario__last_name__unaccent__icontains = palabra))
            asistencias = asistencias.filter(condicion)
   

        context['contexto_asistencia_personal'] = asistencias

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)

class AsistenciaPersonalCreateView(LoginRequiredMixin, BSModalCreateView):
    model = Asistencia
    template_name = "recepcion/asistencia/asistencia.html"
    form_class = AsistenciaForm
    success_url = reverse_lazy('recepcion_app:asistencia_personal_inicio')

    def get_context_data(self, **kwargs):
        context = super(AsistenciaPersonalCreateView, self).get_context_data(**kwargs)
        confirmar = False
        context['confirmar']=confirmar
        context['accion']="Registrar"
        context['titulo']="Asistencia"
        return context

    def form_valid(self, form):
        try:
            print(form.instance.usuario.Asistencia_usuario.all().get(fecha_registro = date.today()))
            form.add_error('usuario', 'Ya registró su asistencia.')
            return super().form_invalid(form)
        except:
            pass
        buscar_ip = IpPublica.objects.filter(sede = form.cleaned_data['sede'])
        if not buscar_ip:
            form.add_error('sede', 'No hay IP registrada en esta sede.')
            return super().form_invalid(form)

        if buscar_ip.latest('created_at').ip != self.request.META[settings.BUSCAR_IP]:
            if self.request.user.ResponsableAsistencia_usuario_responsable.all()[0].permiso_cambio_ip:
                IpPublica.objects.create(ip = self.request.META[settings.BUSCAR_IP], sede = form.cleaned_data['sede'])
            else: 
                form.add_error('usuario', 'No estás en la oficina, no seas sapo.')
                return super().form_invalid(form)

        try:
            sociedad = DatosContratoPlanilla.objects.get(usuario = form.instance.usuario).sociedad
        except:
            try:
                sociedad = DatosContratoHonorarios.objects.get(usuario = form.instance.usuario).sociedad
            except:
                sociedad = None

        form.instance.sociedad = sociedad
        registro_guardar(form.instance, self.request)

        return super().form_valid(form)

class AsistenciaPersonalRegistrarSalidaView(LoginRequiredMixin,BSModalUpdateView):
    model = Asistencia
    template_name = "recepcion/asistencia/asistencia.html"
    form_class = AsistenciaSalidaForm
    success_url = reverse_lazy('recepcion_app:asistencia_personal_inicio')

    def form_valid(self, form):
        self.object = self.get_object()
        hour = datetime.now()     
        self.object.hora_salida = hour.strftime("%H:%M") 
        registro_guardar(self.object, self.request)
        self.object.save()

        buscar_ip = IpPublica.objects.filter(sede = form.cleaned_data['sede'])
        if not buscar_ip:
            form.add_error('sede', 'No hay IP registrada en esta sede.')
            return super().form_invalid(form)

        if buscar_ip.latest('created_at').ip != self.request.META[settings.BUSCAR_IP]:
            if self.request.user.ResponsableAsistencia_usuario_responsable.all()[0].permiso_cambio_ip:
                IpPublica.objects.create(ip = self.request.META[settings.BUSCAR_IP], sede = form.cleaned_data['sede'])
            else: 
                form.add_error('usuario', 'No estás en la oficina, no seas sapo.')
                return super().form_invalid(form)


        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(AsistenciaPersonalRegistrarSalidaView, self).get_context_data(**kwargs)
        context['accion']="Registrar Salida"
        context['titulo']="Asistencia Personal"
        return context

def ConfirmarSedeView(request, id_sede):
    buscar_ip = IpPublica.objects.filter(sede__id = id_sede)
    if buscar_ip:
        if buscar_ip.latest('created_at').ip != request.META[settings.BUSCAR_IP]:
            return HttpResponse('No estás en el wifi correcto.')
    
    return HttpResponse('')
