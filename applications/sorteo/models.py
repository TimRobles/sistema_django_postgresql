from django.db import models

# Create your models here.
# SELECT Nro_Ticket, Razon_Social, RUC, Nombre_Contacto FROM `TAB_MARKETING_004_Tickets_Sorteo` WHERE Nro_Sorteo=1 ORDER BY `Nro_Ticket` ASC
# \copy sorteo_ticket(ticket, razon_social, ruc, contacto, elegido) from /webapps/archivos/TAB_MARKETING_004_Tickets_Sorteo.csv DELIMITER ';' HEADER CSV;
class Ticket(models.Model):
    ticket = models.CharField('Ticket', max_length=4)
    razon_social = models.CharField('Razón Social', max_length=100)
    ruc = models.CharField('RUC', max_length=12)
    contacto = models.CharField('Contacto', max_length=120)
    premio = models.CharField('Premio', max_length=50, blank=True, null=True)
    elegido = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Ticket'
        verbose_name_plural = 'Tickets'
        ordering = [
            'premio',
            '-elegido',
            'ticket',
            ]

    def __str__(self):
        return self.ticket
