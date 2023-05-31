from decimal import Decimal
from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from applications.funciones import ver_proveedor
from applications.rutas import ARCHIVO_RECEPCION_COMPRA_ARCHIVO, FOTO_RECEPCION_COMPRA_FOTO

from applications.variables import ESTADO_COMPROBANTE, ESTADO_DOCUMENTO, TIPO_IGV_CHOICES

# Create your models here.
class RecepcionCompra(models.Model):
    numero_comprobante_compra = models.CharField('Número de Comprobante de Compra', max_length=50)
    content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT) #ComprobanteCompraPI / NotaStockInicial
    id_registro = models.IntegerField()
    fecha_recepcion = models.DateField('Fecha de Recepción', auto_now=False, auto_now_add=False)
    usuario_recepcion = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='RecepcionCompra_usuario_recepcion')
    nro_bultos = models.DecimalField('Número de Bultos', max_digits=4, decimal_places=0)
    observaciones = models.TextField(blank=True, null=True)
    motivo_anulacion = models.TextField(blank=True, null=True)
    estado = models.IntegerField('Estado', choices=ESTADO_COMPROBANTE, default=1)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='RecepcionCompra_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='RecepcionCompra_updated_by', editable=False)

    class Meta:
        verbose_name = 'Recepción de Compra'
        verbose_name_plural = 'Recepciones de Compras'

    @property
    def proveedor(self):
        documento = self.content_type.get_object_for_this_type(id=self.id_registro)
        return ver_proveedor(documento)[0]

    @property
    def interlocutor_proveedor(self):
        documento = self.content_type.get_object_for_this_type(id=self.id_registro)
        return ver_proveedor(documento)[1]

    @property
    def sociedad(self):
        documento = self.content_type.get_object_for_this_type(id=self.id_registro)
        return documento.sociedad

    @property
    def documento(self):
        documento = self.content_type.get_object_for_this_type(id=self.id_registro)
        return documento

    @property
    def fecha(self):
        return self.fecha_recepcion

    def __str__(self):
        try:
            return "%s" % (str(self.content_type.get_object_for_this_type(id=self.id_registro)))
        except:
            return "-"


class ArchivoRecepcionCompra(models.Model):
    archivo = models.FileField('Archivo', upload_to=ARCHIVO_RECEPCION_COMPRA_ARCHIVO, max_length=100)
    recepcion_compra = models.ForeignKey(RecepcionCompra, on_delete=models.CASCADE)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='ArchivoRecepcionCompra_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='ArchivoRecepcionCompra_updated_by', editable=False)

    class Meta:
        verbose_name = 'Archivo de Comprobante de Compra PI'
        verbose_name_plural = 'Archivos de Comprobantes de Compra PIs'
        ordering = [
            'recepcion_compra',
            'archivo',
            ]

    def __str__(self):
        return str(self.archivo)


class FotoRecepcionCompra(models.Model):
    foto = models.ImageField('Foto', upload_to=FOTO_RECEPCION_COMPRA_FOTO, height_field=None, width_field=None, max_length=None)
    recepcion_compra = models.ForeignKey(RecepcionCompra, on_delete=models.CASCADE)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='FotoRecepcionCompra_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='FotoRecepcionCompra_updated_by', editable=False)

    class Meta:
        verbose_name = 'Foto de Comprobante de Compra PI'
        verbose_name_plural = 'Fotos de Comprobantes de Compra PIs'
        ordering = [
            'recepcion_compra',
            'foto',
            ]

    def __str__(self):
        return str(self.foto)


class DocumentoReclamo(models.Model):
    recepcion_compra = models.ForeignKey(RecepcionCompra, on_delete=models.CASCADE)
    fecha_documento = models.DateField('Fecha de Documento', auto_now=False, auto_now_add=False)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='DocumentoReclamo_usuario')
    observaciones = models.TextField(blank=True, null=True)
    motivo_anulacion = models.TextField(blank=True, null=True)
    estado = models.IntegerField('Estado', choices=ESTADO_DOCUMENTO, default=1)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='DocumentoReclamo_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='DocumentoReclamo_updated_by', editable=False)
    
    class Meta:
        verbose_name = 'Documento de Reclamo'
        verbose_name_plural = 'Documentos de Reclamos'

    def __str__(self):
        return f"{self.recepcion_compra}"


class DocumentoReclamoDetalle(models.Model):
    documento_reclamo = models.ForeignKey(DocumentoReclamo, on_delete=models.CASCADE)
    item = models.IntegerField()
    content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT) #Material
    id_registro = models.IntegerField()
    cantidad = models.DecimalField('Cantidad', max_digits=22, decimal_places=10, blank=True, null=True)
    precio_unitario_sin_igv = models.DecimalField('Precio unitario sin igv', max_digits=22, decimal_places=10,default=Decimal('0.00'))
    precio_unitario_con_igv = models.DecimalField('Precio unitario con igv', max_digits=22, decimal_places=10,default=Decimal('0.00'))
    precio_final_con_igv = models.DecimalField('Precio final con igv', max_digits=22, decimal_places=10,default=Decimal('0.00'))
    descuento = models.DecimalField('Descuento', max_digits=14, decimal_places=2,default=Decimal('0.00'))
    sub_total = models.DecimalField('Sub Total', max_digits=14, decimal_places=2,default=Decimal('0.00'))
    igv = models.DecimalField('IGV', max_digits=14, decimal_places=2,default=Decimal('0.00'))
    total = models.DecimalField('Total', max_digits=14, decimal_places=2,default=Decimal('0.00'))
    tipo_igv = models.IntegerField('Tipo de IGV', choices=TIPO_IGV_CHOICES, null=True)
    
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='DocumentoReclamoDetalle_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='DocumentoReclamoDetalle_updated_by', editable=False)
    
    class Meta:
        verbose_name = 'Documento de Reclamo Detalle'
        verbose_name_plural = 'Documentos de Reclamo Detalles'

    @property
    def producto(self):
        return self.content_type.get_object_for_this_type(id = self.id_registro)


    def __str__(self):
        return f"{self.item} - {self.producto}"

