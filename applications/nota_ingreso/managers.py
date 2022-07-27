from django.db import models

class NotaIngresoManager(models.Manager):
    def ver_detalle(self, nota_ingreso_id):
        comprobante = self.get(id = nota_ingreso_id)
        consulta = comprobante.NotaIngresoDetalle_nota_ingreso.all()
        for dato in consulta:
            dato.material = dato.comprobante_compra_detalle.OrdenCompraDetalle.content_type.get_object_for_this_type(id=dato.comprobante_compra_detalle.OrdenCompraDetalle.id_registro)
        return consulta