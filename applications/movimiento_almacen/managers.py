from django.db import models

class MovimientoAlmacenManager(models.Manager):
    def ver_movimientos(self, content_type, id_registro):
        consulta = self.filter(
            content_type_producto = content_type,
            id_registro_producto = id_registro,
        )
        total = 0
        for dato in consulta:
            total += dato.cantidad * dato.signo_factor_multiplicador
        return consulta, total
