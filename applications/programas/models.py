from django.db import models
from django.core.validators import FileExtensionValidator

class NivelUno(models.Model):
    orden = models.IntegerField()
    nombre = models.CharField('Nombre de Nivel Uno', max_length=50)
    icono = models.ImageField('Icono PNG o SVG', upload_to='img/programas/icono/', height_field=None, width_field=None, max_length=None, blank=True, null=True, validators=[FileExtensionValidator(['svg', 'png'])])

    class Meta:
        verbose_name = 'Nivel Uno'
        verbose_name_plural = 'Niveles Uno'
        ordering = ['orden',]

    def __str__(self):
        return str(self.orden) + ' - ' + self.nombre

class NivelDos(models.Model):
    orden = models.IntegerField()
    nombre = models.CharField('Nombre de Nivel Dos', max_length=50)
    app_name = models.CharField('Nombre de App', max_length=50)
    nivel_uno = models.ForeignKey(NivelUno, on_delete=models.CASCADE, related_name="NivelDos_nivel_uno")
    icono = models.ImageField('Icono PNG o SVG', upload_to='img/programas/icono', height_field=None, width_field=None, max_length=None, blank=True, null=True, validators=[FileExtensionValidator(['svg', 'png'])])

    class Meta:
        verbose_name = 'Nivel Dos'
        verbose_name_plural = 'Niveles Dos'
        ordering = ['nivel_uno__orden', 'orden',]

    def __str__(self):
        return str(self.orden) + ' - ' + self.nombre  + str(self.nivel_uno)

class NivelTres(models.Model):
    orden = models.IntegerField()
    nombre = models.CharField('Nombre de Nivel Tres', max_length=50)
    url_name = models.CharField('Nombre de URL', max_length=50, blank=True, null=True)
    nivel_dos = models.ForeignKey(NivelDos, on_delete=models.CASCADE, related_name='NivelTres_nivel_dos')
    icono = models.ImageField('Icono PNG o SVG', upload_to='img/programas/icono', height_field=None, width_field=None, max_length=None, blank=True, null=True, validators=[FileExtensionValidator(['svg', 'png'])])

    class Meta:
        verbose_name = 'Nivel Tres'
        verbose_name_plural = 'Niveles Tres'
        ordering = ['nivel_dos__orden', 'orden',]

    def __str__(self):
        return str(self.orden) + ' - ' + self.nombre + str(self.nivel_dos)

class NivelCuatro(models.Model):
    orden = models.IntegerField()
    nombre = models.CharField('Nombre de Nivel Cuatro', max_length=50)
    url_name = models.CharField('Nombre de URL', max_length=50)
    nivel_tres = models.ForeignKey(NivelTres, on_delete=models.CASCADE, related_name='NivelCuatro_nivel_tres')
    icono = models.ImageField('Icono PNG o SVG', upload_to='img/programas/icono', height_field=None, width_field=None, max_length=None, blank=True, null=True, validators=[FileExtensionValidator(['svg', 'png'])])
 
    class Meta:
        verbose_name = 'Nivel Cuatro'
        verbose_name_plural = 'Niveles Cuatro'
        ordering = ['nivel_tres__orden', 'orden',]

    def __str__(self):
        return str(self.orden) + ' - ' + self.nombre + str(self.nivel_tres)