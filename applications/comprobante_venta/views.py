from django.shortcuts import render
from applications.importaciones import *

from . models import(
    FacturaVenta,
    FacturaVentaDetalle,
)

class FacturaVentaListView(ListView):
    model = FacturaVenta
    template_name = 'comprobante_venta/factura_venta/inicio.html'
    context_object_name = 'contexto_factura_venta'

def FacturaVentaTabla(request):
    data = dict()
    if request.method == 'GET':
        template = 'comprobante_venta/factura_venta/inicio_tabla.html'
        context = {}
        context['contexto_factura_venta'] = FacturaVenta.objects.all()

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)
