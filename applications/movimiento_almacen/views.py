from applications.importaciones import *
from applications.material.models import Material
from applications.movimiento_almacen.models import MovimientosAlmacen

# Create your views here.

class MovimientoMaterialView(BSModalReadView):
    model = ContentType
    template_name = "movimiento_almacen/ver_movimiento.html"
    
    def get_context_data(self, **kwargs):
        movimientos = MovimientosAlmacen.objects.filter(
            content_type_producto = self.get_object(),
            id_registro_producto = self.kwargs['id_registro'],
        )
        context = super(MovimientoMaterialView, self).get_context_data(**kwargs)
        context['movimientos'] = movimientos
        return context
    

class StockMaterialView(BSModalReadView):
    model = Material
    template_name = "movimiento_almacen/ver_stock.html"
