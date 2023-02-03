from applications.importaciones import *
from applications.nota.models import NotaCredito, NotaCreditoDetalle
from applications.funciones import numeroXn, registrar_excepcion


class NotaCreditoView(TemplateView):
    template_name = "notas/nota_credito/inicio.html"

    def get_context_data(self, **kwargs):
        context = super(NotaCreditoView, self).get_context_data(**kwargs)
        context['contexto_nota_credito'] = NotaCredito.objects.all()
        
        return context 

class NotaCreditoDetailView(DetailView):
    model = NotaCredito
    template_name = "notas/nota_credito/detalle.html"
    context_object_name = 'contexto_nota_credito'

    def get_context_data(self, **kwargs):
        context = super(NotaCreditoDetailView, self).get_context_data(**kwargs)
        # context['materiales'] = NotaCredito.objects.ver_detalle(self.get_object().id)
        return context
    


def NotaCreditoDetailTabla(request, id):
    data = dict()
    if request.method == 'GET':
        template = 'notas/nota_credito/detalle_tabla.html'
        context = {}
        nota_credito = NotaCredito.objects.get(id = id)
        context['contexto_nota_credito'] = nota_credito
        # context['materiales'] = NotaCreditoDetalle.objects.ver_detalle(id)


        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)
