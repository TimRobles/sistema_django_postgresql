from applications.links import link_detalle
from applications.home.templatetags.funciones_propias import filename
from applications.importaciones import *
from applications.recepcion_compra.forms import ArchivoRecepcionCompraForm, FotoRecepcionCompraForm
from .models import FotoRecepcionCompra, RecepcionCompra, ArchivoRecepcionCompra

# Create your views here.

class RecepcionCompraDetailView(DetailView):
    model = RecepcionCompra
    template_name = "recepcion_compra/recepcion_compra/detalle.html"
    context_object_name = 'contexto_recepcion_compra'

    def get_context_data(self, **kwargs):
        context = super(RecepcionCompraDetailView, self).get_context_data(**kwargs)
        context['materiales'] = self.get_object().content_type.model_class().objects.ver_detalle(self.get_object().id_registro)
        context['archivos'] = ArchivoRecepcionCompra.objects.filter(recepcion_compra=self.get_object())
        context['fotos'] = FotoRecepcionCompra.objects.filter(recepcion_compra=self.get_object())
        context['regresar'] = link_detalle(self.get_object().content_type, self.get_object().content_type.get_object_for_this_type(id=self.get_object().id_registro).slug)
        return context
    

def RecepcionCompraDetailTabla(request, pk):
    data = dict()
    if request.method == 'GET':
        template = 'recepcion_compra/recepcion_compra/detalle_tabla.html'
        context = {}
        recepcion_compra = RecepcionCompra.objects.get(id = pk)
        context['contexto_recepcion_compra'] = recepcion_compra
        context['materiales'] = recepcion_compra.content_type.model_class().objects.ver_detalle(recepcion_compra.id_registro)
        context['archivos'] = ArchivoRecepcionCompra.objects.filter(recepcion_compra=recepcion_compra)
        context['fotos'] = FotoRecepcionCompra.objects.filter(recepcion_compra=recepcion_compra)

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)


class ArchivoRecepcionCompraCreateView(BSModalCreateView):
    model = ArchivoRecepcionCompra
    template_name = "includes/formulario generico.html"
    form_class = ArchivoRecepcionCompraForm
    success_url = '.'

    def form_valid(self, form):
        form.instance.recepcion_compra = RecepcionCompra.objects.get(pk=self.kwargs['pk'])
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super(ArchivoRecepcionCompraCreateView, self).get_context_data(**kwargs)
        context['accion'] = "Agregar"
        context['titulo'] = "Archivo"
        return context
    

class ArchivoRecepcionCompraDeleteView(BSModalDeleteView):
    model = ArchivoRecepcionCompra
    template_name = "includes/eliminar generico.html"
    
    def get_success_url(self, **kwargs):
        return reverse_lazy('recepcion_compra_app:recepcion_compra_detalle', kwargs={'pk':self.object.recepcion_compra.id})

    def get_context_data(self, **kwargs):
        context = super(ArchivoRecepcionCompraDeleteView, self).get_context_data(**kwargs)
        context['accion'] = "Agregar"
        context['titulo'] = "Archivo"
        context['item'] = filename(self.object.archivo)
        return context


class FotoRecepcionCompraCreateView(BSModalCreateView):
    model = FotoRecepcionCompra
    template_name = "includes/formulario generico.html"
    form_class = FotoRecepcionCompraForm
    success_url = '.'

    def form_valid(self, form):
        form.instance.recepcion_compra = RecepcionCompra.objects.get(pk=self.kwargs['pk'])
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super(FotoRecepcionCompraCreateView, self).get_context_data(**kwargs)
        context['accion'] = "Agregar"
        context['titulo'] = "Foto"
        return context
    

class FotoRecepcionCompraDeleteView(BSModalDeleteView):
    model = FotoRecepcionCompra
    template_name = "includes/eliminar generico.html"
    
    def get_success_url(self, **kwargs):
        return reverse_lazy('recepcion_compra_app:recepcion_compra_detalle', kwargs={'pk':self.object.recepcion_compra.id})

    def get_context_data(self, **kwargs):
        context = super(FotoRecepcionCompraDeleteView, self).get_context_data(**kwargs)
        context['accion'] = "Agregar"
        context['titulo'] = "Foto"
        context['item'] = filename(self.object.foto)
        return context