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




class OrdenCompraDeleteView(BSModalUpdateView):
    model = OrdenCompra
    template_name = "includes/formulario generico.html"
    success_url = reverse_lazy('orden_compra_app:orden_compra_inicio') 
    # form_class = s

    def form_valid(self, form):
        form.instance.estado = 3
        registro_guardar(form.instance, self.request)
        
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super(OrdenCompraDeleteView, self).get_context_data(**kwargs)
        context['accion'] = 'Anular Docuemento'
        context['titulo'] = 'Orden de compra'
        return context


class OrdenCompraDeleteView(BSModalDeleteView):
    model = OrdenCompra
    template_name = "includes/eliminar generico.html"
    success_url = reverse_lazy('orden_compra_app:orden_compra_inicio')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.estado = 3
        registro_guardar(self.object, self.request)
        self.object.save()
        messages.success(request, MENSAJE_ANULAR_ORDEN_COMPRA)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(OrdenCompraDeleteView, self).get_context_data(**kwargs)
        context['accion'] = 'Anular Documento'
        context['titulo'] = 'Orden de compra'
        return context


class OrdenCompraDetailView(DetailView):
    model = OrdenCompra
    template_name = "orden_compra/orden_compra/detalle.html"
    context_object_name = 'contexto_orden_compra'

    def get_context_data(self, **kwargs):
        context = super(OrdenCompraDetailView, self).get_context_data(**kwargs)
        obj = OrdenCompra.objects.get(id = self.kwargs['pk'])
        
        # materiales = obj.oferta_proveedor.requerimiento_material.lista_requerimiento.ListaRequerimientoMaterialDetalle_requerimiento_material.all()
        materiales = obj.OrdenCompraDetalle_orden_compra.all()

        for material in materiales:
            material.material = material.content_type.get_object_for_this_type(id = material.id_registro)
        
        context['detalle_orden_compra'] = materiales 
        return context


def OrdenCompraDetailTabla(request, pk):
    data = dict()
    if request.method == 'GET':
        template = 'orden_compra/orden_compra/detalle_orden_compra_tabla.html'
        context = {}
        obj = OrdenCompra.objects.get(id = pk)
        context['contexto_orden_compra'] = obj
        context['detalle_orden_compra'] = OrdenCompraDetalle.objects.filter(orden_compra = obj)

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)
