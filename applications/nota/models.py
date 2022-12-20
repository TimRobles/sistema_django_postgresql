from django.db import models
from decimal import Decimal
from applications.clientes.models import Cliente, InterlocutorCliente
from applications.funciones import obtener_totales
from applications.sociedad.models import Sociedad
from applications.datos_globales.models import DocumentoFisico, Moneda, SeriesComprobante, TipoCambio, Unidad
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.db.models.signals import pre_save, post_save, pre_delete, post_delete

from applications.variables import ESTADOS_DOCUMENTO, TIPO_COMPROBANTE, TIPO_IGV_CHOICES, TIPO_ISC_CHOICES, TIPO_NOTA_CREDITO, TIPO_PERCEPCION, TIPO_RETENCION, TIPO_VENTA

# Create your models here.
class NotaCredito(models.Model):
    tipo_comprobante = models.IntegerField('Tipo de Comprobante', choices=TIPO_COMPROBANTE, default=3)
    sociedad = models.ForeignKey(Sociedad, on_delete=models.PROTECT)
    serie_comprobante = models.ForeignKey(SeriesComprobante, on_delete=models.PROTECT, blank=True, null=True)
    numero_nota = models.IntegerField('Nro. Nota', blank=True, null=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name='NotaCredito_cliente', blank=True, null=True)
    cliente_interlocutor = models.ForeignKey(InterlocutorCliente, on_delete=models.PROTECT, related_name='NotaCredito_interlocutor', blank=True, null=True)
    fecha_emision = models.DateField('Fecha Emisión', auto_now=False, auto_now_add=False, blank=True, null=True)
    fecha_vencimiento = models.DateField('Fecha Vencimiento', auto_now=False, auto_now_add=False, blank=True, null=True)
    moneda = models.ForeignKey(Moneda, on_delete=models.PROTECT, default=1)
    tipo_cambio = models.ForeignKey(TipoCambio, on_delete=models.PROTECT, related_name='NotaCredito_tipo_cambio')
    tipo_venta = models.IntegerField('Tipo de Venta', choices=TIPO_VENTA, default=1)
    condiciones_pago = models.CharField('Condiciones de Pago', max_length=250, blank=True, null=True, help_text='Factura a 30 días')
    descuento_global = models.DecimalField('Descuento Global', max_digits=14, decimal_places=2, default=Decimal('0.00'))
    total_descuento = models.DecimalField('Total Descuento', max_digits=14, decimal_places=2, default=Decimal('0.00'))
    total_anticipo = models.DecimalField('Total Anticipo', max_digits=14, decimal_places=2, default=Decimal('0.00'))
    total_gravada = models.DecimalField('Total Gravada', max_digits=14, decimal_places=2, default=Decimal('0.00'))
    total_inafecta = models.DecimalField('Total Inafecta', max_digits=14, decimal_places=2, default=Decimal('0.00'))
    total_exonerada = models.DecimalField('Total Exonerada', max_digits=14, decimal_places=2, default=Decimal('0.00'))
    total_igv = models.DecimalField('Total IGV', max_digits=14, decimal_places=2, default=Decimal('0.00'))
    total_gratuita = models.DecimalField('Total Gratuita', max_digits=14, decimal_places=2, default=Decimal('0.00'))
    total_otros_cargos = models.DecimalField('Total Otros Cargos', max_digits=14, decimal_places=2, default=Decimal('0.00'))
    total = models.DecimalField('Total', max_digits=14, decimal_places=2, default=Decimal('0.00'))
    percepcion_tipo = models.IntegerField(choices=TIPO_PERCEPCION, blank=True, null=True)
    percepcion_base_imponible = models.DecimalField('Percepcion Base Imponible', max_digits=14, decimal_places=2, default=Decimal('0.00'), blank=True, null=True)
    total_percepcion = models.DecimalField('Total Percepcion', max_digits=14, decimal_places=2, default=Decimal('0.00'), blank=True, null=True)
    total_incluido_percepcion = models.DecimalField('Total Incluido Percepcion', max_digits=14, decimal_places=2, default=Decimal('0.00'), blank=True, null=True)
    total_impuestos_bolsas = models.DecimalField('Total Impuestos Bolsas', max_digits=14, decimal_places=2, default=Decimal('0.00'), blank=True, null=True)
    detraccion = models.BooleanField(default=False)
    retencion_tipo = models.IntegerField(choices=TIPO_RETENCION, blank=True, null=True)
    retencion_base_imponible = models.DecimalField('Retencion Base Imponible', max_digits=14, decimal_places=2, default=Decimal('0.00'), blank=True, null=True)
    total_retencion = models.DecimalField('Total Retencion', max_digits=14, decimal_places=2, default=Decimal('0.00'), blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True, max_length=1000)
    tipo_nota_credito = models.IntegerField(choices=TIPO_NOTA_CREDITO, blank=True, null=True)
    estado = models.IntegerField(choices = ESTADOS_DOCUMENTO, default=1)
    motivo_anulacion = models.CharField('Motivo de Anulación', max_length=100, blank=True, null=True)
    content_type_documento = models.ForeignKey(DocumentoFisico, on_delete=models.PROTECT, related_name='NotaCredito_content_type_documento', blank=True, null=True) #Factura / Boleta
    id_registro_documento = models.IntegerField(blank=True, null=True)
    content_type_reclamo = models.ForeignKey(ContentType, on_delete=models.PROTECT, related_name='NotaCredito_content_type_reclamo', blank=True, null=True) #NotaCalidadReclamo / NotaAdministrativaReclamo
    id_registro_reclamo = models.IntegerField(blank=True, null=True)
    nubefact = models.URLField(max_length=400, blank=True, null=True)
    slug = models.SlugField(blank=True, null=True)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='NotaCredito_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='NotaCredito_updated_by', editable=False)

    class Meta:
        """Meta definition for NotaCredito."""

        verbose_name = 'Nota de Credito'
        verbose_name_plural = 'Notas de Credito'

    @property
    def documento(self):
        if self.content_type_documento and self.id_registro_documento:
            return self.content_type_documento.modelo.get_object_for_this_type(id=self.id_registro_documento)
        return None

    def __str__(self):
        if self.numero_nota:
            return "%s %s-%s %s %s %s" % (self.get_tipo_comprobante_display(), self.serie_comprobante, self.numero_nota, self.cliente, self.moneda.simbolo, self.total)
        else:
            return "%s %s %s %s %s" % (self.get_tipo_comprobante_display(), self.serie_comprobante, self.cliente, self.moneda.simbolo, self.total)


class NotaCreditoDetalle(models.Model):
    item = models.IntegerField()
    content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT, blank=True, null=True)
    id_registro = models.IntegerField(blank=True, null=True)
    unidad = models.ForeignKey(Unidad, on_delete=models.CASCADE, blank=True, null=True)
    codigo_interno = models.CharField('Código Interno', max_length=250, blank=True, null=True)
    descripcion_documento = models.CharField('Descripción', max_length=250)
    cantidad = models.DecimalField('Cantidad', max_digits=22, decimal_places=10)
    precio_unitario_sin_igv = models.DecimalField('Precio unitario sin IGV',max_digits=22, decimal_places=10, default=Decimal('0.00'))
    precio_unitario_con_igv = models.DecimalField('Precio unitario con IGV',max_digits=22, decimal_places=10, default=Decimal('0.00'))
    precio_final_con_igv = models.DecimalField('Precio final con IGV',max_digits=22, decimal_places=10, default=Decimal('0.00'))
    descuento = models.DecimalField('Descuento',max_digits=22, decimal_places=10, default=Decimal('0.00'))
    sub_total = models.DecimalField('Sub Total',max_digits=14, decimal_places=2, default=Decimal('0.00'))
    tipo_igv = models.IntegerField('Tipo IGV',choices=TIPO_IGV_CHOICES, default=1)
    igv = models.DecimalField('IGV', max_digits=14, decimal_places=2, default=Decimal('0.00'))
    total = models.DecimalField('Total', max_digits=14, decimal_places=2, default=Decimal('0.00'))
    anticipo_regularizacion = models.BooleanField(default=False)
    anticipo_documento_serie = models.ForeignKey(SeriesComprobante, on_delete=models.PROTECT, blank=True, null=True)
    anticipo_documento_numero = models.IntegerField(blank=True, null=True)
    codigo_producto_sunat = models.CharField(max_length=8, blank=True)
    tipo_de_isc = models.IntegerField(choices=TIPO_ISC_CHOICES, blank=True, null=True)
    isc = models.DecimalField('ISC', max_digits=14, decimal_places=2, blank=True, null=True)
    nota_credito = models.ForeignKey(NotaCredito, on_delete=models.CASCADE, related_name='NotaCreditoDetalle_nota_credito')
    
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='NotaCreditoDetalle_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='NotaCreditoDetalle_updated_by', editable=False)

    class Meta:
        verbose_name = 'Nota de Crédito Detalle'
        verbose_name_plural = 'Notas de Crédito Detalle'
        ordering = [
            'nota_credito',
            'item',
            ]

    @property
    def moneda(self):
        return self.nota_credito.moneda
    
    @property
    def documento(self):
        return f'NOTA DE CRÉDITO {self.nota_credito.documento}'
    
    @property
    def fecha(self):
        return self.nota_credito.fecha_emision

    @property
    def cliente(self):
        return self.nota_credito.cliente

    @property
    def producto(self):
        return self.content_type.get_object_for_this_type(id = self.id_registro)

    def __str__(self):
        return str(self.id)


def nota_credito_detalle_post_save(*args, **kwargs):
    obj = kwargs['instance']
    respuesta = obtener_totales(obj.nota_credito)
    obj.nota_credito.total_descuento = respuesta['total_descuento']
    obj.nota_credito.total_anticipo = respuesta['total_anticipo']
    obj.nota_credito.total_gravada = respuesta['total_gravada']
    obj.nota_credito.total_inafecta = respuesta['total_inafecta']
    obj.nota_credito.total_exonerada = respuesta['total_exonerada']
    obj.nota_credito.total_igv = respuesta['total_igv']
    obj.nota_credito.total_gratuita = respuesta['total_gratuita']
    obj.nota_credito.otros_cargos = respuesta['total_otros_cargos']
    obj.nota_credito.total = respuesta['total']
    obj.nota_credito.save()

post_save.connect(nota_credito_detalle_post_save, sender=NotaCreditoDetalle)


class NotaDebito(models.Model):
    """Model definition for NotaDebito."""

    # TODO: Define fields here

    class Meta:
        """Meta definition for NotaDebito."""

        verbose_name = 'NotaDebito'
        verbose_name_plural = 'NotaDebitos'

    def __str__(self):
        """Unicode representation of NotaDebito."""
        pass
