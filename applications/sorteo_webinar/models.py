from django.db import models

# Create your models here.
class Participante(models.Model):
    nombre_completo = models.CharField('Nombre Completo', max_length=500)
    documento = models.CharField('Número de Documento', max_length=50)
    telefono = models.CharField('Número de Telefono', max_length=50)
    correo = models.CharField('Correo electrónico', max_length=500)
    premio = models.CharField('Premio', max_length=50, blank=True, null=True)
    elegido = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Participante'
        verbose_name_plural = 'Participantes'
        ordering = [
            'premio',
            ]

    def __str__(self):
        return self.nombre_completo
