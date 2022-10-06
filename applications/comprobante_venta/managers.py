from django.db import models

class BoletaVentaManager(models.Manager):
    def nuevo_numero(self, obj):
        consulta = self.filter(
            sociedad=obj.sociedad,
            serie_comprobante=obj.serie_comprobante,
            ).aggregate(models.Max('numero_boleta'))
        if consulta['numero_boleta__max']:
            return consulta['numero_boleta__max'] + 1
        else:
            return 1

class FacturaVentaManager(models.Manager):
    def nuevo_numero(self, obj):
        consulta = self.filter(
            sociedad=obj.sociedad,
            serie_comprobante=obj.serie_comprobante,
            ).aggregate(models.Max('numero_factura'))
        if consulta['numero_factura__max']:
            return consulta['numero_factura__max'] + 1
        else:
            return 1