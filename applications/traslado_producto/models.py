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


class MotivoTraslado(models.Model):
    motivo_traslado = models.CharField(max_length=100)
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
    estado = models.IntegerField('Estado', choices=ESTADOS_TRASLADO_PRODUCTO, default=1,blank=True, null=True)

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

    @property
    def fecha(self):
        return self.fecha_traslado

    def __str__(self):
        if self.fecha_traslado:
            return "%s - %s - %s - %s" % (self.fecha_traslado.strftime('%d/%m/%Y'), numeroXn(self.numero_envio_traslado, 6), self.sede_origen, self.responsable)
        else:
            return f"ID:{self.id} {self.created_by}"


class EnvioTrasladoProductoDetalle(models.Model):
    item = models.IntegerField(blank=True, null=True)
    content_type = models.ForeignKey(ContentType, blank=True, null=True, on_delete=models.PROTECT)
    id_registro = models.IntegerField()
    almacen_origen = models.ForeignKey(Almacen, on_delete=models.PROTECT,blank=True, null=True)
    tipo_stock = models.ForeignKey(TipoStock, on_delete=models.CASCADE)
    cantidad_envio = models.DecimalField('Cantidad de Envio', max_digits=8, decimal_places=2,blank=True, null=True)
    unidad = models.ForeignKey(Unidad, on_delete=models.PROTECT,blank=True, null=True)
    estado = models.IntegerField('Estado', choices=ESTADOS_TRASLADO_PRODUCTO_DETALLE, default=1,blank=True, null=True)
    envio_traslado_producto = models.ForeignKey(EnvioTrasladoProducto, on_delete=models.CASCADE, related_name='EnvioTrasladoProductoDetalle_envio_traslado_producto')

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='EnvioTrasladoProductoDetalle_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='EnvioTrasladoProductoDetalle_updated_by', editable=False)

    class Meta:
        verbose_name = 'Envio Traslado Producto Detalle '
        verbose_name_plural = 'Envios Traslado Productos Detalle'
        ordering = ['item',]

    @property
    def producto(self):
        return self.content_type.get_object_for_this_type(id=self.id_registro)
            
    @property
    def control_serie(self):
        return self.producto.control_serie

    @property
    def series_validar(self):
        return Decimal(len(self.ValidarSerieEnvioTrasladoProductoDetalle_envio_traslado_producto_detalle.all())).quantize(Decimal('0.01'))

    def __str__(self):
        return f"{self.item} - {self.producto} - {self.almacen_origen} - {self.tipo_stock}. Cantidad: {self.cantidad_envio}"


class ValidarSerieEnvioTrasladoProductoDetalle(models.Model):
    envio_traslado_producto_detalle = models.ForeignKey(EnvioTrasladoProductoDetalle, on_delete=models.PROTECT, related_name='ValidarSerieEnvioTrasladoProductoDetalle_envio_traslado_producto_detalle')
    serie = models.ForeignKey(Serie, on_delete=models.CASCADE, blank=True, null=True)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='ValidarSerieEnvioTrasladoProductoDetalle_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='ValidarSerieEnvioTrasladoProductoDetalle_updated_by', editable=False)

    class Meta:
        verbose_name = 'Validar Series Envio Traslado Producto Detalle'
        verbose_name_plural = 'Validar Series Envios Traslado Producto Detalle'
        ordering = [
            'created_at',
            ]

    def __str__(self):
        return "%s - %s" % (self.envio_traslado_producto_detalle , str(self.serie))


class RecepcionTrasladoProducto(models.Model):
    envio_traslado_producto = models.ForeignKey(EnvioTrasladoProducto, on_delete=models.CASCADE, related_name='RecepcionTrasladoProducto_envio_traslado_producto', blank=True, null=True)
    numero_recepcion_traslado = models.IntegerField('Número de Recepción Traslado', blank=True, null=True)
    sede_destino = models.ForeignKey(Sede, on_delete=models.PROTECT, blank=True, null=True)
    fecha_recepcion = models.DateField('Fecha Recepción', auto_now=False, auto_now_add=False,blank=True, null=True)
    responsable = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Responsable', on_delete=models.PROTECT, blank=True, null=True, related_name='RecepcionTrasladoProducto_responsable')
    observaciones = models.TextField(blank=True, null=True)
    estado = models.IntegerField('Estado', choices=ESTADOS_TRASLADO_PRODUCTO, default=1,blank=True, null=True)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False, blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='RecepcionTrasladoProducto_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='RecepcionTrasladoProducto_updated_by', editable=False)

    class Meta:
        verbose_name = 'Recepcion Traslado Producto'
        verbose_name_plural = 'Recepcion Traslado Productos'

    @property
    def fecha(self):
        return self.fecha_recepcion

    @property
    def sociedad(self):
        return self.envio_traslado_producto.sociedad

    def __str__(self):
        return "%s - %s - %s - %s" % (self.fecha_recepcion.strftime('%d/%m/%Y'), numeroXn(self.id, 6), self.sede_destino, self.responsable)


class RecepcionTrasladoProductoDetalle(models.Model):
    item = models.IntegerField(blank=True, null=True)
    envio_traslado_producto_detalle = models.ForeignKey(EnvioTrasladoProductoDetalle, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, blank=True, null=True, on_delete=models.PROTECT)
    id_registro = models.IntegerField(blank=True, null=True)
    almacen_destino = models.ForeignKey(Almacen, on_delete=models.PROTECT,blank=True, null=True)
    cantidad_recepcion = models.DecimalField('Cantidad de Recepción', max_digits=8, decimal_places=2,blank=True, null=True)
    unidad = models.ForeignKey(Unidad, on_delete=models.PROTECT,blank=True, null=True)
    estado = models.IntegerField('Estado', choices=ESTADOS_TRASLADO_PRODUCTO_DETALLE, default=1,blank=True, null=True)
    recepcion_traslado_producto = models.ForeignKey(RecepcionTrasladoProducto, on_delete=models.CASCADE, related_name='RecepcionTrasladoProductoDetalle_recepcion_traslado_producto')

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='RecepcionTrasladoProductoDetalle_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='RecepcionTrasladoProductoDetalle_updated_by', editable=False)

    class Meta:
        verbose_name = 'Recepcion Traslado Producto Detalle'
        verbose_name_plural = 'Recepcion Traslado Productos Detalle'

    @property
    def producto(self):
        return self.content_type.get_object_for_this_type(id=self.id_registro)

    def __str__(self):
        return str(self.id)


class ValidarSerieRecepcionTrasladoProductoDetalle(models.Model):
    recepcion_traslado_producto_detalle = models.ForeignKey(RecepcionTrasladoProductoDetalle, on_delete=models.PROTECT, related_name='ValidarSerieRecepcionTrasladoProductoDetalle_recepcion_traslado_producto_detalle')
    serie = models.ForeignKey(Serie, on_delete=models.CASCADE, blank=True, null=True)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='ValidarSerieRecepcionTrasladoProductoDetalle_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='ValidarSerieRecepcionTrasladoProductoDetalle_updated_by', editable=False)

    class Meta:
        verbose_name = 'Validar Series Recepcion Traslado Producto Detalle'
        verbose_name_plural = 'Validar Series Recepciones Traslado Producto Detalle'
        ordering = [
            'created_at',
            ]

    def __str__(self):
        return "%s - %s" % (self.recepcion_traslado_producto_detalle , str(self.serie))


class TraspasoStock(models.Model):
    ESTADOS_TRASPASO_STOCK = (
        (1, 'EN PROCESO'),
        (2, 'CONCLUIDO'),
        (3, 'ANULADO'),
        )
    nro_traspaso = models.CharField('Nro. Traspaso', max_length=100,blank=True, null=True)
    encargado = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True)
    sociedad = models.ForeignKey(Sociedad, on_delete=models.PROTECT,blank=True, null=True)
    sede = models.ForeignKey(Sede, on_delete=models.PROTECT, blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
    estado = models.IntegerField('Estado', choices=ESTADOS_TRASPASO_STOCK, default=1, blank=True, null=True)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False, blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='TraspasoStock_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='TraspasoStock_updated_by', editable=False)

    class Meta:
        verbose_name = 'Traspaso Stock'
        verbose_name_plural = 'Traspasos Stock'
        ordering = ['-nro_traspaso',]

    @property
    def fecha(self):
        return self.updated_at.date()

    def __str__(self):
        return f"{self.sociedad.abreviatura}{numeroXn(self.nro_traspaso, 6)}"


class TraspasoStockDetalle(models.Model):
    item = models.IntegerField(blank=True, null=True)
    traspaso_stock = models.ForeignKey(TraspasoStock, on_delete=models.CASCADE, related_name='TraspasoStockDetalle_traspaso_stock')
    content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT) #Material
    id_registro = models.IntegerField()
    almacen = models.ForeignKey(Almacen, on_delete=models.PROTECT)
    tipo_stock_inicial = models.ForeignKey(TipoStock, related_name = 'TraspasoStockDetalle_tipo_stock_inicial', on_delete=models.PROTECT)
    tipo_stock_final = models.ForeignKey(TipoStock, related_name = 'TraspasoStockDetalle_tipo_stock_final', on_delete=models.PROTECT)
    cantidad = models.DecimalField('Cantidad de Traspaso', max_digits=22, decimal_places=10)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='TraspasoStockDetalle_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='TraspasoStockDetalle_updated_by', editable=False)

    class Meta:
        verbose_name = 'Traspaso Stock Detalle'
        verbose_name_plural = 'Traspasos Stock Detalle'

    @property
    def producto(self):
        return self.content_type.get_object_for_this_type(id=self.id_registro)
            
    @property
    def control_serie(self):
        return self.producto.control_serie
            
    @property
    def sociedad(self):
        return self.traspaso_stock.sociedad

    @property
    def series_validar(self):
        return Decimal(len(self.ValidarSerieTraspasoStockDetalle_traspaso_stock_detalle.all())).quantize(Decimal('0.01'))

    def __str__(self):
        return str(self.id)


class ValidarSerieTraspasoStockDetalle(models.Model):
    traspaso_stock_detalle = models.ForeignKey(TraspasoStockDetalle, on_delete=models.PROTECT, related_name='ValidarSerieTraspasoStockDetalle_traspaso_stock_detalle')
    serie = models.ForeignKey(Serie, on_delete=models.CASCADE, blank=True, null=True)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='ValidarSerieTraspasoStockDetalle_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='ValidarSerieTraspasoStockDetalle_updated_by', editable=False)

    class Meta:
        verbose_name = 'Validar Series Traspaso Stock Detalle'
        verbose_name_plural = 'Validar Series Traspasos Stock Detalle'
        ordering = [
            'created_at',
            ]

    def __str__(self):
        return "%s - %s" % (self.traspaso_stock_detalle , str(self.serie))


