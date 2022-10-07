from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from applications.clientes.models import Cliente, InterlocutorCliente
from applications.sociedad.models import Sociedad
from applications.cotizacion.models import ConfirmacionVenta, ConfirmacionVentaDetalle
from applications.variables import ESTADOS
from applications.almacenes.models import Almacen
from applications.sede.models import Sede

class SolicitudPrestamoMateriales(models.Model):
    ESTADOS_PRESTAMO_MATERIALES = (
        (1, 'EN PROCESO'),
        (2, 'FINALIZADO SIN CONFIRMAR'),
        (3, 'CONFIRMADO'),
        (4, 'ANULADO'),
        (5, 'CONCLUIDO'),
    )
    numero_prestamo = models.IntegerField('Número Prestamo', blank=True, null=True)
    sociedad = models.ForeignKey(Sociedad, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    interlocutor_cliente = models.ForeignKey(InterlocutorCliente, on_delete=models.PROTECT,blank=True, null=True)
    fecha_prestamo = models.DateField('Fecha Prestamo', auto_now=False, auto_now_add=False)
    comentario = models.TextField(blank=True, null=True)
    motivo_anulacion = models.TextField('Motivo Anulación', blank=True, null=True)
    estado = models.IntegerField(choices=ESTADOS_PRESTAMO_MATERIALES, default=1)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='SolicitudPrestamoMateriales_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='SolicitudPrestamoMateriales_updated_by', editable=False)

    class Meta:

        verbose_name = 'Solicitud Prestamo Materiales'
        verbose_name_plural = 'Solicitudes Prestamo Materiales'
        ordering = ['numero_prestamo',]

    def __str__(self):
        return "%s - %s" % (self.numero_prestamo, self.cliente)

class SolicitudPrestamoMaterialesDetalle(models.Model):
    item = models.IntegerField(blank=True, null=True)
    content_type = models.ForeignKey(ContentType, blank=True, null=True, on_delete=models.CASCADE)
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
    ESTADOS_NOTA_SALIDA = (
        (1, 'EN PROCESO'),
        (2, 'ATENDIDO'),
        (3, 'ANULADO'),
    )

    confirmacion_venta = models.ForeignKey(ConfirmacionVenta, on_delete=models.PROTECT, blank=True, null=True)
    solicitud_prestamo_materiales = models.ForeignKey(SolicitudPrestamoMateriales, on_delete=models.CASCADE)
    numero_salida = models.IntegerField('Número Salida', blank=True, null=True)
    observacion_adicional = models.TextField('Observación Adicional', blank=True, null=True)
    motivo_anulacion = models.TextField('Motivo Anulación', blank=True, null=True)
    estado = models.IntegerField(choices=ESTADOS_NOTA_SALIDA, default=1)

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
    confirmacion_venta_detalle = models.ForeignKey(ConfirmacionVentaDetalle, on_delete=models.PROTECT, blank=True, null=True)
    solicitud_prestamo_materiales_detalle = models.ForeignKey(SolicitudPrestamoMaterialesDetalle, on_delete=models.CASCADE)
    sede = models.ForeignKey(Sede, on_delete=models.CASCADE, blank=True, null=True)
    almacen = models.ForeignKey(Almacen, on_delete=models.CASCADE, blank=True, null=True)
    cantidad_salida = models.DecimalField('Cantidad Salida', max_digits=22, decimal_places=10, default=0, blank=True, null=True)
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
    ESTADOS_DESPACHO = (
        (1, 'EN PROCESO'),
        (2, 'DESPACHADO'),
        (3, 'ANULADO'),
        (4, 'CONCLUIDO SIN GUIA'),
        (5, 'CONCLUIDO CON GUIA'),
    )

    sociedad = models.ForeignKey(Sociedad, on_delete=models.CASCADE)
    confirmacion_venta = models.ForeignKey(ConfirmacionVenta, on_delete=models.CASCADE)
    numero_despacho = models.IntegerField('Número Despacho', blank=True, null=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    observacion = models.TextField(blank=True, null=True)
    motivo_anulacion = models.TextField('Motivo Anulación', blank=True, null=True)
    estado = models.IntegerField(choices=ESTADOS_DESPACHO, default=1)

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
    confirmacion_venta_detalle = models.ForeignKey(ConfirmacionVentaDetalle, on_delete=models.CASCADE)
    cantidad_despachada = models.DecimalField('Cantidad Despachada', max_digits=22, decimal_places=10, default=0)
    despacho = models.ForeignKey(Despacho, on_delete=models.CASCADE)
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