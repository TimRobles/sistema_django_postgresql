from applications.importaciones import *
from applications.nota_ingreso.models import NotaIngreso

# Create your views here.

class NotaIngresoDetailView(DetailView):
    model = NotaIngreso
    template_name = "nota_ingreso/nota_ingreso/detalle.html"
    context_object_name = 'contexto_nota_ingreso'

    def get_context_data(self, **kwargs):
        context = super(NotaIngresoDetailView, self).get_context_data(**kwargs)
        context['materiales'] = NotaIngreso.objects.ver_detalle(self.get_object().id)
        return context
    

def NotaIngresoDetailTabla(request, pk):
    data = dict()
    if request.method == 'GET':
        template = 'nota_ingreso/nota_ingreso/detalle_tabla.html'
        context = {}
        nota_ingreso = NotaIngreso.objects.get(id = pk)
        context['contexto_nota_ingreso'] = nota_ingreso
        context['materiales'] = NotaIngreso.objects.ver_detalle(nota_ingreso.id)
        
        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)