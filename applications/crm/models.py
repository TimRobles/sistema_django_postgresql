from django.db import models
from decimal import Decimal
from django.conf import settings
from applications.rutas import CLIENTE_CRM_ARCHIVO_ENVIADO, CLIENTE_CRM_ARCHIVO_RECIBIDO
from applications.comprobante_venta.models import FacturaVenta
from applications.proveedores.models import Proveedor
from applications.variables import ESTADOS_CLIENTE_CRM, MEDIO, ESTADOS_EVENTO_CRM, TIPO_ENCUESTA_CRM, TIPO_PREGUNTA_CRM
from applications.clientes.models import Cliente, RepresentanteLegalCliente, CorreoInterlocutorCliente, InterlocutorCliente, TelefonoInterlocutorCliente
from applications.sorteo.models import Sorteo
from applications.datos_globales.models import Pais, Unidad
from django.contrib.contenttypes.models import ContentType
from applications.almacenes.models import Almacen
from applications.movimiento_almacen.models import TipoStock
from applications.sede.models import Sede
from applications.sociedad.models import Sociedad
from .managers import RespuestaDetalleCRMManager

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
    
    titulo = models.CharField('Titulo Evento', max_length=50)
    pais = models.ForeignKey(Pais, on_delete=models.PROTECT, related_name='Sorteo',blank=True, null=True)
    ubicacion = models.CharField('Ubicación', max_length=100,blank=True, null=True)
    encargado = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Encargado', on_delete=models.PROTECT, blank=True, null=True)
    fecha_inicio = models.DateField('Fecha Inicio', blank=True, null=True)
    fecha_cierre = models.DateField('Fecha Cierre', blank=True, null=True)
    presupuesto_asignado = models.DecimalField('Presupuesto asignado', max_digits=6, decimal_places=3, blank=True, null=True)
    presupuesto_utilizado = models.DecimalField('Presupuesto utilizado', max_digits=6, decimal_places=3, blank=True, null=True)
    total_merchandising = models.DecimalField('Total Merchandising', max_digits=22, decimal_places=10, blank=True, null=True)
    descripcion = models.TextField('Descripción', blank=True, null=True)
    sorteo = models.ForeignKey(Sorteo, on_delete=models.PROTECT, related_name='Sorteo',blank=True, null=True)
    sociedad = models.ForeignKey(Sociedad, on_delete=models.PROTECT,blank=True, null=True)
    sede_origen = models.ForeignKey(Sede, on_delete=models.PROTECT, blank=True, null=True)
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
    

class EventoCRMDetalle(models.Model):
    
    item = models.IntegerField(blank=True, null=True)
    content_type = models.ForeignKey(ContentType, blank=True, null=True, on_delete=models.PROTECT)#Merchandising
    id_registro = models.IntegerField()
    almacen_origen = models.ForeignKey(Almacen, on_delete=models.PROTECT,blank=True, null=True)
    tipo_stock = models.ForeignKey(TipoStock, on_delete=models.CASCADE)
    cantidad_asignada = models.DecimalField('Cantidad Asignada', max_digits=8, decimal_places=2,blank=True, null=True)
    cantidad_utilizada = models.DecimalField('Cantidad Utilizada', max_digits=8, decimal_places=2,blank=True, null=True)
    cantidad_restante = models.DecimalField('Cantidad Restante', max_digits=8, decimal_places=2,blank=True, null=True)
    unidad = models.ForeignKey(Unidad, on_delete=models.PROTECT,blank=True, null=True)
    evento_crm = models.ForeignKey(EventoCRM, on_delete=models.CASCADE, related_name='EventoCRMDetalle_evento_crm')

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='EventoCRMDetalle_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='EventoCRMDetalle_updated_by', editable=False)

    class Meta:
        verbose_name = 'Evento CRM Detalle '
        verbose_name_plural = 'Eventos CRM Detalle'
        ordering = [
            'evento_crm',
            'item',
            ]

    @property
    def producto(self):
        return self.content_type.get_object_for_this_type(id=self.id_registro)
            
    def __str__(self):
        return f"{self.item} - {self.producto}. Cantidad: {self.cantidad_asignada}"
    

class EventoCRMDetalleInformacionAdicional(models.Model):

    fecha = models.DateField('Fecha', auto_now=False, auto_now_add=False, blank=True, null=True)
    comentario = models.TextField('Comentario', blank=True, null=True)
    evento_crm =  models.ForeignKey(EventoCRM, on_delete=models.CASCADE)
    
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='EventoCRMDetalleInformacionAdicional_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='EventoCRMDetalleInformacionAdicional_updated_by', editable=False)

    class Meta:
        verbose_name = 'Evento CRM Detalle Informacion Adicional'
        verbose_name_plural = 'Eventos CRM Detalle Informacion Adicional'

    def __str__(self):
        return str(self.comentario)
    

class PreguntaCRM(models.Model):
    tipo_pregunta = models.IntegerField('Tipo Pregunta', choices=TIPO_PREGUNTA_CRM)
    texto = models.CharField('Pregunta', max_length=100)
    orden = models.IntegerField()
    mostrar = models.BooleanField('Mostrar', default=False)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='PreguntaCRM_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='PreguntaCRM_updated_by', editable=False)

    class Meta:
        verbose_name = 'Pregunta CRM'
        verbose_name_plural = 'Preguntas CRM'
        ordering = [
            'orden',
            '-created_at',
            'mostrar',
        ]

    def __str__(self):
        return str(self.texto)
    

class EncuestaCRM(models.Model):
    tipo_encuesta = models.IntegerField('Tipo Encuesta', choices=TIPO_ENCUESTA_CRM, blank=True, null=True)
    titulo = models.CharField('Titulo Encuesta', max_length=50)
    pregunta_crm = models.ManyToManyField(PreguntaCRM, blank=True)
    mostrar = models.BooleanField('Mostrar', default=False)
    pais = models.ForeignKey(Pais, on_delete=models.PROTECT, related_name='Pais',blank=True, null=True)
    slug = models.SlugField(blank=True, null=True)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='EncuestaCRM_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='EncuestaCRM_updated_by', editable=False)

    class Meta:
        verbose_name = 'Encuesta CRM'
        verbose_name_plural = 'Encuestas CRM'
        ordering = [
            '-created_at',
        ]
    def __str__(self):
        return str(self.titulo)
    

class AlternativaCRM(models.Model):
    orden = models.IntegerField()
    texto = models.CharField('Alternativa', max_length=100)
    valor = models.CharField('Valor', max_length=100)
    mostrar = models.BooleanField('Mostrar', default=False)
    pregunta_crm = models.ForeignKey(PreguntaCRM, on_delete=models.PROTECT, blank=True, null=True, related_name='AlternativaCRM_pregunta_crm')

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='AlternativaCRM_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='AlternativaCRM_updated_by', editable=False)

    class Meta:
        verbose_name = 'Alternativa CRM'
        verbose_name_plural = 'Alternativas CRM'
        ordering = [
            'pregunta_crm',
            'orden',
            'texto',
            'created_at',
        ]
    def __str__(self):
        return str(self.texto)


class RespuestaCRM(models.Model):
    ESTADO_RESPUESTA = (
        (1, 'BORRADOR'),
        (2, 'ENVIADO'),
        (3, 'EXPIRADO'),
    )

    fecha_vencimiento = models.DateField('Fecha de Vencimiento', auto_now=False, auto_now_add=False, blank=True, null=True)
    cliente_crm = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    interlocutor = models.ForeignKey(InterlocutorCliente, on_delete=models.PROTECT, related_name='RespuestaCRM_interlocutor', blank=True, null=True)
    nombre_interlocutor = models.CharField('Nombre Interlocutor', max_length=50, blank=True, null=True)
    encuesta_crm = models.ForeignKey(EncuestaCRM, on_delete=models.PROTECT, blank=True, null=True)
    estado = models.IntegerField(choices=ESTADO_RESPUESTA, default=1)
    slug = models.SlugField(blank=True, null=True)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='RespuestaCRM_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='RespuestaCRM_updated_by', editable=False)

    class Meta:
        verbose_name = 'Respuesta CRM'
        verbose_name_plural = 'Respuestas CRM'
        ordering = [
            '-created_at',
        ]
    def __str__(self):
        return str(self.encuesta_crm)

class RespuestaDetalleCRM(models.Model):
    alternativa_crm = models.ForeignKey(AlternativaCRM, on_delete=models.PROTECT, blank=True, null=True)
    pregunta_crm = models.ForeignKey(PreguntaCRM, on_delete=models.PROTECT, blank=True, null=True)
    respuesta_crm = models.ForeignKey(RespuestaCRM, on_delete=models.PROTECT, blank=True, null=True, related_name='RespuestaDetalleCRM_respuesta_crm')
    texto = models.CharField('Texto', max_length=100, blank=True, null=True)
    borrador = models.BooleanField()

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='RespuestaDetalleCRM_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='RespuestaDetalleCRM_updated_by', editable=False)

    objects = RespuestaDetalleCRMManager()

    class Meta:
        verbose_name = 'Respuesta Detalle CRM'
        verbose_name_plural = 'Respuestas Detalle CRM'

    def __str__(self):
        return str(self.respuesta_crm)

