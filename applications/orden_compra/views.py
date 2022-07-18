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
        context['detalle_orden_compra'] = OrdenCompraDetalle.objects.filter(orden_compra = orden_compra)
        print('///////////////////////////////////////////')
        print(context['detalle_orden_compra'])
        print(orden_compra)
        print(orden_compra.oferta_proveedor)
        print(orden_compra.oferta_proveedor.requerimiento_material)
        print(orden_compra.oferta_proveedor.requerimiento_material.lista_requerimiento)
        print(orden_compra.oferta_proveedor.requerimiento_material.lista_requerimiento.ListaRequerimientoMaterialDetalle_requerimiento_material.all())
        # print(orden_compra.oferta_proveedor.requerimiento_material.lista_requerimiento.ListaRequerimientoMaterialDetalle_requerimiento_material.content_type)
        # print(orden_compra.oferta_proveedor.requerimiento_material.lista_requerimiento.ListaRequerimientoMaterialDetalle_requerimiento_material.id_registro)
        print('///////////////////////////////////////////')
  
        return context


def OrdenCompraDetailTabla(request, pk):
    data = dict()
    if request.method == 'GET':
        template = 'orden_compra/orden_compra/detalle_orden_compra_tabla.html'
        context = {}
        orden_compra = OrdenCompra.objects.get(id = pk)
        context['contexto_orden_compra'] = orden_compra
        context['detalle_orden_compra'] = OrdenCompraDetalle.objects.filter(orden_compra = orden_compra)
        print('/+++++++++++++++++++++++++++++++++++++')
        print(context['detalle_orden_compra'])
        print(orden_compra)
        print('+++++++++++++++++++++++++++++++++++++/')

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)
