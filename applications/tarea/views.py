
from django.shortcuts import render
from applications.importaciones import *
from django.core.paginator import Paginator
from applications.crm.models import ClienteCRM, EventoCRM
from applications.funciones import registrar_excepcion

from .forms import(
    TipoTareaForm,
    TareaForm,
    TareaDescripcionForm,
    HistorialComentarioTareaForm,
    TareaBuscarForm,
    TareaActualizarForm,
    TareaAsignarForm,
    )
           
from .models import(
    TipoTarea,
    Tarea,
    HistorialComentarioTarea,
)

class TipoTareaListView(ListView):
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

class TipoTareaCreateView(BSModalCreateView):
    model = TipoTarea
    template_name = "includes/formulario generico.html"
    form_class = TipoTareaForm
    success_url = reverse_lazy('tarea_app:tipo_tarea_inicio')

    def get_context_data(self, **kwargs):
        context = super(TipoTareaCreateView, self).get_context_data(**kwargs)
        context['accion']="Registrar"
        context['titulo']="Tipo Tarea"
        return context

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)

        return super().form_valid(form)

class TipoTareaUpdateView(BSModalUpdateView):
    model = TipoTarea
    template_name ="includes/formulario generico.html"
    form_class =  TipoTareaForm
    success_url = reverse_lazy('tarea_app:tipo_tarea_inicio')
    
    def get_context_data(self, **kwargs):
        context = super(TipoTareaUpdateView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        context['titulo'] = "Tipo Tarea"
        return context

    def form_valid(self, form):
        registro_guardar(form.instance, self.request)        
        return super().form_valid(form)


class TareaListView(FormView):
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

    
class TareaCreateView(BSModalCreateView):
    model = Tarea
    template_name = "tarea/tarea/crear.html"
    form_class = TareaForm

    def get_success_url(self):
        return reverse_lazy('tarea_app:tarea_inicio')
    
    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(TareaCreateView, self).get_context_data(**kwargs)
        context['accion']="Registrar"
        context['titulo']="Tarea"
        return context
    
class TareaUpdateView(BSModalUpdateView):
    model = Tarea
    template_name ="tarea/tarea/actualizar.html"
    form_class =  TareaActualizarForm
    success_url = reverse_lazy('tarea_app:tarea_inicio')

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
            content_cliente = ContentType.objects.get_for_model(ClienteCRM)
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
            content_cliente = ContentType.objects.get_for_model(ClienteCRM)
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

class TareaDetalleHistorialComentarioDeleteView(BSModalDeleteView): #Falta redireccionar :(
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
        cliente = form.cleaned_data.get('cliente')
        evento = form.cleaned_data.get('evento')

        if cliente:
            form.instance.content_type = ContentType.objects.get_for_model(cliente)
            form.instance.id_registro = cliente.id

        elif evento:
            form.instance.content_type = ContentType.objects.get_for_model(evento)
            form.instance.id_registro = evento.id

        registro_guardar(form.instance, self.request)
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super(TareaAsignarView, self).get_context_data(**kwargs)

        context['accion']="Asignar"
        context['titulo']="Cliente o Evento"
        return context

class TareaCulminarUpdateView(BSModalUpdateView):
    model = Tarea
    template_name ="includes/formulario generico.html"

    def get_success_url(self, **kwargs):
        return reverse_lazy('tarea_app:tarea_detalle', kwargs={'pk':self.object.id})

    def get_context_data(self, **kwargs):
        context = super(TareaCulminarUpdateView, self).get_context_data(**kwargs)
        context['accion'] = "Culminar"
        context['titulo'] = "Tarea"
        return context
    
    def form_valid(self, form):
        form.instance.estado = 3
        registro_guardar(form.instance, self.request)        
        return super().form_valid(form)
    
