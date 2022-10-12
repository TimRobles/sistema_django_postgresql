from django.conf import settings
from django.db import models
from django.contrib.contenttypes.models import ContentType
from applications.sociedad.models import Sociedad
from applications.material.models import SubFamilia

class EstadoSerie(models.Model):
    numero_estado = models.IntegerField()
    descripcion = models.CharField('Descripción', max_length=50)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='EstadoSerie_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='EstadoSerie_updated_by', editable=False)

    class Meta:
        verbose_name = 'Estado Serie'
        verbose_name_plural = 'Estados Serie'

    def __str__(self):
        return str(self.id)


class Serie(models.Model):
    serie_base = models.CharField('Serie Base', max_length=200)
    content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT,blank=True, null=True)
    id_registro = models.IntegerField(blank=True, null=True)
    estado_serie = models.ForeignKey(EstadoSerie, on_delete=models.CASCADE)
    sociedad = models.ForeignKey(Sociedad, on_delete=models.CASCADE)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='Serie_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='Serie_updated_by', editable=False)


    class Meta:
        verbose_name = 'Serie'
        verbose_name_plural = 'Series'

    def __str__(self):
        return str(self.id)


class FallaMaterial(models.Model):
    sub_familia = models.ForeignKey(SubFamilia, on_delete=models.CASCADE)
    titulo = models.CharField('Titulo', max_length=50)
    comentario = models.TextField()
    visible = models.BooleanField()
  
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='FallaMaterial_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='FallaMaterial_updated_by', editable=False)

    class Meta:
        verbose_name = 'Falla Material'
        verbose_name_plural = 'Fallas Materiales'

    def __str__(self):
        return str(self.id)



class HistorialEstadoSerie(models.Model):
    serie = models.ForeignKey(Serie, on_delete=models.CASCADE)
    estado_serie = models.ForeignKey(EstadoSerie, on_delete=models.CASCADE)
    falla_material = models.ForeignKey(FallaMaterial, on_delete=models.CASCADE)
    observacion = models.TextField()

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='HistorialEstadoSerie_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='HistorialEstadoSerie_updated_by', editable=False)

    class Meta:
        verbose_name = 'Historial Estado Serie'
        verbose_name_plural = 'Historial Estado Series'

    def __str__(self):
        return str(self.id)
