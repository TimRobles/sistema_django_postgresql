from django.db import models
from applications.sede.models import Sede
from applications.almacenes.models import Almacen
from applications.sociedad.models import Sociedad
from django.contrib.contenttypes.models import ContentType
from applications.datos_globales.models import Unidad
from django.conf import settings
from applications.variables import ESTADOS_TRASLADO


class MotivoTraslado(models.Model):
    motivo_traslado = models.TextField()
    visible = models.BooleanField()

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='MotivoTraslado_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='MotivoTraslado_updated_by', editable=False)

    class Meta:
        verbose_name = 'Motivo Traslado'
        verbose_name_plural = 'Motivos Traslado'

    def __str__(self):
        return str(self.motivo_traslado)


class EnvioTrasladoProducto(models.Model):
    numero_envio_traslado = models.IntegerField('Número de Envio Traslado', blank=True, null=True)
    sociedad = models.ForeignKey(Sociedad, on_delete=models.PROTECT,blank=True, null=True)
    sede_origen = models.ForeignKey(Sede, on_delete=models.PROTECT, blank=True, null=True)
    direccion_destino = models.CharField('Dirección Destino', max_length=100,blank=True, null=True)
    fecha_traslado = models.DateField('Fecha Traslado', auto_now=False, auto_now_add=False,blank=True, null=True)
    responsable = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Responsable', on_delete=models.PROTECT, blank=True, null=True, related_name='EnvioTrasladoProducto_responsable')
    motivo_traslado = models.ForeignKey(MotivoTraslado, on_delete=models.PROTECT,blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
    estado = models.IntegerField('Estado', choices=ESTADOS_TRASLADO, default=1,blank=True, null=True)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='EnvioTrasladoProducto_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='EnvioTrasladoProducto_updated_by', editable=False)

    class Meta:
        verbose_name = 'Envio Traslado Producto'
        verbose_name_plural = 'Envios Traslado Producto'
        ordering = [
            '-numero_envio_traslado',
            '-fecha_traslado',]


    def __str__(self):
        return str(self.id)


class EnvioTrasladoProductoDetalle(models.Model):
    item = models.IntegerField(blank=True, null=True)
    content_type = models.ForeignKey(ContentType, blank=True, null=True, on_delete=models.PROTECT)
    id_registro = models.IntegerField(blank=True, null=True)
    almacen_origen = models.ForeignKey(Almacen, on_delete=models.PROTECT,blank=True, null=True)
    cantidad_envio = models.DecimalField('Cantidad de Envio', max_digits=5, decimal_places=2,blank=True, null=True)
    unidad = models.ForeignKey(Unidad, on_delete=models.PROTECT,blank=True, null=True)
    estado = models.IntegerField('Estado', choices=ESTADOS_TRASLADO, default=1,blank=True, null=True)
    envio_traslado_almacen = models.ForeignKey(EnvioTrasladoProducto, on_delete=models.CASCADE, related_name='EnvioTrasladoProductoDetalle_envio_traslado_almacen')

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='DetalleEnvioTrasladoProducto_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='DetalleEnvioTrasladoProducto_updated_by', editable=False)

    class Meta:
        verbose_name = 'Envio Traslado Producto Detalle '
        verbose_name_plural = 'Envios Traslado Productos Detalle'
        ordering = ['item',]

    def __str__(self):
        return str(self.id)