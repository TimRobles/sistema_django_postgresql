
from django.shortcuts import render
from applications.importaciones import *
from django.core.paginator import Paginator
from applications.crm.models import EventoCRM
from applications.clientes.models import Cliente


from applications.funciones import registrar_excepcion

from .forms import(
    TipoTareaForm,
    TareaForm,
    TareaDescripcionForm,
    HistorialComentarioTareaForm,
    TareaBuscarForm,
    TareaActualizarForm,
    TareaAsignarForm,
    TareaActualizarClienteForm,
    )
           
from .models import(
    TipoTarea,
    Tarea,
    HistorialComentarioTarea,
)


class TipoTareaListView(PermissionRequiredMixin, ListView):
    permission_required = ('tarea.view_tipotarea')
    model = TipoTarea
    template_name = "tarea/tipo_tarea/inicio.html"
    
    def get_context_data(self, **kwargs):
        context = super(TipoTareaListView, self).get_context_data(**kwargs)
        tipo_tarea = TipoTarea.objects.all()
        objectsxpage =  10 # Show 10 objects per page.

        if len(tipo_tarea) > objectsxpage:
            paginator = Paginator(tipo_tarea, objectsxpage)
            page_number = self.request.GET.get('page')
            tipo_tarea = paginator.get_page(page_number)

        context['contexto_tipo_tarea'] = tipo_tarea
        context['contexto_pagina'] = tipo_tarea
        context['contexto_filtro'] = '?'
        return context

def TipoTareaTabla(request):
    data = dict()
    if request.method == 'GET':
        template = 'tarea/tipo_tarea/inicio_tabla.html'
        context = {}
        tipo_tarea = TipoTarea.objects.all()
        objectsxpage =  10 # Show 10 objects per page.

        if len(tipo_tarea) > objectsxpage:
            paginator = Paginator(tipo_tarea, objectsxpage)
            page_number = request.GET.get('page')
            tipo_tarea = paginator.get_page(page_number)

        context['contexto_tipo_tarea'] = tipo_tarea
        context['contexto_pagina'] = tipo_tarea
        context['contexto_filtro'] = '?'

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)

class TipoTareaCreateView(PermissionRequiredMixin, BSModalCreateView):
    permission_required = ('tarea.add_tipotarea')
    model = TipoTarea
    template_name = "includes/formulario generico.html"
    form_class = TipoTareaForm
    success_url = reverse_lazy('tarea_app:tipo_tarea_inicio')

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(TipoTareaCreateView, self).get_context_data(**kwargs)
        context['accion']="Registrar"
        context['titulo']="Tipo Tarea"
        return context

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)

        return super().form_valid(form)

class TipoTareaUpdateView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('tarea.change_tipotarea')
    model = TipoTarea
    template_name ="includes/formulario generico.html"
    form_class =  TipoTareaForm
    success_url = reverse_lazy('tarea_app:tipo_tarea_inicio')

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(TipoTareaUpdateView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        context['titulo'] = "Tipo Tarea"
        return context

    def form_valid(self, form):
        registro_guardar(form.instance, self.request)        
        return super().form_valid(form)


class TareaListView(PermissionRequiredMixin, FormView):
    permission_required = ('tarea.view_tarea')
    template_name = "tarea/tarea/inicio.html"
    form_class = TareaBuscarForm
    success_url = '.'

    def get_form_kwargs(self):
        kwargs = super(TareaListView, self).get_form_kwargs()
        kwargs['filtro_estado'] = self.request.GET.get('estado')
        kwargs['filtro_fecha_inicio'] = self.request.GET.get('fecha_inicio')
        kwargs['filtro_tipo_tarea'] = self.request.GET.get('tipo_tarea')

        return kwargs

    def get_context_data(self, **kwargs):
        context = super(TareaListView,self).get_context_data(**kwargs)
        tarea = Tarea.objects.all()
        
        filtro_estado = self.request.GET.get('estado')
        filtro_fecha_inicio = self.request.GET.get('fecha_inicio')
        filtro_tipo_tarea = self.request.GET.get('tipo_tarea')
        
        contexto_filtro = []   
        
        if filtro_estado:
            condicion = Q(estado__icontains = filtro_estado)
            tarea = tarea.filter(condicion)
            contexto_filtro.append(f"estado={filtro_estado}")

        if filtro_fecha_inicio:
            condicion = Q(fecha_inicio = filtro_fecha_inicio)
            tarea = tarea.filter(condicion)
            contexto_filtro.append(f"fecha_inicio={filtro_fecha_inicio}")

        if filtro_tipo_tarea:
            condicion = Q(tipo_tarea = filtro_tipo_tarea)
            tarea = tarea.filter(condicion)
            contexto_filtro.append(f"tipo_tarea={filtro_tipo_tarea}")

        context['contexto_filtro'] = "&".join(contexto_filtro)

        context['pagina_filtro'] = ""
        if self.request.GET.get('page'):
            if context['contexto_filtro']:
                context['pagina_filtro'] = f'&page={self.request.GET.get("page")}'
            else:
                context['pagina_filtro'] = f'page={self.request.GET.get("page")}'
        context['contexto_filtro'] = '?' + context['contexto_filtro']

        objectsxpage =  15 # Show 15 objects per page.

        if len(tarea) > objectsxpage:
            paginator = Paginator(tarea, objectsxpage)
            page_number = self.request.GET.get('page')
            tarea = paginator.get_page(page_number)
   
        context['contexto_pagina'] = tarea
        context['contexto_tarea'] = tarea
        return context

def TareaTabla(request):
    data = dict()
    if request.method == 'GET':
        template = 'tarea/tarea/inicio_tabla.html'
        context = {}
        tarea = Tarea.objects.all()

        filtro_estado = request.GET.get('estado')
        filtro_fecha_inicio = request.GET.get('fecha_inicio')

        contexto_filtro = []

        if filtro_estado:
            condicion = Q(estado__icontains = filtro_estado)
            tarea = tarea.filter(condicion)
            contexto_filtro.append(f"estado={filtro_estado}")

        if filtro_fecha_inicio:
            condicion = Q(fecha_inicio = filtro_fecha_inicio)
            tarea = tarea.filter(condicion)
            contexto_filtro.append(f"fecha_inicio={filtro_fecha_inicio}")

        context['contexto_filtro'] = "&".join(contexto_filtro)

        context['pagina_filtro'] = ""
        if request.GET.get('page'):
            if context['contexto_filtro']:
                context['pagina_filtro'] = f'&page={request.GET.get("page")}'
            else:
                context['pagina_filtro'] = f'page={request.GET.get("page")}'
        context['contexto_filtro'] = '?' + context['contexto_filtro']

        objectsxpage =  15 # Show 15 objects per page.

        if len(tarea) > objectsxpage:
            paginator = Paginator(tarea, objectsxpage)
            page_number = request.GET.get('page')
            tarea = paginator.get_page(page_number)
   
        context['contexto_pagina'] = tarea
        context['contexto_tarea'] = tarea

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)

    
class TareaCreateView(PermissionRequiredMixin, BSModalCreateView):
    permission_required = ('tarea.add_tarea')
    model = Tarea
    template_name = "tarea/tarea/crear.html"
    form_class = TareaForm

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('tarea_app:tarea_inicio')
    
    def form_valid(self, form):
        cliente = form.cleaned_data.get('cliente')
        try:
            form.instance.content_type = ContentType.objects.get_for_model(cliente)
            form.instance.id_registro = cliente.id
        except:
            pass
        
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(TareaCreateView, self).get_context_data(**kwargs)
        context['accion']="Registrar"
        context['titulo']="Tarea"
        return context
    
class TareaUpdateView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('tarea.change_tarea')
    model = Tarea
    template_name ="tarea/tarea/actualizar.html"
    form_class =  TareaActualizarForm
    success_url = reverse_lazy('tarea_app:tarea_inicio')

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        registro_guardar(form.instance, self.request)        
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super(TareaUpdateView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        context['titulo'] = "Tarea"
        return context

class TareaDetailView(DetailView):
    model = Tarea
    template_name = "tarea/tarea/detalle.html"
    context_object_name = 'contexto_tarea'

    def get_context_data(self, **kwargs):
        tarea = Tarea.objects.get(id = self.kwargs['pk'])
        try:
            asignados = tarea.content_type.get_object_for_this_type(id = tarea.id_registro)
            content_cliente = ContentType.objects.get_for_model(Cliente)
            content_evento =ContentType.objects.get_for_model(EventoCRM)
        except:
            pass
        context = super(TareaDetailView, self).get_context_data(**kwargs)
        context['contexto_tarea'] = tarea
        context['comentarios'] = HistorialComentarioTarea.objects.filter(tarea = tarea)
        try:
            context['asignados']= asignados
            context['content_cliente']= content_cliente
            context['content_evento']= content_evento
        except:
            pass
        
        return context
    
def TareaDetailTabla(request, pk):
    data = dict()
    if request.method == 'GET':
        template = 'tarea/tarea/detalle_tabla.html'
        context = {}
        tarea = Tarea.objects.get(id = pk)
        try:
            asignados = tarea.content_type.get_object_for_this_type(id = tarea.id_registro)
            content_cliente = ContentType.objects.get_for_model(Cliente)
            content_evento =ContentType.objects.get_for_model(EventoCRM)

        except:
            pass
        context['contexto_tarea'] = tarea
        context['comentarios'] = HistorialComentarioTarea.objects.filter(tarea = tarea)
        try:
            context['asignados']= asignados
            context['content_cliente']= content_cliente
            context['content_evento']= content_evento

        except:
            pass

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)


class  TareaDetalleDescripcionView(BSModalUpdateView):
    model = Tarea
    template_name = "includes/formulario generico.html"
    form_class = TareaDescripcionForm

    def get_success_url(self, **kwargs):
        return reverse_lazy('tarea_app:tarea_detalle', kwargs={'pk':self.object.id})

    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(TareaDetalleDescripcionView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        return context

class TareaDetalleHistorialComentarioCreateView(BSModalCreateView):
    model = HistorialComentarioTarea
    template_name = "includes/formulario generico.html"
    form_class = HistorialComentarioTareaForm

    def get_success_url(self, **kwargs):
        return reverse_lazy('tarea_app:tarea_detalle', kwargs={'pk':self.kwargs['tarea_id']})
    
    def form_valid(self, form):
        tarea = Tarea.objects.get(id = self.kwargs['tarea_id'])
        form.instance.tarea = tarea
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)  
    
    def get_context_data(self, **kwargs):
        context = super(TareaDetalleHistorialComentarioCreateView, self).get_context_data(**kwargs)
        context['accion']="Registrar"
        context['titulo']="Comentario"
        return context

class TareaDetalleHistorialComentarioUpdateView(BSModalUpdateView):
    model = HistorialComentarioTarea
    template_name = "includes/formulario generico.html"
    form_class = HistorialComentarioTareaForm

    def get_success_url(self, **kwargs):
        return reverse_lazy('tarea_app:tarea_detalle', kwargs={'pk':self.object.id})
    
    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)
       
    def get_context_data(self, **kwargs):
        context = super(TareaDetalleHistorialComentarioUpdateView, self).get_context_data(**kwargs)
        context['accion']="Actualizar"
        context['titulo']="Comentarios"
        return context

class TareaDetalleHistorialComentarioDeleteView(BSModalDeleteView):
    model = HistorialComentarioTarea
    template_name = "includes/eliminar generico.html"
    success_url = reverse_lazy('tarea_app:tarea_detalle')

    def get_success_url(self, **kwargs):
        return reverse_lazy('tarea_app:tarea_detalle', kwargs={'pk':self.object.id})
    
    def get_context_data(self, **kwargs):
        context = super(TareaDetalleHistorialComentarioDeleteView, self).get_context_data(**kwargs)
        context['accion']="Eliminar"
        context['titulo']="Comentario" + str(self.object.id)
        return context


class TareaAsignarView(BSModalUpdateView):
    model = Tarea
    template_name = "tarea/tarea/asignar.html"
    form_class = TareaAsignarForm

    def get_success_url(self, **kwargs):
        return reverse_lazy('tarea_app:tarea_detalle', kwargs={'pk':self.object.id})
    
    def form_valid(self, form):
        evento = form.cleaned_data.get('evento')

        if evento:
            form.instance.content_type = ContentType.objects.get_for_model(evento)
            form.instance.id_registro = evento.id

        registro_guardar(form.instance, self.request)
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super(TareaAsignarView, self).get_context_data(**kwargs)

        context['accion']="Asignar"
        context['titulo']="Evento"
        return context

class TareaFinalizarUpdateView(BSModalDeleteView):
    model = Tarea
    template_name ="includes/form generico.html"

    def get_success_url(self, **kwargs):
        return reverse_lazy('tarea_app:tarea_detalle', kwargs={'pk':self.object.id})
    
    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            self.object = self.get_object()
            self.object.estado = 3
            registro_guardar(self.object, self.request)
            self.object.save()
 
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(TareaFinalizarUpdateView, self).get_context_data(**kwargs)
        context['accion'] = "Finalizar"
        context['titulo'] = "Tarea"
        context['texto'] = '¿Está seguro de FINALIZAR la tarea?'
        context['item'] = self.get_object()
        return context

class TareaIniciarUpdateView(BSModalDeleteView):
    model = Tarea
    template_name ="includes/form generico.html"

    def get_success_url(self, **kwargs):
        return reverse_lazy('tarea_app:tarea_detalle', kwargs={'pk':self.object.id})
    
    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            self.object = self.get_object()
            self.object.estado = 2
            registro_guardar(self.object, self.request)
            self.object.save()
 
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(TareaIniciarUpdateView, self).get_context_data(**kwargs)
        context['accion'] = "Iniciar"
        context['titulo'] = "Tarea"
        context['texto'] = '¿Está seguro de INICIAR la tarea?'
        context['item'] = self.get_object()
        return context

class TareaRegistrarTipoTareaCreateView(BSModalCreateView):
    model = TipoTarea
    template_name = "includes/formulario generico.html"
    form_class = TipoTareaForm
    success_url = reverse_lazy('tarea_app:tarea_inicio')

    def get_context_data(self, **kwargs):
        context = super(TareaRegistrarTipoTareaCreateView, self).get_context_data(**kwargs)
        context['accion']="Registrar"
        context['titulo']="Tipo Tarea"
        return context

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)

        return super().form_valid(form)
    
class TareaActualizarClienteView(BSModalUpdateView):
    model = Tarea
    template_name = "tarea/tarea/asignar.html"
    form_class = TareaActualizarClienteForm

    def get_success_url(self, **kwargs):
        return reverse_lazy('tarea_app:tarea_detalle', kwargs={'pk':self.object.id})
    
    def form_valid(self, form):
        cliente = form.cleaned_data.get('cliente')

        if cliente:
            form.instance.content_type = ContentType.objects.get_for_model(cliente)
            form.instance.id_registro = cliente.id

        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(TareaActualizarClienteView, self).get_context_data(**kwargs)

        context['accion']="Actualizar"
        context['titulo']="Clientes"
        return context


# class TareaActualizarClienteView(BSModalUpdateView):
#     model = Tarea
#     template_name = "tarea/tarea/asignar.html"
#     form_class = TareaActualizarClienteForm

#     def get_success_url(self, **kwargs):
#         return reverse_lazy('tarea_app:tarea_detalle', kwargs={'pk':self.object.id})
    
#     def form_valid(self, form):
#         evento = form.cleaned_data.get('evento')

#         if evento:
#             form.instance.content_type = ContentType.objects.get_for_model(evento)
#             form.instance.id_registro = evento.id

#         registro_guardar(form.instance, self.request)
#         return super().form_valid(form)
    
#     def get_context_data(self, **kwargs):
#         context = super(TareaAsignarView, self).get_context_data(**kwargs)

#         context['accion']="Asignar"
#         context['titulo']="Evento"
#         return context