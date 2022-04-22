from django.db import models
from django.core.validators import FileExtensionValidator


class AplicacionUno(models.Model):
    orden = models.IntegerField()
    nombre = models.CharField('Nombre de Aplicación Nivel Uno', max_length=50)
    app_name = models.CharField('Nombre de App en URL', max_length=50)
    url_name = models.CharField('Nombre de URL', max_length=50)
    logo = models.ImageField('Logo PNG o SVG', upload_to='img/home/aplicacion/logo/', height_field=None, width_field=None, max_length=None, blank=True, null=True, validators=[FileExtensionValidator(['svg', 'png'])])

    class Meta:
        verbose_name = 'Aplicacion Uno'
        verbose_name_plural = 'Aplicaciones Uno'
        ordering = ['orden',]

    def __str__(self):
        return str(self.orden) + ' - ' + self.nombre + ' ' + self.app_name + ':' + self.url_name


class AplicacionDos(models.Model):
    orden = models.IntegerField()
    nombre = models.CharField('Nombre de Aplicación Nivel Dos', max_length=50)
    app_name = models.CharField('Nombre de App en URL', max_length=50)
    url_name = models.CharField('Nombre de URL', max_length=50)
    aplicacion_uno = models.ForeignKey(AplicacionUno, on_delete=models.CASCADE)
    logo = models.ImageField('Logo PNG o SVG', upload_to='img/home/aplicacion/logo/', height_field=None, width_field=None, max_length=None, blank=True, null=True, validators=[FileExtensionValidator(['svg', 'png'])])

    class Meta:
        verbose_name = 'Aplicacion Dos'
        verbose_name_plural = 'Aplicaciones Dos'
        ordering = ['aplicacion_uno__orden', 'orden',]

    def __str__(self):
        return str(self.orden) + ' - ' + self.nombre + ' ' + self.app_name + ':' + self.url_name + ' | ' + str(self.aplicacion_uno)