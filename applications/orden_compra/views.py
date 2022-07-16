from django.shortcuts import render
from applications.importaciones import *

from .models import (
    OrdenCompra,
    OrdenCompraDetalle,
    OfertaProveedor,
    OfertaProveedorDetalle
)

from .forms import (
    OrdenCompraForm,
)


class OrdenCompraListView(ListView):
    model = OrdenCompra
    template_name = "orden_compra/orden_compra/inicio.html"
    context_object_name = 'contexto_orden_compra'

def OrdenCompraTabla(request):
    data = dict()
    if request.method == 'GET':
        template = 'orden_compra/orden_compra/inicio_tabla.html'
        context = {}
        context['contexto_orden_compra'] = OrdenCompra.objects.all()

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)



class OrdenCompraDetailView(DetailView):
    model = OrdenCompra
    template_name = "orden_compra/orden_compra/detalle.html"
    context_object_name = 'contexto_orden_compra'

    def get_context_data(self, **kwargs):
        orden_compra = OrdenCompra.objects.get(id = self.kwargs['pk'])
        context = super(OrdenCompraDetailView, self).get_context_data(**kwargs)
  
        return context


def OrdenCompraDetailTabla(request, pk):
    data = dict()
    if request.method == 'GET':
        template = 'orden_compra/orden_compra/detalle_tabla.html'
        context = {}
        orden_compra = OrdenCompra.objects.get(id = pk)

        context['contexto_orden_compra'] = orden_compra

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)
