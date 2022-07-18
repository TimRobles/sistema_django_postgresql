from django.shortcuts import render
from applications.importaciones import *
from applications.oferta_proveedor.models import ArchivoOfertaProveedor, OfertaProveedor, OfertaProveedorDetalle
from applications.oferta_proveedor.forms import ArchivoOfertaProveedorForm, OfertaProveedorDetalleUpdateForm, OfertaProveedorForm
from applications.funciones import obtener_totales

class OfertaProveedorListView(PermissionRequiredMixin, ListView):
    permission_required = ('oferta_proveedor.view_ofertaproveedor')
    model = OfertaProveedor
    template_name = "oferta_proveedor/oferta_proveedor/inicio.html"
    context_object_name = 'contexto_oferta_proveedor'

def OfertaProveedorTabla(request):
    data = dict()
    if request.method == 'GET':
        template = 'oferta_proveedor/oferta_proveedor/inicio_tabla.html'
        context = {}
        context['contexto_oferta_proveedor'] = OfertaProveedor.objects.all()

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)

class OfertaProveedorUpdateView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('oferta_proveedor.change_ofertaproveedor')
    model = OfertaProveedor
    template_name = "includes/formulario generico.html"
    form_class = OfertaProveedorForm

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('oferta_proveedor_app:oferta_proveedor_inicio')

    def form_valid(self, form):
        form.instance.estado = 2
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(OfertaProveedorUpdateView, self).get_context_data(**kwargs)
        context['accion']="Finalizar"
        context['titulo']="Oferta Proveedor"
        return context

class OfertaProveedorDetailView(PermissionRequiredMixin, DetailView):
    permission_required = ('oferta_proveedor.view_OfertaProveedordetalle')
    model = OfertaProveedor
    template_name = "oferta_proveedor/oferta_proveedor/detalle.html"
    context_object_name = 'contexto_oferta_proveedor'

    def get_context_data(self, **kwargs):
        oferta_proveedor = OfertaProveedor.objects.get(id = self.kwargs['pk'])
        context = super(OfertaProveedorDetailView, self).get_context_data(**kwargs)
        context['materiales'] = OfertaProveedorDetalle.objects.filter(oferta_proveedor = oferta_proveedor)
        context['archivos'] = ArchivoOfertaProveedor.objects.filter(oferta_proveedor = oferta_proveedor)
        context['totales'] = obtener_totales(OfertaProveedor.objects.get(id=self.kwargs['pk']))
        return context

def OfertaProveedorDetailTabla(request, pk):
    data = dict()
    if request.method == 'GET':
        template = 'oferta_proveedor/oferta_proveedor/detalle_tabla.html'
        context = {}
        oferta_proveedor = OfertaProveedor.objects.get(id = pk)
        context['contexto_oferta_proveedor'] = oferta_proveedor
        context['materiales'] = OfertaProveedorDetalle.objects.filter(oferta_proveedor = oferta_proveedor)
        context['archivos'] = ArchivoOfertaProveedor.objects.filter(oferta_proveedor = oferta_proveedor)

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)

class OfertaProveedorDetalleUpdateView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('oferta_proveedor.change_ofertaproveedordetalle')

    model = OfertaProveedorDetalle
    template_name = "oferta_proveedor/oferta_proveedor/actualizar.html"
    form_class = OfertaProveedorDetalleUpdateForm

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('oferta_proveedor_app:oferta_proveedor_detalle', kwargs={'pk':self.get_object().oferta_proveedor.id})

    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(OfertaProveedorDetalleUpdateView, self).get_context_data(**kwargs)
        context['accion']="Actualizar"
        context['titulo']="Precios"
        return context

class ArchivoOfertaProveedorCreateView(PermissionRequiredMixin, BSModalCreateView):
    permission_required = ('oferta_proveedor.add_ofertaproveedordetalle')
    model = ArchivoOfertaProveedor
    template_name = "includes/formulario generico.html"
    form_class = ArchivoOfertaProveedorForm

    def get_success_url(self, **kwargs):
        return reverse_lazy('oferta_proveedor_app:oferta_proveedor_detalle', kwargs={'pk':self.kwargs['oferta_proveedor_id']})

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.oferta_proveedor = OfertaProveedor.objects.get(id = self.kwargs['oferta_proveedor_id'])

        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ArchivoOfertaProveedorCreateView, self).get_context_data(**kwargs)
        context['accion']="Agregar"
        context['titulo']="Documento"
        return context


