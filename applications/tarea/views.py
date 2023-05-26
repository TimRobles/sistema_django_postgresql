
from django.shortcuts import render
from applications.importaciones import *
from django.core.paginator import Paginator
from applications.clientes.models import Cliente, ClienteInterlocutor, InterlocutorCliente

from .forms import(
    TipoTareaForm,
    TareaForm,
    TareaDescripcionForm,
    HistorialComentarioTareaForm,
    TareaClienteForm,
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


class TareaListView(ListView):
    model = Tarea
    template_name = "tarea/tarea/inicio.html"
    
    def get_context_data(self, **kwargs):
        context = super(TareaListView, self).get_context_data(**kwargs)
        tarea = Tarea.objects.all()
        objectsxpage =  10 # Show 10 objects per page.

        if len(tarea) > objectsxpage:
            paginator = Paginator(tarea, objectsxpage)
            page_number = self.request.GET.get('page')
            tarea = paginator.get_page(page_number)
        
        context['contexto_tarea'] = tarea
        context['contexto_pagina'] = tarea
        context['contexto_filtro'] = '?'
        return context

def TareaTabla(request):
    data = dict()
    if request.method == 'GET':
        template = 'tarea/tarea/inicio_tabla.html'
        context = {}
        tarea = Tarea.objects.all()
        objectsxpage =  10 # Show 10 objects per page.

        if len(tarea) > objectsxpage:
            paginator = Paginator(tarea, objectsxpage)
            page_number = request.GET.get('page')
            tarea = paginator.get_page(page_number)

        context['contexto_tarea'] = tarea
        context['contexto_pagina'] = tarea
        context['contexto_filtro'] = '?'

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)

class TareaCreateView(BSModalCreateView):
    model = TipoTarea
    template_name = "includes/formulario generico.html"
    form_class = TareaForm
    success_url = reverse_lazy('tarea_app:tarea_inicio')

    def get_context_data(self, **kwargs):
        context = super(TareaCreateView, self).get_context_data(**kwargs)
        context['accion']="Registrar"
        context['titulo']="Tarea"
        return context

    def form_valid(self, form):
        registro_guardar(form.instance, self.request)

        return super().form_valid(form)
    
class TareaUpdateView(BSModalUpdateView):
    model = Tarea
    template_name ="includes/formulario generico.html"
    form_class =  TareaForm
    success_url = reverse_lazy('tarea_app:tarea_inicio')
    
    def get_context_data(self, **kwargs):
        context = super(TareaUpdateView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        context['titulo'] = "Tarea"
        return context

    def form_valid(self, form):
        registro_guardar(form.instance, self.request)        
        return super().form_valid(form)
    

class TareaDetailView(DetailView):
    model = Tarea
    template_name = "tarea/tarea/detalle.html"
    context_object_name = 'contexto_tarea'

    def get_context_data(self, **kwargs):
        tarea = Tarea.objects.get(id = self.kwargs['pk'])
        context = super(TareaDetailView, self).get_context_data(**kwargs)
        context['contexto_tarea'] = tarea
        context['comentarios'] = HistorialComentarioTarea.objects.filter(tarea = tarea)
        
        return context

def TareaDetailTabla(request, pk):
    data = dict()
    if request.method == 'GET':
        template = 'tarea/tarea/detalle_tabla.html'
        context = {}
        tarea = Tarea.objects.get(id = pk)
        # content_type = ContentType.objects.get_for_model(tarea)

        context['contexto_tarea'] = tarea
        context['comentarios'] = HistorialComentarioTarea.objects.filter(tarea = tarea)


        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)


class  TareaDescripcionView(BSModalUpdateView):
    model = Tarea
    template_name = "includes/formulario generico.html"
    form_class = TareaDescripcionForm

    def get_success_url(self, **kwargs):
        return reverse_lazy('tarea_app:tarea_detalle', kwargs={'pk':self.object.id})

    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(TareaDescripcionView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        return context
    
class HistorialComentarioTareaCreateView(BSModalCreateView):
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
        context = super(HistorialComentarioTareaCreateView, self).get_context_data(**kwargs)
        context['accion']="Registrar"
        context['titulo']="Comentario"
        return context

class HistorialComentarioTareaUpdateView(BSModalUpdateView):
    model = HistorialComentarioTarea
    template_name = "includes/formulario generico.html"
    form_class = HistorialComentarioTareaForm

    def get_success_url(self, **kwargs):
        return reverse_lazy('tarea_app:tarea_detalle', kwargs={'pk':self.object.id})
    
    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)
       
    def get_context_data(self, **kwargs):
        context = super(HistorialComentarioTareaUpdateView, self).get_context_data(**kwargs)
        context['accion']="Actualizar"
        context['titulo']="Comentarios"
        return context

class HistorialComentarioTareaDeleteView(BSModalDeleteView): #Falta redireccionar :(
    model = HistorialComentarioTarea
    template_name = "includes/eliminar generico.html"

    def get_success_url(self, **kwargs):
        return reverse_lazy('tarea_app:tarea_detalle', kwargs={'pk':self.object.id})
    
    def get_context_data(self, **kwargs):
        context = super(HistorialComentarioTareaDeleteView, self).get_context_data(**kwargs)
        context['accion']="Eliminar"
        context['titulo']="Comentario"
        return context


class TareaClienteView(BSModalUpdateView):
    model = Tarea
    template_name = "includes/formulario generico.html"
    form_class = TareaClienteForm

    def get_success_url(self, **kwargs):
        return reverse_lazy('tarea_app:tarea_detalle', kwargs={'pk':self.object.id})

    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        tarea = kwargs['instance']
        lista = []
        relaciones = ClienteInterlocutor.objects.filter(cliente = tarea.cliente)
        for relacion in relaciones:
            lista.append(relacion.interlocutor.id)

        kwargs['interlocutor_queryset'] = InterlocutorCliente.objects.filter(id__in = lista)
        kwargs['interlocutor'] = tarea.cliente_interlocutor
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(TareaClienteView, self).get_context_data(**kwargs)
        context['accion'] = "Elegir"
        context['titulo'] = "Cliente"
        return context