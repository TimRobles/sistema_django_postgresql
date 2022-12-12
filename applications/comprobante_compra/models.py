from decimal import Decimal
from django.db import models
from applications.comprobante_compra.managers import ComprobanteCompraCIDetalleManager, ComprobanteCompraPIDetalleManager, ComprobanteCompraPIManager
from applications.datos_globales.models import Moneda
from django.conf import settings
from applications.orden_compra.models import OrdenCompra, OrdenCompraDetalle
from django.contrib.contenttypes.models import ContentType
from applications.rutas import ARCHIVO_COMPROBANTE_COMPRA_PI_ARCHIVO, COMPROBANTE_COMPRA_CI_ARCHIVO, COMPROBANTE_COMPRA_PI_ARCHIVO
from applications.sociedad.models import Sociedad

from applications.variables import ESTADO_COMPROBANTE_PI, ESTADO_COMPROBANTE_CI, INCOTERMS, INTERNACIONAL_NACIONAL, TIPO_IGV_CHOICES

# Create your models here.
class ComprobanteCompraPI(models.Model):
    internacional_nacional = models.IntegerField('Internacional-Nacional', choices=INTERNACIONAL_NACIONAL, default=1)
    incoterms = models.IntegerField('INCOTERMS', choices=INCOTERMS, blank=True, null=True)
    numero_comprobante_compra = models.CharField('Número de Comprobante de Compra', max_length=50, blank=True, null=True)
    orden_compra = models.OneToOneField(OrdenCompra, on_delete=models.PROTECT)
    sociedad = models.ForeignKey(Sociedad, on_delete=models.PROTECT)
    fecha_comprobante = models.DateField('Fecha del Comprobante', auto_now=False, auto_now_add=False, blank=True, null=True)
    moneda = models.ForeignKey(Moneda, on_delete=models.PROTECT)
    descuento_global = models.DecimalField('Descuento Global', max_digits=14, decimal_places=2, default=Decimal('0.00'))
    total_descuento = models.DecimalField('Total Descuento', max_digits=14, decimal_places=2, default=Decimal('0.00'))
    total_anticipo = models.DecimalField('Total Anticipo', max_digits=14, decimal_places=2, default=Decimal('0.00'))
    total_gravada = models.DecimalField('Total Gravada', max_digits=14, decimal_places=2, default=Decimal('0.00'))
    total_inafecta = models.DecimalField('Total Inafecta', max_digits=14, decimal_places=2, default=Decimal('0.00'))
    total_exonerada = models.DecimalField('Total Exonerada', max_digits=14, decimal_places=2, default=Decimal('0.00'))
    total_igv = models.DecimalField('Total IGV', max_digits=14, decimal_places=2, default=Decimal('0.00'))
    total_gratuita = models.DecimalField('Total Gratuita', max_digits=14, decimal_places=2, default=Decimal('0.00'))
    total_otros_cargos = models.DecimalField('Total Otros Cargos', max_digits=14, decimal_places=2, default=Decimal('0.00'))
    total_icbper = models.DecimalField('Total ICBPER', max_digits=14, decimal_places=2, default=Decimal('0.00'))
    total = models.DecimalField('Total', max_digits=14, decimal_places=2, default=Decimal('0.00'))
    slug = models.SlugField(blank=True, null=True)
    archivo = models.FileField('Archivo', upload_to=COMPROBANTE_COMPRA_PI_ARCHIVO, max_length=100, blank=True, null=True)
    condiciones = models.TextField('Condiciones', blank=True, null=True)
    estado = models.IntegerField('Estado', choices=ESTADO_COMPROBANTE_PI, default=1)
    motivo_anulacion = models.CharField('Motivo de anulación', max_length=50, blank=True, null=True)
    logistico = models.DecimalField('Margen logístico', max_digits=3, decimal_places=2, default=1)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='ComprobanteCompraPI_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='ComprobanteCompraPI_updated_by', editable=False)

    objects = ComprobanteCompraPIManager()

    class Meta:
        verbose_name = 'Comprobante de Compra PI'
        verbose_name_plural = 'Comprobantes de Compra PIs'

    @property
    def no_existe_CI(self):
        if hasattr(self, 'ComprobanteCompraCI_comprobante_compra_PI'):
            return False
        else:
            return True

    @property
    def fecha(self):
        return self.fecha_comprobante

    @property
    def proveedor(self):
        return self.orden_compra.proveedor

    @property
    def detalle(self):
        return self.ComprobanteCompraPIDetalle_comprobante_compra.all()

    def get_tipo_comprobante_display(self):
        return 'PI'

    @property
    def documento(self):
        return self.numero_comprobante_compra
        
    def __str__(self):
        return "%s" % (self.numero_comprobante_compra)


class ComprobanteCompraPIDetalle(models.Model):
    item = models.IntegerField()
    orden_compra_detalle = models.OneToOneField(OrdenCompraDetalle, on_delete=models.PROTECT, related_name='ComprobanteCompraPIDetalle_orden_compra_detalle')
    cantidad = models.DecimalField('Cantidad', max_digits=22, decimal_places=10)
    precio_unitario_sin_igv = models.DecimalField('Precio Unitario Sin IGV', max_digits=22, decimal_places=10, default=Decimal('0.00'))
    precio_unitario_con_igv = models.DecimalField('Precio Unitario Con IGV', max_digits=22, decimal_places=10, default=Decimal('0.00'))
    precio_final_con_igv = models.DecimalField('Precio Final Con IGV', max_digits=22, decimal_places=10, default=Decimal('0.00'))
    descuento = models.DecimalField('Descuento', max_digits=14, decimal_places=2, default=Decimal('0.00'))
    sub_total = models.DecimalField('Sub Total', max_digits=14, decimal_places=2, default=Decimal('0.00'))
    igv = models.DecimalField('IGV', max_digits=14, decimal_places=2, default=Decimal('0.00'))
    total = models.DecimalField('Total', max_digits=14, decimal_places=2, default=Decimal('0.00'))
    tipo_igv = models.IntegerField(choices=TIPO_IGV_CHOICES)
    comprobante_compra = models.ForeignKey(ComprobanteCompraPI, on_delete=models.CASCADE, related_name='ComprobanteCompraPIDetalle_comprobante_compra')

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='ComprobanteCompraPIDetalle_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='ComprobanteCompraPIDetalle_updated_by', editable=False)

    objects = ComprobanteCompraPIDetalleManager()

    class Meta:
        verbose_name = 'Comprobante de Compra PI Detalle'
        verbose_name_plural = 'Comprobantes de Compra PI Detalles'
        ordering = [
            'comprobante_compra',
            'item',
            ]

    @property
    def producto(self):
        return self.orden_compra_detalle.producto

    def __str__(self):
        return "%s" % (str(self.orden_compra_detalle))


class ArchivoComprobanteCompraPI(models.Model):
    archivo = models.FileField('Archivo', upload_to=ARCHIVO_COMPROBANTE_COMPRA_PI_ARCHIVO, max_length=100)
    comprobante_compra = models.ForeignKey(ComprobanteCompraPI, on_delete=models.CASCADE)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='ArchivoComprobanteCompraPI_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='ArchivoComprobanteCompraPI_updated_by', editable=False)

    class Meta:
        verbose_name = 'Archivo de Comprobante de Compra PI'
        verbose_name_plural = 'Archivos de Comprobantes de Compra PIs'

    def __str__(self):
        return self.archivo

        
class ComprobanteCompraCI(models.Model):
    internacional_nacional = models.IntegerField('Internacional-Nacional', choices=INTERNACIONAL_NACIONAL, default=1)
    incoterms = models.IntegerField('INCOTERMS', choices=INCOTERMS, blank=True, null=True)
    numero_comprobante_compra = models.CharField('Número de Comprobante de Compra', max_length=50, blank=True, null=True)
    comprobante_compra_PI = models.OneToOneField(ComprobanteCompraPI, on_delete=models.PROTECT, related_name='ComprobanteCompraCI_comprobante_compra_PI')
    sociedad = models.ForeignKey(Sociedad, on_delete=models.PROTECT)
    fecha_comprobante = models.DateField('Fecha del Comprobante', auto_now=False, auto_now_add=False)
    moneda = models.ForeignKey(Moneda, on_delete=models.PROTECT)
    descuento_global = models.DecimalField('Descuento Global', max_digits=14, decimal_places=2, default=Decimal('0.00'))
    total_descuento = models.DecimalField('Total Descuento', max_digits=14, decimal_places=2, default=Decimal('0.00'))
    total_anticipo = models.DecimalField('Total Anticipo', max_digits=14, decimal_places=2, default=Decimal('0.00'))
    total_gravada = models.DecimalField('Total Gravada', max_digits=14, decimal_places=2, default=Decimal('0.00'))
    total_inafecta = models.DecimalField('Total Inafecta', max_digits=14, decimal_places=2, default=Decimal('0.00'))
    total_exonerada = models.DecimalField('Total Exonerada', max_digits=14, decimal_places=2, default=Decimal('0.00'))
    total_igv = models.DecimalField('Total IGV', max_digits=14, decimal_places=2, default=Decimal('0.00'))
    total_gratuita = models.DecimalField('Total Gratuita', max_digits=14, decimal_places=2, default=Decimal('0.00'))
    total_otros_cargos = models.DecimalField('Total Otros Cargos', max_digits=14, decimal_places=2, default=Decimal('0.00'))
    total_icbper = models.DecimalField('Total ICBPER', max_digits=14, decimal_places=2, default=Decimal('0.00'))
    total = models.DecimalField('Total', max_digits=14, decimal_places=2, default=Decimal('0.00'))
    slug = models.SlugField(blank=True, null=True)
    archivo = models.FileField('Archivo', upload_to=COMPROBANTE_COMPRA_CI_ARCHIVO, max_length=100, blank=True, null=True)
    condiciones = models.TextField('Condiciones', blank=True, null=True)
    estado = models.IntegerField('Estado', choices=ESTADO_COMPROBANTE_CI, default=1)
    motivo_anulacion = models.CharField('Motivo de anulación', max_length=50, blank=True, null=True)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='ComprobanteCompraCI_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='ComprobanteCompraCI_updated_by', editable=False)

    class Meta:
        verbose_name = 'Comprobante de Compra CI'
        verbose_name_plural = 'Comprobantes de Compra CIs'

    def __str__(self):
        return self.numero_comprobante_compra


class ComprobanteCompraCIDetalle(models.Model):
    item = models.IntegerField()
    content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT)
    id_registro = models.IntegerField()
    cantidad = models.DecimalField('Cantidad', max_digits=22, decimal_places=10)
    precio_unitario_sin_igv = models.DecimalField('Precio Unitario Sin IGV', max_digits=22, decimal_places=10, default=Decimal('0.00'))
    precio_unitario_con_igv = models.DecimalField('Precio Unitario Con IGV', max_digits=22, decimal_places=10, default=Decimal('0.00'))
    precio_final_con_igv = models.DecimalField('Precio Final Con IGV', max_digits=22, decimal_places=10, default=Decimal('0.00'))
    descuento = models.DecimalField('Descuento', max_digits=14, decimal_places=2, default=Decimal('0.00'))
    sub_total = models.DecimalField('Sub Total', max_digits=14, decimal_places=2, default=Decimal('0.00'))
    igv = models.DecimalField('IGV', max_digits=14, decimal_places=2, default=Decimal('0.00'))
    total = models.DecimalField('Total', max_digits=14, decimal_places=2, default=Decimal('0.00'))
    tipo_igv = models.IntegerField(choices=TIPO_IGV_CHOICES)
    comprobante_compra = models.ForeignKey(ComprobanteCompraCI, on_delete=models.CASCADE, related_name='ComprobanteCompraCIDetalle_comprobante_compra')

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='ComprobanteCompraCIDetalle_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='ComprobanteCompraCIDetalle_updated_by', editable=False)

    objects = ComprobanteCompraCIDetalleManager()

    class Meta:
        verbose_name = 'Comprobante de Compra CI Detalle'
        verbose_name_plural = 'Comprobantes de Compra CI Detalles'
        ordering = [
            'comprobante_compra',
            'item',
            ]

    def __str__(self):
        return str(self.item)