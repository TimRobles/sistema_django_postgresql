from applications.importaciones import *
from applications.nota_ingreso.forms import NotaIngresoAgregarMaterialForm
from applications.nota_ingreso.models import NotaIngreso, NotaIngresoDetalle
from applications.recepcion_compra.models import RecepcionCompra

# Create your views here.

class NotaIngresoView(TemplateView):
    template_name = "nota_ingreso/nota_ingreso/inicio.html"

    def get_context_data(self, **kwargs):
        context = super(NotaIngresoView, self).get_context_data(**kwargs)
        recepcion = RecepcionCompra.objects.get(id=self.kwargs['recepcion_id'])
        context['contexto_nota_ingreso'] = NotaIngreso.objects.filter(recepcion_compra=recepcion)
        context['recepcion'] = recepcion
        context['regresar'] = reverse_lazy('recepcion_compra_app:recepcion_compra_detalle', kwargs={'pk':self.kwargs['recepcion_id']})
        return context


class NotaIngresoDetailView(DetailView):
    model = NotaIngreso
    template_name = "nota_ingreso/nota_ingreso/detalle.html"
    context_object_name = 'contexto_nota_ingreso'

    def get_context_data(self, **kwargs):
        context = super(NotaIngresoDetailView, self).get_context_data(**kwargs)
        context['materiales'] = NotaIngreso.objects.ver_detalle(self.get_object().id)
        context['regresar'] = reverse_lazy('recepcion_compra_app:recepcion_compra_detalle', kwargs={'pk':self.get_object().recepcion_compra.id})
        return context
    

def NotaIngresoDetailTabla(request, recepcion_id):
    data = dict()
    if request.method == 'GET':
        template = 'nota_ingreso/nota_ingreso/detalle_tabla.html'
        context = {}
        nota_ingreso = NotaIngreso.objects.get(id = recepcion_id)
        context['contexto_nota_ingreso'] = nota_ingreso
        context['materiales'] = NotaIngreso.objects.ver_detalle(recepcion_id)
        context['regresar'] = reverse_lazy('recepcion_compra_app:recepcion_compra_detalle', kwargs={'pk':recepcion_id})
        
        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)


class NotaIngresoAgregarMaterialView(BSModalFormView):
    template_name = "includes/formulario generico.html"
    form_class = NotaIngresoAgregarMaterialForm
    
    def get_success_url(self, **kwargs):
        return reverse_lazy('nota_ingreso_app:nota_ingreso_detalle', kwargs={'pk':self.kwargs['pk']})

    def get_form_kwargs(self, *args, **kwargs):
        nota_ingreso = NotaIngreso.objects.get(id=self.kwargs['pk'])
        productos = []
        for detalle in nota_ingreso.recepcion_compra.documento.detalle:
            valor = "%s|%s" % (ContentType.objects.get_for_model(detalle).id, detalle.id)
            productos.append((valor, detalle.producto))
        kwargs = super(NotaIngresoAgregarMaterialView, self).get_form_kwargs(*args, **kwargs)
        kwargs['productos'] = productos
        return kwargs

    def form_valid(self, form):
        if self.request.session['primero']:
            nota_ingreso = NotaIngreso.objects.get(id=self.kwargs['pk'])
            nuevo_item = len(NotaIngresoDetalle.objects.filter(nota_ingreso = nota_ingreso)) + 1
            cantidad = form.cleaned_data['cantidad']
            producto = form.cleaned_data['producto'].split("|")
            almacen = form.cleaned_data['almacen']
            content_type = ContentType.objects.get(id = int(producto[0]))
            id_registro = int(producto[1])
            comprobante_compra_detalle = content_type.model_class().objects.get(id = id_registro)
            
            NotaIngresoDetalle.objects.create(
                item = nuevo_item,
                comprobante_compra_detalle = comprobante_compra_detalle,
                cantidad_conteo = cantidad,
                almacen = almacen,
                nota_ingreso = nota_ingreso,
                created_by = self.request.user,
                updated_by = self.request.user,
            )
            self.request.session['primero'] = False
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        self.request.session['primero'] = True
        context = super(NotaIngresoAgregarMaterialView, self).get_context_data(**kwargs)
        context['accion'] = "Contar"
        context['titulo'] = "Material"
        return context