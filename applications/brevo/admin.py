from django.contrib import admin

from .models import *

class BrevoWebhookEventAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'event',
        'email',
        'sender_email',
        'subject',
        'date',
        'ts',
        'ts_event',
        'ts_epoch',
        'message_id',
        'sending_ip',
        'reason',
        'mirror_link',
        'tag',
        'created_at'
    )
    list_filter = ('event',)
    search_fields = ('email',)