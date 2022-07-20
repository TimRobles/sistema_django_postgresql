from django.db import models

class ComprobanteCompraPIDetalleManager(models.Manager):
    def ver_detalle(self, comprobante_compra_pi):
        consulta = self.filter(comprobante_compra = comprobante_compra_pi)
        for dato in consulta:
            dato.material = dato.orden_compra_detalle.content_type.get_object_for_this_type(id=dato.orden_compra_detalle.id_registro)
        return consulta
