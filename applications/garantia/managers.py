from django.db import models

class IngresoReclamoGarantiaManager(models.Manager):
    def ver_detalle(self, ingreso_garantia_id):
        ingreso_garantia = self.get(id = ingreso_garantia_id)
        consulta = ingreso_garantia.IngresoReclamoGarantiaDetalle_ingreso_garantia.all()
        for dato in consulta:
            dato.material = dato.producto
        return consulta