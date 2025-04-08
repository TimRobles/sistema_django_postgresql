from django.db import models

class BrevoWebhookEvent(models.Model):
    EVENT_TYPES = [
        ('request', 'Request'),
        ('delivered', 'Delivered'),
        ('opened', 'Opened'),
        ('click', 'Click'),
        ('bounce', 'Bounce'),
        ('spam', 'Spam'),
        ('blocked', 'Blocked'),
        ('invalid_email', 'Invalid Email'),
        ('sent', 'Sent'),
    ]

    event = models.CharField(max_length=50, choices=EVENT_TYPES)
    email = models.EmailField()  # Destinatario
    sender_email = models.EmailField(blank=True, null=True)  # Remitente
    subject = models.CharField(max_length=255, blank=True, null=True)
    date = models.DateTimeField()
    ts = models.BigIntegerField(blank=True, null=True)
    ts_event = models.BigIntegerField(blank=True, null=True)
    ts_epoch = models.BigIntegerField(blank=True, null=True)
    message_id = models.CharField(max_length=255, blank=True, null=True)
    sending_ip = models.GenericIPAddressField(blank=True, null=True)
    reason = models.CharField(max_length=255, blank=True, null=True)
    mirror_link = models.URLField(blank=True, null=True)
    tag = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.email} - {self.event} - {self.date}"
