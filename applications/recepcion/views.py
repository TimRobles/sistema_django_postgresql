from datetime import datetime, time
from django.shortcuts import render
from django.core.paginator import Paginator

from django.conf import settings
from applications.funciones import consulta_distancia, registrar_excepcion
from applications.importaciones import *
from applications.colaborador.models import DatosContratoHonorarios, DatosContratoPlanilla

from .forms import (
    VisitaForm,VisitaBuscarForm,
    AsistenciaForm,AsistenciaBuscarForm,AsistenciaPersonalBuscarForm,AsistenciaSalidaForm,
    InasistenciaForm,InasistenciaAprobarForm,InasistenciaRechazarForm, InasistenciaActualizarForm
    )

from .models import (
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
 
        contexto_filtro = []

        if filtro_nombre:
            condicion = Q(nombre__unaccent__icontains = filtro_nombre.split(" ")[0]) |Q(nombre__unaccent__icontains=filtro_nombre)
            for palabra in filtro_nombre.split(" ")[1:]:
                condicion &= Q(nombre__unaccent__icontains = palabra)
            visitas = visitas.filter(condicion)
            contexto_filtro.append("nombre" + filtro_nombre)

        if filtro_fecha:
            condicion = Q(fecha_registro = datetime.strptime(filtro_fecha, "%Y-%m-%d").date())
            visitas = visitas.filter(condicion)
            contexto_filtro.append("nombre" + filtro_fecha)

        context['contexto_filtro'] = "&".join(contexto_filtro)

        context['pagina_filtro'] = ""
        if self.request.GET.get('page'):
            if context['contexto_filtro']:
                context['pagina_filtro'] = f'&page={self.request.GET.get("page")}'
            else:
                context['pagina_filtro'] = f'page={self.request.GET.get("page")}'
        context['contexto_filtro'] = '?' + context['contexto_filtro']

        objectsxpage =  15 # Show 15 objects per page.

        if len(visitas) > objectsxpage:
            paginator = Paginator(visitas, objectsxpage)
            page_number = self.request.GET.get('page')
            visitas = paginator.get_page(page_number)

        context['contexto_pagina'] = visitas
        return context

def VisitaTabla(request):
    data = dict()
    if request.method == 'GET':
        template = 'recepcion/visita/inicio_tabla.html'
        context = {}
        visitas = Visita.objects.all()
        filtro_nombre = request.GET.get('nombre')
        filtro_fecha = request.GET.get('fecha')
 
        contexto_filtro = []

        if filtro_nombre:
            condicion = Q(nombre__unaccent__icontains = filtro_nombre.split(" ")[0]) |Q(nombre__unaccent__icontains=filtro_nombre)
            for palabra in filtro_nombre.split(" ")[1:]:
                condicion &= Q(nombre__unaccent__icontains = palabra)
            visitas = visitas.filter(condicion)
            contexto_filtro.append("nombre" + filtro_nombre)

        if filtro_fecha:
            condicion = Q(fecha_registro = datetime.strptime(filtro_fecha, "%Y-%m-%d").date())
            visitas = visitas.filter(condicion)
            contexto_filtro.append("nombre" + filtro_fecha)

        context['contexto_filtro'] = "&".join(contexto_filtro)

        context['pagina_filtro'] = ""
        if request.GET.get('page'):
            if context['contexto_filtro']:
                context['pagina_filtro'] = f'&page={request.GET.get("page")}'
            else:
                context['pagina_filtro'] = f'page={request.GET.get("page")}'
        context['contexto_filtro'] = '?' + context['contexto_filtro']

        objectsxpage = 15 # Show 15 objects per page.

        if len(visitas) > objectsxpage:
            paginator = Paginator(visitas, objectsxpage)
            page_number = request.GET.get('page')
            visitas = paginator.get_page(page_number)

        context['contexto_pagina'] = visitas

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
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

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
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)    

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            self.object = self.get_object()
            hour = datetime.now()
            self.object.hora_salida = hour.strftime("%H:%M")
            registro_guardar(self.object, self.request)
            self.object.save()
            messages.success(request, MENSAJE_REGISTRAR_SALIDA)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(VisitaRegistrarSalidaView, self).get_context_data(**kwargs)
        context['accion'] = "Registrar Salida"
        context['titulo'] = "Visita"
        context['dar_baja'] = "true"
        context['item'] = self.object.nombre
        return context


class AsistenciaListView(PermissionRequiredMixin, FormView):
    permission_required = ('recepcion.view_asistencia')
    template_name = "recepcion/asistencia/inicio.html"
    form_class = AsistenciaBuscarForm
    success_url = '.'

    def get_form_kwargs(self):
        kwargs = super(AsistenciaListView, self).get_form_kwargs()
        kwargs['filtro_nombre'] = self.request.GET.get('nombre')
        kwargs['filtro_fecha'] = self.request.GET.get('fecha_de')
        kwargs['filtro_fecha_dos'] = self.request.GET.get('fecha_hasta')
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(AsistenciaListView,self).get_context_data(**kwargs)
        asistencias = Asistencia.objects.all()
        filtro_nombre = self.request.GET.get('nombre')
        filtro_fecha = self.request.GET.get('fecha_de')
        filtro_fecha_dos = self.request.GET.get('fecha_hasta')

        contexto_filtro = []

        if filtro_nombre:
            condicion = (Q(usuario__first_name__unaccent__icontains = filtro_nombre.split(" ")[0]) | Q(usuario__last_name__unaccent__icontains = filtro_nombre.split(" ")[0])) |Q(usuario__username__unaccent__icontains = filtro_nombre)
            for palabra in filtro_nombre.split(" ")[1:]:
                condicion &= (Q(usuario__first_name__unaccent__icontains = palabra) | Q(usuario__last_name__unaccent__icontains = palabra))
            asistencias = asistencias.filter(condicion)
            contexto_filtro.append("nombre=" + filtro_nombre)

        # if filtro_fecha:
        #     condicion = Q(fecha_registro = datetime.strptime(filtro_fecha, "%Y-%m-%d").date())
        #     asistencias = asistencias.filter(condicion)
        #     contexto_filtro.append("fecha_registro=" + filtro_fecha)

            
        # if filtro_fecha_dos:
        #     condicion = Q(fecha_registro = datetime.strptime(filtro_fecha_dos, "%Y-%m-%d").date())
        #     asistencias = asistencias.filter(condicion)
        #     contexto_filtro.append("fecha_registro_dos=" + filtro_fecha_dos)
        #     print(contexto_filtro)

        if filtro_fecha and filtro_fecha_dos:
            fecha_inicio = datetime.strptime(filtro_fecha, "%Y-%m-%d").date()
            fecha_fin = datetime.strptime(filtro_fecha_dos, "%Y-%m-%d").date()

            asistencias = asistencias.filter(fecha_registro__range=(fecha_inicio, fecha_fin))
            contexto_filtro.append("fecha_registro_de: {} a {}".format(filtro_fecha, filtro_fecha_dos))
        
        context['contexto_filtro'] = "&".join(contexto_filtro)

        context['pagina_filtro'] = ""
        if self.request.GET.get('page'):
            if context['contexto_filtro']:
                context['pagina_filtro'] = f'&page={self.request.GET.get("page")}'
            else:
                context['pagina_filtro'] = f'page={self.request.GET.get("page")}'
        context['contexto_filtro'] = '?' + context['contexto_filtro']
   
        objectsxpage =  15 # Show 15 objects per page.

        if len(asistencias) > objectsxpage:
            paginator = Paginator(asistencias, objectsxpage)
            page_number = self.request.GET.get('page')
            asistencias = paginator.get_page(page_number)

        context['contexto_pagina'] = asistencias
        return context

def AsistenciaTabla(request):
    data = dict()
    if request.method == 'GET':
        template = 'recepcion/asistencia/inicio_tabla.html'
        context = {}
        asistencias = Asistencia.objects.all()
        filtro_nombre = request.GET.get('nombre')
        filtro_fecha = request.GET.get('fecha_de')
        filtro_fecha_dos = request.GET.get('fecha_hasta')

        contexto_filtro = []

        if filtro_nombre:
            condicion = (Q(usuario__first_name__unaccent__icontains = filtro_nombre.split(" ")[0]) | Q(usuario__last_name__unaccent__icontains = filtro_nombre.split(" ")[0])) |Q(usuario__username__unaccent__icontains = filtro_nombre)
            for palabra in filtro_nombre.split(" ")[1:]:
                condicion &= (Q(usuario__first_name__unaccent__icontains = palabra) | Q(usuario__last_name__unaccent__icontains = palabra))
            asistencias = asistencias.filter(condicion)
            contexto_filtro.append("nombre=" + filtro_nombre)

        # if filtro_fecha:
        #     condicion = Q(fecha_registro = datetime.strptime(filtro_fecha, "%Y-%m-%d").date())
        #     asistencias = asistencias.filter(condicion)
        #     contexto_filtro.append("fecha_registro=" + filtro_fecha)

        # if filtro_fecha_dos:
        #     condicion = Q(fecha_registro = datetime.strptime(filtro_fecha_dos, "%Y-%m-%d").date())
        #     asistencias = asistencias.filter(condicion)
        #     contexto_filtro.append("fecha_registro_dos=" + filtro_fecha_dos)

        if filtro_fecha and filtro_fecha_dos:
            fecha_inicio = datetime.strptime(filtro_fecha, "%Y-%m-%d").date()
            fecha_fin = datetime.strptime(filtro_fecha_dos, "%Y-%m-%d").date()
            asistencias = asistencias.filter(fecha_registro__range=(fecha_inicio, fecha_fin))
            contexto_filtro.append("fecha_registro_de: {} a {}".format(filtro_fecha, filtro_fecha_dos))

        context['contexto_filtro'] = "&".join(contexto_filtro)

        context['pagina_filtro'] = ""
        if request.GET.get('page'):
            if context['contexto_filtro']:
                context['pagina_filtro'] = f'&page={request.GET.get("page")}'
            else:
                context['pagina_filtro'] = f'page={request.GET.get("page")}'
        context['contexto_filtro'] = '?' + context['contexto_filtro']


        objectsxpage = 15 # Show 15 objects per page.

        if len(asistencias) > objectsxpage:
            paginator = Paginator(asistencias, objectsxpage)
            page_number = request.GET.get('page')
            asistencias = paginator.get_page(page_number)

        context['contexto_pagina'] = asistencias

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

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_anonymous:
            return self.handle_no_permission()
        if len(ResponsableAsistencia.objects.filter(usuario_responsable = self.request.user)) == 0:
            return self.handle_no_permission()
        return super(AsistenciaPersonalView, self).dispatch(request, *args, **kwargs)    
    
    def get_form_kwargs(self):
        kwargs = super(AsistenciaPersonalView, self).get_form_kwargs()
        kwargs['filtro_nombre'] = self.request.GET.get('nombre')
        kwargs['filtro_fecha_registro'] = self.request.GET.get('fecha_registro')
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(AsistenciaPersonalView,self).get_context_data(**kwargs)
        usuarios = list(ResponsableAsistencia.objects.get(usuario_responsable = self.request.user).usuario_a_registrar.all())
        asistencias = Asistencia.objects.filter(usuario__in=usuarios)
        
        filtro_nombre = self.request.GET.get('nombre')
        filtro_fecha_registro = self.request.GET.get('fecha_registro')

        contexto_filtro = []

        if filtro_nombre:
            condicion = (Q(usuario__first_name__unaccent__icontains = filtro_nombre.split(" ")[0]) | Q(usuario__last_name__unaccent__icontains = filtro_nombre.split(" ")[0])) |Q(usuario__username__unaccent__icontains = filtro_nombre)
            for palabra in filtro_nombre.split(" ")[1:]:
                condicion &= (Q(usuario__first_name__unaccent__icontains = palabra) | Q(usuario__last_name__unaccent__icontains = palabra))
            asistencias = asistencias.filter(condicion)
            contexto_filtro.append("nombre=" + filtro_nombre)

        if filtro_fecha_registro:
            condicion = Q(fecha_registro = datetime.strptime(filtro_fecha_registro, "%Y-%m-%d").date())
            asistencias = asistencias.filter(condicion)
            contexto_filtro.append("fecha_registro=" + filtro_fecha_registro)
        
        context['contexto_filtro'] = "&".join(contexto_filtro)

        context['pagina_filtro'] = ""
        if self.request.GET.get('page'):
            if context['contexto_filtro']:
                context['pagina_filtro'] = f'&page={self.request.GET.get("page")}'
            else:
                context['pagina_filtro'] = f'page={self.request.GET.get("page")}'
        context['contexto_filtro'] = '?' + context['contexto_filtro']

        objectsxpage =  15 # Show 15 objects per page.

        if len(asistencias) > objectsxpage:
            paginator = Paginator(asistencias, objectsxpage)
            page_number = self.request.GET.get('page')
            asistencias = paginator.get_page(page_number)

        permiso_asistencia = False
        if 'recepcion.aprobar_rechazar' in self.request.user.get_all_permissions():
            permiso_asistencia = True
        context['contexto_asistencia_personal'] = asistencias
        context['contexto_pagina'] = asistencias
        context['permiso_asistencia'] = permiso_asistencia
        
        return context

def AsistenciaPersonalTabla(request):
    data = dict()
    if request.method == 'GET':
        template = 'recepcion/asistencia/inicio_personal_tabla.html'
        context = {}
        usuarios = list(ResponsableAsistencia.objects.get(usuario_responsable = request.user).usuario_a_registrar.all())

        asistencias = Asistencia.objects.filter(usuario__in=usuarios)
        filtro_nombre = request.GET.get('nombre')
        filtro_fecha_registro = request.GET.get('fecha')

        contexto_filtro = []

        if filtro_nombre:
            condicion = (Q(usuario__first_name__unaccent__icontains = filtro_nombre.split(" ")[0]) | Q(usuario__last_name__unaccent__icontains = filtro_nombre.split(" ")[0])) |Q(usuario__username__unaccent__icontains = filtro_nombre)
            for palabra in filtro_nombre.split(" ")[1:]:
                condicion &= (Q(usuario__first_name__unaccent__icontains = palabra) | Q(usuario__last_name__unaccent__icontains = palabra))
            asistencias = asistencias.filter(condicion)
            contexto_filtro.append("nombre=" + filtro_nombre)

        if filtro_fecha_registro:
            condicion = Q(fecha_registro = datetime.strptime(filtro_fecha_registro, "%Y-%m-%d").date())
            asistencias = asistencias.filter(condicion)
            contexto_filtro.append("fecha_registro=" + filtro_fecha_registro)

        context['contexto_filtro'] = "&".join(contexto_filtro)

        context['pagina_filtro'] = ""
        if request.GET.get('page'):
            if context['contexto_filtro']:
                context['pagina_filtro'] = f'&page={request.GET.get("page")}'
            else:
                context['pagina_filtro'] = f'page={request.GET.get("page")}'
        context['contexto_filtro'] = '?' + context['contexto_filtro']

        objectsxpage =  15 # Show 15 objects per page.

        if len(asistencias) > objectsxpage:
            paginator = Paginator(asistencias, objectsxpage)
            page_number = request.GET.get('page')
            asistencias = paginator.get_page(page_number)

        permiso_asistencia = False
        if 'recepcion.aprobar_rechazar' in request.user.get_all_permissions():
            permiso_asistencia = True
        context['contexto_asistencia_personal'] = asistencias
        context['contexto_pagina'] = asistencias
        context['permiso_asistencia'] = permiso_asistencia

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)

class AsistenciaPersonalCreateView(PermissionRequiredMixin, BSModalCreateView):
    permission_required = ('recepcion.add_asistencia')
    model = Asistencia
    template_name = "recepcion/asistencia/asistencia.html"
    form_class = AsistenciaForm
    success_url = reverse_lazy('recepcion_app:asistencia_personal_inicio')
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)    

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
        
        longitud = form.cleaned_data['longitud']
        latitud = form.cleaned_data['latitud']
        sede = form.cleaned_data['sede']
        
        if consulta_distancia(longitud, latitud, sede.id) != "Estás en la oficina":
            if not self.request.user.is_superuser:
                form.add_error('sede', 'No estás en la oficina, no seas sapo.')
                return super().form_invalid(form)

        try:
            sociedad = DatosContratoPlanilla.objects.get(usuario = form.instance.usuario).sociedad
    
        except:
            try:
                sociedad = DatosContratoHonorarios.objects.get(usuario = form.instance.usuario).sociedad

            except:
                sociedad = None
                form.add_error('usuario', 'Este usuario no tiene contrato vigente.')
                return super().form_invalid(form)

        form.instance.sociedad = sociedad
        form.instance.fecha_registro = date.today()
        registro_guardar(form.instance, self.request)

        return super().form_valid(form)

class AsistenciaPersonalRegistrarSalidaView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('recepcion.change_asistencia')
    model = Asistencia
    template_name = "recepcion/asistencia/asistencia.html"
    form_class = AsistenciaSalidaForm
    success_url = reverse_lazy('recepcion_app:asistencia_personal_inicio')
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)    

    def form_valid(self, form):
        self.object = self.get_object()

        longitud = form.cleaned_data['longitud']
        latitud = form.cleaned_data['latitud']
        sede = form.cleaned_data['sede']
        
        if consulta_distancia(longitud, latitud, sede.id) != "Estás en la oficina":
            if not self.request.user.is_superuser:
                form.add_error('sede', 'No estás en la oficina, no seas sapo.')
                return super().form_invalid(form)

        hour = datetime.now()     
        self.object.hora_salida = hour.strftime("%H:%M") 
        registro_guardar(self.object, self.request)
        self.object.save()
        
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(AsistenciaPersonalRegistrarSalidaView, self).get_context_data(**kwargs)
        context['accion']="Registrar Salida"
        context['titulo']="Asistencia Personal"
        return context


class InasistenciaRegistrarView(PermissionRequiredMixin, BSModalFormView):
    permission_required = ('recepcion.change_asistencia')
    template_name = "recepcion/asistencia/crear_inasistencia.html"
    form_class = InasistenciaForm
    success_url = reverse_lazy('recepcion_app:asistencia_personal_inicio')

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)    

    @transaction.atomic
    def form_valid(self, form):
        fecha = form.cleaned_data['fecha']

        try:
            print(form.instance.usuario.Asistencia_usuario.all().get(fecha_registro = fecha))
            form.add_error('usuario', 'Ya existe registro con la fecha seleccionada.')
            return super().form_invalid(form)
        except:
            pass

        sid = transaction.savepoint()
        try:
            if self.request.session['primero']:
                try:
                    sociedad = DatosContratoPlanilla.objects.get(usuario = form.instance.usuario).sociedad
            
                except:
                    try:
                        sociedad = DatosContratoHonorarios.objects.get(usuario = form.instance.usuario).sociedad

                    except:
                        sociedad = None
                        form.add_error('usuario', 'Este usuario no tiene contrato vigente.')
                        return super().form_invalid(form)

                fecha = form.cleaned_data['fecha']

                form.instance.sociedad = sociedad
                form.instance.fecha_registro = fecha
                form.instance.estado_solicitud = 1

                registro_guardar(form.instance, self.request)
                form.instance.save()
                self.request.session['primero'] = False
                return super().form_valid(form)
        
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.success_url)

    def get_context_data(self, **kwargs):
        self.request.session['primero'] = True
        context = super(InasistenciaRegistrarView, self).get_context_data(**kwargs)
        confirmar = False
        context['confirmar']=confirmar
        context['accion']="Registrar"
        context['titulo']="Inasistencia"
        return context

class InasistenciaActualizarView(BSModalUpdateView):
    model = Asistencia
    template_name = "includes/formulario generico.html"
    form_class = InasistenciaActualizarForm
    success_url = reverse_lazy('recepcion_app:asistencia_personal_inicio')

    def form_valid(self, form):
        registro_guardar(self.object, self.request)
        self.object.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(InasistenciaActualizarView, self).get_context_data(**kwargs)
        context['accion']="Actualizar"
        context['titulo']="Inasistencia"
        return context
    

class InasistenciaDetalleView(PermissionRequiredMixin, DetailView):
    permission_required = ('recepcion.view_asistencia')
    model = Asistencia
    template_name = "recepcion/asistencia/detalle_inasistencia.html"
    context_object_name = 'contexto_inasistencia'
    success_url = reverse_lazy('recepcion_app:asistencia_personal_inicio')
     
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)    

    def get_context_data(self, **kwargs):
        context = super(AsistenciaPersonalView,self).get_context_data(**kwargs)
        asistencias = Asistencia.objects.get(id = self.kwargs['pk'])

        context['contexto_inasistencia'] = asistencias

    def get_context_data(self, **kwargs):
        self.request.session['primero'] = True
        context = super(InasistenciaDetalleView, self).get_context_data(**kwargs)
        context['titulo']="Inasistencia | Permisos"
        return context

class InasistenciaAprobarView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('recepcion.change_asistencia')
    model = Asistencia
    template_name = "includes/formulario generico.html"
    form_class = InasistenciaAprobarForm
    success_url = reverse_lazy('recepcion_app:asistencia_personal_inicio')

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)    

    def form_valid(self, form):
        form.instance.estado_solicitud = 2
        form.instance.editar_solicitud = False
        registro_guardar(self.object, self.request)
        self.object.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(InasistenciaAprobarView, self).get_context_data(**kwargs)
        context['accion']="Aprobar"
        context['titulo']="Inasistencia"
        return context
    
class InasistenciaRechazarView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('recepcion.change_asistencia')
    model = Asistencia
    template_name = "includes/formulario generico.html"
    form_class = InasistenciaRechazarForm
    success_url = reverse_lazy('recepcion_app:asistencia_personal_inicio')

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)    

    def form_valid(self, form):
        form.instance.estado_solicitud = 3
        registro_guardar(self.object, self.request)
        self.object.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(InasistenciaRechazarView, self).get_context_data(**kwargs)
        context['accion']="Rechazar"
        context['titulo']="Inasistencia"
        return context

