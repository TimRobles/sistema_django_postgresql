from django.db import models
from django.contrib.contenttypes.models import ContentType
from applications.activos.models import MarcaActivo
from applications.sede.models import Sede

from applications.datos_globales.models import Moneda, SeriesComprobante, TipoCambio, Unidad
from applications.sociedad.models import Sociedad
from applications.clientes.models import Cliente, InterlocutorCliente
from applications.envio_clientes.models import Transportista
from applications.variables import TIPO_DOCUMENTO_SUNAT, TIPO_IGV_CHOICES, TIPO_ISC_CHOICES, TIPO_PERCEPCION, TIPO_RETENCION, TIPO_VENTA, ESTADOS
from django.conf import settings

class Guia(models.Model):
    sociedad = models.ForeignKey(Sociedad, on_delete=models.PROTECT)
    serie_comprobante = models.ForeignKey(SeriesComprobante, on_delete=models.PROTECT, blank=True, null=True)
    numero_guia = models.IntegerField()
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name='Guia_cliente', blank=True, null=True)
    cliente_interlocutor = models.ForeignKey(InterlocutorCliente, on_delete=models.PROTECT, related_name='Guia_interlocutor', blank=True, null=True)
    fecha_emision = models.DateField('Fecha Emisión', auto_now=False, auto_now_add=False, blank=True, null=True)
    fecha_traslado = models.DateField('Fecha Traslado', auto_now=False, auto_now_add=False, blank=True, null=True)
    sede = models.ForeignKey(Sede, on_delete=models.CASCADE)
    transportista = models.ForeignKey(Transportista, on_delete=models.PROTECT, blank=True, null=True)
    observaciones = models.TextField()
    numero_bultos = models.IntegerField()
    direccion_partida = models.TextField()
    direccion_destino = models.TextField()
    ubigeo_partida = models.IntegerField()
    ubigeo_destino = models.IntegerField()
    url = models.URLField('URL Guia', max_length=200)
    estado = models.IntegerField()
    motivo_anulación = models.TextField()
   
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='Guia_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='Guia_updated_by', editable=False)

    class Meta:
        verbose_name = 'Guia'
        verbose_name_plural = 'Guias'

    def __str__(self):
        return str(self.id)


class GuiaDetalle(models.Model):
    item = models.IntegerField()
    content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT)
    id_registro = models.IntegerField()
    cantidad = models.DecimalField('Cantidad', max_digits=22, decimal_places=10)
    peso = models.DecimalField('Peso', max_digits=5, decimal_places=2)
    guia = models.ForeignKey(Guia, on_delete=models.CASCADE, related_name='GuiaDetalle_guia_venta', blank=True, null=True)
  
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='GuiaDetalle_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='GuiaDetalle_updated_by', editable=False)

    class Meta:
        verbose_name = 'Guia Detalle'
        verbose_name_plural = 'Guias Detalle'

    def __str__(self):
        return str(self.id)
