from decimal import Decimal
from django.db import models
from django.db.models import Sum

class ComprobanteCompraPIManager(models.Manager):
    def ver_detalle(self, comprobante_compra_pi):
        comprobante = self.get(id = comprobante_compra_pi)
        consulta = comprobante.ComprobanteCompraPIDetalle_comprobante_compra.all()
        for dato in consulta:
            dato.material = dato.orden_compra_detalle.content_type.get_object_for_this_type(id=dato.orden_compra_detalle.id_registro)
            if dato.NotaIngresoDetalle_comprobante_compra_detalle.all().aggregate(Sum('cantidad_conteo'))['cantidad_conteo__sum']:
                dato.contado = dato.NotaIngresoDetalle_comprobante_compra_detalle.all().aggregate(Sum('cantidad_conteo'))['cantidad_conteo__sum']
            else:
                dato.contado = Decimal('0.00')

            if dato.cantidad > dato.contado:
                dato.pendiente = dato.cantidad - dato.contado
                dato.exceso = Decimal('0.00')
            else:
                dato.pendiente = Decimal('0.00')
                dato.exceso = dato.contado - dato.cantidad
        return consulta
        

class ComprobanteCompraPIDetalleManager(models.Manager):
    def ver_detalle(self, comprobante_compra_pi):
        consulta = self.filter(comprobante_compra = comprobante_compra_pi)
        for dato in consulta:
            dato.material = dato.orden_compra_detalle.content_type.get_object_for_this_type(id=dato.orden_compra_detalle.id_registro)
        return consulta


class ComprobanteCompraCIDetalleManager(models.Manager):
    def ver_detalle(self, comprobante_compra_ci):
        consulta = self.filter(comprobante_compra = comprobante_compra_ci)
        for dato in consulta:
            dato.material = dato.content_type.get_object_for_this_type(id=dato.id_registro)
        return consulta
