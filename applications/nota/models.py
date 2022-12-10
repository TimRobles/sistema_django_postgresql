from django.db import models

# Create your models here.
class NotaCredito(models.Model):
    """Model definition for NotaCredito."""

    # TODO: Define fields here

    class Meta:
        """Meta definition for NotaCredito."""

        verbose_name = 'NotaCredito'
        verbose_name_plural = 'NotaCreditos'

    def __str__(self):
        """Unicode representation of NotaCredito."""
        pass


class NotaDebito(models.Model):
    """Model definition for NotaDebito."""

    # TODO: Define fields here

    class Meta:
        """Meta definition for NotaDebito."""

        verbose_name = 'NotaDebito'
        verbose_name_plural = 'NotaDebitos'

    def __str__(self):
        """Unicode representation of NotaDebito."""
        pass
