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
        movimientos, total = MovimientosAlmacen.objects.ver_movimientos(
            self.get_object(),
            self.kwargs['id_registro'],
        )
        context = super(MovimientoMaterialView, self).get_context_data(**kwargs)
        context['titulo'] = "Movimientos"
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
        stocks, estados = MovimientosAlmacen.objects.ver_stock(
            self.get_object(),
            self.kwargs['id_registro'],
            TipoStock.objects.all(),
        )
        context = super(StockMaterialView, self).get_context_data(**kwargs)
        context['titulo'] = "Stock"
        context['stocks'] = stocks
        context['estados'] = estados
        return context