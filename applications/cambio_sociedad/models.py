from decimal import Decimal
from django.db import models
from applications.calidad.models import Serie
from applications.funciones import numeroXn
from applications.movimiento_almacen.models import TipoStock
from applications.sede.models import Sede
from applications.almacenes.models import Almacen
from applications.sociedad.models import Sociedad
from django.contrib.contenttypes.models import ContentType
from applications.datos_globales.models import Unidad
from django.conf import settings
from applications.variables import ESTADOS_TRASLADO_PRODUCTO, ESTADOS_TRASLADO_PRODUCTO_DETALLE
from applications.material.models import Material
from applications.movimiento_almacen.models import TipoStock


class CambioSociedadStock(models.Model):
    ESTADOS_CAMBIO_SOCIEDAD_STOCK = (
        (1, 'EN PROCESO'),
        (2, 'CONCLUIDO'),
        (3, 'ANULADO'),
        )
    nro_cambio = models.IntegerField('Nro. Cambio', blank=True, null=True)
    encargado = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True)
    sociedad_inicial = models.ForeignKey(Sociedad, related_name = 'CambioSociedadStock_sociedad_inicial', on_delete=models.PROTECT,blank=True, null=True)
    sociedad_final = models.ForeignKey(Sociedad, related_name = 'CambioSociedadStock_sociedad_final', on_delete=models.PROTECT,blank=True, null=True)
    sede = models.ForeignKey(Sede, on_delete=models.PROTECT, blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
    estado = models.IntegerField('Estado', choices=ESTADOS_CAMBIO_SOCIEDAD_STOCK, default=1, blank=True, null=True)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False, blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='CambioSociedadStock_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='CambioSociedadStock_updated_by', editable=False)

    class Meta:
        verbose_name = 'Cambio Sociedad Stock'
        verbose_name_plural = 'Cambios Sociedad Stock'
        ordering = ['-nro_cambio',]

    @property
    def fecha(self):
        return self.updated_at.date()

    def __str__(self):
        return f"{self.sociedad_final.abreviatura}{numeroXn(self.nro_cambio, 6)}"


class CambioSociedadStockDetalle(models.Model):
    item = models.IntegerField(blank=True, null=True)
    cambio_sociedad_stock = models.ForeignKey(CambioSociedadStock, on_delete=models.CASCADE, related_name='CambioSociedadStockDetalle_cambio_sociedad_stock')
    content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT) #Material
    id_registro = models.IntegerField()
    almacen = models.ForeignKey(Almacen, on_delete=models.PROTECT)
    tipo_stock = models.ForeignKey(TipoStock, related_name = 'CambioSociedadStockDetalle_tipo_stock', on_delete=models.PROTECT)
    cantidad = models.DecimalField('Cantidad de Cambio', max_digits=22, decimal_places=10)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='CambioSociedadStockDetalle_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='CambioSociedadStockDetalle_updated_by', editable=False)

    class Meta:
        verbose_name = 'Cambio Sociedad Stock Detalle'
        verbose_name_plural = 'Cambios Sociedad Stock Detalle'
        ordering = (
            'item',
            )

    @property
    def producto(self):
        return self.content_type.get_object_for_this_type(id=self.id_registro)
            
    @property
    def control_serie(self):
        return self.producto.control_serie
            
    @property
    def sociedad_inicial(self):
        return self.cambio_sociedad_stock.sociedad_inicial

    @property
    def sociedad_final(self):
        return self.cambio_sociedad_stock.sociedad_final

    @property
    def series_validar(self):
        return Decimal(len(self.ValidarSerieCambioSociedadStockDetalle_cambio_sociedad_stock_detalle.all())).quantize(Decimal('0.01'))

    def __str__(self):
        return str(self.id)


class ValidarSerieCambioSociedadStockDetalle(models.Model):
    cambio_sociedad_stock_detalle = models.ForeignKey(CambioSociedadStockDetalle, on_delete=models.PROTECT, related_name='ValidarSerieCambioSociedadStockDetalle_cambio_sociedad_stock_detalle')
    serie = models.ForeignKey(Serie, on_delete=models.CASCADE, blank=True, null=True)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='ValidarSerieCambioSociedadStockDetalle_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='ValidarSerieCambioSociedadStockDetalle_updated_by', editable=False)

    class Meta:
        verbose_name = 'Validar Series Cambio Sociedad Stock Detalle'
        verbose_name_plural = 'Validar Series Cambios Sociedad Stock Detalle'
        ordering = [
            'created_at',
            ]

    def __str__(self):
        return "%s - %s" % (self.cambio_sociedad_stock_detalle , str(self.serie))