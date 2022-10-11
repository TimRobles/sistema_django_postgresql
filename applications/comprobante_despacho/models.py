from decimal import Decimal
from django.db import models
from django.contrib.contenttypes.models import ContentType
from applications.activos.models import MarcaActivo
from applications.sede.models import Sede

from applications.datos_globales.models import Distrito, Moneda, SeriesComprobante, TipoCambio, Unidad
from applications.sociedad.models import Sociedad
from applications.clientes.models import Cliente, InterlocutorCliente
from applications.envio_clientes.models import Transportista
from applications.variables import ESTADOS_GUIA, MOTIVO_TRASLADO, TIPO_COMPROBANTE, TIPO_DOCUMENTO_SUNAT, TIPO_IGV_CHOICES, TIPO_ISC_CHOICES, TIPO_PERCEPCION, TIPO_RETENCION, TIPO_VENTA, ESTADOS
from django.conf import settings

class Guia(models.Model):
    tipo_comprobante = models.IntegerField('Tipo de Comprobante', choices=TIPO_COMPROBANTE, default=7)
    sociedad = models.ForeignKey(Sociedad, on_delete=models.CASCADE)
    serie_comprobante = models.ForeignKey(SeriesComprobante, on_delete=models.PROTECT, blank=True, null=True)
    numero_guia = models.IntegerField('Número Guía',blank=True, null=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name='Guia_cliente', blank=True, null=True)
    cliente_interlocutor = models.ForeignKey(InterlocutorCliente, on_delete=models.PROTECT, related_name='Guia_interlocutor', blank=True, null=True)
    fecha_emision = models.DateField('Fecha Emisión', auto_now=False, auto_now_add=False, blank=True, null=True)
    fecha_traslado = models.DateField('Fecha Traslado', auto_now=False, auto_now_add=False, blank=True, null=True)
    transportista = models.ForeignKey(Transportista, on_delete=models.PROTECT, blank=True, null=True)
    conductor_tipo_documento = models.CharField('Tipo de Documento', max_length=1, choices=TIPO_DOCUMENTO_SUNAT, blank=True, null=True)
    conductor_numero_documento = models.CharField('Número de Documento', max_length=15, blank=True, null=True)
    conductor_denominacion = models.CharField('Nombre completo', max_length=100, blank=True, null=True)
    placa_numero = models.CharField('Número de placa', max_length=8, blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
    motivo_traslado = models.CharField('Motivo de Traslado', choices=MOTIVO_TRASLADO, default='01', max_length=2)
    numero_bultos = models.IntegerField(blank=True, null=True)
    direccion_partida = models.CharField('Dirección de Partida', max_length=100, blank=True, null=True)
    direccion_destino = models.CharField('Dirección de Destino', max_length=100, blank=True, null=True)
    ubigeo_partida = models.ForeignKey(Distrito, on_delete=models.PROTECT, related_name='Guia_ubigeo_partida',blank=True, null=True)
    ubigeo_destino = models.ForeignKey(Distrito, on_delete=models.PROTECT, related_name='Guia_ubigeo_destino',blank=True, null=True)
    motivo_anulación = models.TextField('Motivo Anulación', blank=True, null=True)
    estado = models.IntegerField('Estado', choices=ESTADOS_GUIA, default=1)
   
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='Guia_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='Guia_updated_by', editable=False)

    class Meta:
        verbose_name = 'Guia'
        verbose_name_plural = 'Guias'

    @property
    def peso_total(self):
        if self.GuiaDetalle_guia_venta.all():
            return self.GuiaDetalle_guia_venta.aggregate(models.Sum('peso'))['peso__sum']
        else:
            return Decimal('0.00')

    def __str__(self):
        return str(self.id)


class GuiaDetalle(models.Model):
    item = models.IntegerField(blank=True, null=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT,blank=True, null=True)
    id_registro = models.IntegerField(blank=True, null=True)
    cantidad = models.DecimalField('Cantidad', max_digits=22, decimal_places=10,blank=True, null=True)
    peso = models.DecimalField('Peso', max_digits=5, decimal_places=2, blank=True, null=True)
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
