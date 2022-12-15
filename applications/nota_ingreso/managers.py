from django.db import models

class NotaIngresoManager(models.Manager):
    def ver_detalle(self, nota_ingreso_id):
        comprobante = self.get(id = nota_ingreso_id)
        consulta = comprobante.NotaIngresoDetalle_nota_ingreso.all()
        for dato in consulta:
            dato.material = dato.comprobante_compra_detalle.orden_compra_detalle.content_type.get_object_for_this_type(id=dato.comprobante_compra_detalle.orden_compra_detalle.id_registro)
        return consulta


class NotaStockInicialManager(models.Manager):
    def ver_detalle(self, nota_ingreso_id):
        comprobante = self.get(id = nota_ingreso_id)
        consulta = comprobante.NotaStockInicialDetalle_nota_stock_inicial.all()
        for dato in consulta:
            dato.material = dato.producto
        return consulta