from django.db import models
from django.conf import settings
from applications.datos_globales.models import Area
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from applications.variables import ESTADO_TAREA, PRIORIDAD_TAREA

class TipoTarea(models.Model):
    nombre = models.CharField('Nombre', max_length=50)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='TipoTarea_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='TipoTarea_updated_by', editable=False)

    class Meta: 
        verbose_name = 'Tipo de Tarea'
        verbose_name_plural = 'Tipos de Tarea'
        ordering = [
            'nombre',
        ]

    def __str__(self):
        return str(self.nombre)


class Tarea(models.Model):

    fecha_inicio = models.DateField('Fecha Inicio', blank=True, null=True)
    fecha_limite = models.DateField('Fecha Limite', blank=True, null=True)
    fecha_cierre = models.DateField('Fecha Cierre', blank=True, null=True)
    tipo_tarea = models.ForeignKey(TipoTarea, on_delete=models.PROTECT, related_name='TipoTarea')
    descripcion = models.TextField('Descripción')
    area = models.ForeignKey(Area, on_delete=models.PROTECT, related_name='Área',blank=True, null=True)
    encargado = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Encargado',on_delete=models.PROTECT, blank=True, null=True,related_name='Tarea_encargado')
    apoyo = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name='Apoyo', blank=True,null=True, related_name='Tarea_apoyo')
    prioridad = models.IntegerField('Prioridad',choices=PRIORIDAD_TAREA,blank=True, null=True)
    content_type = models.ForeignKey(ContentType, blank=True, null=True, on_delete=models.PROTECT) # Cliente | Evento
    id_registro = models.IntegerField(blank=True, null=True)
    estado = models.IntegerField('Estado', choices=ESTADO_TAREA, default=1)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='Tarea_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='Tarea_updated_by', editable=False)

    class Meta: 
        verbose_name = 'Tarea'
        verbose_name_plural = 'Tareas'
        ordering = [
            '-created_at',
        ]    

    def __str__(self):
        return str(self.descripcion)


class HistorialComentarioTarea(models.Model):
    tarea = models.ForeignKey(Tarea, on_delete=models.PROTECT, related_name='Tarea',blank=True, null=True)
    comentario = models.TextField('Comentario',blank=True, null=True)
    
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='HistorialComentarioTarea_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='HistorialComentarioTarea_updated_by', editable=False)

    class Meta:
        verbose_name = 'Historial Comentario Tarea'
        verbose_name_plural = 'Historial Comentarios Tarea'

    def __str__(self):
        return str(self.comentario)

