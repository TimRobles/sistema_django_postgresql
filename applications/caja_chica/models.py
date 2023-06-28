from decimal import Decimal
from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType

from applications.datos_globales.models import Moneda, Unidad
from applications.sociedad.models import Sociedad
from applications.contabilidad.models import Cheque
from applications.rutas import REQUERIMIENTO_FOTO_PRODUCTO, REQUERIMIENTO_VOUCHER

from datetime import datetime
from django.core.validators import MaxValueValidator, MinValueValidator
from applications.variables import MESES, TIPO_PRESTAMO, ESTADO_PRESTAMO_CAJA_CHICA, ESTADO_CAJA_CHICA, ESTADO_RECIBO_CAJA_CHICA
from applications.caja_chica import funciones
from django.db.models.signals import pre_save, post_save, pre_delete, post_delete

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
    dato_rechazado = models.CharField('Detalle del rechazo', max_length=300, blank=True, null=True)
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
        ordering = [
            'estado',
            '-fecha',
            'created_at',
            ]

    @property
    def vouchers(self):
        for documento in self.RequerimientoDocumento_requerimiento.all():
            if documento.voucher:
                return True
        return False

    @property
    def vuelto_extra(self):
        if self.RequerimientoVueltoExtra_requerimiento.all():
            return self.RequerimientoVueltoExtra_requerimiento.all().aggregate(models.Sum('vuelto_extra'))['vuelto_extra__sum']
        return Decimal('0.00')

    @property
    def utilizado(self):
        if self.RequerimientoDocumento_requerimiento.all():
            return self.RequerimientoDocumento_requerimiento.all().aggregate(models.Sum('total_requerimiento'))['total_requerimiento__sum']
        return Decimal('0.00')

    @property
    def caja_cheque(self):
        return self.content_type.get_object_for_this_type(id=self.id_registro)

    def __str__(self):
        if self.concepto_final:
            return self.concepto_final + '-' + self.get_estado_display()
        else:
            return self.concepto + '-' + self.get_estado_display()


post_save.connect(funciones.cheque_monto_usado_post_save, sender=Requerimiento)


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
    numero = models.CharField('Número de Documento', max_length=50, blank=True, null=True)
    establecimiento = models.CharField('Establecimiento', max_length=50, blank=True, null=True)
    moneda = models.ForeignKey(Moneda, on_delete=models.PROTECT)
    total_documento = models.DecimalField('Total en Documento', max_digits=7, decimal_places=2)
    tipo_cambio = models.DecimalField('Tipo de Cambio', max_digits=5, decimal_places=4)
    total_requerimiento = models.DecimalField('Total en Requerimiento', max_digits=7, decimal_places=2)
    voucher = models.FileField('Documento', upload_to=REQUERIMIENTO_VOUCHER, max_length=100, blank=True, null=True)
    sociedad = models.ForeignKey(Sociedad, on_delete=models.PROTECT, blank=True, null=True)
    requerimiento = models.ForeignKey(Requerimiento, on_delete=models.CASCADE, related_name='RequerimientoDocumento_requerimiento')

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

    @property
    def total(self):
        return self.cantidad * self.precio_unitario

    def __str__(self):
        texto = []
        texto.append(str(self.item))
        texto.append(self.producto)
        texto.append(str(self.documento_requerimiento.id))
        return " ".join(texto)


class CajaChica(models.Model):
    saldo_inicial = models.DecimalField('Saldo Inicial', max_digits=7, decimal_places=2)
    moneda = models.ForeignKey(Moneda, on_delete=models.PROTECT)
    saldo_inicial_caja_chica = models.OneToOneField('self', on_delete=models.PROTECT, null=True)
    month = models.IntegerField('Mes',choices=MESES, blank=True, null=True)
    year = models.IntegerField('Año', validators=[MinValueValidator(2015),MaxValueValidator(datetime.now().year)], default=datetime.now().year ,blank=True, null=True)
    ingresos = models.DecimalField('Ingresos', max_digits=7, decimal_places=2, default=0)
    egresos = models.DecimalField('Egresos', max_digits=7, decimal_places=2, default=0)
    saldo_final = models.DecimalField('Saldo Inicial', max_digits=7, decimal_places=2, default=0)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Usuario', on_delete=models.PROTECT, related_name='CajaChica_usuario')
    estado = models.IntegerField(choices=ESTADO_CAJA_CHICA, default=1)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='CajaChica_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='CajaChica_updated_by', editable=False)
    

    class Meta:
        verbose_name = 'Caja Chica'
        verbose_name_plural = 'Cajas Chicas'
        ordering = [
            'estado',
            '-year',
            '-month',
        ]

    @property
    def cantidad_requerimientos(self):
        return len(Requerimiento.objects.filter(content_type=ContentType.objects.get_for_model(self), id_registro=self.id))

    @property
    def periodo(self):
        return f"{self.get_month_display()} {self.year}"

    def __str__(self):
        return "CAJA CHICA %s %s - %s - %s" % (self.get_month_display(), self.year, self.get_estado_display(), self.usuario.username ) 

class CajaChicaSalida(models.Model):
    concepto = models.CharField('Concepto Salida', max_length=50, null=True)
    fecha = models.DateField('Fecha', auto_now=False, auto_now_add=False)
    monto = models.DecimalField('Monto', max_digits=7, decimal_places=2)
    caja_chica = models.ForeignKey(CajaChica, on_delete=models.PROTECT, null=True)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Usuario', on_delete=models.PROTECT, related_name='CajaChicaSalida_usuario')

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='CajaChicaSalida_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='CajaChicaSalida_updated_by', editable=False)
    
    class Meta:
        verbose_name = 'Caja Chica Salida'
        verbose_name_plural = 'Caja Chica Salidas'

    def __str__(self):
        return str(self.id)

class CajaChicaPrestamo(models.Model):
    fecha = models.DateField('Fecha', auto_now=False, auto_now_add=False)
    caja_origen = models.ForeignKey(CajaChica, on_delete=models.PROTECT, related_name='CajaChicaPrestamo_caja_origen')
    caja_destino = models.ForeignKey(CajaChica, on_delete=models.PROTECT, related_name='CajaChicaPrestamo_caja_destino')
    monto = models.DecimalField('Monto', max_digits=7, decimal_places=2)
    tipo = models.IntegerField(choices=TIPO_PRESTAMO, default=1)    
    devolucion = models.OneToOneField('self', on_delete=models.PROTECT, null=True)
    estado = models.IntegerField(choices=ESTADO_PRESTAMO_CAJA_CHICA, default=1)    

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='CajaChicaPrestamo_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='CajaChicaPrestamo_updated_by', editable=False)
    
    class Meta:
        verbose_name = 'Caja Chica Prestamo'
        verbose_name_plural = 'Caja Chica Prestamos'

    def __str__(self):
        return str(self.id)

class ReciboCajaChica(models.Model):
    concepto = models.CharField('Concepto', max_length=50, null=True)
    fecha = models.DateField('Fecha', auto_now=False, auto_now_add=False)
    monto = models.DecimalField('Monto', max_digits=7, decimal_places=2)
    moneda = models.ForeignKey(Moneda, on_delete=models.PROTECT)
    redondeo = models.DecimalField('Redondeo', max_digits=3, decimal_places=2, default=0)
    monto_pagado = models.DecimalField('Monto pagado', max_digits=7, decimal_places=2, default=0)
    fecha_pago = models.DateField('Fecha de pago', auto_now=False, auto_now_add=False,blank=True, null=True)
    cheque = models.ForeignKey(Cheque, on_delete=models.PROTECT, null=True)
    caja_chica = models.ForeignKey(CajaChica, on_delete=models.PROTECT, null=True)
    estado = models.IntegerField(choices=ESTADO_RECIBO_CAJA_CHICA, default=1)    

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='ReciboCajaChica_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='ReciboCajaChica_updated_by', editable=False)
    
    class Meta:
        verbose_name = 'Recibo Caja Chica'
        verbose_name_plural = 'Recibos Caja Chica'
        ordering = [
            'estado',
            '-fecha',
        ]

    def __str__(self):
        return f"{self.concepto} - {self.caja_chica} - {self.fecha}"

post_save.connect(funciones.cheque_monto_usado_post_save, sender=ReciboCajaChica)