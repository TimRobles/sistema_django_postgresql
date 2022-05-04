from applications.importaciones import *

from .forms import (
    SociedadForm,
    DocumentoForm,
    RepresentanteLegalForm,
    RepresentanteLegalDarBajaForm,
    )

from .models import (
    Sociedad,
    Documento,
    RepresentanteLegal,
    )

class SociedadListView(ListView):
    model = Sociedad
    template_name = "sociedad/sociedad/inicio.html"
    context_object_name = 'contexto_sociedad'


def SociedadTabla(request):
    data = dict()
    if request.method == 'GET':
        template = 'sociedad/sociedad/inicio_tabla.html'
        context = {}
        context['contexto_sociedad'] = Sociedad.objects.all()

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)


class SociedadUpdateView(BSModalUpdateView):
    model = Sociedad
    template_name = "sociedad/sociedad/actualizar.html"
    form_class = SociedadForm
    success_url = reverse_lazy('sociedad_app:sociedad_inicio')

    def get_context_data(self, **kwargs):
        context = super(SociedadUpdateView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        context['titulo'] = "Sociedad"
        context['ruc'] = self.object.ruc
        return context

    def form_valid(self, form):

        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)
        
        return super().form_valid(form)

class SociedadDarBajaView(BSModalDeleteView):
    model = Sociedad
    template_name = "includes/eliminar generico.html"
    success_url = reverse_lazy('sociedad_app:sociedad_inicio')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.estado_sunat = 7
        registro_guardar(self.object, self.request)
        self.object.save()
        messages.success(request, MENSAJE_DAR_BAJA)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(SociedadDarBajaView, self).get_context_data(**kwargs)
        context['accion'] = "Dar Baja"
        context['titulo'] = "Sociedad"
        context['dar_baja'] = "true"
        context['item'] = self.object.razon_social
        return context


class SociedadDarAltaView(BSModalDeleteView):
    model = Sociedad
    template_name = "includes/eliminar generico.html"
    success_url = reverse_lazy('sociedad_app:sociedad_inicio')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.estado_sunat = 1
        registro_guardar(self.object, self.request)
        self.object.save()
        messages.success(request, MENSAJE_DAR_ALTA)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(SociedadDarAltaView, self).get_context_data(**kwargs)
        context['accion']="Dar Alta"
        context['titulo'] = "Sociedad"
        context['dar_baja'] = "true"
        context['item'] = self.object.razon_social
        return context

class SociedadDetailView(DetailView):
    model = Sociedad
    template_name = "sociedad/sociedad/detalle.html"
    context_object_name = 'contexto_sociedad'

    def get_context_data(self, **kwargs):
        sociedad = Sociedad.objects.get(id = self.kwargs['pk'])
        context = super(SociedadDetailView, self).get_context_data(**kwargs)
        context['documentos'] = Documento.objects.filter(sociedad = sociedad)
        context['representantes'] = RepresentanteLegal.objects.filter(sociedad = sociedad)
        return context


def SociedadDetailTabla(request, pk):
    data = dict()
    if request.method == 'GET':
        template = 'sociedad/sociedad/detalle_tabla.html'
        context = {}
        sociedad = Sociedad.objects.get(id = pk)
        context['contexto_sociedad'] = sociedad
        context['documentos'] = Documento.objects.filter(sociedad = sociedad)
        context['representantes'] = RepresentanteLegal.objects.filter(sociedad = sociedad)
        
        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)


class DocumentoCreateView(BSModalCreateView):
    model = Documento
    template_name = "includes/formulario generico.html"
    form_class = DocumentoForm
    
    def get_success_url(self, **kwargs):
        return reverse_lazy('sociedad_app:sociedad_detalle', kwargs={'pk':self.kwargs['sociedad_id']})

    def form_valid(self, form):
        form.instance.sociedad = Sociedad.objects.get(id = self.kwargs['sociedad_id'])

        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(DocumentoCreateView, self).get_context_data(**kwargs)
        context['accion']="Registrar"
        context['titulo']="Documento"
        return context

class DocumentoDeleteView(BSModalDeleteView):
    model = Documento
    template_name = "sociedad/documento/eliminar.html"
    context_object_name = 'contexto_documento' 

    def get_success_url(self, **kwargs):
        return reverse_lazy('sociedad_app:sociedad_detalle', kwargs={'pk':self.object.sociedad.id})

    def get_context_data(self, **kwargs):
        context = super(DocumentoDeleteView, self).get_context_data(**kwargs)
        context['accion']="Eliminar"
        context['titulo']="Documento"
        return context

class RepresentanteCreateView(BSModalCreateView):
    model = RepresentanteLegal
    template_name = "includes/formulario generico.html"
    form_class = RepresentanteLegalForm
    
    def get_success_url(self, **kwargs):
        return reverse_lazy('sociedad_app:sociedad_detalle', kwargs={'pk':self.kwargs['sociedad_id']})

    def form_valid(self, form):
        form.instance.sociedad = Sociedad.objects.get(id = self.kwargs['sociedad_id'])
        registro_guardar(form.instance, self.request)

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(RepresentanteCreateView, self).get_context_data(**kwargs)
        context['accion']="Registrar"
        context['titulo']="Representante Legal"
        return context

class RepresentanteLegalDarBajaView(BSModalUpdateView):
    model = RepresentanteLegal
    template_name = "includes/formulario generico.html"
    form_class = RepresentanteLegalDarBajaForm

    def get_success_url(self, **kwargs):
        return reverse_lazy('sociedad_app:sociedad_detalle', kwargs={'pk':self.object.sociedad.id})

    def form_valid(self, form):
        form.instance.estado = 2
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(RepresentanteLegalDarBajaView, self).get_context_data(**kwargs)
        context['accion']="Dar Baja"
        context['titulo']="Representante Legal"
        return context