from django.contrib import admin
from .models import Ticket

# Register your models here.
@admin.register(Ticket)
class SorteoAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'ticket',
        'razon_social',
        'ruc',
        'contacto',
        'premio',
        'elegido',
        'bloqueo',
        )
    list_filter = (
        'contacto',
        )
    search_fields = (
        'contacto',
        )
