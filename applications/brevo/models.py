from django.db import models

class BrevoWebhookEvent(models.Model):
    EVENT_TYPES = [
        ('delivered', 'Delivered'),
        ('opened', 'Opened'),
        ('click', 'Click'),
        ('bounce', 'Bounce'),
        ('spam', 'Spam'),
        ('blocked', 'Blocked'),
        ('invalid_email', 'Invalid Email'),
        ('request', 'Request'),
        ('sent', 'Sent'),
    ]

    event = models.CharField(max_length=50, choices=EVENT_TYPES)
    email = models.EmailField()
    brevo_id = models.BigIntegerField(blank=True, null=True)  # Renombrado para evitar conflictos con el ID de Django
    date = models.DateTimeField()
    ts = models.BigIntegerField(blank=True, null=True)
    message_id = models.CharField(max_length=255, blank=True, null=True)
    ts_event = models.BigIntegerField(blank=True, null=True)
    subject = models.CharField(max_length=255, blank=True, null=True)
    tag = models.CharField(max_length=100, blank=True, null=True)
    sending_ip = models.GenericIPAddressField(blank=True, null=True)
    ts_epoch = models.BigIntegerField(blank=True, null=True)
    tags = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.email} - {self.event} - {self.date}"
