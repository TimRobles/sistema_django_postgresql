from decimal import Decimal
from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from applications import datos_globales
from applications.almacenes.models import Almacen
from applications.variables import ESTADOS_INGRESO_RECLAMO_GARANTIA
from applications.sociedad.models import Sociedad
from applications.calidad.models import HistorialEstadoSerie, Serie
from applications.clientes.models import Cliente, InterlocutorCliente
from applications.garantia.managers import IngresoReclamoGarantiaManager


class IngresoReclamoGarantia(models.Model):
    nro_ingreso_reclamo_garantia = models.IntegerField('Número de Ingreso Reclamo Garantia', help_text='Correlativo', blank=True, null=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name='IngresoReclamoGarantia_cliente', blank=True, null=True)
    cliente_interlocutor = models.ForeignKey(InterlocutorCliente, on_delete=models.PROTECT, related_name='IngresoReclamoGarantia_interlocutor', blank=True, null=True)
    sociedad = models.ForeignKey(Sociedad, on_delete=models.CASCADE, blank=True, null=True)
    almacen = models.ForeignKey(Almacen, on_delete=models.CASCADE, blank=True, null=True)
    fecha_ingreso = models.DateField('Fecha Ingreso', auto_now=False, auto_now_add=False, blank=True, null=True)
    observacion = models.TextField(blank=True, null=True, max_length=1000)
    encargado = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True)
    estado = models.IntegerField('Estado', choices=ESTADOS_INGRESO_RECLAMO_GARANTIA, default=1)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='IngresoReclamoGarantia_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='IngresoReclamoGarantia_updated_by', editable=False)
    
    objects = IngresoReclamoGarantiaManager()

    class Meta:
        verbose_name = 'Ingreso Reclamo Garantia'
        verbose_name_plural = 'Ingresos Reclamo Garantia'
        ordering = [
            'fecha_ingreso',
            ]

    @property
    def detalles(self):
        return self.IngresoReclamoGarantiaDetalle_ingreso_reclamo_garantia.all()

    def __str__(self):
        return str(self.id)

class IngresoReclamoGarantiaDetalle(models.Model):
    item = models.IntegerField(blank=True, null=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT,blank=True, null=True) #Material
    id_registro = models.IntegerField(blank=True, null=True)
    cantidad = models.DecimalField('Cantidad', max_digits=22, decimal_places=10, default=Decimal('0.00'),blank=True, null=True)
    ingreso_reclamo_garantia = models.ForeignKey(IngresoReclamoGarantia, on_delete=models.CASCADE, related_name='IngresoReclamoGarantiaDetalle_ingreso_reclamo_garantia', blank=True, null=True)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='IngresoReclamoGarantiaDetalle_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='IngresoReclamoGarantiaDetalle_updated_by', editable=False)

    class Meta:
        verbose_name = 'Ingreso Reclamo Garantia Detalle'
        verbose_name_plural = 'Ingresos Reclamo Garantia Detalle'
        ordering = [
            'ingreso_reclamo_garantia',
            'item',
            ]

    @property
    def producto(self):
        return self.content_type.get_object_for_this_type(id = self.id_registro)

    @property
    def series(self):
        return Decimal(len(self.SerieIngresoReclamoGarantiaDetalle_ingreso_reclamo_garantia_detalle.all())).quantize(Decimal('0.01'))
        
    def __str__(self):
        return f"{self.item} - {self.producto}"


class SerieIngresoReclamoGarantiaDetalle(models.Model):
    ingreso_reclamo_garantia_detalle = models.ForeignKey(IngresoReclamoGarantiaDetalle, on_delete=models.CASCADE, related_name='SerieIngresoReclamoGarantiaDetalle_ingreso_reclamo_garantia_detalle')
    serie = models.ForeignKey(Serie, on_delete=models.CASCADE)
    content_type_documento = models.ForeignKey(ContentType, on_delete=models.PROTECT,blank=True, null=True)
    id_registro_documento = models.IntegerField(blank=True, null=True)
    comentario = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='SerieIngresoReclamoGarantiaDetalle_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='SerieIngresoReclamoGarantiaDetalle_updated_by', editable=False)

    class Meta:
        verbose_name = 'Serie Ingreso Reclamo Garantia Detalle'
        verbose_name_plural = 'Serie Ingreso Reclamo Garantia Detalles'
        ordering = [
            'ingreso_reclamo_garantia_detalle',
            '-created_at',
        ]

    @property
    def documento(self):
        return self.content_type_documento.get_object_for_this_type(id = self.id_registro_documento)

    def __str__(self):
        return f"{self.serie} - {self.ingreso_reclamo_garantia_detalle}"


class ControlCalidadReclamoGarantia(models.Model):
    ingreso_reclamo_garantia = models.ForeignKey(IngresoReclamoGarantia, on_delete=models.CASCADE, related_name='ControlCalidadReclamoGarantia_ingreso_reclamo_garantia')
    observacion = models.TextField(blank=True, null=True, max_length=1000)
    estado = models.IntegerField('Estado', choices=ESTADOS_INGRESO_RECLAMO_GARANTIA, default=1)
  
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='ControlCalidadReclamoGarantia_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='ControlCalidadReclamoGarantia_updated_by', editable=False)
    
    class Meta:
        verbose_name = 'Control Calidad Reclamo Garantia'
        verbose_name_plural = 'Control Calidad Reclamos Garantia'

    @property
    def sociedad(self):
        return self.ingreso_reclamo_garantia.sociedad

    @property
    def cliente(self):
        return self.ingreso_reclamo_garantia.cliente

    @property
    def cliente_interlocutor(self):
        return self.ingreso_reclamo_garantia.cliente_interlocutor

    @property
    def nro_calidad_garantia(self):
        return self.ingreso_reclamo_garantia.nro_ingreso_reclamo_garantia

    def __str__(self):
        return str(self.id)


class ControlCalidadReclamoGarantiaDetalle(models.Model):
    TIPO_ANALISIS = (
        (1, 'SOLUCIONADO'),
        (2, 'CAMBIO'),
        (3, 'DEVOLUCIÓN'),
    )

    control_calidad_reclamo_garantia = models.ForeignKey(ControlCalidadReclamoGarantia, on_delete=models.CASCADE)
    serie_ingreso_reclamo_garantia_detalle = models.ForeignKey(SerieIngresoReclamoGarantiaDetalle, on_delete=models.CASCADE)
    serie_cambio = models.ForeignKey(Serie, on_delete=models.CASCADE, blank=True, null=True)
    tipo_analisis = models.IntegerField(choices=TIPO_ANALISIS, blank=True, null=True)
    comentario = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='ControlCalidadReclamoGarantiaDetalle_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='ControlCalidadReclamoGarantiaDetalle_updated_by', editable=False)

    class Meta:
        verbose_name = 'Control Calidad Reclamo Garantia Detalle'
        verbose_name_plural = 'Control Calidad Reclamo Garantia Detalles'

    def __str__(self):
        return str(self.id)


class SerieReclamoHistorial(models.Model):
    serie_ingreso_reclamo_garantia_detalle = models.ForeignKey(SerieIngresoReclamoGarantiaDetalle, on_delete=models.CASCADE)
    historia_estado_serie = models.ForeignKey(HistorialEstadoSerie, on_delete=models.CASCADE)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='SerieReclamoHistorial_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='SerieReclamoHistorial_updated_by', editable=False)

    class Meta:
        verbose_name = 'Serie Reclamo Historial'
        verbose_name_plural = 'Serie Reclamo Historiales'
        ordering = [
            '-created_at',
        ]

    def __str__(self):
        return str(self.id)


class SalidaReclamoGarantia(models.Model):
    control_calidad_reclamo_garantia = models.OneToOneField(ControlCalidadReclamoGarantia, on_delete=models.CASCADE)
    fecha_salida = models.DateField('Fecha Salida', auto_now=False, auto_now_add=False, blank=True, null=True)
    observacion = models.TextField(blank=True, null=True, max_length=1000)
    estado = models.IntegerField('Estado', choices=ESTADOS_INGRESO_RECLAMO_GARANTIA, default=1)
  
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='SalidaReclamoGarantia_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='SalidaReclamoGarantia_updated_by', editable=False)
    
    class Meta:
        verbose_name = 'Salida Reclamo Garantia'
        verbose_name_plural = 'Salida Reclamos Garantia'

    def __str__(self):
        return str(self.id)



