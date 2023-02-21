from django.db import models

class NotaCreditoManager(models.Manager):
    def ver_detalle(self, nota_credito_id):
        nota_credito = self.get(id = nota_credito_id)
        consulta = nota_credito.NotaCreditoDetalle_nota_credito.all()
        for dato in consulta:
            dato.material = dato.producto
        return consulta