from django.conf import settings
from django.db import models

class Sorteo(models.Model):
    nombre_sorteo = models.CharField(max_length=50)
    nombre_dato_uno = models.CharField(max_length=50)
    nombre_dato_dos = models.CharField(max_length=50)
    nombre_dato_tres = models.CharField(max_length=50, blank=True, null=True)
    nombre_dato_cuatro = models.CharField(max_length=50, blank=True, null=True)
    slug = models.SlugField(blank=True, null=True)
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='Sorteo_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='Sorteo_updated_by', editable=False)

    class Meta:
        verbose_name = "Sorteo"
        verbose_name_plural = "Sorteos"

    def __str__(self):
        return self.nombre_sorteo


class Ticket(models.Model):
    dato_uno = models.CharField(max_length=200)
    dato_dos = models.CharField(max_length=200)
    dato_tres = models.CharField(max_length=200, blank=True, null=True)
    dato_cuatro = models.CharField(max_length=200, blank=True, null=True)
    premio = models.CharField('Premio', max_length=50, blank=True, null=True)
    elegido = models.BooleanField(default=False)
    bloqueo = models.BooleanField(default=False)
    sorteo = models.ForeignKey(Sorteo, on_delete=models.CASCADE, related_name='Ticket_sorteo')
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='Ticket_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='Ticket_updated_by', editable=False)

    class Meta:
        verbose_name = 'Ticket'
        verbose_name_plural = 'Tickets'
        ordering = [
            'sorteo',
            'premio',
            '-elegido',
            'id',
            ]

    def __str__(self):
        return f"{self.dato_uno}"
