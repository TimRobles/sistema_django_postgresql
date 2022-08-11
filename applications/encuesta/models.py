from pyexpat import model
from django.db import models
from django.conf import settings

from applications.clientes.models import Cliente, InterlocutorCliente, TipoInterlocutorCliente

# Create your models here.

class Encuesta(models.Model):
    nombre = models.CharField('Nombre', max_length=150)
    mostrar = models.BooleanField('Mostrar')
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='Encuesta_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='Encuesta_updated_by', editable=False)

    class Meta:
        verbose_name = 'Encuesta'
        verbose_name_plural = 'Encuestas'

    def __str__(self):
        return self.nombre

class Pregunta(models.Model):
    TIPO_PREGUNTA = [
        (1, 'Una opción'),
        (2, 'Para marcar'),
        (3, 'Para escribir'),
    ]

    texto = models.CharField('Texto', max_length=150)
    tipo_pregunta = models.IntegerField(choices=TIPO_PREGUNTA)
    orden = models.IntegerField('Orden')
    mostrar = models.BooleanField('Mostrar')
    encuesta = models.ForeignKey(Encuesta, on_delete=models.PROTECT)
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='Pregunta_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='Pregunta_updated_by', editable=False)

    class Meta:
        verbose_name = 'Pregunta'
        verbose_name_plural = 'Preguntas'
        ordering = [
            'orden',
            ]

    def __str__(self):
        return self.texto


class Alternativa(models.Model):    
    pregunta = models.ForeignKey(Pregunta, on_delete=models.PROTECT, related_name='Alternativa_pregunta')
    orden = models.IntegerField('Orden')
    texto = models.CharField('Texto', max_length=150)
    mostrar = models.BooleanField('Mostrar')
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='Alternativa_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='Alternativa_updated_by', editable=False)

    class Meta:
        verbose_name = 'Alternativa'
        verbose_name_plural = 'Alternativas'
        ordering = [
            'pregunta',
            'orden',
            ]

    def __str__(self):
        return self.texto


class Respuesta(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT)
    interlocutor = models.ForeignKey(InterlocutorCliente, on_delete=models.PROTECT, blank=True, null=True)
    nombre_interlocutor = models.CharField('Nombre Interlocutor', max_length=50, blank=True, null=True)
    tipo_interlocutor = models.ForeignKey(TipoInterlocutorCliente, on_delete=models.PROTECT, blank=True, null=True)
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='Respuesta_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='Respuesta_updated_by', editable=False)

    class Meta:
        verbose_name = 'Respuesta'
        verbose_name_plural = 'Respuestas'
        ordering = [
            '-created_by',
            ]

    def tipo_encuesta(self):
        if self.RespuestaDetalle_respuesta.all():
            return self.RespuestaDetalle_respuesta.all()[0].pregunta.encuesta
        else:
            return None

    def __str__(self):
        if self.interlocutor:
            return "%s - %s %s" % (self.cliente, self.interlocutor, self.created_at)
        else:
            return "%s - %s %s" % (self.cliente, self.nombre_interlocutor, self.created_at)


class RespuestaDetalle(models.Model):
    respuesta = models.ForeignKey(Respuesta, on_delete=models.CASCADE, related_name='RespuestaDetalle_respuesta')
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
    alternativa = models.ForeignKey(Alternativa, on_delete=models.CASCADE, blank=True, null=True)
    texto = models.CharField('Texto', max_length=150, blank=True, null=True)
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='RespuestaDetalle_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='RespuestaDetalle_updated_by', editable=False)

    class Meta:
        verbose_name = 'RespuestaDetalle'
        verbose_name_plural = 'RespuestaDetalles'

    def __str__(self):
        return str(self.id)


        

        

    
