from django.db import models
from django.conf import settings
from applications.variables import ESTADOS_CLIENTE_CRM, MEDIO, ESTADOS_EVENTO_CRM, TIPO_ENCUESTA_CRM, TIPO_PREGUNTA_CRM
from applications.clientes.models import Cliente, CorreoInterlocutorCliente, InterlocutorCliente, TelefonoInterlocutorCliente
from applications.sorteo.models import Sorteo
from applications.datos_globales.models import Pais
from .managers import RespuestaDetalleCRMManager

class ClienteCRM(models.Model):

    cliente_crm = models.OneToOneField(Cliente, on_delete=models.CASCADE)
    medio = models.IntegerField('Medio', choices=MEDIO)
    estado = models.IntegerField('Estado', choices=ESTADOS_CLIENTE_CRM, default=1)
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='ClienteCRM_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='ClienteCRM_updated_by', editable=False)

    class Meta:
        verbose_name = 'Cliente CRM'
        verbose_name_plural = 'Clientes CRM'

    def __str__(self):
        return self.cliente_crm.razon_social

class ClienteCRMDetalle(models.Model):

    interlocutor = models.ForeignKey(InterlocutorCliente, on_delete=models.PROTECT)
    correo = models.ForeignKey(CorreoInterlocutorCliente, on_delete=models.PROTECT)
    telefono = models.ForeignKey(TelefonoInterlocutorCliente, on_delete=models.PROTECT)
    cliente_crm =  models.ForeignKey(ClienteCRM, on_delete=models.CASCADE)
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='ClienteCRMDetalle_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='ClienteCRMDetalle_updated_by', editable=False)

    class Meta:
        verbose_name = 'Cliente CRM Detalle '
        verbose_name_plural = 'Clientes CRM Detalle '

    def __str__(self):
        return self.interlocutor

class EventoCRM(models.Model):
    
    fecha_inicio = models.DateField('Fecha Inicio', blank=True, null=True)
    fecha_cierre = models.DateField('Fecha Cierre', blank=True, null=True)
    titulo = models.CharField('Titulo Evento', max_length=50)
    descripcion = models.TextField('Descripción', blank=True, null=True)
    # total_merchandising = models.DecimalField('Total Merchandising', max_digits=22, decimal_places=10)
    sorteo = models.ForeignKey(Sorteo, on_delete=models.PROTECT, related_name='Sorteo',blank=True, null=True)
    presupuesto_asignado = models.DecimalField('Presupuesto asignado', max_digits=6, decimal_places=3, blank=True, null=True)
    presupuesto_utilizado = models.DecimalField('Presupuesto utilizado', max_digits=6, decimal_places=3, blank=True, null=True)
    pais = models.ForeignKey(Pais, on_delete=models.PROTECT, related_name='pais',blank=True, null=True)
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

