from django.shortcuts import render
from applications.comprobante_compra.models import ComprobanteCompraPI, ComprobanteCompraPIDetalle
from applications.importaciones import *
from .models import PrecioListaMaterial


class PrecioListaMaterialListView(ListView):
    model = PrecioListaMaterial
    template_name = "cotizacion/precio/inicio.html"
    context_object_name = 'contexto_cotizacion'

def PrecioListaMaterialTabla(request):
    data = dict()
    if request.method == 'GET':
        template = 'cotizacion/cotizacion/inicio_tabla.html'
        context = {}
        context['contexto_cotizacion'] = PrecioListaMaterial.objects.all()

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)

