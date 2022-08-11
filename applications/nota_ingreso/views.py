from applications.importaciones import *
from applications.nota_ingreso.forms import NotaIngresoAgregarMaterialForm
from applications.nota_ingreso.models import NotaIngreso
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
    success_url = '.'

    def get_context_data(self, **kwargs):
        context = super(NotaIngresoAgregarMaterialView, self).get_context_data(**kwargs)
        context['accion'] = "Contar"
        context['titulo'] = "Material"
        return context