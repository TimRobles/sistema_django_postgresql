from django.db import models

class TipoCambioManager(models.Manager):
    def tipo_cambio_venta(self, fecha):
        try:
            return self.filter(fecha=fecha).latest('created_at').tipo_cambio_venta
        except:
            return None