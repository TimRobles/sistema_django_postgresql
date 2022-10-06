from django.db import models

class TipoCambioManager(models.Manager):
    def tipo_cambio_venta(self, fecha):
        try:
            return self.filter(fecha=fecha).latest('created_at').venta
        except:
            return None


class SeriesComprobanteManager(models.Manager):
    def por_defecto(self, modelo):
        try:
            return self.filter(tipo_comprobante=modelo, defecto=True).earliest('updated_at')
        except:
            return None


class NubefactAccesoManager(models.Manager):
    def acceder(self, sociedad, modelo):
        try:
            filtro = self.get(
                sociedad = sociedad,
                content_type = modelo,
            )
            if filtro.acceso.ruta and filtro.acceso.token:
                return 'NUBEFACT'
        except:
            pass
        return 'MANUAL'

    def envio(self, sociedad, modelo):
        try:
            filtro = self.get(
                sociedad = sociedad,
                content_type = modelo,
            )
            return filtro
        except:
            pass
        return None