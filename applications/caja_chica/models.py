from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType

from applications.datos_globales.models import Moneda, Unidad
from applications.sociedad.models import Sociedad
from applications.rutas import REQUERIMIENTO_FOTO_PRODUCTO, REQUERIMIENTO_VOUCHER

class Requerimiento(models.Model):
    ESTADO_CHOICES = (
        (1, 'BORRADOR'),
        (2, 'SOLICITADO'),
        (3, 'APROBADO'),
        (4, 'RECHAZADO'),
        (5, 'REVISAR RENDICIÓN'),
        (6, 'RENDICIÓN RECHAZADA'),
        (7, 'FINALIZADO'),
    )

    fecha = models.DateField('Fecha',)
    monto = models.DecimalField('Monto', max_digits=7, decimal_places=2)
    moneda = models.ForeignKey(Moneda, on_delete=models.PROTECT)
    tipo_cambio = models.DecimalField('Tipo de Cambio', max_digits=5, decimal_places=4, default=1)
    concepto = models.CharField('Concepto Inicial', max_length=255)
    motivo_rechazo = models.CharField('Motivo de Rechazo', max_length=50, blank=True, null=True)
    dato_rechazado = models.CharField('Dato Rechazado', max_length=300, blank=True, null=True)
    monto_final = models.DecimalField('Monto Final', max_digits=7, decimal_places=2, default=0)
    concepto_final = models.CharField('Concepto Final', max_length=255, blank=True, null=True)
    fecha_entrega = models.DateField('Fecha de Entrega', null=True)
    monto_usado = models.DecimalField('Monto Usado', max_digits=7, decimal_places=2, default=0)
    redondeo = models.DecimalField('Redondeo', max_digits=7, decimal_places=2, default=0)
    vuelto = models.DecimalField('Vuelto', max_digits=7, decimal_places=2, default=0)
    rechazo_rendicion = models.CharField('Rechazo de Rendición', max_length=50, blank=True, null=True)
    content_type = models.ForeignKey(ContentType, blank=True, null=True, on_delete=models.PROTECT) #Documento de pago (Cheque / Caja Chica)
    id_registro = models.IntegerField(blank=True, null=True)
    usuario_pedido = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Pedir a', on_delete=models.PROTECT, related_name='requerimiento_usuario_pedido', blank=True, null=True)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='requerimiento_usuario') #Usuario que realiza el pedido
    estado = models.IntegerField('Estado', choices=ESTADO_CHOICES, default=1)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='Requerimiento_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='Requerimiento_updated_by', editable=False)

    class Meta:
        verbose_name = 'Requerimiento'
        verbose_name_plural = 'Requerimientos'
        ordering = ['estado', 'fecha', 'created_at' ]

    def __str__(self):
        if self.concepto_final:
            return self.concepto_final + '-' + self.get_estado_display()
        else:
            return self.concepto + '-' + self.get_estado_display()


class RequerimientoVueltoExtra(models.Model):
    vuelto_original = models.DecimalField('Vuelto en Efectivo', max_digits=7, decimal_places=2)
    vuelto_extra = models.DecimalField('Vuelto en Moneda del Requerimiento', max_digits=7, decimal_places=2)
    moneda = models.ForeignKey(Moneda, on_delete=models.PROTECT)
    tipo_cambio = models.DecimalField('Tipo de Cambio', max_digits=6, decimal_places=4)
    requerimiento = models.ForeignKey(Requerimiento, on_delete=models.CASCADE, related_name='RequerimientoVueltoExtra_requerimiento')

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='RequerimientoVueltoExtra_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='RequerimientoVueltoExtra_updated_by', editable=False)

    class Meta:
        verbose_name = 'Requerimiento Vuelto Extra'
        verbose_name_plural = 'Requerimiento Vueltos Extras'

    def __str__(self):
        return str(self.requerimiento) + " " + self.moneda.simbolo + " " + str(self.vuelto_extra)


class RequerimientoDocumento(models.Model):
    TIPO_CHOICES = (
        (1, 'FACTURA'),
        (2, 'BOLETA'),
        (3, 'SIN DOCUMENTO'),
    )

    fecha = models.DateField('Fecha', auto_now=False, auto_now_add=False)
    tipo = models.IntegerField('Tipo de Documento', choices=TIPO_CHOICES)
    numero = models.CharField('Número de Documento', max_length=50)
    establecimiento = models.CharField('Establecimiento', max_length=50, blank=True, null=True)
    moneda = models.ForeignKey(Moneda, on_delete=models.PROTECT)
    total_documento = models.DecimalField('Total en Documento', max_digits=7, decimal_places=2)
    tipo_cambio = models.DecimalField('Tipo de Cambio', max_digits=5, decimal_places=4)
    total_requerimiento = models.DecimalField('Total en Requerimiento', max_digits=7, decimal_places=2)
    voucher = models.FileField('Documento', upload_to=REQUERIMIENTO_VOUCHER, max_length=100, blank=True, null=True)
    sociedad = models.ForeignKey(Sociedad, on_delete=models.PROTECT)
    requerimiento = models.ForeignKey(Requerimiento, on_delete=models.CASCADE)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='RequerimientoDocumento_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='RequerimientoDocumento_updated_by', editable=False)
    
    class Meta:
        verbose_name = 'Documento Requerimiento'
        verbose_name_plural = 'Documentos Requerimientos'
        ordering = ['tipo', 'fecha', 'establecimiento',]

    def __str__(self):
        return self.get_tipo_display() + ' ' + str(self.numero) + ' ' + str(self.establecimiento) + ' ' + self.moneda.simbolo + ' ' + str(self.total_documento)


class RequerimientoDocumentoDetalle(models.Model):
    item = models.IntegerField('Item')
    producto = models.CharField('Producto', max_length=120)
    cantidad = models.DecimalField('Cantidad', max_digits=5, decimal_places=2)
    unidad = models.ForeignKey(Unidad, on_delete=models.PROTECT)
    precio_unitario = models.DecimalField('Precio Unitario', max_digits=5, decimal_places=2)
    foto = models.ImageField('Foto de Producto', upload_to=REQUERIMIENTO_FOTO_PRODUCTO, height_field=None, width_field=None, max_length=None, blank=True, null = True)
    documento_requerimiento = models.ForeignKey(RequerimientoDocumento, on_delete=models.CASCADE, related_name='RequerimientoDocumentoDetalle_documento_requerimiento')

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='RequerimientoDocumentoDetalle_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='RequerimientoDocumentoDetalle_updated_by', editable=False)
    
    class Meta:
        verbose_name = 'Documento Requerimiento Detalle'
        verbose_name_plural = 'Documento Requerimiento Detalles'
        ordering = ['item',]

    def __str__(self):
        texto = []
        texto.append(str(self.item))
        texto.append(self.producto)
        texto.append(str(self.documento_requerimiento.id))
        return " ".join(texto)
