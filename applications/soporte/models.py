from django.db import models
from django.conf import settings
from applications.variables import ESTADO_PROBLEMAS, ESTADO_SOLICITUD
from applications.rutas import PROBLEMA_FOTO, SOLICITUD_FOTO


class Problema(models.Model):

    titulo = models.CharField('Titulo', max_length=100)
    descripcion = models.TextField('Descripción')
    estado = models.IntegerField('Estado', choices=ESTADO_PROBLEMAS, default=1)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='Problema_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='Problema_updated_by', editable=False)

    class Meta:
        verbose_name = 'Problema'
        verbose_name_plural = 'Problemas'

    def __str__(self):
        return str(self.titulo)

class ProblemaDetalle(models.Model):
    imagen = models.ImageField('Imagen', upload_to=PROBLEMA_FOTO, height_field=None, width_field=None, max_length=None, blank=True, null = True)
    url = models.URLField('URL', max_length=200, null=True, blank=True)
    problema = models.ForeignKey(Problema, on_delete=models.CASCADE, related_name='ProblemaDetalle_problema')
    nota_solucion = models.TextField('Nota de Solución', null=True, blank=True)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='ProblemaDetalle_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='ProblemaDetalle_updated_by', editable=False)


    class Meta:
        verbose_name = 'Problema Detalle'
        verbose_name_plural = 'Problemas Detalle'

    def __str__(self):
        return str(self.id)



class Solicitud(models.Model):
    titulo = models.CharField('Titulo', max_length=100)
    descripcion = models.TextField('Descripción')
    estado = models.IntegerField('Estado', choices=ESTADO_SOLICITUD, default=1)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='Solicitud_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='Solicitud_updated_by', editable=False)

    class Meta:
        verbose_name = 'Solicitud'
        verbose_name_plural = 'Solicitudes'

    def __str__(self):
        return str(self.id)


class SolicitudDetalle(models.Model):
    imagen = models.ImageField('Imagen', upload_to=SOLICITUD_FOTO, height_field=None, width_field=None, max_length=None, blank=True, null = True)
    url = models.URLField('URL', max_length=200, null=True, blank=True)
    solicitud = models.ForeignKey(Solicitud, on_delete=models.CASCADE, related_name='SolicitudDetalle_solicitud')

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='SolicitudDetalle_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='SolicitudDetalle_updated_by', editable=False)


    class Meta:
        verbose_name = 'Solicitud Detalle'
        verbose_name_plural = 'Solicitudes Detalle'

    def __str__(self):
        return str(self.id)