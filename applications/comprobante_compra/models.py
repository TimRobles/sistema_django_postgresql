from decimal import Decimal
from django.db import models
from applications.comprobante_compra.managers import ComprobanteCompraCIDetalleManager, ComprobanteCompraPIDetalleManager, ComprobanteCompraPIManager
from applications.datos_globales.models import Moneda
from django.conf import settings
from applications.funciones import obtener_totales
from applications.material.models import ProveedorMaterial
from applications.orden_compra.models import OrdenCompra, OrdenCompraDetalle
from django.contrib.contenttypes.models import ContentType
from applications.recepcion_compra.models import RecepcionCompra
from applications.rutas import ARCHIVO_COMPROBANTE_COMPRA_PI_ARCHIVO, COMPROBANTE_COMPRA_CI_ARCHIVO, COMPROBANTE_COMPRA_PI_ARCHIVO
from applications.sociedad.models import Sociedad
from django.db.models.signals import pre_save, post_save, pre_delete, post_delete

from applications.variables import ESTADO_COMPROBANTE_PI, ESTADO_COMPROBANTE_CI, INCOTERMS, INTERNACIONAL_NACIONAL, TIPO_IGV_CHOICES

# Create your models here.
class ComprobanteCompraPI(models.Model):
    internacional_nacional = models.IntegerField('Internacional-Nacional', choices=INTERNACIONAL_NACIONAL, default=1)
    incoterms = models.IntegerField('INCOTERMS', choices=INCOTERMS, blank=True, null=True)
    numero_comprobante_compra = models.CharField('Número de Comprobante de Compra', max_length=50, blank=True, null=True)
    orden_compra = models.OneToOneField(OrdenCompra, on_delete=models.PROTECT, related_name='ComprobanteCompraPI_orden_compra')
    sociedad = models.ForeignKey(Sociedad, on_delete=models.PROTECT)
    fecha_comprobante = models.DateField('Fecha del Comprobante', auto_now=False, auto_now_add=False, blank=True, null=True)
    fecha_estimada_llegada = models.DateField('Fecha Estimada de Llegada', auto_now=False, auto_now_add=False, blank=True, null=True)
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
    condiciones = models.TextField('Condiciones', blank=True, null=True)
    estado = models.IntegerField('Estado', choices=ESTADO_COMPROBANTE_PI, default=0)
    motivo_anulacion = models.CharField('Motivo de anulación', max_length=50, blank=True, null=True)
    logistico = models.DecimalField('Margen logístico', max_digits=3, decimal_places=2, default=Decimal('0.00'))

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='ComprobanteCompraPI_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='ComprobanteCompraPI_updated_by', editable=False)

    objects = ComprobanteCompraPIManager()

    class Meta:
        verbose_name = 'Comprobante de Compra PI'
        verbose_name_plural = 'Comprobantes de Compra PIs'
        ordering = [
            'estado',
            '-fecha_comprobante',
        ]

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
    def fecha_recepcion(self):
        fechas = []
        try:
            recepciones = RecepcionCompra.objects.filter(
                content_type=self.content_type,
                id_registro=self.id,
            )
            for recepcion in recepciones:
                fechas.append(recepcion.fecha_recepcion)
            return max(fechas)
        except:
            return None

    @property
    def proveedor(self):
        return self.orden_compra.proveedor

    @property
    def detalle(self):
        return self.ComprobanteCompraPIDetalle_comprobante_compra.all()

    def get_tipo_comprobante_display(self):
        return 'PI'

    @property
    def content_type(self):
        return ContentType.objects.get_for_model(self)

    @property
    def id_registro(self):
        return self.id

    @property
    def documento(self):
        return self.numero_comprobante_compra
        
    def __str__(self):
        return "PROFORMA INVOICE %s" % (self.numero_comprobante_compra)


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
    def content_type(self):
        return ContentType.objects.get_for_model(self)

    @property
    def id_registro(self):
        return self.id

    @property
    def producto(self):
        return self.orden_compra_detalle.producto
    
    @property
    def proveedor(self):
        return self.comprobante_compra.proveedor
    
    @property
    def descripcion_proveedor(self):
        proveedor_material = ProveedorMaterial.objects.get(
            content_type = self.orden_compra_detalle.content_type,
            id_registro = self.orden_compra_detalle.id_registro,
            proveedor = self.proveedor,
            estado_alta_baja = 1,
        )
        return "%s %s" % (proveedor_material.name, proveedor_material.description)

    @property
    def sociedad(self):
        return self.comprobante_compra.sociedad

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
    descripcion = models.CharField(max_length=200, blank=True, null=True)
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

def comprobante_compra_ci_detalle_post_save(*args, **kwargs):
    obj = kwargs['instance']
    respuesta = obtener_totales(obj.comprobante_compra)
    obj.comprobante_compra.total_descuento = respuesta['total_descuento']
    obj.comprobante_compra.total_anticipo = respuesta['total_anticipo']
    obj.comprobante_compra.total_gravada = respuesta['total_gravada']
    obj.comprobante_compra.total_inafecta = respuesta['total_inafecta']
    obj.comprobante_compra.total_exonerada = respuesta['total_exonerada']
    obj.comprobante_compra.total_igv = respuesta['total_igv']
    obj.comprobante_compra.total_gratuita = respuesta['total_gratuita']
    obj.comprobante_compra.otros_cargos = respuesta['total_otros_cargos']
    obj.comprobante_compra.total = respuesta['total']
    obj.comprobante_compra.save()

post_save.connect(comprobante_compra_ci_detalle_post_save, sender=ComprobanteCompraCIDetalle)