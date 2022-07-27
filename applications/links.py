from django.contrib.contenttypes.models import ContentType
from applications.comprobante_compra.models import ComprobanteCompraPI
from django.urls import reverse_lazy

def link_detalle(content_type, registro):
    if content_type == ContentType.objects.get_for_model(ComprobanteCompraPI):
        return reverse_lazy('comprobante_compra_app:comprobante_compra_pi_detalle', kwargs={'slug':registro})