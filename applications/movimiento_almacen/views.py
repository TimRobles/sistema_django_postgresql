from applications.importaciones import *
from applications.material.models import Material
from applications.movimiento_almacen.models import MovimientosAlmacen, TipoStock

# Create your views here.

class MovimientoMaterialView(PermissionRequiredMixin, BSModalReadView):
    permission_required = ('material.view_material')
    model = ContentType
    template_name = "movimiento_almacen/ver_movimiento.html"

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        content_type = self.get_object()
        id_registro = self.kwargs['id_registro']
        producto = content_type.model_class().objects.get(id=id_registro)
        movimientos, total = MovimientosAlmacen.objects.ver_movimientos(
            content_type,
            id_registro,
        )
        context = super(MovimientoMaterialView, self).get_context_data(**kwargs)
        context['titulo'] = f"Movimientos - {producto}"
        context['movimientos'] = movimientos
        context['total'] = total
        return context
    

class StockMaterialView(PermissionRequiredMixin, BSModalReadView):
    permission_required = ('material.view_material')
    model = ContentType
    template_name = "movimiento_almacen/ver_stock.html"

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        content_type = self.get_object()
        id_registro = self.kwargs['id_registro']
        producto = content_type.model_class().objects.get(id=id_registro)
        stocks, estados = MovimientosAlmacen.objects.ver_stock(
            content_type,
            id_registro,
            TipoStock.objects.all(),
        )
        context = super(StockMaterialView, self).get_context_data(**kwargs)
        context['titulo'] = f"Stock - {producto}"
        context['stocks'] = stocks
        context['estados'] = estados
        return context