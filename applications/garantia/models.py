from decimal import Decimal
from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from applications import datos_globales
from applications.variables import ESTADOS_INGRESO_RECLAMO_GARANTIA
from applications.sociedad.models import Sociedad
from applications.calidad.models import Serie
from applications.clientes.models import Cliente, InterlocutorCliente
from applications.garantia.managers import IngresoReclamoGarantiaManager


class IngresoReclamoGarantia(models.Model):
    nro_ingreso_garantia = models.IntegerField('Número de Ingreso Reclamo Garantia', help_text='Correlativo', blank=True, null=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name='IngresoReclamoGarantia_cliente', blank=True, null=True)
    cliente_interlocutor = models.ForeignKey(InterlocutorCliente, on_delete=models.PROTECT, related_name='IngresoReclamoGarantia_interlocutor', blank=True, null=True)
    sociedad = models.ForeignKey(Sociedad, on_delete=models.CASCADE, blank=True, null=True)
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

    def __str__(self):
        return str(self.id)

class IngresoReclamoGarantiaDetalle(models.Model):
    item = models.IntegerField(blank=True, null=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT,blank=True, null=True)
    id_registro = models.IntegerField(blank=True, null=True)
    serie = models.ForeignKey(Serie, on_delete=models.PROTECT, related_name='IngresoReclamoGarantiaDetalle_serie',blank=True, null=True)
    cantidad = models.DecimalField('Cantidad', max_digits=22, decimal_places=10, default=Decimal('0.00'),blank=True, null=True)
    precio_venta = models.DecimalField('Precio Venta', max_digits=22, decimal_places=10, default=Decimal('0.00'),blank=True, null=True)
    ingreso_garantia = models.ForeignKey(IngresoReclamoGarantia, on_delete=models.CASCADE, related_name='IngresoReclamoGarantiaDetalle_ingreso_garantia', blank=True, null=True)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='IngresoReclamoGarantiaDetalle_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='IngresoReclamoGarantiaDetalle_updated_by', editable=False)

    class Meta:
        verbose_name = 'Ingreso Reclamo Garantia Detalle'
        verbose_name_plural = 'Ingresos Reclamo Garantia Detalle'


    @property
    def producto(self):
        return None
        return self.content_type.get_object_for_this_type(id = self.id_registro)
        

    def __str__(self):
        return str(self.id)



class ControlCalidadReclamoGarantia(models.Model):
    nro_calidad_garantia = models.IntegerField('Número de Control Reclamo Garantia', help_text='Correlativo', blank=True, null=True)   
    ingreso_garantia = models.ForeignKey(IngresoReclamoGarantia, on_delete=models.CASCADE, related_name='ControlCalidadReclamoGarantia_ingreso_garantia')
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name='ControlCalidadReclamoGarantia_cliente', blank=True, null=True)
    cliente_interlocutor = models.ForeignKey(InterlocutorCliente, on_delete=models.PROTECT, related_name='ControlCalidadReclamoGarantia_interlocutor', blank=True, null=True)
    sociedad = models.ForeignKey(Sociedad, on_delete=models.CASCADE, blank=True, null=True)
    fecha_control = models.DateField('Fecha Control', auto_now=False, auto_now_add=False, blank=True, null=True)
    observacion = models.TextField(blank=True, null=True, max_length=1000)
    encargado = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True)
    estado = models.IntegerField('Estado', choices=ESTADOS_INGRESO_RECLAMO_GARANTIA, default=1)
  
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='ControlCalidadReclamoGarantia_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='ControlCalidadReclamoGarantia_updated_by', editable=False)
    
    class Meta:
        verbose_name = 'Control Calidad Reclamo Garantia'
        verbose_name_plural = 'Control Calidad Reclamos Garantia'

    def __str__(self):
        return str(self.id)

class ControlCalidadReclamoGarantiaDetalle(models.Model):

    item = models.IntegerField(blank=True, null=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT,blank=True, null=True)
    id_registro = models.IntegerField(blank=True, null=True)
    serie = models.ForeignKey(Serie, on_delete=models.PROTECT, related_name='ControlCalidadReclamoGarantiaDetalle_serie',blank=True, null=True)
    cantidad = models.DecimalField('Cantidad', max_digits=22, decimal_places=10, default=Decimal('0.00'),blank=True, null=True)
    precio_venta = models.DecimalField('Precio Venta', max_digits=22, decimal_places=10, default=Decimal('0.00'),blank=True, null=True)
    calidad_garantia = models.ForeignKey(ControlCalidadReclamoGarantia, on_delete=models.CASCADE, related_name='ControlCalidadReclamoGarantiaDetalle_calidad_garantia', blank=True, null=True)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='ControlCalidadReclamoGarantiaDetalle_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='ControlCalidadReclamoGarantiaDetalle_updated_by', editable=False)

    class Meta:
        verbose_name = 'Control Calidad Reclamo Garantia Detalle'
        verbose_name_plural = 'Control Calidad Reclamo Garantia Detalles'

    def __str__(self):
        return str(self.id)



class SalidaReclamoGarantia(models.Model):
    nro_salida_garantia = models.IntegerField('Número de Salida Reclamo Garantia', help_text='Correlativo', blank=True, null=True)   
    control_garantia = models.ForeignKey(ControlCalidadReclamoGarantia, on_delete=models.CASCADE, related_name='SalidaReclamoGarantia_ingreso_garantia')
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name='SalidaReclamoGarantia_cliente', blank=True, null=True)
    cliente_interlocutor = models.ForeignKey(InterlocutorCliente, on_delete=models.PROTECT, related_name='SalidaReclamoGarantia_interlocutor', blank=True, null=True)
    sociedad = models.ForeignKey(Sociedad, on_delete=models.CASCADE, blank=True, null=True)
    fecha_salida = models.DateField('Fecha Salida', auto_now=False, auto_now_add=False, blank=True, null=True)
    observacion = models.TextField(blank=True, null=True, max_length=1000)
    encargado = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True)
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

class SalidaReclamoGarantiaDetalle(models.Model):
    item = models.IntegerField(blank=True, null=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT,blank=True, null=True)
    id_registro = models.IntegerField(blank=True, null=True)
    serie = models.ForeignKey(Serie, on_delete=models.PROTECT, related_name='SalidaReclamoGarantiaDetalle_serie',blank=True, null=True)
    cantidad = models.DecimalField('Cantidad', max_digits=22, decimal_places=10, default=Decimal('0.00'),blank=True, null=True)
    precio_venta = models.DecimalField('Precio Venta', max_digits=22, decimal_places=10, default=Decimal('0.00'),blank=True, null=True)
    salida_garantia = models.ForeignKey(SalidaReclamoGarantia, on_delete=models.CASCADE, related_name='SalidaReclamoGarantiaDetalle_salida_garantia', blank=True, null=True)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='SalidaReclamoGarantiaDetalle_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='SalidaReclamoGarantiaDetalle_updated_by', editable=False)
    

    class Meta:
        verbose_name = 'Salida Reclamo Garantia Detalle'
        verbose_name_plural = 'Salida Reclamo Garantia Detalles'

    def __str__(self):
        return str(self.id)



