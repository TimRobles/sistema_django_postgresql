from django.db import models
from django.contrib.contenttypes.models import ContentType

class TipoCambioManager(models.Manager):
    def tipo_cambio_venta(self, fecha):
        try:
            return self.filter(fecha=fecha).latest('created_at').venta
        except:
            return None


class SeriesComprobanteManager(models.Manager):
    def por_defecto(self, modelo):
        try:
            return self.filter(tipo_comprobante=modelo, defecto=True, mostrar=True).earliest('updated_at')
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


class NubefactRespuestaManager(models.Manager):
    def respuesta(self, obj):
        try:
            filtro = self.filter(
                content_type = ContentType.objects.get_for_model(obj),
                id_registro = obj.id
            ).filter(aceptado=True).latest('updated_at')
            return filtro
        except:
            pass
        return None
    
    def respuestas(self, obj):
        try:
            filtro = self.filter(
                content_type = ContentType.objects.get_for_model(obj),
                id_registro = obj.id
            )
            return filtro
        except:
            pass
        return None