from email.policy import default
from django.db import models
from django.conf import settings
from applications import datos_globales
from applications.rutas import RUTA_SOCIEDAD_DOCUMENTO, RUTA_SOCIEDAD_LOGO
from applications.variables import ESTADO_SUNAT, TIPO_DOCUMENTO_SUNAT, CONDICION_SUNAT
from colorfield.fields import ColorField

from applications.funciones import validar_numero

# Create your models here.

class Sociedad(models.Model):
    tipo_documento = models.CharField('Tipo de Documento', choices=TIPO_DOCUMENTO_SUNAT, max_length=1, default="6")
    ruc = models.CharField('RUC', max_length=11, unique=True, validators=[validar_numero])
    razon_social = models.CharField('Razón Social', max_length=100)
    nombre_comercial = models.CharField('Nombre Comercial', max_length=100, blank=True, null=True)
    direccion_legal = models.CharField('Dirección Legal', max_length=100)
    ubigeo = models.CharField('Ubigeo', max_length=6)
    distrito = models.ForeignKey('datos_globales.Distrito', on_delete=models.CASCADE, blank=True, null=True)
    estado_sunat = models.IntegerField('Estado SUNAT', choices=ESTADO_SUNAT, default=1)
    condicion_sunat = models.IntegerField('Condición SUNAT', choices=CONDICION_SUNAT, default=1)
    logo = models.ImageField('Logo', upload_to=RUTA_SOCIEDAD_LOGO, height_field=None, width_field=None, max_length=None, blank=True, null=True)
    color = ColorField(default='#FF0000')
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='Sociedad_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='Sociedad_updated_by', editable=False)

    class Meta:
        verbose_name = 'Sociedad'
        verbose_name_plural = 'Sociedades'
        ordering = ['estado_sunat', 'razon_social']

    def save(self, *args, **kwargs):
        if self.ubigeo:
            self.distrito = datos_globales.models.Distrito.objects.get(codigo = self.ubigeo)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.razon_social

class Documento(models.Model):
    nombre_documento = models.CharField('Nombre de documento', max_length=50)
    descripcion_documento = models.CharField('Descripción del documento', max_length=100)
    documento = models.FileField('Documento', upload_to=RUTA_SOCIEDAD_DOCUMENTO, max_length=100, blank=True, null=True)
    sociedad = models.ForeignKey(Sociedad, on_delete=models.PROTECT, blank=True, null=True)
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='Documento_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='Documento_updated_by', editable=False)

    class Meta:
        """Meta definition for Sociedad."""

        verbose_name = 'Documento'
        verbose_name_plural = 'Documentos'

    def __str__(self):
        """Unicode representation of Sociedad."""
        return self.nombre_documento

class TipoRepresentanteLegal(models.Model):
    '''Solo por Admin'''
    
    nombre = models.CharField('Nombre', max_length=50, unique=True)
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='TipoRepresentanteLegal_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='TipoRepresentanteLegal_updated_by', editable=False)

    class Meta:
        verbose_name = 'Tipo Representante Legal'
        verbose_name_plural = 'Tipos Representante Legal'
        ordering = ['nombre',]

    def __str__(self):
        return self.nombre

class RepresentanteLegal(models.Model):
    '''Solo por Admin'''

    ESTADO = (
    (1, 'ACTIVO'),
    (2, 'BAJA'),
    )

    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='Usuario', verbose_name='Representante Legal')
    sociedad = models.ForeignKey(Sociedad, on_delete=models.PROTECT, blank=True, null=True, related_name='Sociedad', editable=False)
    tipo_representante_legal = models.ForeignKey(TipoRepresentanteLegal, on_delete=models.PROTECT, blank=True, null=True, related_name='TipoRepresentanteLegal')
    fecha_registro = models.DateField('Fecha de Registro', auto_now=False, auto_now_add=False, blank=True, null=True)
    fecha_baja= models.DateField('Fecha de Baja', auto_now=False, auto_now_add=False, blank=True, null=True)
    estado = models.IntegerField('Estado', choices=ESTADO, default=1)
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='RepresentanteLegal_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='RepresentanteLegal_updated_by', editable=False)

    class Meta:
        verbose_name = 'Representante Legal'
        verbose_name_plural = 'Representantes Legales'

    def __str__(self):
        return str(self.tipo_representante_legal)

