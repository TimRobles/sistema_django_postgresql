from django.db import models
from django.conf import settings
from applications.datos_globales.models import ProductoSunat, Unidad
# from applications.material.models import SubFamilia
from applications.variables import ESTADOS


class FamiliaActivo(models.Model):
    nombre = models.CharField('Nombre', max_length=50)
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='FamiliaActivo_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='FamiliaActivo_updated_by', editable=False)

    class Meta:
        verbose_name = 'Familia Activo'
        verbose_name_plural = 'Familias Activo'
        ordering = ['nombre',]

    def __str__(self):
        return self.nombre


class SubFamiliaActivo(models.Model):
    nombre = models.CharField('Nombre', max_length=50)
    familia = models.ForeignKey(FamiliaActivo, on_delete=models.PROTECT)
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='SubFamiliaActivo_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='SubFamiliaActivo_updated_by', editable=False)

    class Meta:
        verbose_name = 'SubFamilia Activo'
        verbose_name_plural = 'SubFamilias Activo'
        ordering = ['nombre',]

    def __str__(self):
        return self.nombre


class ModeloActivo(models.Model):
    nombre = models.CharField('Nombre', max_length=50)
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='ModeloActivo_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='ModeloActivo_updated_by', editable=False)

    class Meta:
        verbose_name = 'Modelo Activo'
        verbose_name_plural = 'Modelos Activo'
        ordering = ['nombre',]

    def __str__(self):
        return self.nombre


class MarcaActivo(models.Model):
    nombre = models.CharField('Nombre', max_length=50)
    modelos = models.ManyToManyField(ModeloActivo)
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='MarcaActivo_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='MarcaActivo_updated_by', editable=False)

    class Meta:
        verbose_name = 'Marca Activo'
        verbose_name_plural = 'Marcas Activo'
        ordering = ['nombre',]

    def __str__(self):
        return self.nombre


class ActivoBase(models.Model):
    descripcion_venta = models.CharField('Descripción de Venta', max_length=150, null=True, blank=True)
    descripcion_corta = models.CharField('Descripción Corta', max_length=150)
    unidad = models.ForeignKey(Unidad, on_delete=models.CASCADE, blank=True, null=True)
    peso = models.DecimalField('Peso', max_digits=6, decimal_places=2, blank=True, null=True)
    sub_familia = models.ForeignKey(SubFamiliaActivo, on_delete=models.CASCADE, blank=True, null=True)
    depreciacion = models.DecimalField('Depreciación', max_digits=6, decimal_places=3)
    vida_util = models.IntegerField('Vida Útil (meses)', blank=True, null=True)
    producto_sunat = models.ForeignKey(ProductoSunat, on_delete=models.CASCADE, blank=True, null=True)
    estado = models.IntegerField('Estado Activo', choices=ESTADOS, default=1)
    traduccion = models.CharField('Traducción', max_length=255, blank=True, null=True)
    partida = models.CharField('Partida', max_length=30, blank=True, null=True)
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='ActivoBase_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='ActivoBase_updated_by', editable=False)


    class Meta:
        verbose_name = 'Activo Base'
        verbose_name_plural = 'Activos Base'
        ordering = [
            'descripcion_corta',
            ]

    def __str__(self):
        return self.descripcion_corta.upper()
