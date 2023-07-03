from django.db import models
from decimal import Decimal
from django.conf import settings
from applications.variables import ESTADOS_CLIENTE_CRM, MEDIO, ESTADOS_EVENTO_CRM
from applications.clientes.models import Cliente, RepresentanteLegalCliente
from applications.rutas import CLIENTE_CRM_ARCHIVO_ENVIADO, CLIENTE_CRM_ARCHIVO_RECIBIDO
from applications.comprobante_venta.models import FacturaVenta
from applications.proveedores.models import Proveedor
from applications.sorteo.models import Sorteo
from applications.datos_globales.models import Pais

class ClienteCRM(models.Model):

    cliente_crm = models.OneToOneField(Cliente, on_delete=models.CASCADE)
    medio = models.IntegerField('Medio', choices=MEDIO)
    fecha_registro = models.DateField('Fecha de Registro', auto_now=False, auto_now_add=True, blank=True, null=True, editable=False)
    estado = models.IntegerField('Estado', choices=ESTADOS_CLIENTE_CRM, default=1)
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='ClienteCRM_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='ClienteCRM_updated_by', editable=False)

    class Meta:
        verbose_name = 'Cliente CRM'
        verbose_name_plural = 'Clientes CRM'

    @property
    def representante(self):
        return RepresentanteLegalCliente.objects.get(cliente = self.cliente_crm)
    
    @property
    def nro_factura(self):
        return FacturaVenta.objects.filter(cliente = self.cliente_crm).order_by('-fecha_emision').latest('fecha_emision')

    def __str__(self):
        return str(self.cliente_crm)

class ClienteCRMDetalle(models.Model):

    fecha = models.DateField('Fecha', auto_now=False, auto_now_add=False, blank=True, null=True)
    comentario = models.TextField('Comentario', blank=True, null=True)
    monto = models.DecimalField('Monto', max_digits=14, decimal_places=2, default=Decimal('0.00'))
    archivo_recibido = models.FileField('Archivo Recibido', upload_to=CLIENTE_CRM_ARCHIVO_RECIBIDO, max_length=100, blank=True, null=True)
    archivo_enviado = models.FileField('Archivo Enviado', upload_to=CLIENTE_CRM_ARCHIVO_ENVIADO, max_length=100, blank=True, null=True)
    cliente_crm =  models.ForeignKey(ClienteCRM, on_delete=models.CASCADE)
    
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='ClienteCRMDetalle_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='ClienteCRMDetalle_updated_by', editable=False)

    class Meta:
        verbose_name = 'Cliente CRM Detalle '
        verbose_name_plural = 'Clientes CRM Detalle '

    def __str__(self):
        return str(self.cliente_crm)


class ProveedorCRM(models.Model):

    proveedor_crm = models.OneToOneField(Proveedor, on_delete=models.CASCADE)
    fecha_registro = models.DateField('Fecha de Registro', auto_now=False, auto_now_add=True, blank=True, null=True, editable=False)
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='ProveedorCRM_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='ProveedorCRM_updated_by', editable=False)

    class Meta:
        verbose_name = 'Proveedor CRM'
        verbose_name_plural = 'Proveedores CRM'

    def __str__(self):
        return str(self.proveedor_crm)
    
from applications import cotizacion, comprobante_venta, cobranza

def actualizar_estado_cliente_crm(id_cliente=None):
    if id_cliente:
        try:
            clientes = ClienteCRM.objects.filter(cliente_crm__id=id_cliente)
        except:
            return False

    else:
        clientes = ClienteCRM.objects.all()

    for cliente in clientes:
        if len(cotizacion.models.CotizacionVenta.objects.filter(cliente=cliente.cliente_crm, estado__gte=2).exclude(estado=8).exclude(estado=9).exclude(estado=10)) > 0:
            cliente.estado = 3
        else:
            cliente.estado = 1
        if len(comprobante_venta.models.FacturaVenta.objects.filter(cliente=cliente.cliente_crm, estado__gte=2).exclude(estado=3))>0:
            cliente.estado == 4
        else:
            cliente.estado == 1
        if len(cobranza.models.Deuda.objects.filter(cliente=cliente.cliente_crm))>0:
            cliente.estado == 6
        else:
            cliente.estado == 1
        cliente.save()

class EventoCRM(models.Model):
    
    fecha_inicio = models.DateField('Fecha Inicio', blank=True, null=True)
    fecha_cierre = models.DateField('Fecha Cierre', blank=True, null=True)
    titulo = models.CharField('Titulo Evento', max_length=50)
    descripcion = models.TextField('Descripción', blank=True, null=True)
    # total_merchandising = models.DecimalField('Total Merchandising', max_digits=22, decimal_places=10)
    sorteo = models.ForeignKey(Sorteo, on_delete=models.PROTECT, related_name='Sorteo',blank=True, null=True)
    presupuesto_asignado = models.DecimalField('Presupuesto asignado', max_digits=6, decimal_places=3, blank=True, null=True)
    presupuesto_utilizado = models.DecimalField('Presupuesto utilizado', max_digits=6, decimal_places=3, blank=True, null=True)
    pais = models.ForeignKey(Pais, on_delete=models.PROTECT, related_name='Sorteo',blank=True, null=True)
    estado = models.IntegerField('Estado', choices=ESTADOS_EVENTO_CRM, default=1)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='EventoCRM_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='EventoCRM_updated_by', editable=False)

    class Meta:
        verbose_name = 'Evento CRM'
        verbose_name_plural = 'Eventos CRM'

    def __str__(self):
        return str(self.titulo)



