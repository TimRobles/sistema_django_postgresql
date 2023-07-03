from django.db import models

class NotaCreditoManager(models.Manager):
    def ver_detalle(self, nota_credito_id):
        nota_credito = self.get(id = nota_credito_id)
        consulta = nota_credito.NotaCreditoDetalle_nota_credito.all()
        for dato in consulta:
            dato.material = dato.producto
        return consulta

    def nuevo_numero(self, obj):
        consulta = self.filter(
            sociedad=obj.sociedad,
            serie_comprobante=obj.serie_comprobante,
            ).aggregate(models.Max('numero_nota'))
        if consulta['numero_nota__max']:
            return consulta['numero_nota__max'] + 1
        else:
            return 1


class NotaDevolucionManager(models.Manager):
    def ver_detalle(self, nota_ingreso_id):
        comprobante = self.get(id = nota_ingreso_id)
        consulta = comprobante.NotaDevolucionDetalle_nota_ingreso.all()
        for dato in consulta:
            dato.material = dato.comprobante_compra_detalle.orden_compra_detalle.content_type.get_object_for_this_type(id=dato.comprobante_compra_detalle.orden_compra_detalle.id_registro)
        return consulta