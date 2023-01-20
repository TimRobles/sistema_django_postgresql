from decimal import Decimal
from django.db import models
from django.conf import settings

from django.contrib.contenttypes.models import ContentType
from applications.funciones import numeroXn
from applications.muestra.managers import NotaIngresoMuestraManager
from applications.nota_ingreso.models import NotaIngresoDetalle
from applications.sociedad.models import Sociedad
from applications.variables import ESTADO_NOTA_INGRESO

# Create your models here.

class NotaIngresoMuestra(models.Model):
    nro_nota_ingreso_muestra = models.IntegerField('Número de Nota de Ingreso de Muestra', help_text='Correlativo', blank=True, null=True)
    sociedad = models.ForeignKey(Sociedad, on_delete=models.PROTECT)
    fecha_ingreso = models.DateField('Fecha de Ingreso', auto_now=False, auto_now_add=False)
    observaciones = models.TextField(blank=True, null=True)
    motivo_anulacion = models.TextField('Motivo de Anulación', blank=True, null=True)
    estado = models.IntegerField('Estado', choices=ESTADO_NOTA_INGRESO, default=1)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='NotaIngresoMuestra_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='NotaIngresoMuestra_updated_by', editable=False)

    objects = NotaIngresoMuestraManager()

    class Meta:
        verbose_name = 'Nota de Ingreso de Muestra'
        verbose_name_plural = 'Notas de Ingreso de Muestra'

    @property
    def fecha(self):
        return self.fecha_ingreso
    
    @property
    def documento(self):
        return self
    
    @property
    def proveedor(self):
        return ""
    
    @property
    def detalle(self):
        return self.NotaIngresoMuestraDetalle_nota_ingreso_muestra.all()

    def __str__(self):
        return "NOTA DE INGRESO DE MUESTRA %s" % (numeroXn(self.nro_nota_ingreso_muestra, 6))


class NotaIngresoMuestraDetalle(models.Model):
    item = models.IntegerField(blank=True, null=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT) #Material
    id_registro = models.IntegerField()
    cantidad_total = models.DecimalField('Cantidad total', max_digits=22, decimal_places=10, default=Decimal('0.00'))
    nota_ingreso_muestra = models.ForeignKey(NotaIngresoMuestra, on_delete=models.PROTECT, related_name='NotaIngresoMuestraDetalle_nota_ingreso_muestra')

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='NotaIngresoMuestraDetalle_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='NotaIngresoMuestraDetalle_updated_by', editable=False)

    class Meta:
        verbose_name = 'Nota de Ingreso de Muestra Detalle'
        verbose_name_plural = 'Notas de Ingreso de Muestra Detalles'
        ordering = [
            'nota_ingreso_muestra',
            'item',
            ]

    @property
    def producto(self):
        return self.content_type.get_object_for_this_type(id=self.id_registro)

    @property
    def cantidad(self):
        return self.cantidad_total
    
    @property
    def orden_compra_detalle(self):
        return self

    @property #Cambiar por cantidad registrada por series temporales
    def cantidad_contada(self):
        nota_ingreso_muestra_detalle = NotaIngresoDetalle.objects.filter(
            content_type=ContentType.objects.get_for_model(self),
            id_registro=self.id,
        )
        if nota_ingreso_muestra_detalle:
            return nota_ingreso_muestra_detalle.aggregate(models.Sum('cantidad_conteo'))['cantidad_conteo__sum']
        return Decimal('0.00')

    @property
    def pendiente(self):
        return self.cantidad - self.cantidad_contada

    @property
    def sociedad(self):
        return self.nota_ingreso_muestra.sociedad

    def __str__(self):
        return "%s - %s" % (self.item, self.producto)
