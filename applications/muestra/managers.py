from django.db import models

class NotaIngresoMuestraManager(models.Manager):
    def ver_detalle(self, nota_ingreso_id):
        comprobante = self.get(id = nota_ingreso_id)
        consulta = comprobante.NotaIngresoMuestraDetalle_nota_ingreso_muestra.all()
        for dato in consulta:
            dato.material = dato.producto
        return consulta