from django.db import models

class IngresoReclamoGarantiaManager(models.Manager):
    def ver_detalle(self, ingreso_reclamo_garantia_id):
        ingreso_reclamo_garantia = self.get(id = ingreso_reclamo_garantia_id)
        consulta = ingreso_reclamo_garantia.IngresoReclamoGarantiaDetalle_ingreso_reclamo_garantia.all()
        for dato in consulta:
            dato.material = dato.producto
        return consulta