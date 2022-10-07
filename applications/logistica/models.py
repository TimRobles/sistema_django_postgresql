from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from applications.clientes.models import Cliente, ClienteInterlocutor
from applications.sociedad.models import Sociedad
from applications.cotizacion.models import ConfirmacionVenta, ConfirmacionVentaDetalle
from applications.variables import ESTADOS
from applications.almacenes.models import Almacen
from applications.sede.models import Sede

class SolicitudPrestamoMateriales(models.Model):
    ESTADOS_PRESTAMO = (
        (1, 'EN PROCESO'),
        (2, 'FINALIZADO SIN CONFIRMAR'),
        (3, 'CONFIRMADO'),
        (4, 'ANULADO'),
        (5, 'CONCLUIDO'),
    )
    numero_prestamo = models.CharField('Número Prestamo', max_length=50, blank=True, null=True)
    sociedad = models.ForeignKey(Sociedad, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    cliente_interlocutor = models.ForeignKey(ClienteInterlocutor, on_delete=models.CASCADE)
    fecha_prestamo = models.DateField('Fecha Prestamo', auto_now=False, auto_now_add=False)
    comentario = models.TextField(blank=True, null=True)
    motivo_anulacion = models.TextField('Motivo Anulación', blank=True, null=True)
    estado = models.IntegerField(choices=ESTADOS_PRESTAMO, default=1)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='SolicitudPrestamoMateriales_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='SolicitudPrestamoMateriales_updated_by', editable=False)

    class Meta:

        verbose_name = 'Solicitud Prestamo Materiales'
        verbose_name_plural = 'Solicitudes Prestamo Materiales'
        ordering = ['numero_prestamo',]

    def __str__(self):
        return str(self.numero_prestamo)

class SolicitudPrestamoMaterialesDetalle(models.Model):
    item = models.IntegerField(blank=True, null=True)
    content_type = models.ForeignKey(ContentType, blank=True, null=True, on_delete=models.PROTECT)
    id_registro = models.IntegerField(blank=True, null=True)
    cantidad_prestamo = models.DecimalField('Cantidad Prestamo', max_digits=22, decimal_places=10, default=0)
    observacion = models.TextField(blank=True, null=True)
    solicitud_prestamo_materiales = models.ForeignKey(SolicitudPrestamoMateriales, blank=True, null=True, on_delete=models.CASCADE, related_name='SolicitudPrestamoMaterialesDetalle_solicitud_prestamo_materiales')

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='SolicitudPrestamoMaterialesDetalle_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='SolicitudPrestamoMaterialesDetalle_updated_by', editable=False)

    class Meta:

        verbose_name = 'Solicitud Prestamo Materiales Detalle'
        verbose_name_plural = 'Solicitudes Prestamo Materiales Detalle'
        ordering = ['item',]

    def __str__(self):
        return str(self.item)

class DocumentoPrestamoMateriales(models.Model):
    comentario = models.TextField(blank=True, null=True)
    documento = models.FileField('Documento', blank=True, null=True)
    solicitud_prestamo_materiales = models.ForeignKey(SolicitudPrestamoMateriales, blank=True, null=True, on_delete=models.CASCADE)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='DocumentoPrestamoMateriales_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='DocumentoPrestamoMateriales_updated_by', editable=False)

    class Meta:

        verbose_name = 'Documento Prestamo Materiales'
        verbose_name_plural = 'Documentos Prestamo Materiales'

    def __str__(self):
        return str(self.documento)

class NotaSalida(models.Model):
    confirmacion_venta = models.ForeignKey(ConfirmacionVenta, on_delete=models.PROTECT)
    solicitud_prestamo_materiales = models.ForeignKey(SolicitudPrestamoMateriales, on_delete=models.PROTECT)
    numero_salida = models.CharField('Número Salida', max_length=50)
    observacion_adicional = models.TextField('Observación Adicional', blank=True, null=True)
    motivo_anulacion = models.TextField('Motivo Anulación', blank=True, null=True)
    estado = models.IntegerField(choices=ESTADOS, default=1)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='NotaSalida_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='NotaSalida_updated_by', editable=False)
    
    class Meta:

        verbose_name = 'Nota de Salida'
        verbose_name_plural = 'Notas de Salida'
        ordering = ['numero_salida',]

    def __str__(self):
        return str(self.numero_salida)

class NotaSalidaDetalle(models.Model):
    item = models.IntegerField(blank=True, null=True)
    confirmacion_venta_detalle = models.ForeignKey(ConfirmacionVentaDetalle, verbose_name='Confirmación Venta Detalle', on_delete=models.PROTECT)
    sede = models.ForeignKey(Sede, on_delete=models.CASCADE, blank=True, null=True)
    almacen = models.ForeignKey(Almacen, on_delete=models.CASCADE)
    cantidad_salida = models.DecimalField('Cantidad Salida', max_digits=22, decimal_places=10, default=0)
    nota_salida = models.ForeignKey(NotaSalida, on_delete=models.CASCADE)
    estado = models.IntegerField(choices=ESTADOS, default=1)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='NotaSalidaDetalle_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='NotaSalidaDetalle_updated_by', editable=False)
    
    class Meta:

        verbose_name = 'Nota de Salida Detalle'
        verbose_name_plural = 'Notas de Salida Detalle' 
        ordering = ['item',]

    def __str__(self):
        return str(self.item)

class Despacho(models.Model):
    sociedad = models.ForeignKey(Sociedad, on_delete=models.CASCADE,blank=True, null=True)
    nota_salida = models.ForeignKey(NotaSalida, on_delete=models.CASCADE,blank=True, null=True)
    numero_despacho = models.CharField('Número Despacho', max_length=50, blank=True, null=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE,blank=True, null=True)
    fecha_despacho = models.DateField('Fecha Despacho', auto_now=False, auto_now_add=False, blank=True, null=True)
    observacion = models.TextField(blank=True, null=True)
    motivo_anulacion = models.TextField('Motivo Anulación', blank=True, null=True)
    estado = models.IntegerField(choices=ESTADOS, default=1)
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='Despacho_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='Despacho_updated_by', editable=False)

    class Meta:

        verbose_name = 'Despacho'
        verbose_name_plural = 'Despachos'
        ordering = ['numero_despacho',]

    def __str__(self):
        return str(self.numero_despacho)

class DespachoDetalle(models.Model):
    item = models.IntegerField(blank=True, null=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT, blank=True, null=True)
    id_registro = models.IntegerField(blank=True, null=True)   
    cantidad_despachada = models.DecimalField('Cantidad Despachada', max_digits=22, decimal_places=10, default=0)
    despacho = models.ForeignKey(Despacho, on_delete=models.CASCADE, related_name='DespachoDetalle_despacho')
    estado = models.IntegerField(choices=ESTADOS, default=1)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='DespachoDetalle_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='DespachoDetalle_updated_by', editable=False)

    class Meta:

        verbose_name = 'Despacho Detalle'
        verbose_name_plural = 'Despachos Detalle'
        ordering = ['item',]

    def __str__(self):
        return str(self.item)