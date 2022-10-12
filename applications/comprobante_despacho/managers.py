from django.db import models

class GuiaVentaManager(models.Manager):
    def nuevo_numero(self, obj):
        consulta = self.filter(
            sociedad=obj.sociedad,
            serie_comprobante=obj.serie_comprobante,
            ).aggregate(models.Max('numero_guia'))
        if consulta['numero_guia__max']:
            return consulta['numero_guia__max'] + 1
        else:
            return 1