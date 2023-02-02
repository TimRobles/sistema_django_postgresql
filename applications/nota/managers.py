from django.db import models

class NotaCreditoManager(models.Manager):
    def ver_detalle(self, nota_credito_id):
        comprobante = self.get(id = nota_credito_id)
        consulta = comprobante.NotaCreditoDetalle_nota_credito.all()
        # for dato in consulta:
        #     dato.material = dato.comprobante_compra_detalle.orden_compra_detalle.content_type.get_object_for_this_type(id=dato.comprobante_compra_detalle.orden_compra_detalle.id_registro)
        return consulta

