from decimal import Decimal
from django.db import models

from applications import material

class ComprobanteCompraMerchandisingManager(models.Manager):
    def ver_detalle(self, comprobante_compra):
        comprobante = self.get(id = comprobante_compra)
        consulta = comprobante.ComprobanteCompraMerchandisingDetalle_comprobante_compra_merchandising.all()
        for dato in consulta:
            dato.material = dato.orden_compra_merchandising_detalle.content_type.get_object_for_this_type(id=dato.orden_compra_merchandising_detalle.id_registro)

            # if dato.cantidad > dato.contado:
            #     dato.pendiente = dato.cantidad - dato.contado
            #     dato.exceso = Decimal('0.00')
            # else:
            #     dato.pendiente = Decimal('0.00')
            #     dato.exceso = dato.contado - dato.cantidad
        return consulta


class ComprobanteCompraMerchandisingDetalleManager(models.Manager):
    def ver_detalle(self, comprobante_compra):
        consulta = self.filter(comprobante_compra = comprobante_compra)
        for dato in consulta:
            dato.material = dato.orden_compra_merchandising_detalle.content_type.get_object_for_this_type(id=dato.orden_compra_merchandising_detalle.id_registro)
        return consulta


#Nota de ingreso

class NotaIngresoMerchandisingManager(models.Manager):
    def ver_detalle_nota(self, nota_ingreso_id):
        comprobante = self.get(id = nota_ingreso_id)
        consulta = comprobante.NotaIngresoMerchandisingDetalle_nota_ingreso.all()
        for dato in consulta:
            dato.material = dato.comprobante_compra_detalle.orden_compra_merchandising_detalle.content_type.get_object_for_this_type(id=dato.comprobante_compra_detalle.orden_compra_merchandising_detalle.id_registro)
        return consulta


