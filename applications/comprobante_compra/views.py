from applications.comprobante_compra.forms import ArchivoComprobanteCompraPIForm, ComprobanteCompraPILogisticoForm
from applications.comprobante_compra.models import ArchivoComprobanteCompraPI, ComprobanteCompraPI, ComprobanteCompraPIDetalle
from applications.funciones import obtener_totales
from applications.home.templatetags.funciones_propias import filename
from applications.importaciones import *

# Create your views here.


class ComprobanteCompraPIListView(ListView):
    model = ComprobanteCompraPI
    template_name = "comprobante_compra/comprobante_compra_pi/inicio.html"
    context_object_name = 'contexto_comprobante_compra_pi'


class ComprobanteCompraPIDetailView(DetailView):
    model = ComprobanteCompraPI
    template_name = "comprobante_compra/comprobante_compra_pi/detalle.html"
    context_object_name = 'contexto_comprobante_compra_pi'

    def get_context_data(self, **kwargs):
        context = super(ComprobanteCompraPIDetailView, self).get_context_data(**kwargs)
        context['materiales'] = ComprobanteCompraPIDetalle.objects.ver_detalle(self.get_object())
        context['archivos'] = ArchivoComprobanteCompraPI.objects.filter(comprobante_compra=self.get_object())
        context['totales'] = obtener_totales(self.get_object())
        return context
    

def ComprobanteCompraPIDetailTabla(request, slug):
    data = dict()
    if request.method == 'GET':
        template = 'comprobante_compra/comprobante_compra_pi/detalle_tabla.html'
        context = {}
        comprobante_compra = ComprobanteCompraPI.objects.get(slug = slug)
        context['contexto_comprobante_compra_pi'] = comprobante_compra
        context['materiales'] = ComprobanteCompraPIDetalle.objects.ver_detalle(comprobante_compra)
        context['archivos'] = ArchivoComprobanteCompraPI.objects.filter(comprobante_compra=comprobante_compra)
        context['totales'] = obtener_totales(comprobante_compra)

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)


class ComprobanteCompraPILogisticoUpdateView(BSModalUpdateView):
    model = ComprobanteCompraPI
    template_name = "includes/formulario generico.html"
    form_class = ComprobanteCompraPILogisticoForm
    success_url = '.'

    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super(ComprobanteCompraPILogisticoUpdateView, self).get_context_data(**kwargs)
        context['accion'] = "Agregar"
        context['titulo'] = "Logístico"
        return context
    

class ArchivoComprobanteCompraPICreateView(BSModalCreateView):
    model = ArchivoComprobanteCompraPI
    template_name = "includes/formulario generico.html"
    form_class = ArchivoComprobanteCompraPIForm
    success_url = '.'

    def form_valid(self, form):
        form.instance.comprobante_compra = ComprobanteCompraPI.objects.get(slug=self.kwargs['slug'])
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super(ArchivoComprobanteCompraPICreateView, self).get_context_data(**kwargs)
        context['accion'] = "Agregar"
        context['titulo'] = "Archivo"
        return context
    

class ArchivoComprobanteCompraPIDeleteView(BSModalDeleteView):
    model = ArchivoComprobanteCompraPI
    template_name = "includes/eliminar generico.html"
    
    def get_success_url(self, **kwargs):
        return reverse_lazy('comprobante_compra_app:comprobante_compra_pi_detalle', kwargs={'slug':self.object.comprobante_compra.slug})

    def get_context_data(self, **kwargs):
        context = super(ArchivoComprobanteCompraPIDeleteView, self).get_context_data(**kwargs)
        context['accion'] = "Agregar"
        context['titulo'] = "Archivo"
        context['item'] = filename(self.object.archivo)
        return context