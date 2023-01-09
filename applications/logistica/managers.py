from django.db import models

class SerieManager(models.Manager):
    def buscar_series(self, movimientos):
        consulta = self.filter(
            serie_movimiento_almacen__in = movimientos,
        )
        return consulta