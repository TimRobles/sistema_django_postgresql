from django.shortcuts import render
from applications.importaciones import *
from django.core.paginator import Paginator
from applications.funciones import registrar_excepcion

from django import forms

from .forms import (
    ProblemaBuscarForm,
    ProblemaForm,
    ProblemaUpdateForm,
    ProblemaDetalleForm,
    ProblemaDetalleUpdateForm,
    ProblemaDetalleNotaSolucionForm,
    SolicitudBuscarForm,
    SolicitudForm,
    SolicitudUpdateForm,
    SolicitudDetalleForm,
    SolicitudDetalleUpdateForm,
    SolicitudMotivoRechazoUpdateForm,
)

from .models import (
    Problema,
    ProblemaDetalle,
    Solicitud,
    SolicitudDetalle
)

class ProblemaListView(PermissionRequiredMixin, FormView):
    permission_required = ('soporte.view_problema')

    template_name = "soporte/problema/inicio.html"
    form_class = ProblemaBuscarForm

    def get_form_kwargs(self):
        kwargs = super(ProblemaListView, self).get_form_kwargs()
        kwargs['filtro_titulo'] = self.request.GET.get('titulo')
        kwargs['filtro_estado'] = self.request.GET.get('estado')
        kwargs['filtro_usuario'] = self.request.GET.get('usuario')
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super(ProblemaListView,self).get_context_data(**kwargs)
        problemas = Problema.objects.all().order_by('-created_at')

        filtro_titulo = self.request.GET.get('titulo')
        filtro_estado = self.request.GET.get('estado')
        filtro_usuario = self.request.GET.get('usuario')

        contexto_filtro = []

        if filtro_titulo:
            condicion = Q(titulo__unaccent__icontains = filtro_titulo.split(" ")[0])
            for palabra in filtro_titulo.split(" ")[1:]:
                condicion &= Q(titulo__unaccent__icontains = palabra)
            encuesta_crm = encuesta_crm.filter(condicion)
            contexto_filtro.append(f"titulo={filtro_titulo}")

        if filtro_estado:
            condicion = Q(estado = filtro_estado)
            nota_control_calidad_stock = nota_control_calidad_stock.filter(condicion)
            contexto_filtro.append(f"estado={filtro_estado}")
        
        if filtro_usuario:
            condicion = Q(created_by = filtro_usuario)
            nota_control_calidad_stock = nota_control_calidad_stock.filter(condicion)
            contexto_filtro.append(f"usuario={filtro_usuario}")        

        context['contexto_filtro'] = "&".join(contexto_filtro)

        context['pagina_filtro'] = ""
        if self.request.GET.get('page'):
            if context['contexto_filtro']:
                context['pagina_filtro'] = f'&page={self.request.GET.get("page")}'
            else:
                context['pagina_filtro'] = f'page={self.request.GET.get("page")}'
        context['contexto_filtro'] = '?' + context['contexto_filtro']

        objectsxpage = 15 # Show 15 objects per page.

        if len(problemas) > objectsxpage:
            paginator = Paginator(problemas, objectsxpage)
            page_number = self.request.GET.get('page')
            problemas = paginator.get_page(page_number)

        context['contexto_problemas'] = problemas
        context['contexto_pagina'] = problemas

        return context

def ProblemaTabla(request):
    data = dict()
    if request.method == 'GET':
        template = 'soporte/problema/inicio_tabla.html'
        context = {}
        problemas = Problema.objects.all().order_by('-created_at')

        filtro_titulo = request.GET.get('titulo')
        filtro_estado = request.GET.get('estado')
        filtro_usuario = request.GET.get('usuario')
        
        contexto_filtro = []

        if filtro_titulo:
            condicion = Q(titulo__unaccent__icontains = filtro_titulo.split(" ")[0])
            for palabra in filtro_titulo.split(" ")[1:]:
                condicion &= Q(titulo__unaccent__icontains = palabra)
            encuesta_crm = encuesta_crm.filter(condicion)
            contexto_filtro.append(f"titulo={filtro_titulo}")

        if filtro_estado:
            condicion = Q(estado = filtro_estado)
            nota_control_calidad_stock = nota_control_calidad_stock.filter(condicion)
            contexto_filtro.append(f"estado={filtro_estado}")

        if filtro_usuario:
            condicion = Q(created_by = filtro_usuario)
            nota_control_calidad_stock = nota_control_calidad_stock.filter(condicion)
            contexto_filtro.append(f"usuario={filtro_usuario}")

        context['contexto_filtro'] = "&".join(contexto_filtro)

        context['pagina_filtro'] = ""
        if request.GET.get('page'):
            if context['contexto_filtro']:
                context['pagina_filtro'] = f'&page={request.GET.get("page")}'
            else:
                context['pagina_filtro'] = f'page={request.GET.get("page")}'
        context['contexto_filtro'] = '?' + context['contexto_filtro']

        objectsxpage = 15 # Show 15 objects per page.

        if len(problemas) > objectsxpage:
            paginator = Paginator(problemas, objectsxpage)
            page_number = request.GET.get('page')
            problemas = paginator.get_page(page_number)
   
        context['contexto_problemas'] = problemas
        context['contexto_pagina'] = problemas

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)

class ProblemaCreateView(BSModalCreateView):
    model = Problema
    template_name = "includes/formulario generico.html"
    form_class = ProblemaForm
    success_url = reverse_lazy('soporte_app:problema_inicio')

    def get_context_data(self, **kwargs):
        context = super(ProblemaCreateView, self).get_context_data(**kwargs)
        context['accion']="Registrar"
        context['titulo']="Problema"
        return context

    def form_valid(self, form):
        form.instance.estado = 1
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)
    
class  ProblemaUpdateView(BSModalUpdateView):
    model = Problema
    template_name = "includes/formulario generico.html"
    form_class = ProblemaUpdateForm
    success_url = reverse_lazy('soporte_app:problema_inicio')

    def get_context_data(self, **kwargs):
        context = super(ProblemaUpdateView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        context['titulo'] = "Problema"
        return context

    def form_valid(self, form):
        registro_guardar(form.instance, self.request)        
        return super().form_valid(form)

class ProblemaDeleteView(BSModalDeleteView):
    model = Problema
    template_name = "includes/eliminar generico.html"
    context_object_name = 'contexto_problemas' 

    def get_success_url(self, **kwargs):
        return reverse_lazy('soporte_app:problema_inicio')

    def get_context_data(self, **kwargs):
        context = super(ProblemaDeleteView, self).get_context_data(**kwargs)
        context['accion'] = "Eliminar"
        context['titulo'] = "Problema"
        context['item'] = self.object.titulo
        return context


class ProblemaDetailView(PermissionRequiredMixin,DetailView):
    permission_required = ('soporte.view_problemadetalle')

    model = Problema
    template_name = "soporte/problema/detalle.html"
    context_object_name = 'contexto_problema'

    def get_context_data(self, **kwargs):
        problema = Problema.objects.get(id = self.kwargs['pk'])
        context = super(ProblemaDetailView, self).get_context_data(**kwargs)
        context['contexto_problema_detalle'] = ProblemaDetalle.objects.filter(problema = problema)

        if 'soporte.delete_problemadetalle' in self.request.user.get_all_permissions():
            context['permiso_botones_problema'] = True

        return context

def ProblemaDetalleTabla(request, pk):
    data = dict()
    if request.method == 'GET':
        template = 'soporte/problema/detalle_tabla.html'
        context = {}
        problema = Problema.objects.get(id = pk)
        context['contexto_problema'] = problema
        context['contexto_problema_detalle'] = ProblemaDetalle.objects.filter(problema = problema)

        if 'soporte.delete_problemadetalle' in request.user.get_all_permissions():
            context['permiso_botones_problema'] = True

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)


class ProblemaDetalleCreateView(BSModalCreateView):
    model = ProblemaDetalle
    template_name = "includes/formulario generico.html"
    form_class = ProblemaDetalleForm

    def get_success_url(self, **kwargs):
        return reverse_lazy('soporte_app:problema_detalle', kwargs={'pk': self.kwargs['problema_id']})

    def form_valid(self, form):
        form.instance.problema = Problema.objects.get(id = self.kwargs['problema_id'])
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ProblemaDetalleCreateView, self).get_context_data(**kwargs)
        context['accion']="Agregar Imagenes"
        context['titulo']="del problema"
        return context


class ProblemaDetalleDeleteView(BSModalDeleteView):
    model = ProblemaDetalle
    template_name = "includes/eliminar generico.html"
    
    def get_success_url(self, **kwargs):
        detalle = ProblemaDetalle.objects.get(id = self.kwargs['pk'])
        return reverse_lazy('soporte_app:problema_detalle', kwargs={'pk':detalle.problema.id})
    
    def get_context_data(self, **kwargs):
        context = super(ProblemaDetalleDeleteView, self).get_context_data(**kwargs)
        context['accion']="Eliminar"
        context['titulo']="Item"
        context['item'] = ("URL:" + str(self.object.url) +  "\n" + "Imagen:" + str(self.object.imagen))
        context['dar_baja'] = "true"
        return context


class ProblemaDetalleUpdateView(BSModalUpdateView):
    model = ProblemaDetalle
    template_name = "includes/formulario generico.html"
    form_class = ProblemaDetalleUpdateForm

    def get_success_url(self, **kwargs):
        return reverse_lazy('soporte_app:problema_detalle', kwargs={'pk':self.get_object().problema_id})

    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ProblemaDetalleUpdateView, self).get_context_data(**kwargs)
        context['accion']="Actualizar"
        context['titulo']="Item"
        return context
    
class ProblemaDetalleNotaSolucionView(BSModalUpdateView):
    model = ProblemaDetalle
    template_name = "includes/formulario generico.html"
    form_class = ProblemaDetalleNotaSolucionForm

    def get_success_url(self, **kwargs):
        return reverse_lazy('soporte_app:problema_detalle', kwargs={'pk':self.get_object().problema_id})

    def form_valid(self, form):
        form.instance.estado = 4
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ProblemaDetalleNotaSolucionView, self).get_context_data(**kwargs)
        context['accion']="Nota"
        context['titulo']="Solución"
        return context


class ProblemaNotificarView(BSModalDeleteView):
    model = Problema
    template_name = "includes/eliminar generico.html"
    
    def get_success_url(self, **kwargs):
        return reverse_lazy('soporte_app:problema_detalle', kwargs={'pk':self.get_object().id})

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            self.object = self.get_object()
            self.object.estado = 2
            registro_guardar(self.object, self.request)
            self.object.save()
            messages.success(request, MENSAJE_PROBLEMA_NOTIFICADO)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(ProblemaNotificarView, self).get_context_data(**kwargs)
        context['accion'] = "Notificar"
        context['titulo'] = "Problema"
        context['dar_baja'] = "true"
        context['item'] = str(self.object.titulo)
        return context


class ProblemaDetalleIniciarSolucionView(BSModalDeleteView):
    model = Problema
    template_name = "includes/eliminar generico.html"    
    
    def get_success_url(self, **kwargs):
        return reverse_lazy('soporte_app:problema_detalle', kwargs={'pk':self.get_object().id})

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            self.object = self.get_object()
            self.object.estado = 3
            registro_guardar(self.object, self.request)
            self.object.save()
            messages.success(request, MENSAJE_INICIAR_SOLUCION)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(ProblemaDetalleIniciarSolucionView, self).get_context_data(**kwargs)
        context['accion'] = "Iniciar"
        context['titulo'] = "Solución"
        context['dar_baja'] = "true"
        context['item'] = str(self.object.titulo)
        return context



class ProblemaDetalleFinalizarProblemaView(BSModalDeleteView):
    model = Problema
    template_name = "includes/eliminar generico.html"

    def get_success_url(self, **kwargs):
        return reverse_lazy('soporte_app:problema_detalle', kwargs={'pk':self.get_object().id})

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            self.object = self.get_object()
            self.object.estado = 4
            registro_guardar(self.object, self.request)
            self.object.save()
            messages.success(request, MENSAJE_FINALIZAR_PROBLEMA)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(ProblemaDetalleFinalizarProblemaView, self).get_context_data(**kwargs)
        context['accion'] = "Finalizar"
        context['titulo'] = "Problema"
        context['dar_baja'] = "true"
        context['item'] = str(self.object.titulo)
        return context

#----- SOLICITUD ---------

class SolicitudListView(PermissionRequiredMixin, FormView):
    permission_required = ('soporte.view_solicitud')

    template_name = "soporte/solicitud/inicio.html"
    form_class = SolicitudBuscarForm

    def get_form_kwargs(self):
        kwargs = super(SolicitudListView, self).get_form_kwargs()
        kwargs['filtro_titulo'] = self.request.GET.get('titulo')
        kwargs['filtro_estado'] = self.request.GET.get('estado')
        kwargs['filtro_usuario'] = self.request.GET.get('usuario')
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super(SolicitudListView,self).get_context_data(**kwargs)
        solicitudes = Solicitud.objects.all().order_by('-created_at')

        filtro_titulo = self.request.GET.get('titulo')
        filtro_estado = self.request.GET.get('estado')
        filtro_usuario = self.request.GET.get('usuario')

        contexto_filtro = []

        if filtro_titulo:
            condicion = Q(titulo__unaccent__icontains = filtro_titulo.split(" ")[0])
            for palabra in filtro_titulo.split(" ")[1:]:
                condicion &= Q(titulo__unaccent__icontains = palabra)
            encuesta_crm = encuesta_crm.filter(condicion)
            contexto_filtro.append(f"titulo={filtro_titulo}")

        if filtro_estado:
            condicion = Q(estado = filtro_estado)
            nota_control_calidad_stock = nota_control_calidad_stock.filter(condicion)
            contexto_filtro.append(f"estado={filtro_estado}")
        
        if filtro_usuario:
            condicion = Q(created_by = filtro_usuario)
            nota_control_calidad_stock = nota_control_calidad_stock.filter(condicion)
            contexto_filtro.append(f"usuario={filtro_usuario}")        

        context['contexto_filtro'] = "&".join(contexto_filtro)

        context['pagina_filtro'] = ""
        if self.request.GET.get('page'):
            if context['contexto_filtro']:
                context['pagina_filtro'] = f'&page={self.request.GET.get("page")}'
            else:
                context['pagina_filtro'] = f'page={self.request.GET.get("page")}'
        context['contexto_filtro'] = '?' + context['contexto_filtro']

        objectsxpage = 15 # Show 15 objects per page.

        if len(solicitudes) > objectsxpage:
            paginator = Paginator(solicitudes, objectsxpage)
            page_number = self.request.GET.get('page')
            solicitudes = paginator.get_page(page_number)

        context['contexto_solicitudes'] = solicitudes
        context['contexto_pagina'] = solicitudes

        return context


def SolicitudTabla(request):
    data = dict()
    if request.method == 'GET':
        template = 'soporte/solicitud/inicio_tabla.html'
        context = {}
        solicitudes = Solicitud.objects.all().order_by('-created_at')

        filtro_titulo = request.GET.get('titulo')
        filtro_estado = request.GET.get('estado')
        filtro_usuario = request.GET.get('usuario')
        
        contexto_filtro = []

        if filtro_titulo:
            condicion = Q(titulo__unaccent__icontains = filtro_titulo.split(" ")[0])
            for palabra in filtro_titulo.split(" ")[1:]:
                condicion &= Q(titulo__unaccent__icontains = palabra)
            encuesta_crm = encuesta_crm.filter(condicion)
            contexto_filtro.append(f"titulo={filtro_titulo}")

        if filtro_estado:
            condicion = Q(estado = filtro_estado)
            nota_control_calidad_stock = nota_control_calidad_stock.filter(condicion)
            contexto_filtro.append(f"estado={filtro_estado}")

        if filtro_usuario:
            condicion = Q(created_by = filtro_usuario)
            nota_control_calidad_stock = nota_control_calidad_stock.filter(condicion)
            contexto_filtro.append(f"usuario={filtro_usuario}")

        context['contexto_filtro'] = "&".join(contexto_filtro)

        context['pagina_filtro'] = ""
        if request.GET.get('page'):
            if context['contexto_filtro']:
                context['pagina_filtro'] = f'&page={request.GET.get("page")}'
            else:
                context['pagina_filtro'] = f'page={request.GET.get("page")}'
        context['contexto_filtro'] = '?' + context['contexto_filtro']

        objectsxpage = 15 # Show 15 objects per page.

        if len(solicitudes) > objectsxpage:
            paginator = Paginator(solicitudes, objectsxpage)
            page_number = request.GET.get('page')
            solicitudes = paginator.get_page(page_number)
   
        context['contexto_solicitudes'] = solicitudes
        context['contexto_pagina'] = solicitudes

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)


class SolicitudCreateView(BSModalCreateView):
    model = Solicitud
    template_name = "includes/formulario generico.html"
    form_class = SolicitudForm
    success_url = reverse_lazy('soporte_app:solicitud_inicio')

    def form_valid(self, form):
        form.instance.estado = 1
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super(SolicitudCreateView, self).get_context_data(**kwargs)
        context['accion']="Registrar"
        context['titulo']="Solicitud"
        return context


class  SolicitudUpdateView(BSModalUpdateView):
    model = Solicitud
    template_name = "includes/formulario generico.html"
    form_class = SolicitudUpdateForm
    success_url = reverse_lazy('soporte_app:solicitud_inicio')

    def get_context_data(self, **kwargs):
        context = super(SolicitudUpdateView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        context['titulo'] = "Solicitud"
        return context

    def form_valid(self, form):
        registro_guardar(form.instance, self.request)        
        return super().form_valid(form)

class SolicitudDeleteView(BSModalDeleteView):
    model = Solicitud
    template_name = "includes/eliminar generico.html"
    context_object_name = 'contexto_solicitudes' 

    def get_success_url(self, **kwargs):
        return reverse_lazy('soporte_app:solicitud_inicio')

    def get_context_data(self, **kwargs):
        context = super(SolicitudDeleteView, self).get_context_data(**kwargs)
        context['accion'] = "Eliminar"
        context['titulo'] = "Solicitud"
        context['item'] = self.object.titulo
        return context

class SolicitudDetailView(PermissionRequiredMixin, DetailView):
    permission_required = ('soporte.view_solicituddetalle')

    model = Solicitud
    template_name = "soporte/solicitud/detalle.html"
    context_object_name = 'contexto_solicitud'

    def get_context_data(self, **kwargs):
        solicitud = Solicitud.objects.get(id = self.kwargs['pk'])
        context = super(SolicitudDetailView, self).get_context_data(**kwargs)
        context['contexto_solicitud_detalle'] = SolicitudDetalle.objects.filter(solicitud = solicitud)
        if 'soporte.delete_solicituddetalle' in self.request.user.get_all_permissions():
            context['permiso_botones_solicitud'] = True

        return context

def SolicitudDetalleTabla(request, pk):
    data = dict()
    if request.method == 'GET':
        template = 'soporte/solicitud/detalle_tabla.html'
        context = {}
        solicitud = Solicitud.objects.get(id = pk)
        context['contexto_solicitud'] = solicitud
        context['contexto_solicitud_detalle'] = SolicitudDetalle.objects.filter(solicitud = solicitud)
        if 'soporte.delete_solicituddetalle' in request.user.get_all_permissions():
            context['permiso_botones_solicitud'] = True
        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)

class SolicitudDetalleCreateView(BSModalCreateView):
    model = SolicitudDetalle
    template_name = "includes/formulario generico.html"
    form_class = SolicitudDetalleForm

    def get_success_url(self, **kwargs):
        return reverse_lazy('soporte_app:solicitud_detalle', kwargs={'pk': self.kwargs['solicitud_id']})

    def form_valid(self, form):
        form.instance.solicitud = Solicitud.objects.get(id = self.kwargs['solicitud_id'])
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(SolicitudDetalleCreateView, self).get_context_data(**kwargs)
        context['accion']="Agregar Documentación"
        context['titulo']="de la solicitud resulta"
        return context


class SolicitudDetalleDeleteView(BSModalDeleteView):
    model = SolicitudDetalle
    template_name = "includes/eliminar generico.html"
    
    def get_success_url(self, **kwargs):
        detalle = SolicitudDetalle.objects.get(id = self.kwargs['pk'])
        return reverse_lazy('soporte_app:solicitud_detalle', kwargs={'pk':detalle.solicitud.id})
    
    def get_context_data(self, **kwargs):
        context = super(SolicitudDetalleDeleteView, self).get_context_data(**kwargs)
        context['accion']="Eliminar"
        context['titulo']="Item"
        context['item'] = ("URL:" + str(self.object.url) +  "\n" + "Imagen:" + str(self.object.imagen))
        context['dar_baja'] = "true"
        return context


class SolicitudDetalleUpdateView(BSModalUpdateView):
    model = SolicitudDetalle
    template_name = "includes/formulario generico.html"
    form_class = SolicitudDetalleUpdateForm

    def get_success_url(self, **kwargs):
        return reverse_lazy('soporte_app:solicitud_detalle', kwargs={'pk':self.get_object().solicitud_id})

    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(SolicitudDetalleUpdateView, self).get_context_data(**kwargs)
        context['accion']="Actualizar"
        context['titulo']="Item"
        return context


class SolicitudSolicitarView(BSModalDeleteView):
    model = Solicitud
    template_name = "includes/eliminar generico.html"
    
    def get_success_url(self):
        return reverse_lazy('soporte_app:solicitud_detalle', kwargs={'pk':self.get_object().id})

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            self.object = self.get_object()
            self.object.estado = 2
            registro_guardar(self.object, self.request)
            self.object.save()
            messages.success(request, MENSAJE_SOLICITADO)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(SolicitudSolicitarView, self).get_context_data(**kwargs)
        context['accion'] = "Solicitar"
        context['titulo'] = "Solicitud"
        context['dar_baja'] = "true"
        context['item'] = str(self.object.titulo)
        return context

class SolicitudAprobarView(BSModalDeleteView):
    model = Solicitud
    template_name = "includes/eliminar generico.html"
    
    def get_success_url(self):
        return reverse_lazy('soporte_app:solicitud_detalle', kwargs={'pk':self.get_object().id})

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            self.object = self.get_object()
            self.object.estado = 3
            registro_guardar(self.object, self.request)
            self.object.save()
            messages.success(request, MENSAJE_SOLICITUD_APROBADA)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(SolicitudAprobarView, self).get_context_data(**kwargs)
        context['accion'] = "Aprobar"
        context['titulo'] = "."
        context['dar_baja'] = "true"
        context['item'] = str(self.object.titulo)
        return context

class SolicitudRechazarView(BSModalUpdateView):
    model = Solicitud
    template_name = "includes/formulario generico.html"
    form_class = SolicitudMotivoRechazoUpdateForm
    success_url = reverse_lazy('soporte_app:solicitud_inicio')

    def get_success_url(self):
        return reverse_lazy('soporte_app:solicitud_detalle', kwargs={'pk':self.get_object().id})
   
    def form_valid(self, form):
        form.instance.estado = 4
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(SolicitudRechazarView, self).get_context_data(**kwargs)
        context['accion']="Rechazar"
        context['titulo']="Solicitud"
        return context

class SolicitudIniciarView(BSModalDeleteView):
    model = Solicitud
    template_name = "includes/eliminar generico.html"
    
    def get_success_url(self):
        return reverse_lazy('soporte_app:solicitud_detalle', kwargs={'pk':self.get_object().id})

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            self.object = self.get_object()
            self.object.estado = 5
            registro_guardar(self.object, self.request)
            self.object.save()
            messages.success(request, MENSAJE_SOLICITUD_INICIADA)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(SolicitudIniciarView, self).get_context_data(**kwargs)
        context['accion'] = "Iniciar"
        context['titulo'] = "."
        context['dar_baja'] = "true"
        context['item'] = str(self.object.titulo)
        return context

class SolicitudResolverView(BSModalDeleteView):
    model = Solicitud
    template_name = "includes/eliminar generico.html"
    
    def get_success_url(self):
        return reverse_lazy('soporte_app:solicitud_detalle', kwargs={'pk':self.get_object().id})

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            self.object = self.get_object()
            self.object.estado = 6
            registro_guardar(self.object, self.request)
            self.object.save()
            messages.success(request, MENSAJE_SOLICITUD_RESULTA)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(SolicitudResolverView, self).get_context_data(**kwargs)
        context['accion'] = "Resolver"
        context['titulo'] = "."
        context['dar_baja'] = "true"
        context['item'] = str(self.object.titulo)
        return context
