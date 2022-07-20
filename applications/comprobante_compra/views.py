from applications.comprobante_compra.models import ComprobanteCompraPI
from applications.importaciones import *

# Create your views here.


class ComprobanteCompraPIListView(ListView):
    model = ComprobanteCompraPI
    template_name = "comprobante_compra/comprobante_compra_pi/inicio.html"
    context_object_name = 'contexto_comprobante_compra_pi'
